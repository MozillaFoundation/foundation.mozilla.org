import ProductReviewCarousel from "./carousel.js";
import { SELECTORS } from "./config.js";

export function initProductReviewCarousels() {
  document
    .querySelectorAll(SELECTORS.root)
    .forEach((el) => new ProductReviewCarousel(el));
}

export { ProductReviewCarousel }; // optional named export if needed elsewhere
