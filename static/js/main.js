// Intro overlay typing effect and interactions
document.addEventListener('DOMContentLoaded', () => {
  const overlay = document.getElementById('intro-overlay');
  const terminal = document.getElementById('intro-terminal');
  const skipBtn = document.getElementById('intro-skip');
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Show only once per session
  const alreadyShown = sessionStorage.getItem('introShown') === '1';
  if (!overlay) return;

  function hideOverlay(immediate = false) {
    sessionStorage.setItem('introShown', '1');
    overlay.setAttribute('aria-hidden', 'true');
    if (immediate) {
      overlay.style.display = 'none';
      return;
    }
    overlay.style.transition = 'opacity 600ms ease';
    overlay.style.opacity = '0';
    window.setTimeout(() => {
      overlay.style.display = 'none';
    }, 620);
  }

  if (prefersReducedMotion || alreadyShown) {
    hideOverlay(true);
    return;
  }

  // Lines to type
  const lines = [
    '> Initializing portfolio...',
    '> Loading skills... [████████] 100%',
    '> Loading projects... [████████] 100%',
    '>',
    '> Portfolio of Dimitri Gaggioli',
    '> Python Developer - Backend',
    '>',
    '> Philosophie : Think. Code. Push.',
    '>',
    '> Press [ENTER] or wait to continue...'
  ];

  let aborted = false;
  let lineIndex = 0;

  function typeLine(text, speed = 18) {
    return new Promise((resolve) => {
      let i = 0;
      const line = document.createElement('div');
      terminal.appendChild(line);
      const id = window.setInterval(() => {
        if (aborted) {
          window.clearInterval(id);
          resolve();
          return;
        }
        line.textContent = text.slice(0, i + 1);
        i += 1;
        if (i >= text.length) {
          window.clearInterval(id);
          resolve();
        }
        terminal.scrollTop = terminal.scrollHeight;
      }, speed);
    });
  }

  async function runIntro() {
    // Reveal skip after 2s
    window.setTimeout(() => {
      if (skipBtn) skipBtn.classList.remove('invisible');
    }, 4000);

    for (lineIndex = 0; lineIndex < lines.length; lineIndex += 1) {
      const text = lines[lineIndex];
      const fast = text.includes('[████████]');
      await typeLine(text, fast ? 6 : 18);
      if (aborted) break;
      await new Promise((r) => setTimeout(r, fast ? 120 : 240));
    }
    if (!aborted) {
      await new Promise((r) => setTimeout(r, 800));
    }
    hideOverlay();
  }

  function abortIntro() {
    aborted = true;
    hideOverlay();
  }

  // Event bindings
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      abortIntro();
    }
  });
  overlay.addEventListener('click', abortIntro);
  if (skipBtn) skipBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    abortIntro();
  });

  // Auto-hide safety net after 6s
  window.setTimeout(() => {
    if (!aborted) abortIntro();
  }, 6000);

  runIntro();
});


document.addEventListener('DOMContentLoaded', () => {
  const lazyImages = document.querySelectorAll('img.lazy');

  if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const img = entry.target;
          img.src = img.dataset.src;
          img.classList.remove('lazy');
          observer.unobserve(img);
        }
      });
    });

    lazyImages.forEach((img) => imageObserver.observe(img));
  } else {
    lazyImages.forEach((img) => {
      img.src = img.dataset.src;
      img.classList.remove('lazy');
    });
  }
});


// Animate skill bars on scroll (for about page)
document.addEventListener('DOMContentLoaded', () => {
  const skillBars = document.querySelectorAll('.skill-bar');
  if (skillBars.length === 0) return;

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const bar = entry.target;
          const targetWidth = bar.getAttribute('data-width') || bar.style.width;
          bar.style.width = targetWidth;
        }
      });
    },
    { threshold: 0.5 }
  );

  skillBars.forEach((bar) => {
    const targetWidth = bar.style.width;
    bar.setAttribute('data-width', targetWidth);
    bar.style.width = '0%';
    observer.observe(bar);
  });
});


