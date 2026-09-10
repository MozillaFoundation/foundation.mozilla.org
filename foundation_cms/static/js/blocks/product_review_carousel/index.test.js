import { afterEach, describe, expect, it, vi } from "vitest";
import ProductReviewCarousel from "./carousel.js";
import {
  ProductReviewCarousel as NamedProductReviewCarousel,
  initProductReviewCarousels,
} from "./index.js";

describe("product review carousel entry point", () => {
  afterEach(() => {
    vi.restoreAllMocks();
    document.body.innerHTML = "";
  });

  it("exports the carousel and initializes every matching root", () => {
    document.body.innerHTML = `
      <section class="product-review-carousel"></section>
      <section class="product-review-carousel"></section>
    `;
    const initSpy = vi
      .spyOn(ProductReviewCarousel.prototype, "init")
      .mockImplementation(() => {});

    initProductReviewCarousels();

    expect(NamedProductReviewCarousel).toBe(ProductReviewCarousel);
    expect(initSpy).toHaveBeenCalledTimes(2);
  });
});
