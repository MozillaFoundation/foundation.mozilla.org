import LocomotiveScroll from "locomotive-scroll";
import {gsap} from "gsap";
import ScrollTrigger from "gsap/ScrollTrigger";
import TextPlugin from "gsap/TextPlugin";

export const initYoutubeRegretsLocomotiveScroll = () => {

  // Gsap settings
  gsap.registerPlugin(ScrollTrigger, TextPlugin);

  const scrollContainerSelector = ".scroll-container";

  // // Locomotive scroll settings
  // const locoScroll = new LocomotiveScroll({
  //   el: document.querySelector(scrollContainerSelector),
  //   smooth: true,
  // });
  // locoScroll.on("scroll", ScrollTrigger.update);
  //
  // // tell ScrollTrigger to use these proxy methods for the ".smooth-scroll" element since Locomotive Scroll is hijacking things
  // ScrollTrigger.scrollerProxy(scrollContainerSelector, {
  //   scrollTop(value) {
  //     return arguments.length ? locoScroll.scrollTo(value, 0, 0) : locoScroll.scroll.instance.scroll.y;
  //   }, // we don't have to define a scrollLeft because we're only scrolling vertically.
  //   getBoundingClientRect() {
  //     return {top: 0, left: 0, width: window.innerWidth, height: window.innerHeight};
  //   },
  //   // LocomotiveScroll handles things completely differently on mobile devices - it doesn't even transform the container at all! So to get the correct behavior and avoid jitters, we should pin things with position: fixed on mobile. We sense it by checking to see if there's a transform applied to the container (the LocomotiveScroll-controlled element).
  //   pinType: document.querySelector(scrollContainerSelector).style.transform ? "transform" : "fixed"
  // });

  let sceneOneText = "[data-scene='1'] [data-scene-text]";

  // First Scene is special because of the X and the text appearing
  let firstScene = gsap
    .timeline({defaults: {duration: 20}})
    .set(
      sceneOneText,
      {
        autoAlpha: 1,
        text: "A user sees a video they would rather not see again",
        duration: 2,
      },
      1
    )
    .to(".timeline__scene-image", {autoAlpha: 1, duration: 1}, 1)
    .set(
      sceneOneText,
      {
        delay: 5,
        text: "The user decides to use YouTube’s feedback mechanism, ‘Remove from history’",
      },
      2
    )
    .to(".timeline__cross", {autoAlpha: 1, duration: 2, delay: 5}, 2);

  ScrollTrigger.create({
    trigger: ".timeline__scene--first",
    start: "top top+=100",
    end: "+=1000",
    animation: firstScene,
    scrub: true,
    pin: true,
    markers: true,
  });


  // ScrollTrigger.create({
  //   trigger: ".timeline",
  //   start: "top top+=100",
  //   end: "bottom 90%",
  //   pin: ".timeline__person-date",
  //   onEnter: () => gsap.set(".timeline__person-date", {autoAlpha: 1}),
  //   onLeaveBack: () => gsap.set(".timeline__person-date", {autoAlpha: 0}),
  // });

  // const personDate = document.querySelector(".timeline__person-date");

  // each time the window updates, we should refresh ScrollTrigger and then update LocomotiveScroll.
  ScrollTrigger.addEventListener("refresh", () => locoScroll.update());

  // after everything is set up, refresh() ScrollTrigger and update LocomotiveScroll because padding may have been added for pinning, etc.
  ScrollTrigger.refresh();

};
