/* Unit tests for the actual site.js, using a minimal DOM and MediaQueryList.
 * These test state transitions and focus logic, not browser rendering. */
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const source = fs.readFileSync(path.join(__dirname, '../assets/site.js'), 'utf8');

function harness({ mobile = false, hash = '', legacy = false, missingMenu = false, languagePrefix = '' } = {}) {
  const docEvents = {}, winEvents = {};
  let document;
  class Element {
    constructor(attrs = {}) { this.attrs = { ...attrs }; this.hidden = false; this.events = {}; this.children = []; this.parent = null; this.dataset = { openLabel: 'Open menu', closeLabel: 'Close menu' }; }
    getAttribute(key) { return this.attrs[key] ?? null; }
    setAttribute(key, value) { this.attrs[key] = value; }
    addEventListener(name, fn) { this.events[name] = fn; }
    contains(node) { return node === this || this.children.some(c => c.contains(node)); }
    append(child) { this.children.push(child); child.parent = this; }
    focus() { let e = this; while(e) { if (e.hidden) return; e = e.parent; } document.activeElement = this; }
    querySelector(selector) { return selector === 'a' ? this.children[0] : null; }
    closest(selector) { return selector === 'a' && this.attrs.href ? this : this.parent?.closest(selector) ?? null; }
  }
  const button = new Element({ 'aria-expanded': 'false', 'aria-label': 'Open menu' }); button.hidden = true;
  const nav = new Element();
  const link = new Element({ href: '#research' }); nav.append(link);
  const nested = new Element(); link.append(nested);
  const targets = Object.fromEntries(['home','profile','research','experience','projects','contact'].map(id => [id,new Element()]));
  const languageLinks = [new Element({href:languagePrefix+'index.html'}),new Element({href:languagePrefix+'en/index.html'})];
  document = {
    activeElement: null,
    querySelectorAll: () => languageLinks,
    querySelector: () => missingMenu ? null : button,
    getElementById: id => id === 'main-navigation' ? nav : targets[id],
    addEventListener: (name, fn) => docEvents[name] = fn,
  };
  const media = { matches: mobile };
  let onChange;
  if (!legacy) media.addEventListener = (name, fn) => onChange = fn;
  media.addListener = fn => onChange = fn;
  const window = { location: { hash }, addEventListener:(name,fn)=>winEvents[name]=fn, matchMedia:()=>media };
  vm.runInNewContext(source, { window, document, Set, Array });
  return { button,nav,link,nested,targets,languageLinks,document,
    click: () => button.events.click(),
    escape: () => docEvents.keydown({key:'Escape'}),
    navClick: () => nav.events.click({target:nested}),
    resize: matches => { media.matches=matches; onChange(); },
    changeHash: value => { window.location.hash=value;winEvents.hashchange(); },
  };
}
let count = 0;
function test(name, fn) { fn(); count++; console.log('PASS '+name); }
test('Desktop navigation remains visible; menu button hidden', () => {
  const h=harness(); assert.equal(h.nav.hidden,false); assert.equal(h.button.hidden,true);
});
test('Mobile starts closed with a correctly named, focusable toggle', () => {
  const h=harness({mobile:true}); assert.equal(h.nav.hidden,true);assert.equal(h.button.hidden,false);assert.equal(h.button.attrs['aria-expanded'],'false');assert.equal(h.button.attrs['aria-label'],'Open menu');
});
test('Toggle opens and closes, updating ARIA and accessible name', () => {
  const h=harness({mobile:true});h.click();assert.equal(h.nav.hidden,false);assert.equal(h.button.attrs['aria-expanded'],'true');assert.equal(h.button.attrs['aria-label'],'Close menu');h.click();assert.equal(h.nav.hidden,true);assert.equal(h.button.attrs['aria-expanded'],'false');
});
test('Escape closes mobile navigation and returns focus to toggle', () => {
  const h=harness({mobile:true});h.click();h.link.focus();h.escape();assert.equal(h.nav.hidden,true);assert.equal(h.document.activeElement,h.button);
});
test('Escape does not move focus when the menu is already closed', () => {
  const h=harness({mobile:true});h.targets.contact.focus();h.escape();assert.equal(h.document.activeElement,h.targets.contact);
});
test('Nested link click closes mobile menu and moves focus to destination', () => {
  const h=harness({mobile:true});h.click();h.link.focus();h.navClick();assert.equal(h.nav.hidden,true);assert.equal(h.document.activeElement,h.targets.research);
});
test('Desktop link click does not hide navigation', () => {
  const h=harness();h.navClick();assert.equal(h.nav.hidden,false);
});
test('Desktop to mobile resize moves focus out before hiding navigation', () => {
  const h=harness();h.link.focus();h.resize(true);assert.equal(h.document.activeElement,h.button);assert.equal(h.nav.hidden,true);assert.equal(h.button.hidden,false);
});
test('Mobile to desktop resize unhides nav and prevents a hidden focused button', () => {
  const h=harness({mobile:true});h.button.focus();h.resize(false);assert.equal(h.document.activeElement,h.link);assert.equal(h.nav.hidden,false);assert.equal(h.button.hidden,true);
});
test('Open state does not leak across breakpoint transitions', () => {
  const h=harness({mobile:true});h.click();h.resize(false);h.resize(true);assert.equal(h.nav.hidden,true);assert.equal(h.button.attrs['aria-expanded'],'false');
});
test('Language links carry a recognized section hash', () => {
  const h=harness({hash:'#research'});assert.equal(h.languageLinks[1].attrs.href,'en/index.html#research');h.changeHash('#projects');assert.equal(h.languageLinks[0].attrs.href,'index.html#projects');
});
test('Language links ignore unknown or unsafe-looking hashes', () => {
  const h=harness({hash:'#not-a-section'});assert.equal(h.languageLinks[0].attrs.href,'index.html');h.changeHash('#<script>');assert.equal(h.languageLinks[1].attrs.href,'en/index.html');
});
test('Hash updates are not appended repeatedly', () => {
  const h=harness({hash:'#profile'});h.changeHash('#research');h.changeHash('');assert.equal(h.languageLinks[1].attrs.href,'en/index.html');
});
test('English-page relative language URLs remain correct', () => {
  const h=harness({hash:'#contact',languagePrefix:'../'});assert.equal(h.languageLinks[0].attrs.href,'../index.html#contact');assert.equal(h.languageLinks[1].attrs.href,'../en/index.html#contact');
});
test('Legacy MediaQueryList addListener branch works', () => {
  const h=harness({legacy:true});h.resize(true);assert.equal(h.nav.hidden,true);h.click();assert.equal(h.nav.hidden,false);
});
test('Language enhancement works when navigation markup is absent', () => {
  const h=harness({missingMenu:true,hash:'#experience'});assert.equal(h.languageLinks[1].attrs.href,'en/index.html#experience');
});
console.log(`\n${count} interaction unit tests passed. Browser layout is not covered.`);
