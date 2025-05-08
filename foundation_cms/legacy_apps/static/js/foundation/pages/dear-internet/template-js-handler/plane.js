const SVG_WRAPPER = document.querySelector("#plane-pathway-wrapper");
const SVG = document.querySelector("#plane-pathway-wrapper svg");
const PATH = document.querySelector("#plane-pathway-wrapper #path");
const PLANE = document.querySelector("#plane-pathway-wrapper #plane");

class Plane {
  constructor() {
    this.defaultPlaneRotation = 0;
    this.init();
  }

  movePlane() {
    if (SVG_WRAPPER.classList.contains("invisible")) {
      SVG_WRAPPER.classList.remove("invisible");
    }

    // distance scrolled
    let scrollDist =
      document.documentElement.scrollTop + document.body.scrollTop;

    // what percentage has the user scrolled?
    let scrollPercentage = scrollDist / SVG.scrollHeight;

    // find path length
    let pathLen = PATH.getTotalLength();

    // get the position of a point at <scrollPercentage> along the path.
    let point = PATH.getPointAtLength(scrollPercentage * pathLen);

    // get the position of a point slightly ahead so we can calculate the angle we want the plane to rotate
    let pointAhead = PATH.getPointAtLength(
      (scrollPercentage + 0.0001) * pathLen
    );

    // find rotating angle
    let angleDeg =
      Math.atan2(pointAhead.y - point.y, pointAhead.x - point.x) *
      (180 / Math.PI);

    // position plane at this point
    PLANE.setAttribute(
      "transform",
      `translate(${point.x}, ${point.y}) rotate(${
        angleDeg + this.defaultPlaneRotation
      } 0 0)`
    );

    this.revealPath(scrollPercentage);
  }

  revealPath(scrollPercentage) {
    // revealing/hiding PATH by adjusting the dash gap size
    PATH.setAttribute(
      "stroke-dashoffset",
      (1 - scrollPercentage) * PATH.getTotalLength()
    );
  }

  findDefaultPlaneRotation() {
    if (PLANE.getAttribute("transform")) {
      // Get the first rotation value out of the transforms.
      // Example of "transform" attribute value:
      // "translate(num num num) rotate(num num num)"
      const match = PLANE.getAttribute("transform").match(/rotate\((\S+)[ )]/);
      if (match) {
        this.defaultPlaneRotation = parseFloat(match[1]);
      }
    }
  }

  init() {
    if (!SVG_WRAPPER || !SVG || !PATH || !PLANE) {
      console.error(`Some DOM elements are missing`);
      return;
    }

    this.findDefaultPlaneRotation();

    window.addEventListener("scroll", () => this.movePlane(), {
      passive: true,
    });

    // set dash gap of the PATH to be the totaly length of PATH so it appears "invisible" at start
    PATH.setAttribute("stroke-dasharray", PATH.getTotalLength());
  }
}

export default Plane;
