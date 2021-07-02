import { CountUp } from 'countup.js';

export const initYoutubeRegretsResearchCountUp = () => {
  if ('IntersectionObserver' in window) {
    const reportCountUp = new CountUp('reports-count-up', 5234);
    const volunteersCountUp = new CountUp('volunteers-count-up', 1662);
    const countriesCountUp = new CountUp('countries-count-up', 91);

    let observer = new IntersectionObserver(
      (entries, observer) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
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

    document.querySelectorAll('.stat').forEach(stat => { observer.observe(stat) });
  }
}
