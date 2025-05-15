import LocomotiveScroll from "locomotive-scroll";

export const initYoutubeRegretsLocomotiveScroll = () => {
  const locoScroll = new LocomotiveScroll({
    el: document.querySelector(".scroll-container"),
    smooth: true,
    repeat: true,
    smartphone: {
      smooth: false,
      breakpoint: 576,
    },
    tablet: {
      smooth: false,
      breakpoint: 768,
    },
  });

  // Make sure loco scroll is up to date after page has totally finished laoding
  var interval = setInterval(function () {
    if (document.readyState === "complete") {
      clearInterval(interval);
      locoScroll.update();
    }
  }, 100);
};
