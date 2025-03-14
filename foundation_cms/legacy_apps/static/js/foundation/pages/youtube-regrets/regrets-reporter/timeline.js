import utility from "../../../../utility.js";

/**
 * Animating the timeline on the youtube regrets work page.
 */

let elements = {
  timeline: `#view-youtube-regrets-reporter .timeline-wrapper .timeline`,
  segments: `#view-youtube-regrets-reporter .timeline-wrapper .timeline .segment`,
  button: `#view-youtube-regrets-reporter .timeline-wrapper .btn-timeline-next`,
};

class RegretsReporterTimeline {
  constructor() {
    this.buttonClickCounter = 0;

    this.init();
  }

  /**
   * Check if segment is fully shown in current viewport
   */
  checkIfInView(seg) {
    let windowWidth = window.innerWidth || document.documentElement.clientWidth;

    return seg.getBoundingClientRect().right <= windowWidth;
  }

  /**
   * Update each timeline segment's opacity
   */
  updateOpacity() {
    elements.segments.forEach((seg) => {
      if (this.checkIfInView(seg)) {
        seg.classList.remove(`faded`);
      } else {
        seg.classList.add(`faded`);
      }
    });
  }

  /**
   * Initiate RegretsReporter timeline
   */
  init() {
    this.loadAttempt = this.loadAttempt || 1;

    if (!utility.checkAndBindDomNodes(elements, true)) {
      if (this.loadAttempt++ < 5) {
        setTimeout(() => this.init(), 200);
      }
      return;
    }

    this.timeline = elements.timeline[0];
    const last = this.timeline.querySelector(".timeline .segment:last-of-type");

    this.updateOpacity();

    this.timeline.addEventListener("transitionend", () => {
      this.updateOpacity();
    });

    window.addEventListener("resize", () => {
      this.updateOpacity();
    });

    elements.button[0].addEventListener("click", () => {
      let segmentWidth = elements.segments[0].offsetWidth;
      let windowWidth =
        window.innerWidth || document.documentElement.clientWidth;
      let lastItemShown = this.checkIfInView(last);
      let offset;

      if (lastItemShown) {
        // move back to first item
        offset = 0;
        this.buttonClickCounter = 0;
      } else {
        this.buttonClickCounter++;
        offset = segmentWidth * this.buttonClickCounter;

        if (windowWidth + offset >= this.timeline.offsetWidth) {
          // show the last item
          offset = this.timeline.offsetWidth - windowWidth;
        }
      }

      this.timeline.style.transform = `translateX(-${offset}px)`;
    });
  }
}

export default RegretsReporterTimeline;
