const SELECTORS = {
  root: ".portrait-card-set",
  viewport: ".portrait-card-set__card-container",
  track: ".carousel-track",
  card: ".portrait-card",
  prevBtn: ".pagination-controls__prev",
  nextBtn: ".pagination-controls__next",
  counter: "[data-active-index]",
  total: ".pagination-controls__total",
};

const NUM_CARD_DESIGNS = 4;
const RESIZE_DEBOUNCE_MS = 200;
const SWIPE_THRESHOLD = 50;
const DISABLE_CAROUSEL_MIN_WIDTH = 1024;

export function initPortraitCardSetCarousels() {
  const carousels = document.querySelectorAll(SELECTORS.root);
  carousels.forEach((carousel) => new TransformCarousel(carousel));
}

class TransformCarousel {
  constructor(rootEl) {
    this.root = rootEl;
    this.viewport = this.root.querySelector(SELECTORS.viewport);
    this.track = this.viewport.querySelector(SELECTORS.track);
    this.originalCards = Array.from(
      this.track.querySelectorAll(SELECTORS.card),
    );
    this.prevBtn = this.root.querySelector(SELECTORS.prevBtn);
    this.nextBtn = this.root.querySelector(SELECTORS.nextBtn);
    this.counterEl = this.root.querySelector(SELECTORS.counter);
    this.total = this.originalCards.length;

    this.visibleCount = 3;
    this.index = this.total;
    this.middleStart = this.total;
    this.middleEnd = this.total * 2;
    this.nextCloneTrackStart = this.middleEnd + 1;
    this.prevCloneTrackEnd = this.middleStart - 1;

    this.isCarousel = this.root.classList.contains("is-carousel");

    this.resizeTimer = null;
    this.slideOffset = 0;
    this.carouselTransition = "";

    this.init();
  }

  init() {
    this.applyCardColorDataAttrs(this.originalCards);
    this.setupTrack();
    this.cacheComputedValues();
    this.setInitialPosition();
    this.bindEvents();
    this.updateCounter();
  }

  // Store cachable values like width/offset and transition variable.
  cacheComputedValues() {
    const card = this.cards[this.index];
    if (card) {
      const style = window.getComputedStyle(card);
      this.slideOffset =
        card.getBoundingClientRect().width + parseFloat(style.marginRight);
    }
    this.carouselTransition = getComputedStyle(this.track)
      .getPropertyValue("--carousel-transition")
      .trim();
  }

  // Add data-card-design based on how many card designs we have
  applyCardColorDataAttrs(cards) {
    cards.forEach((card, i) => {
      card.setAttribute("data-card-design", i % NUM_CARD_DESIGNS);
    });
  }

  // Create a tripled set of cards to simulate infinite scroll
  setupTrack() {
    const tripled = [
      ...this.originalCards.map((card) => card.cloneNode(true)),
      ...this.originalCards,
      ...this.originalCards.map((card) => card.cloneNode(true)),
    ];

    const fragment = document.createDocumentFragment();
    tripled.forEach((card) => fragment.appendChild(card));

    this.track.innerHTML = "";
    this.track.appendChild(fragment);
    this.cards = Array.from(this.track.querySelectorAll(SELECTORS.card));
  }

  // Move the carousel track by transform
  updateTransform(index, animate = true) {
    const offset = this.slideOffset * index;
    this.track.style.transition = animate ? this.carouselTransition : "none";
    this.track.style.transform = `translateX(-${offset}px)`;
  }

  // Initial transform (no animation)
  setInitialPosition() {
    requestAnimationFrame(() => {
      this.cacheComputedValues();
      this.updateTransform(this.index, false);
    });
  }

  // Navigate to a given index
  slideTo(newIndex) {
    if (!this.isCarousel && window.innerWidth >= DISABLE_CAROUSEL_MIN_WIDTH)
      return;

    // handle loop
    if (this.handleLoop(newIndex)) return;

    // or increment
    this.index = newIndex;
    this.updateTransform(this.index, true);
    this.updateCounter();
  }

  // Loop logic to simulate infinite scroll
  handleLoop(newIndex) {
    if (newIndex === this.nextCloneTrackStart) {
      this.track.style.transition = "none";
      this.index = this.middleStart;
      this.updateTransform(this.index, false);

      // Double requestAnimationFrame required to avoid visual jump
      requestAnimationFrame(() => {
        requestAnimationFrame(() => {
          this.index += 1;
          this.updateTransform(this.index, true);
          this.updateCounter();
        });
      });
      return true;
    }

    if (newIndex === this.prevCloneTrackEnd) {
      this.track.style.transition = "none";
      this.index = this.middleEnd;
      this.updateTransform(this.index, false);

      // Double requestAnimationFrame required to avoid visual jump
      requestAnimationFrame(() => {
        requestAnimationFrame(() => {
          this.index -= 1;
          this.updateTransform(this.index, true);
          this.updateCounter();
        });
      });
      return true;
    }

    return false;
  }

  // Update visual counter display
  updateCounter() {
    if (this.counterEl) {
      this.counterEl.textContent = `${this.getLogicalIndex() + 1}`;
    }
  }

  // Return current logical index within original card set
  getLogicalIndex() {
    return ((this.index % this.total) + this.total) % this.total;
  }

  // Recalc based on window resize w/ debounce
  handleResize() {
    clearTimeout(this.resizeTimer);
    this.resizeTimer = setTimeout(() => {
      this.setInitialPosition();
    }, RESIZE_DEBOUNCE_MS);
  }

  // Unified swipe/drag handler
  handleSwipe(delta) {
    if (Math.abs(delta) > SWIPE_THRESHOLD) {
      this.slideTo(delta < 0 ? this.index + 1 : this.index - 1);
    }
  }

  // Bind arrow keys, buttons, swipe, and drag for navigation
  bindEvents() {
    this.nextBtn?.addEventListener("click", () => this.slideTo(this.index + 1));
    this.prevBtn?.addEventListener("click", () => this.slideTo(this.index - 1));

    let startX = 0;
    let isDragging = false;

    const onStart = (x) => {
      startX = x;
      isDragging = true;
    };

    const onEnd = (x) => {
      if (!isDragging) return;
      isDragging = false;
      const delta = x - startX;
      this.handleSwipe(delta);
    };

    // Touch support
    this.viewport.addEventListener(
      "touchstart",
      (e) => onStart(e.touches[0].clientX),
      { passive: true },
    );
    this.viewport.addEventListener(
      "touchend",
      (e) => onEnd(e.changedTouches[0].clientX),
      { passive: true },
    );

    // Mouse drag support
    this.viewport.addEventListener("mousedown", (e) => onStart(e.clientX));
    this.viewport.addEventListener("mouseup", (e) => onEnd(e.clientX));
    this.viewport.addEventListener("mouseleave", () => {
      if (isDragging) isDragging = false;
    });

    // Keyboard navigation
    this.root.setAttribute("tabindex", "0");
    this.root.addEventListener("keydown", (e) => {
      if (e.key === "ArrowRight") this.slideTo(this.index + 1);
      if (e.key === "ArrowLeft") this.slideTo(this.index - 1);
    });

    // Recalculate position on resize
    window.addEventListener("resize", () => this.handleResize());
  }
}
