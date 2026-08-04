import { beforeAll, beforeEach, describe, expect, it, vi } from "vitest";

let CharacterCountdownController;

beforeAll(async () => {
  window.StimulusModule = { Controller: class {} };
  ({ default: CharacterCountdownController } =
    await import("./character_countdown_controller.js"));
});

function createController(element) {
  const controller = new CharacterCountdownController();
  controller.element = element;
  return controller;
}

describe("CharacterCountdownController", () => {
  beforeEach(() => {
    document.body.innerHTML = "";
    window.ngettext = vi.fn((singular, plural, count) =>
      count === 1 ? singular : plural,
    );
    window.interpolate = vi.fn((message, values) =>
      message.replace("%(count)s", values.count),
    );
  });

  it("initializes native and legacy fields inside the edit form", () => {
    document.body.innerHTML = `
      <form data-edit-form>
        <input id="title" maxlength="10" value="abc">
        <input id="legacy" maxlength="2" data-max-length="5" value="abc">
        <h3 class="max-length-countdown"></h3>
      </form>
    `;
    const form = document.querySelector("[data-edit-form]");
    const controller = createController(form);

    controller.connect();

    const titleCountdown = document.querySelector(
      "#title + .max-length-countdown",
    );
    const legacyCountdown = document.querySelector(
      "#legacy + .max-length-countdown",
    );

    expect(titleCountdown).toBeInstanceOf(HTMLOutputElement);
    expect(titleCountdown.textContent).toBe("7 characters remaining");
    expect(titleCountdown.getAttribute("for")).toBe("title");
    expect(titleCountdown.getAttribute("aria-live")).toBe("polite");
    expect(legacyCountdown.tagName).toBe("H3");
    expect(legacyCountdown.textContent).toBe("2 characters remaining");
    expect(legacyCountdown.getAttribute("aria-live")).toBe("polite");
  });

  it("uses one delegated listener for dynamically inserted fields", () => {
    document.body.innerHTML = "<form data-edit-form></form>";
    const form = document.querySelector("[data-edit-form]");
    const controller = createController(form);
    controller.connect();

    form.insertAdjacentHTML(
      "beforeend",
      '<textarea id="dynamic" maxlength="4">a</textarea>',
    );
    const field = document.querySelector("#dynamic");

    expect(field.nextElementSibling).toBeNull();

    field.dispatchEvent(new InputEvent("input", { bubbles: true }));
    expect(field.nextElementSibling.textContent).toBe("3 characters remaining");

    field.value = "ab";
    field.dispatchEvent(new InputEvent("input", { bubbles: true }));
    expect(field.nextElementSibling.textContent).toBe("2 characters remaining");
    expect(form.querySelectorAll(".max-length-countdown")).toHaveLength(1);
  });

  it("shows a localized warning when a legacy soft limit is exceeded", () => {
    document.body.innerHTML = `
      <form data-edit-form>
        <input
          id="legacy"
          class="max-length-warning"
          data-max-length="3"
          value="1234"
        >
      </form>
    `;
    const controller = createController(
      document.querySelector("[data-edit-form]"),
    );

    controller.connect();

    const countdown = document.querySelector(".max-length-countdown");
    expect(countdown.textContent).toBe("1 character over limit");
    expect(countdown.classList.contains("warning")).toBe(true);
    expect(window.ngettext).toHaveBeenCalledWith(
      "%(count)s character over limit",
      "%(count)s characters over limit",
      1,
    );
  });

  it("excludes rich-text fields", () => {
    document.body.innerHTML = `
      <form data-edit-form>
        <div class="Draftail-root">
          <textarea id="rich-text" maxlength="20">content</textarea>
        </div>
      </form>
    `;
    const field = document.querySelector("#rich-text");
    const controller = createController(
      document.querySelector("[data-edit-form]"),
    );

    controller.connect();
    field.dispatchEvent(new InputEvent("input", { bubbles: true }));

    expect(document.querySelector(".max-length-countdown")).toBeNull();
  });

  it("does not affect limited fields outside its edit-form boundary", () => {
    document.body.innerHTML = `
      <input id="username" maxlength="150">
      <form data-edit-form>
        <input id="title" maxlength="10">
      </form>
    `;
    const controller = createController(
      document.querySelector("[data-edit-form]"),
    );

    controller.connect();

    expect(
      document.querySelector("#username + .max-length-countdown"),
    ).toBeNull();
    expect(
      document.querySelector("#title + .max-length-countdown"),
    ).not.toBeNull();
  });

  it("stops handling delegated input events after disconnect", () => {
    document.body.innerHTML = "<form data-edit-form></form>";
    const form = document.querySelector("[data-edit-form]");
    const controller = createController(form);
    controller.connect();
    controller.disconnect();

    form.insertAdjacentHTML(
      "beforeend",
      '<input id="after-disconnect" maxlength="10">',
    );
    const field = document.querySelector("#after-disconnect");
    field.dispatchEvent(new InputEvent("input", { bubbles: true }));

    expect(field.nextElementSibling).toBeNull();
  });
});
