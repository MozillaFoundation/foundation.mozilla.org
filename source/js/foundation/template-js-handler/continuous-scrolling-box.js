import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

export default () => {
  /**
   * Creates slideup intro animation when entering a new article. If history.state indicates
   * that it is coming from another article via scrolltrigger, then we animate the white box that is overlaying the article.
   */
  function triggerIntroTransition() {
    if (sessionStorage.contScrolling) {
      gsap.to(".page-enter-transition", {
        y: "-100vh",
        delay: 0.5,
        duration: 0.5,
      });
      sessionStorage.removeItem("contScrolling");
    } else if (document.querySelector(".page-enter-transition")) {
      document.querySelector(".page-enter-transition").remove();
    }
  }

  /**
   * Creates a scroll trigger that will trigger the exit animation when the user scrolls past the bottom of the page.
   */
  function initScrollExitTransition() {
    ScrollTrigger.create({
      trigger: ".cont-scrolling",
      start: "top center",
      end: "bottom bottom",
      scrub: true,
      toggleActions: "play none none reverse",
      onLeave: () => {
        const outro = gsap.timeline({
          onComplete: () => {
            sessionStorage.setItem("contScrolling", "true");
            window.location.href =
              document.querySelector(".cont-scrolling").dataset.href;
          },
        });
        document
          .querySelector(".cont-scrolling")
          .classList.toggle(
            "tw-sticky",
            "tw-absolute",
            "tw-top-0",
            "tw-left-0"
          );
        outro.to(".cont-scrolling .tw-container", {
          autoAlpha: 0,
          duration: 0.2,
          delay: 0.3,
        });
        outro.set(
          "main > div:not(.cont-scrolling),.primary-nav-container,.article-navbar-container",
          {
            display: "none",
            autoAlpha: 0,
          }
        );
        outro.set("main", {
          height: "100vh",
        });
        outro.to(".cont-scrolling", {
          y: "-200vh",
          duration: 0.3,
        });
        outro.to(".cont-scrolling", {
          autoAlpha: 0,
          duration: 0.1,
        });
      },
    });
  }

  triggerIntroTransition();
  gsap.registerPlugin(ScrollTrigger);
  if (document.querySelector(".cont-scrolling")) {
    initScrollExitTransition();
  }
};
