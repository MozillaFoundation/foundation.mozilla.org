import utility from "../../../utility.js";
import navNewsletter from "../../../nav-newsletter.js";

// factor for bringing image blocks closer to perspective origin
const ZOOM_FACTOR = 2.5;
// where on the z-axis do we want the rings to start spread out
const RING_DEPTH_FACTOR = 1 / 4;
// speed factors
const TEXT_SPEED_FACTOR = 0.7;
const BLOCK_SPEED_FACTOR = 0.8;
const RING_SPEED_FACTOR = 0.6;

let elements = {
  introViewport: `#view-youtube-regrets .intro-viewport`,
  blocks: `#view-youtube-regrets .intro-viewport .block`,
  rings: `#view-youtube-regrets .intro-viewport .ring`,
  introText: `#view-youtube-regrets .intro-viewport .intro-text p`,
  scrollHint: `#view-youtube-regrets .intro-viewport .scroll-hint`,
  newsletterButtons: `#view-youtube-regrets .intro-viewport .btn-newsletter`,
  newsletterButtonMobile: `#view-youtube-regrets .intro-viewport .btn-newsletter.for-mobile`,
  newsletterButtonDesktop: `#view-youtube-regrets .intro-viewport .btn-newsletter.for-desktop`
};

class YouTubeRegretsTunnel {
  constructor() {
    this.introScrollHeight = 0;
    this.sceneDepth = 0;
    this.lastPageYOffset = 0;

    this.init();
  }

  /**
   * Fade in text blocks one by one as user scrolls
   */
  setIntroTextOpacity() {
    let introText = elements.introText;
    let length = introText.length;
    let textToBlockRatio = length / elements.blocks.length;
    let totalScrollDistance =
      (this.introScrollHeight * textToBlockRatio) / TEXT_SPEED_FACTOR;

    introText.forEach((item, i) => {
      let positionToShow = totalScrollDistance * (i / length);
      let positionToHide = totalScrollDistance * ((i + 1) / length);

      if (
        positionToShow <= this.lastPageYOffset &&
        this.lastPageYOffset < positionToHide
      ) {
        item.style.opacity = Math.min(
          1 -
            (this.lastPageYOffset - positionToShow) /
              (positionToHide - positionToShow),
          1
        );
      } else {
        item.style.opacity = 0;
      }
    });

    this.setNewsletterButtonVisibility(totalScrollDistance);
  }

  /**
   * Show newsletter signup button if intro is in current viewport.
   * Hide it otherwise.
   */
  setNewsletterButtonVisibility(positionTohide) {
    let buttons = elements.newsletterButtons;

    buttons.forEach(button => {
      if (window.pageYOffset >= positionTohide) {
        button.classList.add(`d-none`);
      } else {
        button.classList.remove(`d-none`);
      }
    });
  }

  /**
   * Set opacity for flying objects so they are become more visible
   * as they come closer to the threshold we set
   */
  setFlyingObjectOpacity(objects, baseGap) {
    const Z_POSITION_TO_SHOW =
      this.scenePerspective - baseGap * Math.ceil(objects.length / 2);
    let opacity = 1;

    objects.forEach(item => {
      let matrix = window.getComputedStyle(item).transform;
      let coord = this.getCoordinatefromMatrix3d(matrix);

      if (coord) {
        opacity = Math.min(1 - coord.z / Z_POSITION_TO_SHOW, 1);
      }

      item.style.opacity = opacity;
    });
  }

  /**
   * Set opacity for image blocks
   */
  setBlocksOpacity() {
    this.setFlyingObjectOpacity(elements.blocks, this.baseBlockGap);
  }

  /**
   * Set opacity for rings
   */
  setRingsOpacity() {
    this.setFlyingObjectOpacity(elements.rings, this.baseRingGap);
  }

