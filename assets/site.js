/* Progressive enhancement only. All page content and links work without JS. */
(() => {
  'use strict';
  const knownSections = new Set(['home', 'profile', 'research', 'experience', 'projects', 'contact']);
  const languageLinks = document.querySelectorAll('[data-language-link]');
  const languageBases = Array.from(languageLinks, link => ({ link, base: link.getAttribute('href') }));

  function updateLanguageLinks() {
    const hash = window.location.hash;
    const suffix = knownSections.has(hash.slice(1)) ? hash : '';
    languageBases.forEach(({ link, base }) => link.setAttribute('href', base + suffix));
  }
  updateLanguageLinks();
  window.addEventListener('hashchange', updateLanguageLinks);

  const button = document.querySelector('.menu-toggle');
  const navigation = document.getElementById('main-navigation');
  if (!button || !navigation || typeof window.matchMedia !== 'function') return;
  const compact = window.matchMedia('(max-width: 959px)');
  let isOpen = false;

  function setOpen(next) {
    isOpen = compact.matches && next;
    button.setAttribute('aria-expanded', String(isOpen));
    button.setAttribute('aria-label', isOpen ? button.dataset.closeLabel : button.dataset.openLabel);
    navigation.hidden = compact.matches && !isOpen;
  }

  function syncLayout() {
    // Make the compact button focusable before moving focus onto it.
    if (compact.matches) button.hidden = false;
    // Move focus out before hiding navigation on a desktop -> mobile resize.
    if (compact.matches && navigation.contains(document.activeElement)) button.focus();
    if (!compact.matches && document.activeElement === button) {
      const firstLink = navigation.querySelector('a');
      navigation.hidden = false;
      if (firstLink) firstLink.focus();
    }
    button.hidden = !compact.matches;
    setOpen(false);
  }

  button.addEventListener('click', () => setOpen(!isOpen));
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && isOpen) {
      setOpen(false);
      button.focus();
    }
  });
  navigation.addEventListener('click', event => {
    const link = event.target.closest('a');
    if (!link || !navigation.contains(link)) return;
    if (compact.matches) {
      const hash = link.getAttribute('href');
      const target = hash && hash.startsWith('#') ? document.getElementById(hash.slice(1)) : null;
      // Do not leave focus on a link that is about to be hidden.
      if (target) target.focus({ preventScroll: true });
      else button.focus();
      setOpen(false);
    }
  });
  if (typeof compact.addEventListener === 'function') compact.addEventListener('change', syncLayout);
  else compact.addListener(syncLayout);
  syncLayout();
})();
