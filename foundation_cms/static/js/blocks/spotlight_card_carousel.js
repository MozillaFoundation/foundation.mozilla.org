/**
 * Configuration for carousel card positions and their corresponding CSS variables
 * @constant {Object}
 */
const CARD_CONFIG = {
  featured: { position: 1, cssVar: "--featured-image-height" },
  middle: { position: 2, cssVar: "--middle-image-height" },
  last: { position: 3, cssVar: "--last-image-height" },
};

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
    this.originalCards = Array.from(root.querySelectorAll(SELECTORS.cards));
    this.cards = this.originalCards;
    this.content = root.querySelectorAll(SELECTORS.content);
    this.navSection = root.querySelector(SELECTORS.navSection);
    this.counter = root.querySelector(SELECTORS.counter);
    this.nextButton = root.querySelector(SELECTORS.navButtonNext);
    this.prevButton = root.querySelector(SELECTORS.navButtonPrev);

    this.currentStep = 1;
    this.totalCards = this.originalCards.length;
    this.resizeTimer = null;
    this.isMobile = false;
    this.cardsByPosition = {};
    this.mobileIndex = 0;
    this.isTransitioning = false;

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
    this.slides.style.minHeight = "";
    this.slides.style.width = "";

    // Remove touch event listeners on desktop
    this.removeTouchListeners();

    // Sync currentStep from mobileIndex if coming from mobile
    if (this.cards.length > this.originalCards.length) {
      // Calculate which logical card we're on (1-3)
      const logicalPosition =
        ((this.mobileIndex % this.totalCards) + this.totalCards) %
        this.totalCards;
      this.currentStep = logicalPosition + 1;

      // Restore original cards after syncing
      this.slides.innerHTML = "";
      this.originalCards.forEach((card) => this.slides.appendChild(card));
      this.cards = this.originalCards;
    }

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

    // Setup tripled cards for infinite scroll
    this.setupMobileInfiniteTrack();

    // Sync mobile index with current step
    // For 3 cards: if currentStep is 1, mobileIndex should be 3 (first real card)
    this.mobileIndex = this.totalCards + (this.currentStep - 1);

    this.addTouchListeners();
    this.updateMobilePosition();

    // Re-enable transition after initial positioning
    requestAnimationFrame(() => {
      this.slides.style.transition = `transform ${SWIPE_TRANSITION_DURATION}ms ease-out`;
    });
  }

  /**
   * Creates a tripled set of cards for seamless infinite scroll on mobile
   */
  setupMobileInfiniteTrack() {
    // Only triple if not already done
    if (this.cards.length === this.originalCards.length) {
      const fragment = document.createDocumentFragment();

      // Clone cards: [clones of originals] [originals] [clones of originals]
      this.originalCards.forEach((card) =>
        fragment.appendChild(card.cloneNode(true)),
      );
      this.originalCards.forEach((card) => fragment.appendChild(card));
      this.originalCards.forEach((card) =>
        fragment.appendChild(card.cloneNode(true)),
      );

      this.slides.innerHTML = "";
      this.slides.appendChild(fragment);
      this.cards = Array.from(this.slides.querySelectorAll(SELECTORS.cards));

      // Ensure slides container is wide enough and cards are displayed inline
      this.slides.style.width = `${this.cards.length * 100}vw`;
    }
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
      if (diff > 0) {
        // Swipe right
        this.handlePrev();
      } else {
        // Swipe left
        this.handleNext();
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
    this.mobileIndex--;
    this.updateMobilePosition();
    this.handleMobileInfiniteLoop();
  }

  /**
   * Updates mobile view when moving to next card
   */
  handleMobileNext() {
    this.mobileIndex++;
    this.updateMobilePosition();
    this.handleMobileInfiniteLoop();
  }

  /**
   * Handles the infinite loop reset for mobile
   */
  handleMobileInfiniteLoop() {
    // Prevent multiple loop handlers
    if (this.isTransitioning) return;

    const middleStart = this.totalCards;
    const middleEnd = this.totalCards * 2 - 1;

    // Check if we need to reset position
    if (this.mobileIndex < middleStart || this.mobileIndex > middleEnd) {
      this.isTransitioning = true;

      // Use transitionend event instead of setTimeout for precise timing
      const handleTransitionEnd = (e) => {
        // Only handle transform transitions
        if (e.propertyName !== "transform") return;

        this.slides.removeEventListener("transitionend", handleTransitionEnd);

        // Now that animation is complete, do the invisible jump
        this.slides.style.transition = "none";

        if (this.mobileIndex < middleStart) {
          // We're in the left clones, jump to corresponding position in middle
          this.mobileIndex = this.mobileIndex + this.totalCards;
        } else {
          // We're in the right clones, jump to corresponding position in middle
          this.mobileIndex = this.mobileIndex - this.totalCards;
        }

        // Apply the new position instantly
        const translateValue = this.mobileIndex * 100;
        this.slides.style.transform = `translateX(-${translateValue}vw)`;

        // Force a reflow to ensure the transform is applied before re-enabling transitions
        void this.slides.offsetWidth;

        // Re-enable transitions for next interaction
        requestAnimationFrame(() => {
          this.slides.style.transition = `transform ${SWIPE_TRANSITION_DURATION}ms ease-out`;
          this.isTransitioning = false;
        });
      };

      this.slides.addEventListener("transitionend", handleTransitionEnd);
    }
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
    const translateValue = this.mobileIndex * 100;
    this.slides.style.transform = `translateX(-${translateValue}vw)`;
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
          // Desktop → Mobile
          this.initMobile();
        } else {
          // Mobile → Desktop
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
