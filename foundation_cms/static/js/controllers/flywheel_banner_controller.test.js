import { beforeAll, beforeEach, describe, expect, it, vi } from "vitest";

let FlywheelBannerController;

beforeAll(async () => {
  window.StimulusModule = { Controller: class {} };
  ({ default: FlywheelBannerController } =
    await import("./flywheel_banner_controller.js"));
});

function createController(heading = "Imagine") {
  document.body.innerHTML = `
    <div data-controller="flywheel-banner">
      <select name="body-0-value-mission">
        <option value="imagine" selected>Imagine</option>
        <option value="co-create">Co-create</option>
        <option value="mobilize">Mobilize</option>
      </select>
      <input name="body-0-value-heading" value="${heading}">
    </div>
  `;

  const controller = new FlywheelBannerController();
  controller.element = document.querySelector("[data-controller]");
  controller.connect();
  return controller;
}

describe("FlywheelBannerController", () => {
  beforeEach(() => {
    document.body.innerHTML = "";
  });

  it("updates an unchanged default heading when the mission changes", () => {
    createController();
    const mission = document.querySelector("select");
    const heading = document.querySelector("input");
    const inputListener = vi.fn();
    heading.addEventListener("input", inputListener);

    mission.value = "co-create";
    mission.dispatchEvent(new Event("change", { bubbles: true }));

    expect(heading.value).toBe("Co-create");
    expect(inputListener).toHaveBeenCalledOnce();
  });

  it("preserves a heading customized by the editor", () => {
    createController("Shape the future");
    const mission = document.querySelector("select");
    const heading = document.querySelector("input");

    mission.value = "mobilize";
    mission.dispatchEvent(new Event("change", { bubbles: true }));

    expect(heading.value).toBe("Shape the future");
  });

  it("stops listening after disconnect", () => {
    const controller = createController();
    const mission = document.querySelector("select");
    const heading = document.querySelector("input");
    controller.disconnect();

    mission.value = "mobilize";
    mission.dispatchEvent(new Event("change", { bubbles: true }));

    expect(heading.value).toBe("Imagine");
  });
});
