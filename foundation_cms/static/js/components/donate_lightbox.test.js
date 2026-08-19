import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { initDonateLightbox } from "./donate_lightbox.js";

function buildLightboxMarkup() {
  document.body.innerHTML = `
    <dialog class="donate-lightbox">
      <button data-donate-lightbox-close-button type="button">Close</button>
      <a data-donate-banner-cta-button href="#">Donate</a>
      <div class="donate-lightbox__content">Support Mozilla</div>
    </dialog>
  `;
}

describe("initDonateLightbox", () => {
  beforeEach(() => {
    document.body.innerHTML = "";
    delete window.wagtailAbTesting;
    HTMLDialogElement.prototype.showModal = vi.fn();
    HTMLDialogElement.prototype.close = vi.fn();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("does nothing when the lightbox is missing", () => {
    document.body.innerHTML = "";

    expect(() => initDonateLightbox()).not.toThrow();
  });

  it("opens the lightbox on initialization", () => {
    buildLightboxMarkup();
    const lightbox = document.querySelector("dialog.donate-lightbox");

    initDonateLightbox();

    expect(lightbox.showModal).toHaveBeenCalledTimes(1);
  });

  it("closes the lightbox when the close button is clicked", () => {
    buildLightboxMarkup();
    const lightbox = document.querySelector("dialog.donate-lightbox");

    initDonateLightbox();
    document
      .querySelector("[data-donate-lightbox-close-button]")
      .dispatchEvent(new MouseEvent("click", { bubbles: true }));

    expect(lightbox.close).toHaveBeenCalledTimes(1);
  });

  it("closes the lightbox when clicking the backdrop", () => {
    buildLightboxMarkup();
    const lightbox = document.querySelector("dialog.donate-lightbox");

    initDonateLightbox();
    lightbox.dispatchEvent(
      new MouseEvent("click", { bubbles: false, cancelable: true }),
    );

    expect(lightbox.close).toHaveBeenCalledTimes(1);
  });

  it("tracks donate CTA clicks and closes the lightbox", () => {
    buildLightboxMarkup();
    const lightbox = document.querySelector("dialog.donate-lightbox");
    window.wagtailAbTesting = {
      triggerEvent: vi.fn(),
    };

    initDonateLightbox();
    document
      .querySelector("[data-donate-banner-cta-button]")
      .dispatchEvent(new MouseEvent("click", { bubbles: true }));

    expect(window.wagtailAbTesting.triggerEvent).toHaveBeenCalledWith(
      "donate-banner-link-click",
    );
    expect(lightbox.close).toHaveBeenCalledTimes(1);
  });
});
