import LocomotiveScroll from "locomotive-scroll";
import { gsap } from "gsap";
import ScrollTrigger from "gsap/ScrollTrigger";
import TextPlugin from "gsap/TextPlugin";

export const initYoutubeRegretsLocomotiveScroll = () => {
  // Locomotive scroll settings
  // const scroll = new LocomotiveScroll({
  //   el: document.querySelector("[data-scroll-container]"),
  // });

  // Gsap settings
  gsap.registerPlugin(ScrollTrigger, TextPlugin);

  let sceneOneText = "[data-scene='1'] [data-scene-text]";

  // First Scene is special because of the X and the text appearing
  let firstScene = gsap
    .timeline({ defaults: { duration: 20 } })
    .set(
      sceneOneText,
      {
        autoAlpha: 1,
        text: "A user sees a video they would rather not see again",
        duration: 2,
      },
      1
    )
    .to(".timeline__scene-image", { autoAlpha: 1, duration: 1 }, 1)
    .set(
      sceneOneText,
      {
        delay: 5,
        text: "The user decides to use YouTube’s feedback mechanism, ‘Remove from history’",
      },
      2
    )
    .to(".timeline__cross", { autoAlpha: 1, duration: 2, delay: 5 }, 2);

  ScrollTrigger.create({
    trigger: ".timeline__scene--first",
    start: "top top+=100",
    end: "+=1000",
    animation: firstScene,
    scrub: true,
    pin: true,
  });

  // const personDate = document.querySelector(".timeline__person-date");
  //
  // // Thinking person and date use height to set Y position on bottom of page (i don't like this)
  // gsap.to(".timeline__person-date", {
  //   y: personDate.offsetHeight,
  //   ease: "none",
  //   scrollTrigger: {
  //     trigger: ".timeline",
  //     start: "top bottom",
  //     end: "bottom bottom",
  //     scrub: true,
  //     pin: true,
  //     markers: true,
  //   },
  // });

  // Get scene elements

  // Set first scene to visible
  // gsap.set(dateScenes[0], {autoAlpha: 1});

  // // Fadeout animation for dates
  // function showNextDate(newSection) {
  //   if (newSection !== currentSection) {
  //     gsap.to(currentSection, {autoAlpha: 0, duration: 0.5});
  //     gsap.to(newSection, {autoAlpha: 1, duration: 0.5});
  //     currentSection = newSection;
  //   }
  // }
  //
  // // Pin the timeline
  // ScrollTrigger.create({
  //   trigger: ".timeline__sections",
  //   start: () => 'top top',
  //   end: () => "+=" + (dateScenes.length - 1) * innerHeight,
  //   pin: true,
  // });
  //
  // // Fade each one in and out
  // dateScenes.forEach((scene, i) => {
  //   ScrollTrigger.create({
  //     trigger: ".timeline__sections",
  //     start: () => "top top-=" + (i -0.5) * innerHeight,
  //     end: () => "+=" + innerHeight,
  //     onToggle: (self) => self.isActive && showNextDate(scene),
  //     markers: true,
  //   });
  // });
};
