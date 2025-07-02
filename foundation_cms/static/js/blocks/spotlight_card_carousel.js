const CARD_CONFIG = {
  featured: { position: 1, cssVar: "--featured-image-height" },
  middle: { position: 2, cssVar: "--middle-image-height" },
  last: { position: 3, cssVar: "--last-image-height" },
};

const SELECTORS = {
  root: ".spotlight-card-set",
  slides: ".spotlight-card-set__slides",
  details: ".spotlight-card-set__details",
  content: ".spotlight-card__content",
  cards: ".spotlight-card",
  next: ".spotlight-card-set__next",
  prev: ".spotlight-card-set__prev",
  counter: "[data-active-index]",
  featuredCard: `.spotlight-card[data-display-position='${CARD_CONFIG.featured.position}']`,
};

class SpotlightCarousel {
  constructor(root) {
    this.root = root;
    this.slides = root.querySelector(SELECTORS.slides);
    this.details = root.querySelector(SELECTORS.details);
    this.cards = root.querySelectorAll(SELECTORS.cards);
    this.content = root.querySelectorAll(SELECTORS.content);
    this.nextBtn = root.querySelector(SELECTORS.next);
    this.prevBtn = root.querySelector(SELECTORS.prev);
    this.counter = root.querySelector(SELECTORS.counter);

    this.currentStep = 1;
    this.totalCards = this.cards.length;
    this.resizeTimer = null;
    this.isMobile = false;

    this.RESIZE_DEBOUNCE_MS = 200;
    this.DESKTOP_BREAKPOINT = 1024; // our desktop breakpoint, "large", in px

    if (this.totalCards === 0) return;

    this.init();
  }

  init() {
    this.checkViewport();
    this.setupEventListeners();

    if (this.isMobile) {
      this.initMobile();
    } else {
      this.initDesktop();
    }
  }

  checkViewport() {
    const wasMobile = this.isMobile;
    this.isMobile = window.innerWidth < this.DESKTOP_BREAKPOINT;

    return wasMobile !== this.isMobile; // returns true if viewport changed
  }

  initDesktop() {
    // Reset any mobile transforms and styles
    this.slides.style.transform = "";
    this.slides.style.minHeight = ""; // Reset minHeight from mobile

    // Set up desktop positioning
    this.updateDesktopPosition(); // do i need this?
    this.updateDetails();
    this.updateAllCardHeights();
    this.updateContainerHeight();
  }

  initMobile() {
    this.slides.style.minHeight = "";

    this.updateMobilePosition();
  }

  setupEventListeners() {
    this.nextBtn?.addEventListener("click", () => this.handleNext());
    this.prevBtn?.addEventListener("click", () => this.handlePrev());
    window.addEventListener("resize", () => this.handleResize());
  }

  wrapStep(step, totalCards) {
    // subtract 1 to go 0-based, mod, then add 1 back
    return ((step - 1 + totalCards) % totalCards) + 1;
  }

  updateDataPosition() {
    const offset = this.currentStep - 1;

    this.cards.forEach((card, i) => {
      card.dataset.displayPosition = this.wrapStep(
        i + 1 - offset,
        this.totalCards,
      );
    });
  }

  handlePrev() {
    this.currentStep = this.wrapStep(this.currentStep - 1, this.totalCards);

    if (this.isMobile) {
      this.handleMobilePrev();
    } else {
      this.handleDesktopPrev();
    }

    this.updateCounterDisplay();
  }

  handleNext() {
    this.currentStep = this.wrapStep(this.currentStep + 1, this.totalCards);

    if (this.isMobile) {
      this.handleMobileNext();
    } else {
      this.handleDesktopNext();
    }

    this.updateCounterDisplay();
  }

  handleDesktopPrev() {
    this.updateDesktopPosition();
    this.updateDetails();
  }

  handleDesktopNext() {
    this.updateDesktopPosition();
    this.updateDetails();
  }

  handleMobilePrev() {
    this.updateMobilePosition();
  }

  handleMobileNext() {
    this.updateMobilePosition();
  }

  updateCounterDisplay() {
    if (this.counter) {
      this.counter.textContent = this.currentStep;
    }
  }

  updateMobilePosition() {
    // calculate translateX based on current step
    const translateValue = (this.currentStep - 1) * -100;
    this.slides.style.transform = `translateX(${translateValue}vw)`;
    this.updateDataPosition();
  }

  updateDesktopPosition() {
    if (this.isMobile) return;

    this.updateDataPosition();
  }

  updateAllCardHeights() {
    // this is only needed for desktop
    if (this.isMobile) return;

    Object.values(CARD_CONFIG).forEach(({ position, cssVar }) => {
      const card = this.root.querySelector(
        `[data-display-position="${position}"]`,
      );
      if (card) {
        this.setCSSVariable(cssVar, `${card.offsetHeight}px`);
      }
    });
  }

  setCSSVariable(name, value) {
    this.root.style.setProperty(name, value);
  }

  updateDetails() {
    // details box only exists on desktop
    if (this.isMobile || !this.details) return;

    const currentFeaturedCard = this.root.querySelector(SELECTORS.featuredCard);
    if (currentFeaturedCard) {
      const content = currentFeaturedCard.querySelector(
        ".spotlight-card__content",
      );
      if (content) {
        this.details.innerHTML = content.innerHTML;
      }
    }
  }

  updateContainerHeight() {
    // this is only needed for desktop
    if (this.isMobile) return;

    const featuredCard = this.root.querySelector(SELECTORS.featuredCard);
    const detailsHeight = this.details.offsetHeight || 0;

    if (featuredCard) {
      this.slides.style.minHeight = `${featuredCard.offsetHeight + detailsHeight}px`;
    }
  }

  handleResize() {
    clearTimeout(this.resizeTimer);
    this.resizeTimer = setTimeout(() => {
      const viewportChanged = this.checkViewport();

      if (viewportChanged) {
        if (this.isMobile) {
          this.initMobile();
        } else {
          this.initDesktop();
        }
      } else if (!this.isMobile) {
        // Still desktop. Just update heights
        this.updateContainerHeight();
        this.updateAllCardHeights();
      }
    }, this.RESIZE_DEBOUNCE_MS);
  }
}

export function initSpotlightCardCarousels() {
  const carousels = document.querySelectorAll(SELECTORS.root);

  carousels.forEach((container) => {
    new SpotlightCarousel(container);
  });
}
