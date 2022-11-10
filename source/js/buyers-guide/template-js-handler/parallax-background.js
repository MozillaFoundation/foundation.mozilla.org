import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

export default () => {
  gsap.registerPlugin(ScrollTrigger);
  const parallaxBackground = document.querySelector("#pni-parallax-background");

  if (parallaxBackground) {
    const svgShapes = document.querySelectorAll("#pni-parallax-background svg");
    svgShapes.forEach((shape) => {
      gsap.to(shape, {
        y: -1500,
        ease: "none",
        scrollTrigger: {
          trigger: "body",
          start: "top top", // when the top of the trigger hits the top of the viewport
          end: "bottom bottom",
          scrub: true,
          markers: true,
        },
      });
    });

    // Need to set since tailwind classes have !important prefix
    gsap.set(".pni-triangle", {
      rotate: 45,
    });

    gsap.set(".pni-asterick", {
      rotate: 15,
    });

    gsap.to(".pni-asterick", {
      rotate: 540,
      ease: "none",
      scrollTrigger: {
        trigger: "body",
        start: "top top", // when the top of the trigger hits the top of the viewport
        end: "bottom bottom",
        scrub: true,
      },
    });
  }
};
