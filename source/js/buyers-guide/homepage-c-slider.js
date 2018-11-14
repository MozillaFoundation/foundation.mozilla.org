import CREEPINESS_LABELS from "./components/creepiness-labels.js";

// Height of a single frame, see the
// ".current-creepiness" rule in homagepage.sccs
const creepStep = 70;

// Total number of frames in our sprite sheet,
// see the "./source/images/buyers-guide/faces/sprite.png" file
const totalSteps = 40;

function isElementInViewport(element) {
  let rect = element.getBoundingClientRect();

  return (
    rect.top >= 0 &&
    rect.left >= 0 &&
    rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
    rect.right <= (window.innerWidth || document.documentElement.clientWidth)
  );
}

export default {
  init: () => {
    let face = document.querySelector(`.current-creepiness`);
    let bubble = document.querySelector(`.speech-bubble`);
    let bubbleText = bubble.querySelector(`.text`);
    let products = document.querySelectorAll(`.product-box`);

    window.addEventListener(`scroll`, () => {

      // Figure out which face to show while scrolling:
      let visible = Array.from(products).filter(v => {
        return isElementInViewport(v) && !v.classList.contains(`d-none`);
      });

      let n = visible.length;

      // shortcut this scroll update if there are no products
      if (n===0) { return; }

      let averageCreepiness = visible.reduce( (tally, v) => tally + parseFloat(v.dataset.creepiness)/n, 0);

      // The averageCreepiness will be in range [1,100] so we can dec1 the
      // valueto make sure we're in frame range [0,frames.length-1]:
      let frame = Math.round((totalSteps-1) * (averageCreepiness-1)/100);

      face.style.backgroundPositionY = `${-frame * creepStep}px`;

      // Figure out what the corresponding creepiness label should be:
      let len = CREEPINESS_LABELS.length;
      let bin = Math.floor(len * (averageCreepiness-1)/100);

      if (bin === -1) {
        bubbleText.textContent = ``;
        bubble.classList.add(`d-none`);
      } else {
        bubbleText.textContent = `${CREEPINESS_LABELS[bin]}!`;
        bubble.classList.remove(`d-none`);
      }
    }, {
      passive: true // remember not to bog down the UI thread.
    });
  }
};
