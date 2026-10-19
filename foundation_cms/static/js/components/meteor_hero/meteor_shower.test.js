import { describe, expect, it } from "vitest";
import { CONFIG, createShower, sampleShower } from "./meteor_shower.js";

const HEAT = ["orange", "yellow", "blue"];
const SIZES = {
  desktop: [1440, 812],
  wide: [1920, 992],
  tablet: [768, 936],
  phone: [390, 756],
};

const sample = (timeMs, [width, height] = SIZES.desktop, seed = 11) =>
  sampleShower(createShower(seed), width, height, timeMs, HEAT);

describe("sampleShower", () => {
  it("gives the same cells for the same seed, size and time", () => {
    expect(sample(1320)).toEqual(sample(1320));
  });

  it("gives a different sky for a different seed", () => {
    const skyAt = (seed) =>
      [1000, 5000, 9000, 13000].map((t) => sample(t, SIZES.desktop, seed));

    expect(skyAt(3)).not.toEqual(skyAt(11));
  });

  // Fingerprints of the seed-11 sky. These values were checked against LP's
  // own code (LP commit 52c6b4100d), so a change here means the port no longer
  // draws the sky LP's Content Studio shows.
  it("still draws LP's sky for seed 11", () => {
    const { rects, cols, rows, cell } = sample(1320);

    expect({ cols, rows, cell, cells: rects.length }).toEqual({
      cols: 25,
      rows: 14,
      cell: 59,
      cells: 19,
    });
    expect(sample(12000).rects).toHaveLength(14);
  });

  it("starts with an empty sky until the first meteor launches", () => {
    const firstLaunchMs = CONFIG.firstBigAt * CONFIG.step;

    expect(sample(firstLaunchMs - 1).rects).toEqual([]);
    expect(sample(firstLaunchMs).rects.length).toBeGreaterThan(0);
  });

  // The hero's reduced-motion frame. LP's original 3600ms fell in a lull and
  // was empty, so guard that this one shows a meteor head at every size.
  it.each(Object.entries(SIZES))(
    "shows a meteor head in the 1320ms still frame on %s",
    (_name, size) => {
      const head = sample(1320, size).rects.filter((rect) => rect.a === 1);

      expect(head.length).toBeGreaterThan(0);
    },
  );

  it("only paints with the colours it's given", () => {
    const colours = new Set();
    for (let t = 0; t < 30000; t += 110) {
      sample(t).rects.forEach((rect) => colours.add(rect.color));
    }

    expect([...colours].every((colour) => HEAT.includes(colour))).toBe(true);
  });

  it("keeps a bounded number of flights however long it runs", () => {
    const shower = createShower(11);
    // An hour of the shower, sampled once per tick.
    for (let t = 0; t < 60 * 60 * 1000; t += CONFIG.step) {
      sampleShower(shower, ...SIZES.desktop, t, HEAT);
    }

    expect(shower.sky.flights.length).toBeLessThanOrEqual(60);
  });
});
