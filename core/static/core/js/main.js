/**
 * Site interactions: hero entrance, pointer parallax, header state,
 * mobile menu, lightboxes and lazy images.
 *
 * Each feature is an independent initializer so pages only pay for what
 * they actually render.
 */

const prefersReducedMotion = () =>
  window.matchMedia('(prefers-reduced-motion: reduce)').matches;

/**
 * Plays the hero entrance sequence once fonts are ready, then binds a
 * pointer-driven parallax on the composition layers.
 */
function initHero() {
  const hero = document.querySelector('[data-hero]');
  if (!hero) return;

  const reveal = () => hero.classList.add('is-ready');
  const fontsReady = document.fonts ? document.fonts.ready : Promise.resolve();
  // Never let a slow font request hold the page hostage.
  Promise.race([fontsReady, new Promise((r) => setTimeout(r, 900))]).then(() =>
    requestAnimationFrame(reveal)
  );

  const svg = hero.querySelector('.composition svg');
  if (prefersReducedMotion()) {
    if (svg && typeof svg.pauseAnimations === 'function') svg.pauseAnimations();
    return;
  }

  const finePointer = window.matchMedia('(pointer: fine)').matches;
  const layers = [...hero.querySelectorAll('.composition .depth')];
  if (!finePointer || layers.length === 0) return;

  const amplitude = 18;
  let frame = 0;

  hero.addEventListener('pointermove', (event) => {
    const rect = hero.getBoundingClientRect();
    const x = (event.clientX - rect.left) / rect.width - 0.5;
    const y = (event.clientY - rect.top) / rect.height - 0.5;
    cancelAnimationFrame(frame);
    frame = requestAnimationFrame(() => {
      layers.forEach((layer) => {
        const depth = Number(layer.dataset.depth || 0.5);
        const dx = (-x * amplitude * depth).toFixed(2);
        const dy = (-y * amplitude * depth).toFixed(2);
        layer.style.transform = `translate(${dx}px, ${dy}px)`;
      });
    });
  });

  hero.addEventListener('pointerleave', () => {
    layers.forEach((layer) => {
      layer.style.transform = '';
    });
  });
}

/**
 * Adds a hairline under the sticky header once the page has scrolled.
 */
function initHeader() {
  const header = document.querySelector('[data-site-header]');
  if (!header) return;

  const sentinel = document.createElement('div');
  sentinel.setAttribute('aria-hidden', 'true');
  sentinel.style.cssText = 'position:absolute;top:0;height:1px;width:1px;';
  document.body.prepend(sentinel);

  new IntersectionObserver(([entry]) => {
    header.dataset.scrolled = String(!entry.isIntersecting);
  }).observe(sentinel);
}

/**
 * Opens the full-screen mobile menu as a modal <dialog>, which provides
 * focus trapping and Escape handling natively.
 */
function initMenu() {
  const dialog = document.querySelector('[data-menu]');
  const openBtn = document.querySelector('[data-menu-open]');
  if (!dialog || !openBtn || typeof dialog.showModal !== 'function') return;

  const closeBtn = dialog.querySelector('[data-menu-close]');

  openBtn.addEventListener('click', () => {
    dialog.showModal();
    document.documentElement.style.overflow = 'hidden';
  });
  closeBtn?.addEventListener('click', () => dialog.close());
  dialog.addEventListener('close', () => {
    document.documentElement.style.overflow = '';
    openBtn.focus();
  });

  // Close when the viewport grows past the mobile breakpoint.
  window.matchMedia('(min-width: 768px)').addEventListener('change', (event) => {
    if (event.matches && dialog.open) dialog.close();
  });
}

/**
 * Generic image lightbox: any [data-lightbox-trigger="id"] opens the
 * <dialog id="id"> it references.
 */
function initLightboxes() {
  document.querySelectorAll('[data-lightbox-trigger]').forEach((trigger) => {
    const dialog = document.getElementById(trigger.dataset.lightboxTrigger);
    if (!dialog || typeof dialog.showModal !== 'function') return;

    trigger.addEventListener('click', () => {
      dialog.showModal();
      document.documentElement.style.overflow = 'hidden';
      const scroller = dialog.querySelector('[data-lightbox-scroll]');
      if (scroller) scroller.scrollTop = 0;
    });

    dialog.addEventListener('close', () => {
      document.documentElement.style.overflow = '';
    });

    dialog.addEventListener('click', (event) => {
      if (event.target === dialog) dialog.close();
    });

    dialog.querySelectorAll('[data-lightbox-close]').forEach((btn) => {
      btn.addEventListener('click', () => dialog.close());
    });
  });
}

/**
 * Submits filter forms as soon as a select or checkbox changes, so the
 * project list responds without an explicit "apply" step.
 */
function initAutoSubmit() {
  document.querySelectorAll('form[data-autosubmit]').forEach((form) => {
    form.addEventListener('change', (event) => {
      if (event.target.matches('select, input[type="checkbox"]')) {
        form.requestSubmit();
      }
    });
  });
}

/**
 * Swaps placeholder sources for real ones on images rendered by the
 * `lazy_img` template tag.
 */
function initLazyImages() {
  const lazyImages = document.querySelectorAll('img.lazy');
  if (lazyImages.length === 0) return;

  const load = (img) => {
    img.src = img.dataset.src;
    img.classList.remove('lazy');
  };

  if (!('IntersectionObserver' in window)) {
    lazyImages.forEach(load);
    return;
  }

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        load(entry.target);
        observer.unobserve(entry.target);
      });
    },
    { rootMargin: '200px 0px' }
  );

  lazyImages.forEach((img) => observer.observe(img));
}

document.addEventListener('DOMContentLoaded', () => {
  initHero();
  initHeader();
  initMenu();
  initLightboxes();
  initAutoSubmit();
  initLazyImages();
});
