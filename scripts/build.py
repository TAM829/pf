#!/usr/bin/env python3
"""Build both static pages from data/site.json. Python 3.9+, standard library only."""
from __future__ import annotations
import argparse
import datetime as dt
from html import escape
import json
from pathlib import Path
from urllib.parse import urlsplit, urljoin

ROOT = Path(__file__).resolve().parents[1]
IDS = ('profile', 'research', 'experience', 'projects', 'contact')
SUBTITLES = ('Profile', 'Research', 'Experience', 'Projects & Skills', 'Contact')
MONTHS = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec')
ICONS = {
    'shop': '<path d="M4 13v15h24V13M2 10l4-8h20l4 8M2 10a5 5 0 0 0 9 3 5 5 0 0 0 10 0 5 5 0 0 0 9-3M12 28v-9h8v9"/>',
    'laptop': '<rect x="5" y="3" width="22" height="21" rx="1"/><path d="M5 24l-4 5h30l-4-5"/>',
    'code': '<path d="M10 6L2 16l8 10M22 6l8 10-8 10M19 2l-6 28"/>',
    'play': '<circle cx="16" cy="16" r="13"/><path d="M13 10l9 6-9 6z"/>',
    'mail': '<rect x="3" y="6" width="26" height="20" rx="1"/><path d="M3 7l13 10L29 7"/>',
    'arrow': '<path d="M5 16h22M20 9l7 7-7 7"/>',
    'down': '<path d="M16 4v24M9 21l7 7 7-7"/>',
    'external': '<path d="M18 4h10v10M28 4L14 18M14 6H5v22h22v-9"/>',
    'terminal': '<rect x="2" y="4" width="28" height="24" rx="2"/><path d="M8 11l5 5-5 5M17 22h7"/>',
    'award': '<circle cx="16" cy="12" r="8"/><path d="M10 18l-2 12 8-4 8 4-2-12"/>'
}

def e(value):
    return escape(str(value), quote=True)

def icon(name, extra=''):
    return f'<svg class="icon {extra}" viewBox="0 0 32 32" width="32" height="32" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{ICONS[name]}</svg>'

def validate_config(data):
    site=data['site']
    base=urlsplit(site['base_url'])
    if base.scheme!='https' or not base.netloc or base.query or base.fragment or not site['base_url'].endswith('/'):
        raise ValueError('base_url must be an absolute https URL ending in /, without query or fragment')
    date=dt.date.fromisoformat(site['updated'])
    if date.isoformat()!=site['updated']:
        raise ValueError('updated must be YYYY-MM-DD')
    email=site['email']
    if any(c.isspace() for c in email) or email.count('@')!=1 or any(c in email for c in '?&#<>"'):
        raise ValueError('Invalid email')
    video=urlsplit(site['youtube'])
    if video.scheme!='https' or video.netloc not in ('www.youtube.com','youtube.com'):
        raise ValueError('youtube must use an https YouTube URL')
    for lang in ('ja','en'):
        text=data[lang]
        if len(text['nav'])!=5 or len(text['headings'])!=5:
            raise ValueError('Exactly five navigation/section labels are required')
        if len(text['skills'])!=7:
            raise ValueError('Exactly seven skill categories are required')
        for item in text['experience']+text['projects']:
            if item['icon'] not in ICONS:
                raise ValueError('Unknown icon')
    return date

