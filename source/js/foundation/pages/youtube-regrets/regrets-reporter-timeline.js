export default () => {
  let timeline = document.querySelector(".timeline");
  let segment = document.querySelector(".timeline .segment");
  let button = document.querySelector(".btn-timeline-next");

  if (!(timeline && segment && button)) {
    return;
  }

  let segmentWidth = segment.offsetWidth;
  let segements = document.querySelectorAll(".timeline .segment");
  let counter = 0;

  let checkIfInView = (elem) => {
    let windowWidth = window.innerWidth || document.documentElement.clientWidth;

    return elem.getBoundingClientRect().right <= windowWidth;
  };

  let updateOpacity = () => {
    segements.forEach((seg, i) => {
      seg.style.opacity = checkIfInView(seg) ? 1 : 0.3;
    });
  };

  updateOpacity();

  timeline.addEventListener("transitionend", () => {
    updateOpacity();
  });

  window.addEventListener("resize", () => {
    updateOpacity();
  });

  button.addEventListener("click", () => {
    let windowWidth = window.innerWidth || document.documentElement.clientWidth;
    let lastItemShown = checkIfInView(
      document.querySelector(".timeline .segment:last-of-type")
    );
    let offset;

    if (lastItemShown) {
      // move back to first item
      offset = 0;
      counter = 0;
    } else {
      counter++;
      offset = segmentWidth * counter;

      if (windowWidth + offset >= timeline.offsetWidth) {
        // show the last item
        offset = timeline.offsetWidth - windowWidth;
      }
    }

    timeline.style.transform = `translateX(-${offset}px)`;
  });
};
