const SVG_WRAPPER = document.querySelector("#plane-pathway-wrapper");
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

    // total scroll height from page top to end of the SVG
    let scrollHeight = SVG_WRAPPER.offsetTop + SVG_WRAPPER.scrollHeight;

    // what percentage down the page are we?
    let scrollPercentage = scrollDist / scrollHeight;

    // find path length
    let pathLen = PATH.getTotalLength();

    // scrollPercentage *= pathLen / (scrollHeight + document.documentElement.clientWidth);

    // get the position of a point at <scrollPercentage> along the path.
    let point = PATH.getPointAtLength(scrollPercentage * pathLen);

    // get the position of a point slightly ahead so we can calculate the angle we want the plane to rotate
    let pointAhead = PATH.getPointAtLength(
      // (scrollPercentage + 1 / document.documentElement.scrollHeight) * pathLen
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
      // example of "transform" attribute value:
      // "translate(num num num) rotate(num num num)"
      let regex = /\brotate\b\([-.0-9]+\s[-.0-9]+\s[-.0-9]+\)/g;

      if (PLANE.getAttribute("transform").match(regex)) {
        this.defaultPlaneRotation = PLANE.getAttribute("transform")
          .match(regex)[0]
          .replace("rotate", "")
          .replace("(", "")
          .replace(")", "")
          .split(" ")[0]
          .trim();
      }
      this.defaultPlaneRotation = parseFloat(this.defaultPlaneRotation);
    }
  }

  init() {
    if (!SVG_WRAPPER || !PATH || !PLANE) {
      console.error(`some DOM elements are missing`);
      return;
    }

    this.findDefaultPlaneRotation();

    window.addEventListener("scroll", () => {
      this.movePlane();
    });

    // set dash gap of the PATH to be the totaly length of PATH so it appears "invisible" at start
    PATH.setAttribute("stroke-dasharray", PATH.getTotalLength());
  }
}

export default Plane;
