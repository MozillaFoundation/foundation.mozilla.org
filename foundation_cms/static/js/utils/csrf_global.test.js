import { describe, expect, it } from "vitest";
import { ensureCsrfToken, getCookie } from "./csrf.js";
import "./csrf_global.js";

describe("CSRF global entry point", () => {
  it("exposes the shared helpers on window.FoundationCSRF", () => {
    expect(window.FoundationCSRF).toEqual({ getCookie, ensureCsrfToken });
  });
});
