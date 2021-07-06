import { CountUp } from 'countup.js';

export const initYoutubeRegretsResearchCountUp = () => {
  if ('IntersectionObserver' in window) {
    const reportCountUp = new CountUp('reports-count-up', 5234);
    const volunteersCountUp = new CountUp('volunteers-count-up', 1662);
    const countriesCountUp = new CountUp('countries-count-up', 91);
    const reportedViewsPerDayCountUp = new CountUp('reported-views-per-day-count-up', 5794, { prefix: '~' })
    const otherViewsPerDayCountUp = new CountUp('other-views-per-day-count-up', 3312, { prefix: '~' })
    const views160DaysCountUp = new CountUp('views-160days-count-up', 160000000);
    const viewsPerVideoCountUp = new CountUp('views-per-video-count-up', 170, { prefix: '~', suffix: 'K' });

    let observer = new IntersectionObserver(
      (entries, observer) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            //todo: count ups inside the accordion need further work to reliably run when the accordion is open and the stat is visible - currently working in chrome but not reliably cross-browser
            views160DaysCountUp.start();
            viewsPerVideoCountUp.start();
            reportedViewsPerDayCountUp.start();
            otherViewsPerDayCountUp.start();
            reportCountUp.start();

            setTimeout(() => {
              volunteersCountUp.start();
            }, 250);

            setTimeout(() => {
              countriesCountUp.start();
            }, 500);

            observer.unobserve(entry.target);
          }
        });
      },
      { rootMargin: "0px 0px -10% 0px" });

    document.querySelectorAll('.stat').forEach(stat => { observer.observe(stat) }
    );
  }
}
