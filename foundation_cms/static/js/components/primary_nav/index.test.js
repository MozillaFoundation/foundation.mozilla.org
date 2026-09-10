import { describe, expect, it } from "vitest";
import * as primaryNav from "./index.js";

describe("primary nav index", () => {
  it("re-exports the primary nav entry points", () => {
    expect(typeof primaryNav.initPrimaryNav).toBe("function");
    expect(typeof primaryNav.initWordmarkVisibilityOnScroll).toBe("function");
    expect(typeof primaryNav.initSearchToggle).toBe("function");
  });
});
