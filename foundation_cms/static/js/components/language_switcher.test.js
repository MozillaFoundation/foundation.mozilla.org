import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { initLanguageSwitcher } from "./language_switcher.js";

describe("initLanguageSwitcher", () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <form id="language-switcher-form">
        <input type="hidden" id="language-csrftoken" value="" />
        <input type="hidden" id="language-next" value="" />
        <select id="language-switcher">
          <option value="en" data-url="/en/example/" selected>English</option>
          <option value="fr" data-url="/fr/example/">French</option>
          <option value="de">German</option>
        </select>
      </form>
    `;
    document.cookie = "csrftoken=test-token";
  });

  afterEach(() => {
    document.cookie = "csrftoken=; Max-Age=0; path=/";
    vi.restoreAllMocks();
  });

  it("sets the localized URL and CSRF token before submitting", async () => {
    const form = document.getElementById("language-switcher-form");
    const selector = document.getElementById("language-switcher");
    const submit = vi.spyOn(form, "submit").mockImplementation(() => {});

    initLanguageSwitcher();
    selector.value = "fr";
    selector.dispatchEvent(new Event("change"));

    await vi.waitFor(() => expect(submit).toHaveBeenCalledOnce());
    expect(document.getElementById("language-next").value).toBe("/fr/example/");
    expect(document.getElementById("language-csrftoken").value).toBe(
      "test-token",
    );
  });

  it("falls back to the site root when the language has no URL", async () => {
    const form = document.getElementById("language-switcher-form");
    const selector = document.getElementById("language-switcher");
    const submit = vi.spyOn(form, "submit").mockImplementation(() => {});

    initLanguageSwitcher();
    selector.value = "de";
    selector.dispatchEvent(new Event("change"));

    await vi.waitFor(() => expect(submit).toHaveBeenCalledOnce());
    expect(document.getElementById("language-next").value).toBe("/");
  });

  it("does nothing when the language switcher is absent", () => {
    document.body.innerHTML = "";

    expect(() => initLanguageSwitcher()).not.toThrow();
  });
});