def render(data, lang):
    site=data['site'];t=data[lang];ja=lang=='ja'
    prefix='' if ja else '../'
    url=urljoin(site['base_url'],'index.html' if ja else 'en/index.html')
    jaurl=urljoin(site['base_url'],'index.html');enurl=urljoin(site['base_url'],'en/index.html')
    name=site['name_ja'] if ja else site['name_en']
    role=site['role_ja'] if ja else site['role_en']
    title=f'{name} | {role}'
    updated=dt.date.fromisoformat(site['updated'])
    display=f'{updated.day:02d}-{MONTHS[updated.month-1]}-{updated.year:04d}'
    image=urljoin(site['base_url'],'assets/og-image.png')
    def turtle(cls):
        return f'<img class="turtle {cls}" src="{prefix}assets/turtle.png" alt="" width="{TURTLE_WIDTH}" height="{TURTLE_HEIGHT}" decoding="async">'
    def heading(n):
        idx=n-1;sid=IDS[idx]
        subtitle=f'<span class="section-translation" lang="en">/ {e(SUBTITLES[idx])}</span>' if ja else ''
        return f'<div class="section-heading"><span class="section-number" aria-hidden="true">{n:02d}</span><span class="heading-rule" aria-hidden="true"></span><h2 id="{sid}-heading">{e(t["headings"][idx])}</h2>{subtitle}</div>'
    nav=''.join(f'<li><a href="#{sid}">{e(label)}</a></li>' for sid,label in zip(IDS,t['nav']))
    ja_attr=' aria-current="page"' if ja else ''
    en_attr='' if ja else ' aria-current="page"'
    langlinks=f'<nav class="language-switch" aria-label="{e(t["language"])}"><a href="{prefix}index.html" lang="ja" hreflang="ja" data-language-link{ja_attr}>日本語</a><span aria-hidden="true">/</span><a href="{prefix}en/index.html" lang="en" hreflang="en" data-language-link{en_attr}>EN</a></nav>'
    profile=''.join(f'<p>{e(p)}</p>' for p in t['profile'])
    c=site['collaborator']
    collaboration=(f'<p class="collaboration">{e(c["ja"])}</p>' if ja else f'<div class="collaboration"><p class="collaboration-label">Joint Research</p><p>{e(c["title"])} {e(c["name"])}</p><p class="collaboration-school">{e(c["school"])}, {e(c["university"])}</p></div>')
    experience=''
    for item in t['experience']:
        badge=f'<span class="badge">{e(t["current"])}</span>' if item.get('current') else ''
        experience+=f'<article class="experience-item">{icon(item["icon"])}<div><h3>{e(item["title"])} {badge}</h3><p>{e(item["text"])}</p></div></article>'
    projects=''
    for item in t['projects']:
        link=''
        if item.get('youtube'):
            link=f'<p class="project-link"><a href="{e(site["youtube"])}" target="_blank" rel="noopener noreferrer">{e(t["youtube_label"])}{icon("external")}<span class="visually-hidden"> — {e(t["external_note"])}</span></a></p>'
        projects+=f'<article class="project-item">{icon(item["icon"])}<div><h3>{e(item["title"])}</h3><p>{e(item["text"])}</p>{link}</div></article>'
    skills=''.join(f'<div class="skill-row"><dt>{e(label)}</dt><dd>'+''.join(f'<span class="skill">{e(value)}</span>' for value in values)+'</dd></div>' for label,values in t['skills'])
    signature=f'<p class="roman-name" lang="en">{e(site["name_en"])}</p>' if ja else ''
    footername=e(site['name_en'])
    lic=t['licenses']
    output=f'''<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light">
  <meta name="theme-color" content="#ffffff">
  <title>{e(title)}</title>
  <meta name="description" content="{e(t['description'])}">
  <link rel="canonical" href="{e(url)}">
  <link rel="alternate" hreflang="ja" href="{e(jaurl)}">
  <link rel="alternate" hreflang="en" href="{e(enurl)}">
  <link rel="alternate" hreflang="x-default" href="{e(jaurl)}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(t['description'])}">
  <meta property="og:url" content="{e(url)}">
  <meta property="og:locale" content="{'ja_JP' if ja else 'en_US'}">
  <meta property="og:locale:alternate" content="{'en_US' if ja else 'ja_JP'}">
  <meta property="og:image" content="{e(image)}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{e(t['og_alt'])}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{e(title)}">
  <meta name="twitter:description" content="{e(t['description'])}">
  <meta name="twitter:image" content="{e(image)}">
  <meta name="twitter:image:alt" content="{e(t['og_alt'])}">
  <link rel="icon" href="{prefix}favicon.ico" sizes="any">
  <link rel="icon" type="image/png" sizes="256x256" href="{prefix}assets/favicon.png">
  <link rel="apple-touch-icon" sizes="180x180" href="{prefix}assets/apple-touch-icon.png">
  <link rel="stylesheet" href="{prefix}assets/site.css">
  <script src="{prefix}assets/site.js" defer></script>
</head>
<body>
<a class="skip-link" href="#main">{e(t['skip'])}</a>
<header class="site-header" id="home">
  <div class="container header-grid">
    <a class="brand" href="#home" aria-label="{e(name+' — '+t['home'])}">{turtle('brand-turtle')}<span>{e(name)}</span></a>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="main-navigation" aria-label="{e(t['menu_open'])}" data-open-label="{e(t['menu_open'])}" data-close-label="{e(t['menu_close'])}" hidden><span class="menu-lines" aria-hidden="true"></span></button>
    <time class="updated" datetime="{e(site['updated'])}">Updated {display}</time>
    {langlinks}
    <nav class="main-navigation" id="main-navigation" aria-label="{e(t['navigation'])}"><ul>{nav}</ul></nav>
  </div>
</header>
<main id="main" tabindex="-1">
  <section class="hero" aria-labelledby="page-title">
    <div class="container hero-inner">
      <div class="hero-copy">
        <p class="hello" lang="en">HELLO NEW WORLD</p>
        <p class="role">{e(role)}</p>
        <h1 id="page-title">{e(name)}</h1>
        {signature}
        <p class="tagline">{e(t['tagline'])}</p>
        <p class="intro">{e(t['intro'])}</p>
        <a class="text-link hero-link" href="#research">{e(t['research_link'])}{icon('down')}</a>
      </div>
      <div class="hero-art" aria-hidden="true"><div class="hero-ground"></div>{turtle('hero-turtle')}</div>
    </div>
  </section>
  <section class="section profile-section" id="profile" aria-labelledby="profile-heading" tabindex="-1">
    <div class="container">{heading(1)}<div class="section-body profile-copy">{profile}</div></div>
  </section>
  <section class="section research-section" id="research" aria-labelledby="research-heading" tabindex="-1">
    <div class="container">
      <div class="research-top">{heading(2)}<span class="status">{e(t['status'])}</span></div>
      <div class="research-grid">
        <div class="research-copy"><h3>{e(t['research_title'])}</h3>{collaboration}<p class="research-summary">{e(t['research_summary'])}</p><p class="research-tasks">{e(t['research_tasks'])}</p></div>
        <div class="research-wordmark" aria-hidden="true"><span>AI</span><span class="times">×</span><span>Persona</span></div>
      </div>
    </div>
  </section>
  <section class="section experience-section" id="experience" aria-labelledby="experience-heading" tabindex="-1">
    <div class="container">{heading(3)}<div class="experience-grid">{experience}</div></div>
  </section>
  <section class="section projects-section" id="projects" aria-labelledby="projects-heading" tabindex="-1">
    <div class="container">
      {heading(4)}
      <div class="project-grid">{projects}</div>
      <article class="local-llm">{icon('terminal')}<div><h3>{e(t['local_title'])}</h3><p>{e(t['local_text'])}</p></div></article>
      <div class="skills-block"><h3>{e(t['skills_title'])}</h3><dl class="skills-list">{skills}</dl></div>
      <div class="qualification">{icon('award')}<div><h3>{e(t['qualifications'])}</h3><p>{e(t['qualification'])}</p></div></div>
    </div>
  </section>
  <section class="section contact-section" id="contact" aria-labelledby="contact-heading" tabindex="-1">
    <div class="container">{heading(5)}
      <div class="contact-grid"><div class="contact-identity"><p class="role">{e(role)}</p><p class="contact-name">{e(name)}</p>{signature}</div>
      <a class="email" href="mailto:{e(site['email'])}">{icon('mail')}<span>{e(site['email'])}</span></a>
      <a class="button" href="mailto:{e(site['email'])}">{e(t['contact_button'])}{icon('arrow')}</a></div>
    </div>
  </section>
</main>
<footer class="site-footer">
  <div class="container footer-content">
    {turtle('footer-turtle')}
    <p class="logo-credit" lang="en">Logo created with <a href="https://www.designevo.com/">DesignEvo</a></p>
    <small>© {footername}</small>
    <details class="licenses" id="licenses">
      <summary>{e(lic['title'])}</summary>
      <div class="licenses-content">
        <p>{e(lic['logo_title'])}{'：' if ja else ': '}<a href="https://www.designevo.com/">DesignEvo</a> / <a href="https://www.designevo.com/terms.html">{e(lic['terms'])}</a></p>
        <p>{e(lic['art_title'])}{'：' if ja else ': '}{e(lic['art_text'])}</p>
      </div>
    </details>
  </div>
</footer>
</body>
</html>
'''
    return '\n'.join(line.rstrip() for line in output.splitlines()) + '\n'

