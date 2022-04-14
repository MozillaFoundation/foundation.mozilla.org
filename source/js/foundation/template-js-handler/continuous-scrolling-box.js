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
            // If it takes more then 400ms show the loading indicator
            setTimeout(() => {
              if (document.querySelector(".article-loading")) {
                document
                  .querySelector(".article-loading")
                  .classList.toggle("tw-hidden");
              }
            }, 400);
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
        outro.set(
          "main > div:not(.cont-scrolling),.primary-nav-container,.article-navbar-container",
          {
            display: "none",
            autoAlpha: 0,
          }
        );
        outro.set("main", {
          height: "100%",
        });
        outro.to(".cont-scrolling", {
          y: "-200vh",
          duration: 0.3,
          delay: 0.5,
        });
        outro.to(".cont-scrolling", {
          autoAlpha: 0,
          duration: 0.3,
        });
      },
    });
  }

  // lets prefetch the next article link to avoid a slow page transition
  function prefetchNextArticle() {
    const nextArticle = document.querySelector(".cont-scrolling").dataset.href;
    if (nextArticle) {
      const nextArticleLink = document.createElement("link");
      nextArticleLink.rel = "prefetch";
      nextArticleLink.href = nextArticle;
      document.head.appendChild(nextArticleLink);
    }
  }

  triggerIntroTransition();
  gsap.registerPlugin(ScrollTrigger);
  if (document.querySelector(".cont-scrolling")) {
    prefetchNextArticle();
    initScrollExitTransition();
  }
};
