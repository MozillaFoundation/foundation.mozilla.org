const SELECTORS = {
  root: '.portrait-card-set',
  container: '.portrait-card-set__card-container',
  card: '.portrait-card',
  prevBtn: '.pagination-controls__prev',
  nextBtn: '.pagination-controls__next',
  counter: '[data-active-index]',
  total: '.pagination-controls__total',
};

export function initPortraitCardSetCarousels() {
  const carousels = document.querySelectorAll(SELECTORS.root);
  carousels.forEach((carousel) => new PortraitCardCarousel(carousel));
}

class PortraitCardCarousel {
  constructor(rootEl) {
    this.root = rootEl;
    this.container = this.root.querySelector(SELECTORS.container);
    this.cards = Array.from(this.container.children);
    this.prevBtn = this.root.querySelector(SELECTORS.prevBtn);
    this.nextBtn = this.root.querySelector(SELECTORS.nextBtn);
    this.counterEl = this.root.querySelector(SELECTORS.counter);
    this.total = this.cards.length;

    this.cardWidth = 0;
    this.currentIndex = 0;
    this.isTransitioning = false;
    this.cloned = false;

    this.init();
  }

  init() {
    this.applyCardColorDataAttrs();
    this.cloneSlides();
    this.updateMeasurements();
    this.goTo(this.currentIndex, false);
    this.bindEvents();
    this.updateCounter();
  }

  applyCardColorDataAttrs() {
    this.originalCards = Array.from(this.container.children);

    this.originalCards.forEach((card, i) => {
      card.setAttribute('data-card-color', i % 4);
    });
  }

  cloneSlides() {
    if (this.cloned) return;

    const headClones = this.cards.slice(0, 2).map(el => el.cloneNode(true));
    const tailClones = this.cards.slice(-2).map(el => el.cloneNode(true));

    tailClones.reverse().forEach(el => this.container.prepend(el));
    headClones.forEach(el => this.container.appendChild(el));

    this.cloned = true;
    this.cards = Array.from(this.container.children);
  }

  updateMeasurements() {
    const firstCard = this.container.querySelector(SELECTORS.card);
    this.cardWidth = firstCard.getBoundingClientRect().width + this.getGap();

    // Scroll to the first "real" card
    this.container.scrollLeft = this.cardWidth * 2;
  }

  getGap() {
    const style = window.getComputedStyle(this.container);
    return parseFloat(style.columnGap || style.gap || 0);
  }

  goTo(index, smooth = true) {
    this.currentIndex = index;

    const scrollTarget = this.cardWidth * (index + 2);
    this.container.scrollTo({
      left: scrollTarget,
      behavior: smooth ? 'smooth' : 'auto'
    });

    this.updateCounter();
  }

  next() {
    if (this.isTransitioning) return;
    this.isTransitioning = true;
    this.goTo(this.currentIndex + 1);

    this.handleLoopIfNeeded();
  }

  prev() {
    if (this.isTransitioning) return;
    this.isTransitioning = true;
    this.goTo(this.currentIndex - 1);

    this.handleLoopIfNeeded();
  }

  handleLoopIfNeeded() {
    setTimeout(() => {
      if (this.currentIndex >= this.total) {
        this.goTo(0, false);
      } else if (this.currentIndex < 0) {
        this.goTo(this.total - 1, false);
      }
      this.isTransitioning = false;
    }, 400); // match smooth scroll duration
  }

  updateCounter() {
    if (this.counterEl) {
      const displayIndex = ((this.currentIndex % this.total + this.total) % this.total) + 1;
      this.counterEl.textContent = `${displayIndex}`;
    }
  }

  bindEvents() {
    this.nextBtn?.addEventListener('click', () => this.next());
    this.prevBtn?.addEventListener('click', () => this.prev());

    let startX = 0;

    this.container.addEventListener('touchstart', (e) => {
      startX = e.touches[0].clientX;
    }, { passive: true });

    this.container.addEventListener('touchend', (e) => {
      const endX = e.changedTouches[0].clientX;
      const delta = endX - startX;
      if (Math.abs(delta) > 50) {
        if (delta < 0) this.next();
        else this.prev();
      }
    }, { passive: true });

    window.addEventListener('resize', () => {
      this.updateMeasurements();
      this.goTo(this.currentIndex, false);
    });
  }
}
