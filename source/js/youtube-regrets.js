const elements = {
  blocks: `#view-youtube-regrets .block`,
  rings: `#view-youtube-regrets .ring`,
  introText: `#view-youtube-regrets .intro-text p`
};

class YouTubeRegretsTunnel {
  constructor() {
    this.introScrollHeight = 0;
    this.sceneDepth = 0;
    this.lastPageYOffset = 0;
  }

  /**
   * Find and bind all necessary DOM nodes, returning "false" if not all DOM nodes were found.
   */
  checkDomNodes() {
    return Object.keys(elements).every(key => {
      // if this element already resolved to a DOM node, move on to the next
      let value = elements[key];
      if (typeof value !== "string") return true;

      // find this DOM node, and report on the result (binding it if found for later use)
      let element = document.querySelectorAll(value);
      if (element) elements[key] = element;
      return !!element;
    });
  }

  /**
   * Fade in text blocks one by one as user scrolls
   */
  setIntroTextOpacity() {
    let length = elements.introText.length;
    let speedFactor = elements.introText.length / elements.blocks.length;
    let baseUnit = this.introScrollHeight * speedFactor;

    for (let i = 0; i < length; i++) {
      let item = elements.introText[i];
      let positionToShow = baseUnit * (i / length);
      let positionToHide = baseUnit * ((i + 1) / length);
      // console.log(this.lastPageYOffset, positionToHide, this.lastPageYOffset / positionToHide);

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
    }
  }

  /**
   * Fade in image block when it's moving towards the origin.
   * Fade out otherwise.
   */
  setBlocksOpacity() {
    for (let i = 0; i < elements.blocks.length; i++) {
      let item = elements.blocks[i];
      let matrix = window.getComputedStyle(item).transform;
      let coord = this.getCoordinatefromMatrix3d(matrix);
      // console.log(coord);
      let percentToOrigin = coord.z / this.introScrollHeight;

      item.style.opacity = Math.min(percentToOrigin + 1, 1);

      // console.log(
      //   `[${i}] `,
      //   coord.z,
      //   window.pageYOffset,
      //   this.introScrollHeight
      // );
    }
  }

  /**
   *
   */
  setRingsOpacity() {
    elements.rings.forEach(ring => {
      ring.style.opacity = 0.3;
    });
  }

  moveObjects() {
    // console.log(`\nScrolling up: `, this.lastPageYOffset > window.pageYOffset);
    this.lastPageYOffset = window.pageYOffset;

    let blocksSpeedFactor = elements.blocks.length / elements.introText.length;
    let ringsSpeedFactor = this.scenePerspective / this.sceneDepth;

    document.documentElement.style.setProperty(
      "--blockZTranslate",
      this.lastPageYOffset * blocksSpeedFactor
    );
    document.documentElement.style.setProperty(
      "--ringZTranslate",
      this.lastPageYOffset * ringsSpeedFactor
    );
  }

  /**
   * Parse x, y, and z coordinate from matrix
   */
  getCoordinatefromMatrix3d(matrix = ``) {
    let matrix3d = {};

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

    return {
      x: matrix3d.m41,
      y: matrix3d.m42,
      z: matrix3d.m43
    };
  }

  setSceneDepth() {
    const scenePerspective = parseFloat(
      getComputedStyle(document.documentElement).getPropertyValue(
        "--scenePerspective"
      )
    );
    this.scenePerspective = scenePerspective;

    // the total scroll distance users have to scroll in order to get through the intro tunnel
    this.introScrollHeight = document.body.scrollHeight;

    // depth of the scene
    this.sceneDepth = this.introScrollHeight - 1 * window.innerHeight;
    document.documentElement.style.setProperty("--sceneDepth", this.sceneDepth);

    console.log(this.introScrollHeight, document.body.scrollHeight);
  }

  /**
   * Update objects' opacity value as user scrolls
   */
  setObjectsOpacity() {
    this.setIntroTextOpacity();
    this.setBlocksOpacity();
    this.setRingsOpacity();
  }

  init() {
    if (!this.checkDomNodes()) return;

    let tunnel = this;
    // console.log(elements.blocks, elements.rings, elements.introText);
    console.log(tunnel);

    window.onload = () => {
      tunnel.setSceneDepth();
      tunnel.setObjectsOpacity();

      window.addEventListener("scroll", event => {
        // console.log(
        //   `intro height: `,
        //   tunnel.introScrollHeight,
        //   `pixels scrolled: `,
        //   window.pageYOffset
        // );
        tunnel.moveObjects();
        tunnel.setObjectsOpacity();
      });
    };
  }
}

const youTubeRegretsTunnel = new YouTubeRegretsTunnel();

export default youTubeRegretsTunnel;
