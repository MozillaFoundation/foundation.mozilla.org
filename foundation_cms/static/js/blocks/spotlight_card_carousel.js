/**
 * Configuration for carousel card positions and their corresponding CSS variables
 * @constant {Object}
 */
const CARD_CONFIG = {
  featured: { position: 1, cssVar: "--featured-image-height" },
  middle: { position: 2, cssVar: "--middle-image-height" },
  last: { position: 3, cssVar: "--last-image-height" },
};

/**
 * CSS selectors used throughout the carousel
 * @constant {Object}
 */
const SELECTORS = {
  root: ".spotlight-card-set",
  slides: ".spotlight-card-set__slides",
  teaserRegion: ".spotlight-card-set__teaser",
  content: ".spotlight-card__content",
  cards: ".spotlight-card",
  next: ".spotlight-card-set__next",
  prev: ".spotlight-card-set__prev",
  counter: "[data-active-index]",
  featuredCard: `.spotlight-card[data-display-position='${CARD_CONFIG.featured.position}']`,
};

/**
 * Spotlight carousel component that handles card rotation and display
 * Supports both desktop (3-card view) and mobile (single card view) layouts
 * @class
 */
class SpotlightCarousel {
  /**
   * Creates a new SpotlightCarousel instance
   * @param {HTMLElement} root - The root carousel container element
   */
  constructor(root) {
    this.root = root;
    this.slides = root.querySelector(SELECTORS.slides);
    this.teaserRegion = root.querySelector(SELECTORS.teaserRegion);
    this.cards = root.querySelectorAll(SELECTORS.cards);
    this.content = root.querySelectorAll(SELECTORS.content);
    this.nextBtn = root.querySelector(SELECTORS.next);
    this.prevBtn = root.querySelector(SELECTORS.prev);
    this.counter = root.querySelector(SELECTORS.counter);

    this.currentStep = 1;
    this.totalCards = this.cards.length;
    this.resizeTimer = null;
    this.isMobile = false;
    this.cardsByPosition = {};

    this.RESIZE_DEBOUNCE_MS = 200;
    this.DESKTOP_BREAKPOINT = 1024; // our desktop breakpoint, "large", in px

    if (this.totalCards === 0) return;

    this.init();
  }

  /**
   * Initializes the carousel based on current viewport
   * Sets up event listeners and determines mobile vs desktop layout
   */
  init() {
    this.checkViewport();
    this.setupEventListeners();

    if (this.isMobile) {
      this.initMobile();
    } else {
      this.initDesktop();
    }
  }

  /**
   * Checks current viewport width and updates mobile state
   * @returns {boolean} True if viewport changed from mobile to desktop or vice versa
   */
  checkViewport() {
    const wasMobile = this.isMobile;
    this.isMobile = window.innerWidth < this.DESKTOP_BREAKPOINT;

    return wasMobile !== this.isMobile; // returns true if viewport changed
  }

  /**
   * Initializes desktop-specific layout and positioning
   * Shows 3 cards at once with a teaser region
   */
  initDesktop() {
    // Reset any mobile transforms and styles
    this.slides.style.transform = "";
    this.slides.style.minHeight = ""; // Reset minHeight from mobile

    // Set up desktop positioning
    this.updateDesktopPosition();
    this.updateTeaserRegion();
    this.updateAllCardHeights();
    this.updateContainerHeight();
  }

  /**
   * Initializes mobile-specific layout
   * Shows one card at a time with horizontal scrolling
   */
  initMobile() {
    this.slides.style.minHeight = "";

    this.updateMobilePosition();
  }

  /**
   * Sets up event listeners for navigation and resize
   */
  setupEventListeners() {
    this.nextBtn?.addEventListener("click", () => this.handleNext());
    this.prevBtn?.addEventListener("click", () => this.handlePrev());
    window.addEventListener("resize", () => this.handleResize());
  }

  /**
   * Wraps a step number to ensure it stays within bounds
   * @param {number} step - The step to wrap (1-based)
   * @param {number} totalCards - Total number of cards
   * @returns {number} Wrapped step number (1-based)
   */
  wrapStep(step, totalCards) {
    // subtract 1 to go 0-based, mod, then add 1 back
    return ((step - 1 + totalCards) % totalCards) + 1;
  }

