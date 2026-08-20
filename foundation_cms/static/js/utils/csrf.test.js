import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { ensureCsrfToken, getCookie, initCsrfForms } from "./csrf.js";

function clearCsrfCookie() {
  document.cookie = "csrftoken=; Max-Age=0; path=/";
}

describe("CSRF utilities", () => {
  beforeEach(() => {
    clearCsrfCookie();
    document.body.innerHTML = "";
  });

  afterEach(() => {
    clearCsrfCookie();
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
  });

  it("reads and decodes a named cookie", () => {
    document.cookie = "other=value; path=/";
    document.cookie = "csrftoken=token%20value; path=/";

    expect(getCookie("csrftoken")).toBe("token value");
    expect(getCookie("missing")).toBe("");
  });

  it("returns an existing token without fetching", async () => {
    document.cookie = "csrftoken=existing; path=/";
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);

    await expect(ensureCsrfToken()).resolves.toBe("existing");
    expect(fetchMock).not.toHaveBeenCalled();
  });

  it("mints and returns a token when the cookie is absent", async () => {
    const fetchMock = vi.fn(async () => {
      document.cookie = "csrftoken=minted; path=/";
      return { ok: true };
    });
    vi.stubGlobal("fetch", fetchMock);

    await expect(ensureCsrfToken()).resolves.toBe("minted");
    expect(fetchMock).toHaveBeenCalledWith("/api/csrf/", {
      credentials: "same-origin",
    });
  });

  it.each([
    ["an unsuccessful response", vi.fn().mockResolvedValue({ ok: false })],
    ["a network failure", vi.fn().mockRejectedValue(new Error("offline"))],
  ])("returns an empty token after %s", async (_label, fetchMock) => {
    vi.stubGlobal("fetch", fetchMock);

    await expect(ensureCsrfToken()).resolves.toBe("");
  });

  it("populates a form token and preserves the clicked submitter", async () => {
    document.cookie = "csrftoken=form-token; path=/";
    document.body.innerHTML = `
      <form data-csrf-form>
        <input type="hidden" data-csrf-field name="csrfmiddlewaretoken">
        <button name="action" value="share">Share</button>
      </form>
    `;
    const form = document.querySelector("form");
    const submitter = form.querySelector("button");
    const submitSpy = vi.spyOn(form, "submit").mockImplementation(() => {});
    initCsrfForms();
    const event = new SubmitEvent("submit", {
      bubbles: true,
      cancelable: true,
      submitter,
    });

    form.dispatchEvent(event);

    await vi.waitFor(() => expect(submitSpy).toHaveBeenCalledOnce());
    expect(event.defaultPrevented).toBe(true);
    expect(form.querySelector("[data-csrf-field]").value).toBe("form-token");
    const mirror = form.querySelector("[data-csrf-submitter]");
    expect(mirror.type).toBe("hidden");
    expect(mirror.name).toBe("action");
    expect(mirror.value).toBe("share");
  });

  it("allows a form with an existing token to submit normally", () => {
    document.body.innerHTML = `
      <form data-csrf-form>
        <input data-csrf-field value="existing">
      </form>
    `;
    const form = document.querySelector("form");
    const submitSpy = vi.spyOn(form, "submit").mockImplementation(() => {});
    initCsrfForms();
    const event = new SubmitEvent("submit", {
      bubbles: true,
      cancelable: true,
    });

    form.dispatchEvent(event);

    expect(event.defaultPrevented).toBe(false);
    expect(submitSpy).not.toHaveBeenCalled();
  });
});
