import utility from "./utility";

let elements = {
  introViewport: `#view-youtube-regrets .intro-viewport`,
  blocks: `#view-youtube-regrets .intro-viewport .block`,
  rings: `#view-youtube-regrets .intro-viewport .ring`,
  introText: `#view-youtube-regrets .intro-viewport .intro-text p`
};
class YouTubeRegretsTunnel {
  constructor() {
    this.introScrollHeight = 0;
    this.sceneDepth = 0;
    this.lastPageYOffset = 0;
  }

  /**
   * Fade in text blocks one by one as user scrolls
   */
  setIntroTextOpacity() {
    let introText = elements.introText;
    let length = introText.length;
    let speedFactor = length / elements.blocks.length;
    let baseUnit = this.introScrollHeight * speedFactor;

    introText.forEach((item, i) => {
      let positionToShow = baseUnit * (i / length);
      let positionToHide = baseUnit * ((i + 1) / length);

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
  }

  /**
   * Fade in image block when it's moving towards the origin.
   * Fade out otherwise.
   */
  setBlocksOpacity() {
    let opacity = 1;

    elements.blocks.forEach(item => {
      let matrix = window.getComputedStyle(item).transform;
      let coord = this.getCoordinatefromMatrix3d(matrix);

      if (coord) {
        let percentToOrigin = coord.z / this.introScrollHeight;
        opacity = Math.min(percentToOrigin + 1, 1);
      }

      item.style.opacity = opacity;
    });
  }

  /**
   * Show rings' opacity vlaue
   */
  setRingsOpacity() {
    elements.rings.forEach(ring => {
      ring.style.opacity = 0.5;
    });
  }

  /**
   * Move objects towards / away from viewint point as user scrolls
   */
  moveObjects() {
    this.lastPageYOffset = window.pageYOffset;

    let blocksSpeedFactor = elements.blocks.length / elements.introText.length;
    let ringsSpeedFactor = (this.scenePerspective / this.sceneDepth) * 1.2;

    this.updateCSSCustomProperty(
      `--blockZTranslate`,
      this.lastPageYOffset * blocksSpeedFactor
    );
    this.updateCSSCustomProperty(
      `--ringZTranslate`,
      this.lastPageYOffset * ringsSpeedFactor
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

    // the total scroll distance users have to scroll in order to get through the intro tunnel
    this.introScrollHeight = window.innerHeight * 5;

    // depth of the scene
    this.sceneDepth = this.introScrollHeight - window.innerHeight;

    // update CSS custom properties
    this.updateCSSCustomProperty(`--sceneDepth`, this.sceneDepth);
    this.updateCSSCustomProperty(
      `--baseBlockGap`,
      this.sceneDepth / elements.blocks.length
    );
    this.updateCSSCustomProperty(
      `--baseRingGap`,
      this.scenePerspective / elements.rings.length
    );
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
   * Initiate interactive intro
   */
  init() {
    if (!utility.checkAndBindDomNodes(elements, true)) return;

    window.onload = () => {
      this.setSceneDepth();
      this.setObjectsOpacity();

      window.addEventListener(`scroll`, event => {
        this.moveObjects();
        this.setObjectsOpacity();
      });
    };
  }
}

const youTubeRegretsTunnel = new YouTubeRegretsTunnel();

export default youTubeRegretsTunnel;