  /**
   * Updates data-display-position attributes and caches cards by position
   * Also updates ARIA attributes for accessibility
   */
  updateDataPosition() {
    const offset = this.currentStep - 1;

    // reset the card cache
    this.cardsByPosition = {};

    this.cards.forEach((card, i) => {
      const position = this.wrapStep(i + 1 - offset, this.totalCards);
      card.dataset.displayPosition = position;
      card.setAttribute(
        "aria-hidden",
        position !== CARD_CONFIG.featured.position,
      );
      card.setAttribute("aria-label", `Card ${i + 1} of ${this.totalCards}`);

      // cache the card by its position
      this.cardsByPosition[position] = card;
    });
  }

  /**
   * Handles previous button click
   * Moves carousel one step backward
   */
  handlePrev() {
    this.currentStep = this.wrapStep(this.currentStep - 1, this.totalCards);

    if (this.isMobile) {
      this.handleMobilePrev();
    } else {
      this.handleDesktopPrev();
    }

    this.updateCounterDisplay();
  }

  /**
   * Handles next button click
   * Moves carousel one step forward
   */
  handleNext() {
    this.currentStep = this.wrapStep(this.currentStep + 1, this.totalCards);

    if (this.isMobile) {
      this.handleMobileNext();
    } else {
      this.handleDesktopNext();
    }

    this.updateCounterDisplay();
  }

  /**
   * Updates desktop view when moving to previous card
   */
  handleDesktopPrev() {
    this.updateDesktopPosition();
    this.updateTeaserRegion();
  }

  /**
   * Updates desktop view when moving to next card
   */
  handleDesktopNext() {
    this.updateDesktopPosition();
    this.updateTeaserRegion();
  }

  /**
   * Updates mobile view when moving to previous card
   */
  handleMobilePrev() {
    this.updateMobilePosition();
  }

  /**
   * Updates mobile view when moving to next card
   */
  handleMobileNext() {
    this.updateMobilePosition();
  }

  /**
   * Updates the counter display with current step
   */
  updateCounterDisplay() {
    if (this.counter) {
      this.counter.textContent = this.currentStep;
    }
  }

  /**
   * Updates mobile carousel position using CSS transform
   * Translates the slides container horizontally
   */
  updateMobilePosition() {
    // calculate translateX based on current step
    const translateValue = (this.currentStep - 1) * -100;
    this.slides.style.transform = `translateX(${translateValue}vw)`;
    this.updateDataPosition();
  }

  /**
   * Updates desktop carousel position by changing data attributes
   * Desktop uses CSS for positioning based on data-display-position
   */
  updateDesktopPosition() {
    if (this.isMobile) return;

    this.updateDataPosition();
  }

  /**
   * Updates CSS variables with current card heights
   * Used for desktop layout calculations
   */
  updateAllCardHeights() {
    // this is only needed for desktop
    if (this.isMobile) return;

    Object.values(CARD_CONFIG).forEach(({ position, cssVar }) => {
      const card = this.cardsByPosition[position];
      if (card) {
        this.setCSSVariable(cssVar, `${card.offsetHeight}px`);
      }
    });
  }

  /**
   * Sets a CSS custom property on the root element
   * @param {string} name - CSS variable name
   * @param {string} value - CSS variable value
   */
  setCSSVariable(name, value) {
    this.root.style.setProperty(name, value);
  }

  /**
   * Updates the teaser region with content from the featured card
   * Desktop only - shows expanded content for the featured card
   */
  updateTeaserRegion() {
    // teaser box only exists on desktop
    if (this.isMobile || !this.teaserRegion) return;

    const currentFeaturedCard =
      this.cardsByPosition[CARD_CONFIG.featured.position];
    if (currentFeaturedCard) {
      const content = currentFeaturedCard.querySelector(
        ".spotlight-card__content",
      );
      if (content) {
        this.teaserRegion.innerHTML = content.innerHTML;
      }
    }
  }

  /**
   * Updates the minimum height of the slides container
   * Ensures container is tall enough for featured card + teaser
   */
  updateContainerHeight() {
    // this is only needed for desktop
    if (this.isMobile) return;

    const featuredCard = this.cardsByPosition[CARD_CONFIG.featured.position];
    const teaserRegionHeight = this.teaserRegion?.offsetHeight || 0;

    if (featuredCard) {
      this.slides.style.minHeight = `${featuredCard.offsetHeight + teaserRegionHeight}px`;
    }
  }

  /**
   * Handles window resize events with debouncing
   * Re-initializes carousel if viewport changes between mobile/desktop
   */
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

/**
 * Initializes all spotlight card carousels on the page
 * @exports
 */
export function initSpotlightCardCarousels() {
  const carousels = document.querySelectorAll(SELECTORS.root);

  carousels.forEach((container) => {
    new SpotlightCarousel(container);
  });
}
