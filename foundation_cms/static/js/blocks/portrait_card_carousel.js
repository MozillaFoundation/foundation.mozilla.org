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
    this.index = this.total * 2; // Start in the middle of the quintupled array
    this.isCarousel = this.root.classList.contains("is-carousel");

    this.resizeTimer = null;
    this.RESIZE_DEBOUNCE_MS = 200;
    this.SWIPE_THRESHOLD = 50;
    this.DISABLE_CAROUSEL_MIN_WIDTH = 1024;

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

  cacheComputedValues() {
    const card = this.cards[this.index];
    if (card) {
      const style = window.getComputedStyle(card);
      this.slideOffset = card.getBoundingClientRect().width + parseFloat(style.marginRight);
    }
    this.carouselTransition = getComputedStyle(this.track)
      .getPropertyValue("--carousel-transition")
      .trim();
  }

  // Add data-card-color based on total colors needed
  applyCardColorDataAttrs(cards) {
    cards.forEach((card, i) => {
      card.setAttribute("data-card-color", i % this.total);
    });
  }

  // Create a quintupled set of cards to simulate infinite scroll with extra buffer
  setupTrack() {
    const quintupled = [
      ...this.originalCards.map((card) => card.cloneNode(true)),
      ...this.originalCards.map((card) => card.cloneNode(true)),
      ...this.originalCards,
      ...this.originalCards.map((card) => card.cloneNode(true)),
      ...this.originalCards.map((card) => card.cloneNode(true)),
    ];

    this.track.innerHTML = "";
    this.applyCardColorDataAttrs(quintupled);

    quintupled.forEach((card) => this.track.appendChild(card));
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
    const shouldDisable =
      !this.root.classList.contains("is-carousel") &&
      window.innerWidth >= this.DISABLE_CAROUSEL_MIN_WIDTH;
    if (shouldDisable) return;

    this.index = newIndex;
    this.updateTransform(this.index, true);
    this.track.addEventListener("transitionend", () => this.handleLoop(), {
      once: true,
    });
  }

  // Loop logic to simulate infinite scroll
  handleLoop() {
    const totalLen = this.total * 5;
    const middleStart = this.total * 2;
    const middleEnd = this.total * 3;

    if (this.index >= middleEnd) {
      this.index -= this.total;
      this.updateTransform(this.index, false);
    } else if (this.index < middleStart) {
      this.index += this.total;
      this.updateTransform(this.index, false);
    }

    this.updateCounter();
  }

  // Update visual counter display
  updateCounter() {
    if (this.counterEl) {
      const logicalIndex =
        ((this.index % this.total) + this.total) % this.total;
      this.counterEl.textContent = `${logicalIndex + 1}`;
    }
  }

  // recalc based on window resize w/ debounce
  handleResize() {
    clearTimeout(this.resizeTimer);
    this.resizeTimer = setTimeout(() => {
      this.setInitialPosition();
    }, this.RESIZE_DEBOUNCE_MS);
  }

  // Bind arrow keys, buttons, swipe, and drag for navigation
  bindEvents() {
    this.nextBtn?.addEventListener("click", () => this.slideTo(this.index + 1));
    this.prevBtn?.addEventListener("click", () => this.slideTo(this.index - 1));

    let startX = 0;
    let isDragging = false;

    // Touch support
    this.viewport.addEventListener(
      "touchstart",
      (e) => {
        startX = e.touches[0].clientX;
        isDragging = true;
      },
      { passive: true },
    );

    this.viewport.addEventListener(
      "touchend",
      (e) => {
        if (!isDragging) return;
        isDragging = false;
        const delta = e.changedTouches[0].clientX - startX;
        if (Math.abs(delta) > this.SWIPE_THRESHOLD)
          delta < 0
            ? this.slideTo(this.index + 1)
            : this.slideTo(this.index - 1);
      },
      { passive: true },
    );

    // Mouse drag support
    this.viewport.addEventListener("mousedown", (e) => {
      startX = e.clientX;
      isDragging = true;
    });

    this.viewport.addEventListener("mouseup", (e) => {
      if (!isDragging) return;
      isDragging = false;
      const delta = e.clientX - startX;
      if (Math.abs(delta) > this.SWIPE_THRESHOLD)
        delta < 0 ? this.slideTo(this.index + 1) : this.slideTo(this.index - 1);
    });

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
