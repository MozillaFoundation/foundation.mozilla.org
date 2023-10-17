const EYE_SELECTOR = ".creepy-eye";

export default () => {
  // Animate creepy eyes so they follow the cursor or taps (on touch screen devices)
  // This script is to be paired with buyersguide/fragments/consumer_creepometer_page_2023/animated-eyes.html
  (function () {
    if (!document.querySelector(EYE_SELECTOR)) {
      return;
    }

    let eventMove = "mousemove";
    // check page is loaded on a touch screen device
    if ("ontouchstart" in window) {
      eventMove = "touchstart";
    }

    function getMouseOrTapPos(event) {
      let x, y;
      if (eventMove === "mousemove") {
        // get coordinates of the cursor relative to the left top corner of the viewport
        x = event.pageX - document.documentElement.scrollLeft;
        y = event.pageY - document.documentElement.scrollTop;
      } else {
        if (event.touches && event.touches[0]) {
          x = event.touches[0].clientX;
          y = event.touches[0].clientY;
        } else if (
          event.originalEvent &&
          event.originalEvent.changedTouches[0]
        ) {
          x = event.originalEvent.changedTouches[0].clientX;
          y = event.originalEvent.changedTouches[0].clientY;
        } else if (event.clientX && event.clientY) {
          x = event.clientX;
          y = event.clientY;
        }
      }

      return {
        x,
        y,
      };
    }

    document
      .querySelector("body")
      .addEventListener(eventMove, function (event) {
        document.querySelectorAll(EYE_SELECTOR).forEach(function (eye) {
          let { x, y } = getMouseOrTapPos(event);

          let xEye = eye.getBoundingClientRect().left + eye.clientWidth / 2;
          let yEye = eye.getBoundingClientRect().top + eye.clientHeight / 2;
          let radian = Math.atan2(x - xEye, y - yEye);
          let rotate = radian * (180 / Math.PI) * -1 + 90;
          let rotateStyleRule = "rotate(" + rotate + "deg)";

          eye.style.webkitTransform = rotateStyleRule;
          eye.style.MozTransform = rotateStyleRule;
          eye.style.msTransform = rotateStyleRule;
          eye.style.transform = rotateStyleRule;
        });
      });
  })();
};
