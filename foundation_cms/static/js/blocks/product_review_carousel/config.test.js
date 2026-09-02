import { describe, expect, it } from "vitest";
import * as config from "./config.js";

describe("product review carousel config", () => {
  it("exports the selectors, class names, and design constants", () => {
    expect(config.SELECTORS.root).toBe(".product-review-carousel");
    expect(config.SELECTORS.focusable).toContain("a[href]");
    expect(config.CLASSNAMES).toEqual({
      paused: "is-paused",
      track: "product-review-carousel__track",
    });
    expect(config.DISABLE_CAROUSEL_MIN_WIDTH).toBe(1024);
    expect(config.GROUP_SIZE).toBe(3);
    expect(config.PREFILL_MULTIPLIER).toBe(2.5);
    expect(config.PREFILL_MAX_LOOPS).toBe(10);
    expect(config.RECYCLE_SAFETY_MAX).toBe(6);
    expect(config.FRACTION_EPSILON).toBe(0.125);
    expect(config.IO_ROOT_MARGIN).toBe("50px 0px");
    expect(config.IO_THRESHOLDS).toEqual([0, 0.01, 0.1]);
    expect(config.MIN_INTERSECTION_RATIO).toBe(0.01);
    expect(config.MAX_FRAME_MS).toBe(48);
    expect(config.DEFAULT_PX_PER_SECOND).toBe(20);
    expect(config.NO_TABINDEX).toBe("__none__");
    expect(config.FOCUS_REFRESH_THROTTLE_MS).toBe(100);
  });
});
