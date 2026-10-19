import { beforeAll, beforeEach, describe, expect, it } from "vitest";

let ConditionalFieldsController;

beforeAll(async () => {
  window.StimulusModule = { Controller: class {} };
  ({ default: ConditionalFieldsController } =
    await import("./conditional_fields_controller.js"));
});

function createController({ disableHidden = true } = {}) {
  const element = document.querySelector("[data-root]");
  const controller = new ConditionalFieldsController();
  controller.element = element;
  controller.triggerFieldValue = "banner_style";
  controller.disableHiddenValue = disableHidden;
  controller.fieldTargets = [...element.querySelectorAll("[data-condition]")];
  return controller;
}

function selectStyle(value) {
  const select = document.querySelector("select");
  select.value = value;
  select.dispatchEvent(new Event("change", { bubbles: true }));
}

describe("ConditionalFieldsController", () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <div data-root>
        <select name="banner_style">
          <option value="pushdown">Pushdown</option>
          <option value="lightbox">Lightbox</option>
          <option value="pencil">Pencil</option>
        </select>
        <div id="image" data-condition="pushdown lightbox"><input name="image"></div>
        <div id="link" data-condition="pencil"><input name="link"></div>
      </div>
    `;
  });

  it("shows targets whose condition list includes the selected value", () => {
    const controller = createController();
    controller.connect();

    expect(document.getElementById("image").classList.contains("hidden")).toBe(
      false,
    );
    expect(document.getElementById("link").classList.contains("hidden")).toBe(
      true,
    );

    selectStyle("lightbox");
    expect(document.getElementById("image").style.display).toBe("block");

    selectStyle("pencil");
    expect(document.getElementById("image").style.display).toBe("none");
    expect(document.getElementById("link").style.display).toBe("block");
  });

  it("disables inputs in hidden targets by default", () => {
    createController().connect();

    expect(document.querySelector("[name=link]").disabled).toBe(true);
    expect(document.querySelector("[name=image]").disabled).toBe(false);
  });

  it("leaves hidden inputs enabled when disableHidden is false", () => {
    createController({ disableHidden: false }).connect();

    expect(document.getElementById("link").style.display).toBe("none");
    expect(document.querySelector("[name=link]").disabled).toBe(false);
  });
});
