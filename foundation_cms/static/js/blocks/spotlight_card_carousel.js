/**
 * Configuration for carousel card positions and their corresponding CSS variables
 * @constant {Object}
 */
const CARD_CONFIG = {
  featured: { position: 1, cssVar: "--featured-image-height" },
  middle: { position: 2, cssVar: "--middle-image-height" },
  last: { position: 3, cssVar: "--last-image-height" },
};

const BTN_DISABLED_ATTR = "disabled";
const SWIPE_THRESHOLD = 50;
const SWIPE_TRANSITION_DURATION = 300; // in milliseconds

/**
 * CSS selectors used throughout the carousel
 * @constant {Object}
 */
const SELECTORS = {
  root: ".spotlight-card-carousel",
  slides: ".spotlight-card-carousel__slides",
  teaserRegion: ".spotlight-card-carousel__teaser",
  content: ".spotlight-card__content",
  cards: ".spotlight-card",
  cardImage: ".spotlight-card__image",
  navSection: ".pagination-controls",
  navButton: ".pagination-controls [data-direction]",
  navButtonNext: ".pagination-controls [data-direction='next']",
  navButtonPrev: ".pagination-controls [data-direction='prev']",
  counter: ".pagination-controls [data-active-index]",
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
    this.navSection = root.querySelector(SELECTORS.navSection);
    this.counter = root.querySelector(SELECTORS.counter);
    this.nextButton = root.querySelector(SELECTORS.navButtonNext);
    this.prevButton = root.querySelector(SELECTORS.prevButtonPrev);

    this.currentStep = 1;
    this.totalCards = this.cards.length;
    this.resizeTimer = null;
    this.isMobile = false;
    this.cardsByPosition = {};

    // For touch/swipe
    this.touchStartX = 0;
    this.touchEndX = 0;
    this.isSwiping = false;
    this.swipeStartTransform = 0;

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

    // Remove disabled attributes on buttons
    this.enableAllButtons();

    // Remove touch event listeners on desktop
    this.removeTouchListeners();

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

    this.addTouchListeners();
    this.updateMobilePosition();
    this.updateMobileButtonStates();
  }

  /**
   * Adds touch event listeners for swipe functionality
   */
  addTouchListeners() {
    this.slides.addEventListener("touchstart", this.handleTouchStart, {
      passive: true,
    });
    this.slides.addEventListener("touchmove", this.handleTouchMove, {
      passive: false,
    });
    this.slides.addEventListener("touchend", this.handleTouchEnd, {
      passive: true,
    });
  }

  /**
   * Removes touch event listeners
   */
  removeTouchListeners() {
    this.slides.removeEventListener("touchstart", this.handleTouchStart);
    this.slides.removeEventListener("touchmove", this.handleTouchMove);
    this.slides.removeEventListener("touchend", this.handleTouchEnd);
  }

  /**
   * Handles touch start event
   * @param {TouchEvent} e - Touch event
   */
  handleTouchStart = (e) => {
    if (!this.isMobile) return;

    this.touchStartX = e.touches[0].clientX;
    this.touchEndX = this.touchStartX;
    this.isSwiping = true;

    // Store the current transform value
    const currentTransform = window.getComputedStyle(this.slides).transform;
    if (currentTransform !== "none") {
      const matrix = new DOMMatrix(currentTransform);
      this.swipeStartTransform = matrix.m41; // translateX value
    } else {
      this.swipeStartTransform = (this.currentStep - 1) * -window.innerWidth;
    }

    // Disable transitions for immediate visual feedback during swipe
    this.slides.style.transition = "none";
  };

  /**
   * Handles touch move event
   * @param {TouchEvent} e - Touch event
   */
  handleTouchMove = (e) => {
    if (!this.isMobile || !this.isSwiping) return;

    this.touchEndX = e.touches[0].clientX;
    const diff = this.touchEndX - this.touchStartX;

    // Apply real-time transform for visual feedback
    const newTransform = this.swipeStartTransform + diff;
    this.slides.style.transform = `translateX(${newTransform}px)`;

    // Prevent vertical scrolling while swiping horizontally
    if (Math.abs(diff) > 10) {
      e.preventDefault();
    }
  };

  /**
   * Handles touch end event
   * @param {TouchEvent} e - Touch event
   */
  handleTouchEnd = (e) => {
    if (!this.isMobile || !this.isSwiping) return;

    this.isSwiping = false;
    const diff = this.touchEndX - this.touchStartX;

    // Re-enable smooth transitions for snap animation
    this.slides.style.transition = `transform ${SWIPE_TRANSITION_DURATION}ms ease-out`;

    // Check if swipe meets threshold
    if (Math.abs(diff) > SWIPE_THRESHOLD) {
      if (diff > 0 && this.currentStep > 1) {
        // Swipe right
        this.handlePrev();
      } else if (diff < 0 && this.currentStep < this.totalCards) {
        // Swipe left
        this.handleNext();
      } else {
        // Can't swipe further, snap back to current position
        this.updateMobilePosition();
      }
    } else {
      // Swipe didn't meet threshold, snap back to current position
      this.updateMobilePosition();
    }

    // Clean up inline transition after animation completes
    setTimeout(() => {
      if (this.slides) {
        this.slides.style.transition = "";
      }
    }, SWIPE_TRANSITION_DURATION);
  };

  /**
   * Updates the disabled state of navigation buttons on mobile
   */
  updateMobileButtonStates() {
    if (!this.isMobile) return;

    // Disable prev button when at first card
    if (this.prevButton) {
      if (this.currentStep === 1) {
        this.prevButton.setAttribute(BTN_DISABLED_ATTR, "");
      } else {
        this.prevButton.removeAttribute(BTN_DISABLED_ATTR);
      }
    }

    // Disable next button when at last card
    if (this.nextButton) {
      if (this.currentStep === this.totalCards) {
        this.nextButton.setAttribute(BTN_DISABLED_ATTR, "");
      } else {
        this.nextButton.removeAttribute(BTN_DISABLED_ATTR);
      }
    }
  }

  /**
   * Enables all navigation buttons
   */
  enableAllButtons() {
    if (this.prevButton) {
      this.prevButton.removeAttribute(BTN_DISABLED_ATTR);
    }
    if (this.nextButton) {
      this.nextButton.removeAttribute(BTN_DISABLED_ATTR);
    }
  }

  /**
   * Sets up event listeners for navigation and resize
   */
  setupEventListeners() {
    // click handlers
    this.root.addEventListener("click", (e) => {
      const navButton = e.target.closest(SELECTORS.navButton);
      const cardImage = e.target.closest(SELECTORS.cardImage);

      if (navButton) {
        if (navButton.hasAttribute("disabled")) {
          return;
        }

        const direction = navButton.dataset.direction;

        if (direction === "next") {
          this.handleNext();
        } else if (direction === "prev") {
          this.handlePrev();
        }
      } else if (cardImage) {
        const card = cardImage.closest(SELECTORS.cards);
        const position = card.dataset.displayPosition;

        if (position == "2") {
          this.handleNext();
        } else if (position == "3") {
          this.handlePrev();
        }
      }
    });

    // keydown handler
    this.root.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") {
        const card = e.target.closest(SELECTORS.cards);
        if (card) {
          const position = card.dataset.displayPosition;
          if (position == "2") {
            e.preventDefault();
            this.handleNext();
          } else if (position == "3") {
            e.preventDefault();
            this.handlePrev();
          }
        }
      }
    });

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

      if (position != "1") {
        card.setAttribute("role", "button");
        card.setAttribute("tabindex", "0");
      } else {
        card.removeAttribute("role");
        card.removeAttribute("tabindex");
      }

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
    this.updateMobileButtonStates();
  }

  /**
   * Updates mobile view when moving to next card
   */
  handleMobileNext() {
    this.updateMobilePosition();
    this.updateMobileButtonStates();
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
    const navSectionHeight = this.navSection?.offsetHeight || 0;

    if (featuredCard) {
      this.slides.style.minHeight = `${featuredCard.offsetHeight + teaserRegionHeight + navSectionHeight}px`;
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