# Web-sized derivative of the user-supplied transparent logo.
TURTLE_WIDTH=256
TURTLE_HEIGHT=224

def build(check=False):
    data=json.loads((ROOT/'data/site.json').read_text(encoding='utf-8'))
    validate_config(data)
    outputs={ROOT/'index.html':render(data,'ja'),ROOT/'en/index.html':render(data,'en')}
    base=data['site']['base_url']
    outputs[ROOT/'sitemap.xml']='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{e(urljoin(base,x))}</loc><lastmod>{e(data["site"]["updated"])}</lastmod></url>\n' for x in ('index.html','en/index.html'))+'</urlset>\n'
    stale=[]
    for path,content in outputs.items():
        if check:
            if not path.exists() or path.read_text(encoding='utf-8')!=content:stale.append(path.relative_to(ROOT).as_posix())
        else:
            path.parent.mkdir(parents=True,exist_ok=True)
            with path.open('w',encoding='utf-8',newline='\n') as stream:
                stream.write(content)
    if stale:raise SystemExit('Generated files are out of date: '+', '.join(stale)+'. Run python3 scripts/build.py')
    print('Generated files are current.' if check else 'Built index.html, en/index.html, and sitemap.xml.')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true',help='Fail if committed HTML differs from generated output')
    build(parser.parse_args().check)
