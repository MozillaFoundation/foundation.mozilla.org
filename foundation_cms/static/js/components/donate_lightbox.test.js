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
  let showModalSpy;
  let closeSpy;
  let originalShowModal;
  let originalClose;

  beforeEach(() => {
    document.body.innerHTML = "";
    delete window.wagtailAbTesting;
    originalShowModal = HTMLDialogElement.prototype.showModal;
    originalClose = HTMLDialogElement.prototype.close;
    showModalSpy = vi.fn();
    closeSpy = vi.fn();
    HTMLDialogElement.prototype.showModal = showModalSpy;
    HTMLDialogElement.prototype.close = closeSpy;
  });

  afterEach(() => {
    if (originalShowModal) {
      HTMLDialogElement.prototype.showModal = originalShowModal;
    } else {
      delete HTMLDialogElement.prototype.showModal;
    }

    if (originalClose) {
      HTMLDialogElement.prototype.close = originalClose;
    } else {
      delete HTMLDialogElement.prototype.close;
    }
  });

  it("does nothing when the lightbox is missing", () => {
    document.body.innerHTML = "";

    expect(() => initDonateLightbox()).not.toThrow();
    expect(showModalSpy).not.toHaveBeenCalled();
  });

  it("opens the lightbox on initialization", () => {
    buildLightboxMarkup();

    initDonateLightbox();

    expect(showModalSpy).toHaveBeenCalledTimes(1);
  });

  it("closes the lightbox when the close button is clicked", () => {
    buildLightboxMarkup();

    initDonateLightbox();
    document
      .querySelector("[data-donate-lightbox-close-button]")
      .dispatchEvent(new MouseEvent("click", { bubbles: true }));

    expect(closeSpy).toHaveBeenCalledTimes(1);
  });

  it("closes the lightbox when clicking the backdrop", () => {
    buildLightboxMarkup();
    const lightbox = document.querySelector("dialog.donate-lightbox");

    initDonateLightbox();
    lightbox.dispatchEvent(
      new MouseEvent("click", { bubbles: false, cancelable: true }),
    );

    expect(closeSpy).toHaveBeenCalledTimes(1);
  });

  it("does not close the lightbox when clicking inside the modal content", () => {
    buildLightboxMarkup();

    initDonateLightbox();
    document
      .querySelector(".donate-lightbox__content")
      .dispatchEvent(new MouseEvent("click", { bubbles: true }));

    expect(closeSpy).not.toHaveBeenCalled();
  });

  it("tracks donate CTA clicks and closes the lightbox", () => {
    buildLightboxMarkup();

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
    expect(closeSpy).toHaveBeenCalledTimes(1);
  });
});
