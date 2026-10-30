import { beforeAll, beforeEach, describe, expect, it } from "vitest";

let HeadingTextGroupController;

const FIELDS = [
  "tag_color",
  "notification_color",
  "big_label_style",
  "number",
  "highlight_color",
  "heading_level",
  "subheading",
  "action_type",
  "action",
];

beforeAll(async () => {
  window.StimulusModule = { Controller: class {} };
  ({ default: HeadingTextGroupController } =
    await import("./heading_text_group_controller.js"));
});

function mount(type, style = "number") {
  const select = (name, value) =>
    `<div class="w-field" data-contentpath="${name}"><select name="body-0-value-${name}"><option value="${value}" selected></option></select></div>`;
  const fields = FIELDS.map(
    (name) => `<div class="w-field" data-contentpath="${name}"></div>`,
  ).join("");

  document.body.innerHTML = `<div data-controller="heading-text-group">${select("label_type", type)}${fields}</div>`;
  document.body.querySelector(
    '[data-contentpath="big_label_style"]',
  ).innerHTML =
    `<select name="body-0-value-big_label_style"><option value="${style}" selected></option></select>`;

  const controller = new HeadingTextGroupController();
  controller.element = document.querySelector("[data-controller]");
  controller.connect();
  return controller;
}

const isHidden = (name) =>
  document.querySelector(`[data-contentpath="${name}"]`).style.display ===
  "none";

describe("HeadingTextGroupController", () => {
  beforeEach(() => {
    document.body.innerHTML = "";
  });

  it("hides every color field for the default label", () => {
    mount("default");

    ["tag_color", "notification_color", "highlight_color"].forEach((name) =>
      expect(isHidden(name)).toBe(true),
    );
    expect(isHidden("heading_level")).toBe(false);
  });

  it("shows only the tag color for a tag", () => {
    mount("tag");

    expect(isHidden("tag_color")).toBe(false);
    expect(isHidden("notification_color")).toBe(true);
  });

  it("hides level, subheading and action for a numbered Big Label", () => {
    mount("big_label", "number");

    [
      "heading_level",
      "subheading",
      "action_type",
      "action",
      "highlight_color",
    ].forEach((name) => expect(isHidden(name)).toBe(true));
    expect(isHidden("number")).toBe(false);
    expect(isHidden("big_label_style")).toBe(false);
  });

  it("shows the highlight color instead of the number for a highlight", () => {
    mount("big_label", "highlight");

    expect(isHidden("number")).toBe(true);
    expect(isHidden("highlight_color")).toBe(false);
  });
});
