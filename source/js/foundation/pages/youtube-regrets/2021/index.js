import { initYouTubeRegretsCategoriesBarChart } from "./categories-bar-chart";
import { initYouTubeRegretsRegretRatesChart } from "./regret-rates-chart";
import { initYoutubeRegretsReadMoreCategories } from "./read-more-categories";
import { initYoutubeRegretsResearchCountUp } from "./count-up";
import { initYoutubeRegretsAccordions } from "./accordion";
import { initYouTubeRegretsRecommendationsPieChart } from "./recommendations-pie-chart";
import { initYoutubeRegretsCarousel } from "./carousel";

export default function initYoutubeRegrets2021() {
    initYouTubeRegretsCategoriesBarChart();
    initYouTubeRegretsRegretRatesChart();
    initYoutubeRegretsReadMoreCategories();
    initYoutubeRegretsResearchCountUp();
    initYoutubeRegretsAccordions();
    initYouTubeRegretsRecommendationsPieChart();
    initYoutubeRegretsCarousel();
}
