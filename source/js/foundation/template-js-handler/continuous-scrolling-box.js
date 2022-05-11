import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

export default () => {
  const CONTINUE_SCROLLING = "contScrolling";

  /**
   * Creates slideup intro animation when entering a new article. If sessionStorage indicates
   * that it is coming from another article via scrolltrigger, then we animate the white box that is overlaying the article.
   */
  function triggerIntroTransition() {
    if (sessionStorage.getItem(CONTINUE_SCROLLING)) {
      gsap.to(".page-enter-transition", {
        y: "-100vh",
        delay: 0.3,
        duration: 0.3,
      });
      sessionStorage.removeItem(CONTINUE_SCROLLING);
    } else if (document.querySelector(".page-enter-transition")) {
      document.querySelector(".page-enter-transition").remove();
    }
  }

  /**
   * Creates a scroll trigger that will trigger the exit animation when the user scrolls past the bottom of the page.
   */
  function initScrollExitTransition() {
    gsap.to(".cont-scrolling .tw-container", {
      scrollTrigger: {
        trigger: ".cont-scrolling",
        scrub: true,
        start: "+250 bottom",
        end: "bottom bottom",
        toggleActions: "play none none reverse",
        onLeave: () => {
          document
            .querySelector(".cont-scrolling .tw-container")
            .classList.add("tw-hidden");
        },
      },
      autoAlpha: 0,
    });

    ScrollTrigger.create({
      trigger: ".cont-scrolling",
      start: "top center",
      end: "bottom bottom",
      scrub: true,
      toggleActions: "play none none reverse",
      onLeave: () => {
        const outro = gsap.timeline({
          onComplete: () => {
            setTimeout(() => {
              const loadIndicator = document.querySelector(".article-loading");
              if (loadIndicator) {
                loadIndicator.classList.toggle("tw-hidden");
              }
            }, 500);

            sessionStorage.setItem(CONTINUE_SCROLLING, "true");
            document.querySelector(".scrolling-link").click();
          },
        });
        // Need to remove a lot of !important classes to allow animation to work.
        document
          .querySelector(".cont-scrolling")
          .classList.toggle(
            "tw-sticky",
            "tw-absolute",
            "tw-top-0",
            "tw-left-0"
          );
        outro.to(".outro-screen", {
          y: "0vh",
          duration: 0.3,
          delay: 0.5,
        });
        outro.set(
          "main > div:not(.cont-scrolling),.primary-nav-container,.article-navbar-container",
          {
            display: "none",
            autoAlpha: 0,
          }
        );
        document
          .querySelector(".publication-hero-container")
          .classList.toggle("d-flex");
        outro.set("main", {
          height: "100%",
        });
      },
    });
  }

  triggerIntroTransition();
  gsap.registerPlugin(ScrollTrigger);
  if (document.querySelector(".cont-scrolling")) {
    initScrollExitTransition();
    // create an Observer instance
    const resizeObserver = new ResizeObserver((entries) =>
      ScrollTrigger.refresh()
    );

    // start observing a DOM node
    resizeObserver.observe(document.body);
  }
};
