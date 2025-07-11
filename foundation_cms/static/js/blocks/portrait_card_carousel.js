const SELECTORS = {
  root: '.portrait-card-set',
  viewport: '.portrait-card-set__card-container',
  track: '.carousel-track',
  card: '.portrait-card',
  prevBtn: '.pagination-controls__prev',
  nextBtn: '.pagination-controls__next',
  counter: '[data-active-index]',
  total: '.pagination-controls__total',
};

export function initPortraitCardSetCarousels() {
  const carousels = document.querySelectorAll(SELECTORS.root);
  carousels.forEach((carousel) => new TransformCarousel(carousel));
}

class TransformCarousel {
  constructor(rootEl) {
    this.root = rootEl;
    this.viewport = this.root.querySelector(SELECTORS.viewport);
    this.track = this.viewport.querySelector(SELECTORS.track);
    this.originalCards = Array.from(this.track.querySelectorAll(SELECTORS.card));
    this.prevBtn = this.root.querySelector(SELECTORS.prevBtn);
    this.nextBtn = this.root.querySelector(SELECTORS.nextBtn);
    this.counterEl = this.root.querySelector(SELECTORS.counter);
    this.total = this.originalCards.length;

    this.visibleCount = 3;
    this.isTransitioning = false;
    this.index = this.total; // Start in the middle of the tripled array
    this.isCarousel = this.root.classList.contains('is-carousel');

    this.init();
  }

  init() {
    this.applyCardColorDataAttrs(this.originalCards);
    this.setupTrack();
    this.setInitialPosition();
    this.bindEvents();
    this.updateCounter();
  }

  // Add data-card-color based on total colors needed
  applyCardColorDataAttrs(cards) {
    cards.forEach((card, i) => {
      card.setAttribute('data-card-color', i % this.total);
    });
  }

  // Create a tripled set of cards to simulate infinite scroll
  setupTrack() {
    const tripled = [
      ...this.originalCards,
      ...this.originalCards.map(card => card.cloneNode(true)),
      ...this.originalCards.map(card => card.cloneNode(true))
    ];

    this.track.innerHTML = '';
    this.applyCardColorDataAttrs(tripled);

    tripled.forEach(card => this.track.appendChild(card));
    this.cards = Array.from(this.track.querySelectorAll(SELECTORS.card));
  }

  // Calculate scroll offset for the current index
  getSlideOffset() {
    const card = this.cards[this.index];
    if (!card) return 0;
    const style = window.getComputedStyle(card);
    return card.getBoundingClientRect().width + parseFloat(style.marginRight);
  }

  // Move the carousel track by transform
  updateTransform(index, animate = true) {
    const offset = this.getSlideOffset() * index;
    this.track.style.transition = animate ? 'transform 0.4s ease' : 'none';
    this.track.style.transform = `translateX(-${offset}px)`;
  }

  // Initial transform (no animation)
  setInitialPosition() {
    requestAnimationFrame(() => {
      this.updateTransform(this.index, false);
    });
  }

  // Navigate to a given index
  slideTo(newIndex) {
    const shouldDisable = !this.root.classList.contains('is-carousel') && window.innerWidth >= 1024;
    if (shouldDisable || this.isTransitioning) return;

    this.isTransitioning = true;
    this.index = newIndex;
    this.updateTransform(this.index, true);

    this.track.addEventListener('transitionend', () => this.handleLoop(), { once: true });
  }

  // Loop logic to simulate infinite scroll
  handleLoop() {
    if (this.index >= this.total * 2) {
      this.index = this.total;
    } else if (this.index < this.total) {
      this.index = this.total * 2 - 1;
    }

    this.updateTransform(this.index, false);
    this.updateCounter();
    this.isTransitioning = false;
  }

  // Update visual counter display
  updateCounter() {
    if (this.counterEl) {
      const logicalIndex = (this.index % this.total + this.total) % this.total;
      this.counterEl.textContent = `${logicalIndex + 1}`;
    }
  }

  // Bind arrow keys, buttons, swipe, and drag for navigation
  bindEvents() {
    this.nextBtn?.addEventListener('click', () => this.slideTo(this.index + 1));
    this.prevBtn?.addEventListener('click', () => this.slideTo(this.index - 1));

    let startX = 0;
    let isDragging = false;

    // Touch support
    this.viewport.addEventListener('touchstart', (e) => {
      startX = e.touches[0].clientX;
      isDragging = true;
    }, { passive: true });

    this.viewport.addEventListener('touchend', (e) => {
      if (!isDragging) return;
      isDragging = false;
      const delta = e.changedTouches[0].clientX - startX;
      if (Math.abs(delta) > 50) delta < 0 ? this.slideTo(this.index + 1) : this.slideTo(this.index - 1);
    }, { passive: true });

    // Mouse drag support
    this.viewport.addEventListener('mousedown', (e) => {
      startX = e.clientX;
      isDragging = true;
    });

    this.viewport.addEventListener('mouseup', (e) => {
      if (!isDragging) return;
      isDragging = false;
      const delta = e.clientX - startX;
      if (Math.abs(delta) > 50) delta < 0 ? this.slideTo(this.index + 1) : this.slideTo(this.index - 1);
    });

    this.viewport.addEventListener('mouseleave', () => {
      if (isDragging) isDragging = false;
    });

    // Keyboard navigation
    this.root.setAttribute('tabindex', '0');
    this.root.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowRight') this.slideTo(this.index + 1);
      if (e.key === 'ArrowLeft') this.slideTo(this.index - 1);
    });

    // Recalculate position on resize
    window.addEventListener('resize', () => {
      this.setInitialPosition();
    });
  }
}
