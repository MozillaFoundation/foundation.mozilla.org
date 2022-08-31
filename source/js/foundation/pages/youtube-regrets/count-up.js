import { CountUp } from "countup.js";

/**
 * Rendering and animating the numbers that "count up" using countup.js.
 *
 *  Attrs:
 *  data-stat - {Required} Value of the stat
 *  data-stat-prefix - {optional} Prefix on the stat
 *  data-stat-suffix - {optional} Suffix on the stat
 *  data-stat-localized-suffix - {optional} Localized suffix on the stat
 */

export const initYoutubeRegretsResearchCountUp = () => {
  if ("IntersectionObserver" in window) {
    const localeSeparator = get_format("THOUSAND_SEPARATOR");
    const stats = document.querySelectorAll("[data-stat]");

    stats.forEach((stat) => {
      const statValue = stat.dataset.stat;
      const prefix = stat.dataset.statPrefix || null;
      const suffix = stat.dataset.statSuffix || null;
      const localizedSuffix = getText(stat.dataset.statLocalizedSuffix) || null;

      new CountUp(stat, statValue, {
        separator: localeSeparator,
        prefix: prefix,
        suffix: suffix,
        localizedSuffix: localizedSuffix,
      });
    });

    // const reportCountUp = new CountUp("reports-count-up", 3362, {
    //   separator: localeSeparator,
    // });
    // const volunteersCountUp = new CountUp("volunteers-count-up", 1662, {
    //   separator: localeSeparator,
    // });
    // const countriesCountUp = new CountUp("countries-count-up", 91);
    // const reportedViewsPerDayCountUp = new CountUp(
    //   "reported-views-per-day-count-up",
    //   5794,
    //   { prefix: "~", separator: localeSeparator }
    // );
    // const otherViewsPerDayCountUp = new CountUp(
    //   "other-views-per-day-count-up",
    //   3312,
    //   { prefix: "~", separator: localeSeparator }
    // );
    // const views160DaysCountUp = new CountUp(
    //   "views-160days-count-up",
    //   160000000,
    //   { separator: localeSeparator }
    // );
    // const viewsPerVideoCountUp = new CountUp("views-per-video-count-up", 760, {
    //   prefix: "~",
    //   suffix: localizedSuffix,
    // });

    let observer = new IntersectionObserver(
      (entries, observer) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            //todo: count ups inside the accordion on youtube_regrets_2021 need further work to reliably run when the accordion is open and the stat is visible - currently working in chrome but not reliably cross-browser

            console.log(entry)
            // views160DaysCountUp.start();
            // viewsPerVideoCountUp.start();
            // reportedViewsPerDayCountUp.start();
            // otherViewsPerDayCountUp.start();
            // reportCountUp.start();

            // setTimeout(() => {
            //   volunteersCountUp.start();
            // }, 250);
            //
            // setTimeout(() => {
            //   countriesCountUp.start();
            // }, 500);

            observer.unobserve(entry.target);
          }
        });
      },
      { rootMargin: "0px 0px -10% 0px" }
    );

    stats.forEach((stat) => {
      observer.observe(stat);
    });
  }
};