  /**
   * Move objects towards / away from viewint point as user scrolls
   */
  moveObjects() {
    this.lastPageYOffset = window.pageYOffset;

    let blocksSpeedFactor = elements.blocks.length / elements.introText.length;

    this.updateCSSCustomProperty(
      `--blockZTranslate`,
      ((this.lastPageYOffset * blocksSpeedFactor) / ZOOM_FACTOR) *
        BLOCK_SPEED_FACTOR
    );
    this.updateCSSCustomProperty(
      `--ringZTranslate`,
      ((this.lastPageYOffset * RING_DEPTH_FACTOR * blocksSpeedFactor) /
        ZOOM_FACTOR) *
        RING_SPEED_FACTOR
    );
  }

  /**
   * Parse x, y, and z coordinate from matrix
   */
  getCoordinatefromMatrix3d(matrix = ``) {
    let matrix3d;

    try {
      if (typeof DOMMatrix !== `undefined`) {
        matrix3d = new DOMMatrix(matrix);
      } else {
        // for Microsoft browsers
        matrix3d = new WebKitCSSMatrix(matrix);
      }
    } catch (error) {
      console.log(error);
    }

    return !!matrix3d
      ? {
          x: matrix3d.m41,
          y: matrix3d.m42,
          z: matrix3d.m43
        }
      : false;
  }

  setSceneDepth() {
    const scenePerspective = parseFloat(
      this.getCSSCustomPropertyValue(`--scenePerspective`)
    );
    this.scenePerspective = scenePerspective;

    // depth of the scene
    this.sceneDepth = window.innerHeight * 3;

    // the total scroll distance users have to scroll in order to get through the intro tunnel
    this.introScrollHeight = this.sceneDepth + this.scenePerspective;

    this.baseBlockGap = this.sceneDepth / elements.blocks.length / ZOOM_FACTOR;
    this.baseRingGap =
      (this.sceneDepth * RING_DEPTH_FACTOR) /
      elements.rings.length /
      ZOOM_FACTOR;

    // update CSS custom properties
    this.updateCSSCustomProperty(`--sceneDepth`, this.sceneDepth);
    this.updateCSSCustomProperty(`--baseBlockGap`, this.baseBlockGap);
    this.updateCSSCustomProperty(`--baseRingGap`, this.baseRingGap);
  }

  /**
   * Update CSS custom property
   */
  updateCSSCustomProperty(property, value) {
    elements.introViewport[0].style.setProperty(property, value);
  }

  /**
   * Get CSS custom property's value
   */
  getCSSCustomPropertyValue(property) {
    return window
      .getComputedStyle(elements.introViewport[0])
      .getPropertyValue(property);
  }

  /**
   * Update objects' opacity value as user scrolls
   */
  setObjectsOpacity() {
    this.setIntroTextOpacity();
    this.setBlocksOpacity();
    this.setRingsOpacity();
  }

  /**
   * Toggle scrolling hint
   */
  toggleScrollHint() {
    if (window.pageYOffset !== 0) {
      elements.scrollHint[0].classList.add(`d-none`);
    } else {
      elements.scrollHint[0].classList.remove(`d-none`);
    }
  }

  /**
   * Initiate interactive intro
   */
  init() {
    this.loadAttempt = this.loadAttempt || 1;

    if (!utility.checkAndBindDomNodes(elements, true)) {
      if (this.loadAttempt++ < 5) {
        setTimeout(() => this.init(), 200);
      }
      return;
    }

    elements.newsletterButtonDesktop[0].addEventListener(`click`, event =>
      navNewsletter.buttonDesktopClickHandler(event)
    );

    elements.newsletterButtonMobile[0].addEventListener(`click`, event => {
      if (navNewsletter.getShownState()) {
        navNewsletter.closeMobileNewsletter(event);
      } else {
        navNewsletter.expandMobileNewsletter(event);
      }
    });

    this.setSceneDepth();
    this.setObjectsOpacity();
    this.toggleScrollHint();

    window.addEventListener(
      `scroll`,
      () => {
        this.moveObjects();
        this.setObjectsOpacity();
        this.toggleScrollHint();
      },
      { passive: true }
    );
  }
}

export default YouTubeRegretsTunnel;
