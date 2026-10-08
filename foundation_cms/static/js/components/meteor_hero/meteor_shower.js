// Ported from LP studio/heroes/meteor.html (the `METEOR` simulation)
// LP commit 52c6b4100d
//
// The pixel meteor shower behind the Meteor hero. Not a copy of LP's file, but
// it behaves exactly the same: for the same seed, size and time it returns the
// same cells as LP's code, so the hero shows the sky LP's Content Studio shows.
//
// From LP, unchanged: every value in CONFIG, the head shapes, the random
// number generator (mulberry32), the per-cell coin (hash2), and all the logic
// for scheduling flights, their arcs, trails, embers, fade and colour cooling.
//
// What we changed:
// - Rewritten as an ES module in modern JS with our formatting, and LP's
//   comments shortened.
// - Only LP's default settings are kept (Logo palette, square cells, 1x speed
//   and rate, no "wild" flights). Two random draws that only the removed
//   settings used are kept, so the sky still matches LP's for the same seed.
// - No DOM access: the colours are passed in as `heat` instead of read from
//   CSS, so meteor_hero.js owns the DOM and this module is testable.
//
// LP's notes: one big star at a time (the storyboard's protagonist), up to two
// small ones. Everything is quantized to the 110ms tick; the arc, head anatomy
// and trail behaviour were measured from the Figma storyboard. Trails mostly
// fade in stepped alpha; a few embers settle toward the ground line first.

export const CONFIG = {
  cellK: 0.0725, // cell size as a share of the viewport's short side
  step: 110, // the tick, ms
  trailLife: 9, // ticks a trail cell lives
  pairFresh: 6, // the freshest ticks also light a pair cell
  settleP: 0.12, // ember probability (lower third only)
  ctrlX: 0.45, // measured arc control (normalized)
  ctrlY: 0.34,
  bigEvery: [26, 46], // gap ticks between big flights
  firstBigAt: 4, // ticks before the first launch
  baseSpd: 2, // the dialled-in flight speed (2x)
};

// Storyboard head anatomy, as offsets from the lead cell. The third field is
// heat rank: 0 is the leading edge and hottest, cooling backward.
const HEAD_BIG = [
  [1, -1, 0], // the nose
  [0, 0, 0], // the hot core pair
  [1, 0, 0],
  [-1, 1, 1], // the shoulder, one cooler
  [0, 1, 1],
];
const HEAD_SMALL = [
  [0, 0, 0],
  [-1, 1, 1],
];

