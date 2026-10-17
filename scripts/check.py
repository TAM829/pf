#!/usr/bin/env python3
"""Validate HTML, assets, metadata and content contracts. Standard library only."""
from __future__ import annotations
import copy
from html.parser import HTMLParser
import importlib.util
import json
from pathlib import Path
import re
import struct
import subprocess
import sys
from urllib.parse import urlsplit,unquote
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
VOID={'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
class Page(HTMLParser):
    def __init__(self,text):
        super().__init__(convert_charrefs=True);self.nodes=[];self.stack=[];self.errors=[];self.text=[];self.feed(text)
        if self.stack:self.errors.append('Unclosed tags: '+str(self.stack))
    def handle_starttag(self,tag,attrs):
        if len(attrs)!=len(dict(attrs)):self.errors.append('Duplicate attributes: '+tag)
        self.nodes.append((tag,dict(attrs)))
        if tag not in VOID:self.stack.append(tag)
    def handle_startendtag(self,tag,attrs):self.nodes.append((tag,dict(attrs)))
    def handle_endtag(self,tag):
        if not self.stack or self.stack[-1]!=tag:self.errors.append('Mismatched end tag: '+tag)
        else:self.stack.pop()
    def handle_data(self,text):self.text.append(text)
    def select(self,tag,**attrs):return [a for t,a in self.nodes if t==tag and all(a.get(k)==v for k,v in attrs.items())]

checks=0
failures=[]
def expect(condition,message):
    global checks
    checks+=1
    if not condition:failures.append(message)

def luminance(color):
    rgb=[int(color[i:i+2],16)/255 for i in (1,3,5)]
    rgb=[v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in rgb]
    return sum(v*c for v,c in zip(rgb,(.2126,.7152,.0722)))
def contrast(a,b):
    x,y=sorted((luminance(a),luminance(b)))
    return (y+.05)/(x+.05)
def png_size(path):
    data=path.read_bytes();assert data[:8]==b'\x89PNG\r\n\x1a\n';return struct.unpack('>II',data[16:24])

def main():
    subprocess.run([sys.executable,str(ROOT/'scripts/build.py'),'--check'],check=True)
    config=json.loads((ROOT/'data/site.json').read_text(encoding='utf-8'))
    spec=importlib.util.spec_from_file_location('site_build',ROOT/'scripts/build.py');build=importlib.util.module_from_spec(spec);spec.loader.exec_module(build)
    pages={rel:Page((ROOT/rel).read_text(encoding='utf-8')) for rel in ('index.html','en/index.html')}
    for rel,page in pages.items():
        lang='ja' if rel=='index.html' else 'en';text=' '.join(page.text);raw=(ROOT/rel).read_text(encoding='utf-8');file=ROOT/rel
        expect(not page.errors,f'{rel}: HTML nesting: {page.errors}')
        expect(page.select('html',lang=lang),f'{rel}: html lang')
        expect(len(page.select('h1'))==1,f'{rel}: exactly one h1')
        expect(len(page.select('main'))==1,f'{rel}: one main landmark')
        expect(len(page.select('title'))==1,f'{rel}: one page title')
        expect(page.select('meta',charset='utf-8'),f'{rel}: UTF-8')
        ids=[a['id'] for _,a in page.nodes if 'id' in a]
        expect(len(ids)==len(set(ids)),f'{rel}: duplicate IDs')
        for id_ in ('home','main','profile','research','experience','projects','contact','main-navigation'):
            expect(id_ in ids,f'{rel}: missing {id_}')
        nav=next(a for t,a in page.nodes if a.get('id')=='main-navigation')
        expect('hidden' not in nav,f'{rel}: no-JS navigation must remain available')
        btn=page.select('button')[0]
        expect('hidden' in btn and btn.get('aria-controls')=='main-navigation',f'{rel}: progressive menu markup')
        expect(btn.get('aria-expanded')=='false' and btn.get('type')=='button',f'{rel}: menu ARIA/type')
        for tag,attrs in page.nodes:
            expect(not any(k.startswith('on') for k in attrs),f'{rel}: inline event handler')
            if tag=='img':
                expect('alt' in attrs,f'{rel}: image alt')
                expect('width' in attrs and 'height' in attrs,f'{rel}: image dimensions')
            for attr in ('href','src'):
                if attr not in attrs:continue
                u=attrs[attr];parts=urlsplit(u)
                expect(parts.scheme not in ('javascript','data'),f'{rel}: disallowed URL scheme')
                if parts.scheme=='mailto':
                    expect(parts.path==config['site']['email'],f'{rel}: email target mismatch');continue
                if parts.scheme:continue
                target=(file.parent/unquote(parts.path)).resolve() if parts.path else file
                expect(target.is_relative_to(ROOT),f'{rel}: local link escapes project')
                expect(target.is_file(),f'{rel}: missing asset/link {u}')
                if parts.fragment and target.suffix=='.html' and target.is_file():
                    other=pages.get(target.relative_to(ROOT).as_posix())
                    if other:expect(parts.fragment in [a.get('id') for _,a in other.nodes],f'{rel}: missing anchor {u}')
        yt=page.select('a',href=config['site']['youtube'])
        expect(len(yt)==1,f'{rel}: exactly one YouTube link')
        expect(yt[0].get('target')=='_blank' and set(yt[0].get('rel','').split())=={'noopener','noreferrer'},f'{rel}: external link attributes')
        expect(config[lang]['external_note'] in text,f'{rel}: new-tab accessible note')
        expect(len(page.select('time',datetime=config['site']['updated']))==1,f'{rel}: shared date')
        expect('Updated 17-Oct-2026' in text if config['site']['updated']=='2026-10-17' else True,f'{rel}: date display')
        for k in ('Oracle SQL','VB.NET','Python','Windows','Linux','WSL','Ollama','Open WebUI','Docker','GitHub'):
            expect(k in text,f'{rel}: missing skill {k}')
        expect(config[lang]['qualification'] in text,f'{rel}: missing qualification')
        expect('基本情報技術者試験' in text if lang=='ja' else 'Yoh-ichi Mototake' in text,f'{rel}: localized facts')
        expect(len([a for t,a in page.nodes if t=='div' and a.get('class')=='skill-row'])==7,f'{rel}: seven skill categories, once')
        expect(not any(x in text for x in ('MOTOTAKE','Yoichi Mototake','Lorem ipsum')),f'{rel}: stale or placeholder text')
        expect('fetch(' not in raw,f'{rel}: no client-side dependency for page content')
        canonical=page.select('link',rel='canonical')[0]['href']
        expect(canonical==config['site']['base_url']+rel,f'{rel}: canonical URL')
        for language,path in [('ja','index.html'),('en','en/index.html'),('x-default','index.html')]:
            expect(page.select('link',rel='alternate',hreflang=language,href=config['site']['base_url']+path),f'{rel}: hreflang {language}')
        props={a.get('property'):a.get('content') for t,a in page.nodes if t=='meta' and 'property'in a}
        for key in ('og:title','og:description','og:url','og:locale','og:locale:alternate','og:image','og:image:alt','og:type'):
            expect(bool(props.get(key)),f'{rel}: missing {key}')
        expect(props.get('og:url')==canonical,f'{rel}: og:url and canonical differ')
        expect(props.get('og:locale')==('ja_JP' if lang=='ja' else 'en_US'),f'{rel}: localized OGP')
        expect(props.get('og:description')==config[lang]['description'],f'{rel}: localized description')
        for link in page.select('a'):
            if 'data-language-link' in link:expect(link.get('target') is None,f'{rel}: language links must use same tab')
        for image in page.select('img'):
            path=file.parent/image['src'];w,h=png_size(path)
            expect((w,h)==(int(image['width']),int(image['height'])),f'{rel}: image aspect ratio mismatch')
        # Final supplied specification and material-credit requirements.
        uploaded_spec=(ROOT/'docs/site-spec.md').read_text(encoding='utf-8')
        for key in ('tagline','research_summary','research_tasks','intro','local_text','qualification'):
            expect(config[lang][key] in uploaded_spec,f'{rel}: {key} differs from supplied specification')
            expect(config[lang][key] in text,f'{rel}: {key} missing from initial HTML')
        images=page.select('img')
        expect(len(images)==3 and all(a.get('src','').endswith('assets/turtle.png') for a in images),f'{rel}: shared logo in exactly three positions')
        for classname in ('brand-turtle','hero-turtle','footer-turtle'):
            expect(sum(classname in a.get('class','').split() for a in images)==1,f'{rel}: logo position {classname}')
        expect(page.select('details',id='licenses'),f'{rel}: native no-JS license disclosure')
        expect(config[lang]['licenses']['title'] in text,f'{rel}: localized credits')
        expect(text.count('Logo created with')==1,f'{rel}: credit shown once')
        expect(page.select('a',href='https://www.designevo.com/terms.html'),f'{rel}: license link')
        expect(not any(word in text for word in ('BASIC','PLUS','Free plan','（Free）','未確認')),f'{rel}: no purchase or internal notes')
        for tag,attrs in page.nodes:
            if tag=='script' or (tag=='link' and attrs.get('rel')=='stylesheet'):
                expect(not urlsplit(attrs.get('src',attrs.get('href',''))).scheme,f'{rel}: no remote runtime resource')
    # Native SVGs must parse, and CSS asset URLs must resolve.
    for svg in (ROOT/'assets').glob('*.svg'):ET.parse(svg);expect(True,f'{svg.name}: XML')
    css=(ROOT/'assets/site.css').read_text()
    for url in re.findall(r'url\([\"\']?([^\)\"\']+)',css):expect((ROOT/'assets'/url).is_file(),f'CSS missing {url}')
    defined=set(re.findall(r'--([\w-]+):',css));used=set(re.findall(r'var\(--([\w-]+)',css))
    expect(used<=defined,'CSS custom properties must all be defined')
    # Network strokes must meet circle centers; no filled triangles or bitmap assets.
    network=ET.parse(ROOT/'assets/network.svg').getroot();ns={'s':'http://www.w3.org/2000/svg'}
    centers={(float(c.attrib['cx']),float(c.attrib['cy'])) for c in network.findall('.//s:circle',ns)}
    lines=network.findall('.//s:line',ns)
    expect(len(centers)>10 and len(lines)>10,'Network contains authored connected geometry')
    edge_keys=[]
    for line in lines:
        p=(float(line.attrib['x1']),float(line.attrib['y1']));q=(float(line.attrib['x2']),float(line.attrib['y2']))
        expect(p in centers and q in centers and p!=q,'Network line ends meet distinct node centers')
        edge_keys.append(tuple(sorted((p,q))))
    expect(len(edge_keys)==len(set(edge_keys)),'Network has no duplicated edges')
    expect(not network.findall('.//s:image',ns) and not network.findall('.//s:polygon',ns),'Network uses lines, no bitmap or triangle fills')
    expect('Math.random' not in (ROOT/'assets/site.js').read_text(),'No runtime-random decoration')
    expect('@media (max-width: 959px)' in css,f'CSS and JS breakpoint must match')
    expect('[hidden] { display: none !important; }' in css,'Hidden menu content must not be displayed')
    expect('@media (prefers-reduced-motion: reduce)' in css,'Reduced motion support')
    expect(png_size(ROOT/'assets/og-image.png')==(1200,630),'OG image size')
    expect(png_size(ROOT/'assets/favicon.png')==(256,256),'PNG favicon size')
    expect((ROOT/'favicon.ico').read_bytes()[:4]==b'\x00\x00\x01\x00','ICO format')
    ET.parse(ROOT/'sitemap.xml');expect(True,'Sitemap XML parses')
    # Negative data-contract tests are in-memory and never change the real pages.
    for field,value in [('updated','2026-02-30'),('base_url','javascript:alert(1)'),('email','bad@example.com?subject=x'),('youtube','https://not-youtube.example/')]:
        bad=copy.deepcopy(config);bad['site'][field]=value
        try:build.validate_config(bad)
        except ValueError:expect(True,'reject invalid '+field)
        else:expect(False,'must reject invalid '+field)
    dirty=copy.deepcopy(config);dirty['ja']['tagline']='<script>alert("x")</script>'
    output=build.render(dirty,'ja')
    expect('<script>alert(' not in output and '&lt;script&gt;' in output,'content is escaped, not interpreted as HTML')
    # Check the real CSS color tokens against each of their text backgrounds.
    colors=dict(re.findall(r'--([\w-]+):\s*(#[0-9a-fA-F]{6})',css))
    ratios=[]
    for foreground in ('ink','body','muted','blue','blue-dark'):
        for bg in ('#ffffff',colors['pale']):
            ratio=contrast(colors[foreground],bg);ratios.append(ratio)
            expect(ratio>=4.5,f'Contrast {foreground}/{bg}: {ratio:.2f}')
    badge=contrast(colors['blue-dark'],colors['badge'])
    expect(badge>=4.5,f'Status badge contrast: {badge:.2f}')
    expect(contrast('#ffffff',colors['blue'])>=4.5,'Button text contrast')
    expect(contrast(colors['blue'],colors['pale'])>=3,'Control icon contrast')
    print(f'Lowest tested ordinary text contrast: {min(ratios):.2f}:1; badge: {badge:.2f}:1')
    if failures:
        for f in failures:print('FAIL '+f,file=sys.stderr)
        raise SystemExit(f'{len(failures)} failures / {checks} checks')
    print(f'{checks} static/content checks passed. Actual browser layout and live remote URLs are not covered.')

if __name__=='__main__':main()
