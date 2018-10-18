const creepStep = 70; // height of a single frame, see the ".current-creepiness" rule in homagepage.sccs
const totalSteps = 50; // total number of frames in our sprite sheet

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
    let products = document.querySelectorAll(`.product-box`);

    window.addEventListener(`scroll`, () => {
      let visible = Array.from(products).filter(v => isElementInViewport(v));
      let n = visible.length;
      let averageCreepiness = visible.reduce( (tally, v) => tally + parseFloat(v.dataset.creepiness)/n, 0);
      let frame = Math.round(totalSteps * averageCreepiness/100);
      let offset = `${-frame * creepStep}px`;

      face.style.backgroundPositionY = offset;
    }, {
      passive: true // remember not to bog down the UI thread.
    });
  }
};
