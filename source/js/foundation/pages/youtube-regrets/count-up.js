import {CountUp} from "countup.js";

/**
 * Rendering and animating the numbers that "count up" using countup.js.
 *
 *  Attrs:
 *  data-stat - {Required} Value of the stat
 *  data-stat-delay - {Optional} delay number eg. 250
 *  data-stat-prefix - {optional} Prefix on the stat eg. ~
 *  data-stat-suffix - {optional} Suffix on the stat eg. % or K
 */

export const initYoutubeRegretsResearchCountUp = () => {
  if ("IntersectionObserver" in window) {
    const localeSeparator = get_format("THOUSAND_SEPARATOR");
    const stats = document.querySelectorAll("[data-stat]");
    let state = {
      stats: {},
    };

    // Creates and returns a CountUp object
    const createCountUp = (element) => {
      const statValue = element.dataset.stat;
      const prefix = element.dataset.statPrefix;
      const suffix = window.gettext(element.dataset.statSuffix); // localized
      const delay = element.dataset.statDelay || null;

      const countUpObj = new CountUp(element, statValue, {
        separator: localeSeparator,
        ...(prefix && { prefix }),
        ...(suffix && { suffix }),
      });

      return {
        countUpObj: countUpObj,
        delay: delay,
      }
    }

    let observer = new IntersectionObserver(
      (entries, observer) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            /*  TODO: count ups inside the accordion on youtube_regrets_2021 need further work
             *  to reliably run when the accordion is open and the stat is visible
             *  currently working in chrome but not reliably cross-browser
             *  Hint: listen to the openDrawer event on the accordion.
             */
            const { countUpObj, delay } = state.stats[entry.target.id];

            if (delay) {
              setTimeout(() => {
                countUpObj.start();
              }, delay);
            } else {
              countUpObj.start();
            }

            observer.unobserve(entry.target);
          }
        });
      },
      {rootMargin: "0px 0px -10% 0px"}
    );

    stats.forEach((stat) => {
      // Get all stats elements and create CountUp objects with el ID as the key,
      // so we can access them in IntersectionObserver
      state.stats[stat.id] = createCountUp(stat);
      observer.observe(stat);
    });
  }
};
