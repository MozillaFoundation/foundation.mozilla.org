import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

export default () => {
  const CONTINUE_SCROLLING = "contScrolling";

  /**
   * Creates slideup intro animation when entering a new article. If sessionStorage indicates
   * that it is coming from another article via scrolltrigger, then we animate the white box that is overlaying the article.
   */
  function triggerIntroTransition() {
    if (
      sessionStorage.getItem(CONTINUE_SCROLLING) &&
      document.querySelector(".page-enter-transition")
    ) {
      document.querySelector(".page-enter-transition").remove();
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

    const SCROLL_BUFFER = 30;
    let outro;
    let bottomOfPage = false;

    //detects if it is on the bottom of the page
    window.onscroll = function (ev) {
      if (
        window.innerHeight + window.pageYOffset + SCROLL_BUFFER >=
          document.body.offsetHeight &&
        !bottomOfPage
      ) {
        bottomOfPage = true;
        outro = gsap.timeline({
          onComplete: () => {
            setTimeout(() => {
              const loadIndicator = document.querySelector(".article-loading");
              if (loadIndicator) {
                loadIndicator.classList.remove("tw-hidden");
              }
            }, 2000);

            sessionStorage.setItem(CONTINUE_SCROLLING, "true");
            document.querySelector(".scrolling-link").click();
          },
        });
        // Need to remove a lot of !important classes to allow animation to work.
        document
          .querySelector(".cont-scrolling")
          .classList.add("tw-sticky", "tw-absolute", "tw-top-0", "tw-left-0");
        outro.to(".outro-screen", {
          y: "0vh",
          duration: 0.1,
        });
        [
          ...document.querySelectorAll(
            "main > div:not(.cont-scrolling),.primary-nav-container,.article-navbar-container"
          ),
        ].forEach((q) => q.classList.add("tw-hidden"));

        document
          .querySelector(".publication-hero-container,#custom-hero")
          .classList.remove("d-flex");
        outro.set("main", {
          height: "100%",
        });
      }
    };

    // Needed for firebox bfcache when navigating back to the article.
    window.addEventListener("pagehide", function (event) {
      if (event.persisted === true && outro) {
        document
          .querySelector(".cont-scrolling")
          .classList.toggle(
            "tw-sticky",
            "tw-absolute",
            "tw-top-0",
            "tw-left-0"
          );
        const loadIndicator = document.querySelector(".article-loading");
        if (loadIndicator) {
          loadIndicator.classList.toggle("tw-hidden");
        }
        document
          .querySelector(".publication-hero-container,#custom-hero")
          .classList.toggle("d-flex");
        outro.seek(0);
        outro.pause();
        window.scrollTo({ top: 0 });
        ScrollTrigger.refresh();
      }
    });
  }

  triggerIntroTransition();
  gsap.registerPlugin(ScrollTrigger);
  if (document.querySelector(".cont-scrolling")) {
    initScrollExitTransition();
  }
};
