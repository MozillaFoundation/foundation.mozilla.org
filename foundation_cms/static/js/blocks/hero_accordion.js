/**
 * CSS selectors used to locate key DOM elements in the component.
 */
const SELECTORS = {
  root: ".hero-accordion",
  panel: ".hero-accordion__panel",
  videoWrapper: ".hero-accordion__panel--video-video-wrapper",
  videoOverlay: ".hero-accordion__panel--video-video-wrapper-overlay",
  videoTextWrapper: ".hero-accordion__panel--video-text-wrapper",
};

/**
 * Class names used within the component
 */
const CLASS_NAMES = {
  active: "active",
  hidden: "hidden",
};

/**
 * A horizontal accordion
 */
export class HorizontalAccordion {
  /**
   * @param {HTMLElement} root - The root element of the accordion.
   */
  constructor(root) {
    this.root = root;
    this.panels = root.querySelectorAll(SELECTORS.panel);
  }

  /**
   * Initializes event listeners and sets ARIA attributes.
   */
  init() {
    if (!this.root || this.root.dataset.initialized === "true") return;
    this.root.dataset.initialized = "true";

    this.panels.forEach((panel) => {
      // Ensure every panel has the correct ARIA and tabindex attributes
      panel.setAttribute("role", "button");
      panel.setAttribute("tabindex", "0");
      panel.setAttribute("aria-expanded", "false");

      panel.addEventListener("click", () => {
        if (!panel.classList.contains(CLASS_NAMES.active)) {
          this._deactivateAll();
          this._activate(panel);
        }
      });

      panel.addEventListener("keydown", (e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          panel.click();
        }
      });
    });

    // If there's an active panel by default, mark it expanded
    const active = this.root.querySelector(
      `${SELECTORS.panel}.${CLASS_NAMES.active}`,
    );
    if (active) {
      active.setAttribute("aria-expanded", "true");
    }
  }

  /**
   * Removes the "active" class and aria-expanded="true" from all panels,
   * and restores any video panels to their overlay + text-wrapper state.
   * @private
   */
  _deactivateAll() {
    this.panels.forEach((panel) => {
      if (panel.classList.contains(CLASS_NAMES.active)) {
        this._revertVideoPanel(panel);
      }
      panel.classList.remove(CLASS_NAMES.active);
      panel.setAttribute("aria-expanded", "false");
    });
  }

  /**
   * Adds the "active" class and sets aria-expanded="true" on the target panel.
   * @param {HTMLElement} panel
   * @private
   */
  _activate(panel) {
    panel.classList.add(CLASS_NAMES.active);
    panel.setAttribute("aria-expanded", "true");
  }

  /**
   * Restores a video panel from playing state back to overlay + text-wrapper.
   * Removes any injected <iframe>, shows overlay, and slides text-wrapper back up.
   * @param {HTMLElement} panel
   * @private
   */
  _revertVideoPanel(panel) {
    // Find the video-wrapper inside this panel
    const wrapper = panel.querySelector(SELECTORS.videoWrapper);
    if (!wrapper) return;

    // Remove the <iframe> if one exists
    const existingIframe = wrapper.querySelector("iframe");
    if (existingIframe) {
      existingIframe.remove();
    }

    // Show the overlay again (un-hide it)
    const overlay = wrapper.querySelector(SELECTORS.videoOverlay);
    if (overlay) {
      overlay.classList.remove(CLASS_NAMES.hidden);
    }

    // Show the text-wrapper back into view
    const textWrapper = panel.querySelector(SELECTORS.videoTextWrapper);
    if (textWrapper) {
      textWrapper.classList.remove(CLASS_NAMES.hidden);
    }
  }
}

/**
 * Initializes all horizontal accordions on the page.
 * Assumes multiple accordions may exist with the same selector.
 */
export function initAllHorizontalAccordions() {
  document.querySelectorAll(SELECTORS.root).forEach((el) => {
    new HorizontalAccordion(el).init();
  });

  // Set up the video‐overlay click handlers
  initVideoOverlays();
}

/**
 * Utility: Extracts the numeric Vimeo ID from a URL like "https://vimeo.com/12345678"
 * @param {string} vimeoUrl
 * @returns {string}
 */
function extractVimeoId(vimeoUrl) {
  return vimeoUrl.replace(/^(https?:\/\/)?(www\.)?vimeo\.com\//, "");
}

/**
 * Sets up click handlers on each video-overlay to hide the overlay and text-wrapper,
 * then inject the <iframe>. When a panel is deactivated, HorizontalAccordion._revertVideoPanel()
 * will restore overlay + text.
 */
function initVideoOverlays() {
  document.querySelectorAll(SELECTORS.videoOverlay).forEach((overlay) => {
    overlay.addEventListener("click", () => {
      // Find the closest video-wrapper
      const wrapper = overlay.closest(SELECTORS.videoWrapper);
      if (!wrapper) return;

      // Read the Vimeo URL from data attribute and extract ID
      const videoUrl = overlay.getAttribute("data-video-url") || "";
      const videoId = extractVimeoId(videoUrl.trim());
      if (!videoId) {
        console.warn("Invalid Vimeo URL:", videoUrl);
        return;
      }

      // Hide the bottom text-wrapper in the same panel
      const panel = wrapper.closest(SELECTORS.panel);
      if (panel) {
        const textWrapper = panel.querySelector(SELECTORS.videoTextWrapper);
        if (textWrapper) {
          textWrapper.classList.add(CLASS_NAMES.hidden);
        }
      }

      // Hide the overlay (instead of removing it)
      overlay.classList.add(CLASS_NAMES.hidden);

      // Create the <iframe> to fill the wrapper
      const iframe = document.createElement("iframe");
      iframe.setAttribute(
        "src",
        "https://player.vimeo.com/video/" + videoId + "?autoplay=1",
      );
      iframe.setAttribute("allow", "autoplay; fullscreen; picture-in-picture");
      iframe.setAttribute("allowfullscreen", "");
      iframe.setAttribute("title", "Embedded Vimeo Video");

      wrapper.appendChild(iframe);

      // [TODO/FIXME] Trigger a Sentry call if Vimeo iframe fails to load
    });
  });
}
