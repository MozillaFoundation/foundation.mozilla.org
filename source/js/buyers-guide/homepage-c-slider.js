import CREEPINESS_LABELS from "./components/creepiness-labels.js";

// Height of a single frame in the emoji sprite sheet,
// see the ".current-creepiness" rule in homagepage.sccs
const EMOJI_FRAME_HEIGHT = 70;

// Total number of frames in our sprite sheet, see the
// "./source/images/buyers-guide/faces/sprite.png" file.
const SPRITE_FRAME_COUNT = 40;

// Our threshold value for which average creepiness ratings
// still count as "happy face" for the purpose of showing
// the emoji while scrolling.
//
// Note: this is a cosmetic value for scroll only.
const MINIMUM_HAPPINESS_RATING = 25;

// Our threshold value beyond which everything is super
// creepy by default.
//
// Note: this is a cosmetic value for scroll only.
const MAXIMUM_CREEPINESS_RATING = 80;

// Sticky search bar
const SEARCH_BAR = document.getElementById("sticky-bar");

// Creepy-face container
const CREEPY_FACE = document.querySelector(".creep-o-meter-information");

// Category bar. Used for relocating the creepo-face on desktop.
const CATEGORY_BAR = document.getElementById("multipage-nav")

// Helper function to determine whether products are
// in view, and so need to be considered for averaging.
function isElementInViewport(element) {
  let rect = element.getBoundingClientRect();

  return (
    rect.top >= 0 &&
    rect.left >= 0 &&
    rect.bottom <=
      (window.innerHeight || document.documentElement.clientHeight) &&
    rect.right <= (window.innerWidth || document.documentElement.clientWidth)
  );
}

// map a value from one range to another
function map(v, s1, e1, s2, e2) {
  return s2 + ((v - s1) * (e2 - s2)) / (e1 - s1);
}

// cap a value to a range
function cap(v, m, M) {
  m = m || 0;
  M = M || 100;
  return v < m ? m : v > M ? M : v;
}

export default {
  init: () => {
    let face = document.querySelector(`.current-creepiness`);
    let bubble = document.querySelector(`.speech-bubble`);
    let bubbleText = bubble.querySelector(`.text`);
    let products = document.querySelectorAll(`.product-box`);

    window.addEventListener(
      `scroll`,
      () => {
        // Figure out which face to show while scrolling:
        let visible = Array.from(products).filter((v) => {
          return isElementInViewport(v) && !v.classList.contains(`d-none`);
        });

        let n = visible.length;

        // Shortcut this scroll update if there are no products
        if (n === 0) {
          return;
        }

        // Reduce the creepiness, treating any product without votes
        // as a "neutral" product with creepiness = 50
        let averageCreepiness = visible.reduce((tally, v) => {
          let value = parseFloat(v.dataset.creepiness) || 50;

          return tally + value / n;
        }, 0);

        // Compress the value so that we show a smiley face even for products with a lowish creepiness score.
        let mappedAverageCreepiness = cap(
          map(
            averageCreepiness,
            MINIMUM_HAPPINESS_RATING,
            MAXIMUM_CREEPINESS_RATING,
            0,
            100
          ),
          1,
          100
        );

        // The averageCreepiness will be in range [1,100] so we can dec1 the
        // valueto make sure we're in frame range [0,frames.length-1]:
        let frame = Math.round(
          ((SPRITE_FRAME_COUNT - 1) * (mappedAverageCreepiness - 1)) / 100
        );

        face.style.backgroundPositionY = `${-frame * EMOJI_FRAME_HEIGHT}px`;

        // Figure out what the corresponding creepiness label should be:
        let len = CREEPINESS_LABELS.length;
        let bin = Math.floor((len * (mappedAverageCreepiness - 1)) / 100);

        if (bin === -1) {
          bubbleText.textContent = ``;
          bubble.classList.add(`d-none`);
        } else {
          bubbleText.textContent = `${CREEPINESS_LABELS[bin]}!`;
          bubble.classList.remove(`d-none`);
        }
      },
      {
        passive: true, // remember not to bog down the UI thread.
      }
    );

    /**
     * querySelectors in this event listener are constantly polled on scroll
     * to ensure when a browser width changes creepo-face still works as expected
     * And getElementById is used in places to speed up DOM searching
     */
    window.addEventListener(
      "scroll",
      () => {
        const element = document.getElementById("product-list");
        const position = element.getBoundingClientRect();

        // If on desktop, don't delay moving creepo-face into the corner
        // If on mobile, make the creepy face move to the corner sooner
        const offset = window.innerWidth > 768 ? window.innerHeight - CATEGORY_BAR.offsetHeight : 100;

        /**
         * Check if the product grid area is partially visible in the viewport
         */
        if (
          position.top + offset < window.innerHeight &&
          position.bottom >= 0
        ) {
          SEARCH_BAR.classList.add("search-active" ,"creep-o-meter-moved");
        }

        const recommendProduct = document.getElementById("recommend-product");
        const heightFromTop = recommendProduct.getBoundingClientRect().top;
        const diff = heightFromTop - window.innerHeight + 50;

        if (diff > 0) {
          CREEPY_FACE.classList.remove("fade-out");
        } else {
          CREEPY_FACE.classList.add("fade-out");
        }
      },
      {
        passive: true, // remember not to bog down the UI thread.
      }
    );
  },
};