// LP's seeded PRNG, so a seed always gives the same sky.
function mulberry32(a) {
  return function () {
    a |= 0;
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

// A deterministic per-cell coin.
function hash2(a, b) {
  let h = (a * 374761393 + b * 668265263) | 0;
  h = Math.imul(h ^ (h >>> 13), 1274126177);
  return ((h ^ (h >>> 16)) >>> 0) / 4294967296;
}

// The sky is one composed score, like a real shower: lulls, lone strays,
// two-star volleys, solo bigs, and a big followed by two smalls. Flights are
// generated lazily from one seeded stream.
function makeSky(seed) {
  return { rnd: mulberry32(seed), flights: [], cursor: CONFIG.firstBigAt };
}

function newFlight(r, big, launch, cols, rows) {
  const f = { launch, big };
  // LP drew here to decide whether this is a "wild" flight. The hero never
  // has them, but the draw stays so the sequence matches LP's.
  r();
  // Organic chords: enter from the bottom edge or low on the left edge, exit
  // through the right edge or high on the top edge.
  if (r() < 0.6) {
    f.x0 = -2 + r() * (cols * 0.55 + 2);
    f.y0 = rows + r() * 2;
  } else {
    f.x0 = -2 - r() * 1.5;
    f.y0 = rows * 0.55 + r() * (rows * 0.45 + 1);
  }
  if (r() < 0.6) {
    f.x1 = cols + r() * 3;
    f.y1 = -1 + r() * (rows * 0.6 + 1);
  } else {
    f.x1 = cols * 0.5 + r() * (cols * 0.5 + 2);
    f.y1 = -2 - r() * 1.5;
  }
  f.cx = f.x0 + (f.x1 - f.x0) * (CONFIG.ctrlX + (r() - 0.5) * 0.1);
  f.cy = f.y0 + (f.y1 - f.y0) * (1 - CONFIG.ctrlY + (r() - 0.5) * 0.1);
  const span = (cols + rows) * 0.72;
  if (big) {
    // Some cross in a blaze, some hang in the sky.
    f.u0 = 0;
    f.u1 = 1;
    f.dur = Math.max(7, Math.round(span * (0.38 + r() * 0.65)));
  } else {
    // A small one ignites mid-sky and burns out mid-sky, on its own arc.
    f.u0 = 0.12 + r() * 0.35;
    f.u1 = Math.min(0.92, f.u0 + 0.22 + r() * 0.3);
    f.dur = Math.max(4, Math.round(span * 0.62 * (0.34 + r() * 0.68)));
  }
  // Only the Spectrum palette used the rung, but the draw stays for the same
  // reason as the wild-flight one above.
  f.rung = big ? Math.floor(r() * 3) : Math.floor(r() * 4);
  f.small = r() < 0.5 ? 1 : 2;
  return f;
}

function ensureFlights(sky, T, cols, rows) {
  const r = sky.rnd;
  const gap = (n) => Math.max(1, Math.round(n));
  const bigGap = () =>
    gap(CONFIG.bigEvery[0] + r() * (CONFIG.bigEvery[1] - CONFIG.bigEvery[0]));

  while (sky.cursor <= T + 2) {
    let roll = r();
    const c2 = sky.cursor;
    // The score opens on the protagonist: the first flight is always a big one.
    if (sky.flights.length === 0) roll = 0.7;
    const smallDur = Math.round((cols + rows) * 0.45);
    if (roll < 0.28) {
      // A lull: the sky rests.
      sky.cursor = c2 + gap(16 + r() * 26);
    } else if (roll < 0.5) {
      // A lone stray.
      sky.flights.push(newFlight(r, false, c2, cols, rows));
      sky.cursor = c2 + gap(smallDur + 6 + r() * 14);
    } else if (roll < 0.68) {
      // A volley: two smalls, staggered.
      sky.flights.push(newFlight(r, false, c2, cols, rows));
      sky.flights.push(
        newFlight(r, false, c2 + 3 + Math.floor(r() * 4), cols, rows),
      );
      sky.cursor = c2 + gap(smallDur + 10 + r() * 16);
    } else if (roll < 0.85) {
      // The big one, alone.
      const fb = newFlight(r, true, c2, cols, rows);
      sky.flights.push(fb);
      sky.cursor = c2 + fb.dur + bigGap();
    } else {
      // The big one, then two smalls in its wake.
      const fb2 = newFlight(r, true, c2, cols, rows);
      const wake = c2 + Math.round(fb2.dur * 0.5);
      sky.flights.push(fb2);
      sky.flights.push(newFlight(r, false, wake, cols, rows));
      sky.flights.push(newFlight(r, false, wake + 5, cols, rows));
      sky.cursor = c2 + fb2.dur + bigGap();
    }
    // Keep memory bounded.
    if (sky.flights.length > 60) {
      sky.flights.splice(0, sky.flights.length - 60);
    }
  }
}

// A quadratic bezier, in grid coordinates.
function pathAt(f, u) {
  const v = 1 - u;
  return [
    v * v * f.x0 + 2 * v * u * f.cx + u * u * f.x1,
    v * v * f.y0 + 2 * v * u * f.cy + u * u * f.y1,
  ];
}

// Stepped fade: the storyboard's thinning, in quantized levels.
function trailAlpha(age) {
  if (age <= 1) return 1;
  if (age <= 3) return 0.72;
  if (age <= 5) return 0.45;
  if (age <= 7) return 0.22;
  if (age <= CONFIG.trailLife) return 0.1;
  return 0;
}

/**
 * Starts a new sky. The hero uses LP's seed, 11.
 *
 * @param {number} seed
 * @returns {{seed: number, sky: object}}
 */
export function createShower(seed) {
  return { seed, sky: makeSky(seed * 3 + 1) };
}

/**
 * Samples the shower at a moment in time. Deterministic for a given shower,
 * size and time, so the same inputs always give the same cells.
 *
 * @param {{seed: number, sky: object}} shower - From createShower().
 * @param {number} width - Drawing width, CSS px.
 * @param {number} height - Drawing height, CSS px.
 * @param {number} timeMs - Time since the shower started.
 * @param {string[]} heat - Colours from hottest to coolest (LP's Logo ladder:
 *   orange, yellow, blue).
 * @returns {{rects: {x: number, y: number, w: number, h: number, color: string, a: number}[], cell: number, cols: number, rows: number, tick: number}}
 */
export function sampleShower(shower, width, height, timeMs, heat) {
  const spd = CONFIG.baseSpd;
  const cell = Math.max(8, Math.round(Math.min(width, height) * CONFIG.cellK));
  const cols = Math.ceil(width / cell);
  const rows = Math.ceil(height / cell);
  const T = Math.floor(timeMs / CONFIG.step);
  const rects = [];
  const heatAt = (rank) => heat[Math.min(heat.length - 1, rank)];

  ensureFlights(shower.sky, T, cols, rows);

  for (const f of shower.sky.flights) {
    if (T < f.launch || T > f.launch + f.dur / spd + CONFIG.trailLife + rows) {
      continue;
    }
    // The head's live position, needed by the trail's ball-cull.
    const uT = f.u0 + (f.u1 - f.u0) * (((T - f.launch) * spd) / f.dur);
    const headAlive = uT <= f.u1 + 1e-9 && (T - f.launch) * spd <= f.dur;
    const hp = pathAt(f, Math.min(uT, f.u1));
    const hx = Math.round(hp[0]);
    const hy = Math.round(hp[1]);

    // The trail: cells at past head positions, in a stepped fade. A few
    // embers settle toward the ground line before going.
    const from = Math.max(f.launch, T - CONFIG.trailLife - rows);
    for (let pt = from; pt < Math.min(T, f.launch + f.dur); pt++) {
      const age = T - pt;
      const pu = f.u0 + (f.u1 - f.u0) * (((pt - f.launch) * spd) / f.dur);
      const pp = pathAt(f, pu);
      const tx = Math.round(pp[0]);
      let ty = Math.round(pp[1]);
      const ember =
        hash2(shower.seed * 131 + f.launch, pt) < CONFIG.settleP &&
        ty > rows * 0.66;
      let a;
      if (ember) {
        // Settle: down one cell every 2 ticks to the bottom row, then a short
        // stepped fade.
        const drop = Math.min(rows - 1 - ty, Math.floor(age / 2));
        ty += drop;
        const rest = age - drop * 2;
        if (ty >= rows - 1) {
          a = rest <= 3 ? 0.45 : rest <= 6 ? 0.22 : 0;
        } else {
          a = 0.6;
        }
      } else {
        a = trailAlpha(age);
      }
      if (a <= 0.004) continue;
      if (tx < -1 || tx > cols || ty < -1 || ty > rows) continue;
      // The ball owns its ground: no trail cell inside the head's footprint
      // while the head is alive.
      if (
        headAlive &&
        tx >= hx - 1 &&
        tx <= hx + 1 &&
        ty >= hy - 1 &&
        ty <= hy + 1
      ) {
        continue;
      }
      // The tail cools in hue as it ages, stepping down the ladder; embers
      // are the coldest remnants.
      const rank = ember ? 9 : age <= 2 ? 1 : age <= 4 ? 2 : age <= 6 ? 3 : 4;
      const color = heatAt(rank);
      rects.push({ x: tx * cell, y: ty * cell, w: cell, h: cell, color, a });
      // The paired second row right behind the head.
      if (!ember && age <= CONFIG.pairFresh && f.big) {
        const psx = f.x1 >= f.x0 ? 1 : -1;
        const psy = f.y1 <= f.y0 ? 1 : -1;
        rects.push({
          x: (tx - psx) * cell,
          y: (ty + psy) * cell,
          w: cell,
          h: cell,
          color,
          a: age <= 2 ? a : a * 0.85,
        });
      }
    }

    // The head lives on its own segment of the arc: smalls ignite mid-sky (u0)
    // and burn out mid-sky (u1).
    if (headAlive) {
      const tpl = f.big ? HEAD_BIG : HEAD_SMALL.slice(0, f.small);
      const sx = f.x1 >= f.x0 ? 1 : -1;
      const sy = f.y1 <= f.y0 ? 1 : -1; // 1 = climbing
      for (const [dx, dy, rank] of tpl) {
        const gx = hx + dx * sx;
        const gy = hy + dy * sy;
        if (gx < -1 || gx > cols || gy < -1 || gy > rows) continue;
        rects.push({
          x: gx * cell,
          y: gy * cell,
          w: cell,
          h: cell,
          color: heatAt(rank),
          a: 1,
        });
      }
    }
  }

  return { rects, cell, cols, rows, tick: T };
}
