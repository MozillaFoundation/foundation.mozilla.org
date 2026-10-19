// Ported from LP studio/heroes/galaxy.html, final handoff 804c5fd.
// The seeded field and sampling math stay independent of the browser.
export function createGalaxyField(colorToken) {
  // Spectrum weights preserve LP's reference composition.
  const PALETTE = [
    {
      hex: colorToken("--color-spectrum-yellow-600"),
      w: 30,
    },
    { hex: colorToken("--color-spectrum-cyan"), w: 23 },
    {
      hex: colorToken("--color-spectrum-apricot"),
      w: 10,
    },
    { hex: colorToken("--color-accent-blue"), w: 10 },
    { hex: colorToken("--color-spectrum-crimson"), w: 9 },
    { hex: colorToken("--color-accent-orange"), w: 8 },
    { hex: colorToken("--color-card-pink"), w: 7 },
    { hex: colorToken("--color-card-lime"), w: 3 },
  ];

  /* Cluster shapes on the square grid; cells are offsets from the
     anchor and each shape carries its bbox so it can be centered. */
  function shape(w, cells) {
    let maxX = 0,
      maxY = 0;
    for (let i = 0; i < cells.length; i++) {
      if (cells[i][0] > maxX) maxX = cells[i][0];
      if (cells[i][1] > maxY) maxY = cells[i][1];
    }
    const widthInCells = maxX + 1,
      heightInCells = maxY + 1; /* bbox, cells */
    /* symmetric overhang past the true center per axis, in cells,
       incl. 0.5 cell grid-snap slop */
    return {
      w: w,
      cells: cells,
      widthInCells: widthInCells,
      heightInCells: heightInCells,
      mx: widthInCells / 2 + 0.5,
      my: heightInCells / 2 + 0.5,
    };
  }
  const SHAPES = [
    shape(24, [[0, 0]]),
    shape(14, [
      [0, 0],
      [1, 0],
    ]),
    shape(14, [
      [0, 0],
      [0, 1],
    ]),
    shape(10, [
      [0, 0],
      [1, 0],
      [1, 1],
    ]),
    shape(10, [
      [0, 0],
      [0, 1],
      [1, 1],
    ]),
    shape(8, [
      [0, 0],
      [1, 0],
      [0, 1],
    ]),
    shape(6, [
      [0, 0],
      [1, 0],
      [2, 0],
    ]),
    shape(6, [
      [0, 0],
      [0, 1],
      [0, 2],
    ]),
    shape(8, [
      [0, 0],
      [1, 0],
      [0, 1],
      [1, 1],
    ]),
  ];

  const CONFIG = {
    n: 64 /* clusters */,
    arms: 8 /* spiral arms — fewer, denser chains */,
    armJitter: 0.12 /* angular scatter within an arm (rad) */,
    armTwist: 1.7 /* arm curvature: theta advance per unit radius */,
    cellK: 0.0725 /* cell = cellK * min(W,H)  (0.073 in reference) */,
    innerKX: 0.727 /* inner ellipse semi-x = innerKX * W/2 */,
    innerKY: 1.089 /* inner ellipse semi-y = innerKY * H/2 */,
    cornerK: 1.1 /* outer band reaches corner distance * cornerK */,
    radialBias: 1.6 /* >1 packs clusters toward inner edge */,
    dodgeFromMs: 1150 /* copy keep-out engages just before the fade */,
    dodgePad: 0.4 /* clearance around copy, cells */,
    step: 110 /* quantized clock, ms */,
    holdMs: 320 /* dense pinwheel hold before burst */,
    burstMs: 1500 /* per-cluster radial travel */,
    waveMs: 520 /* emanation wavefront (delay grows w/ radius) */,
    jitterMs: 180 /* per-cluster delay jitter */,
    swirlMin: 0.65 /* rad unwound during burst */,
    swirlMax: 1.15,
    omega: (2 * Math.PI) / 140000 /* settled rotation: 1 rev / 140 s */,
  };

  function mulberry32(a) {
    return function () {
      a |= 0;
      a = (a + 0x6d2b79f5) | 0;
      let t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  function pickWeighted(list, r) {
    let total = 0,
      i;
    for (i = 0; i < list.length; i++) total += list[i].w;
    let x = r * total;
    for (i = 0; i < list.length; i++) {
      x -= list[i].w;
      if (x <= 0) return list[i];
    }
    return list[list.length - 1];
  }
  function easeOutQuart(t) {
    t = 1 - t;
    return 1 - t * t * t * t;
  }
  function clamp01(t) {
    return t < 0 ? 0 : t > 1 ? 1 : t;
  }

  /* place (optional) moves the galaxy off the viewport centre for the
     mobile options: cx, cy centre the field; ccx, ccy centre the copy
     keep-out; rx, ry replace the inner ellipse. */
  function buildField(
    seed,
    width,
    height,
    clearHalfX,
    clearHalfY,
    palette,
    place,
  ) {
    palette = palette || PALETTE;
    place = place || {};
    const rnd = mulberry32(seed);
    const shortSide = Math.min(width, height);
    const cell = Math.max(8, Math.round(shortSide * CONFIG.cellK));
    const rx =
      place.rx || (CONFIG.innerKX * width) / 2; /* inner ellipse semi-axes */
    const ry = place.ry || (CONFIG.innerKY * height) / 2;
    const fieldCenterX = place.cx != null ? place.cx : width / 2;
    const fieldCenterY = place.cy != null ? place.cy : height / 2;
    /* outer band pinned to the farthest viewport corner */
    const cornerRadiusX = Math.max(fieldCenterX, width - fieldCenterX) / rx,
      cornerRadiusY = Math.max(fieldCenterY, height - fieldCenterY) / ry;
    const outerRadius =
      Math.sqrt(cornerRadiusX * cornerRadiusX + cornerRadiusY * cornerRadiusY) *
      CONFIG.cornerK;
    /* Each arm is a chain: members stratified along the radial band,
       tight angular scatter, strong shared twist — the arm stays
       legible through burst, settle, and rotation. */
    const perArm = Math.ceil(CONFIG.n / CONFIG.arms);
    const armSwirl = [];
    for (let a = 0; a < CONFIG.arms; a++)
      armSwirl.push(
        CONFIG.swirlMin + rnd() * (CONFIG.swirlMax - CONFIG.swirlMin),
      );
    const clusters = [];
    for (let i = 0; i < CONFIG.n; i++) {
      const arm = i % CONFIG.arms;
      const member = Math.floor(i / CONFIG.arms);
      const clusterShape = pickWeighted(SHAPES, rnd());
      const along = (member + rnd() * 0.7) / perArm; /* 0..1 along the arm */
      const finalRadius =
        1 + (outerRadius - 1) * Math.pow(along, CONFIG.radialBias);
      const theta =
        arm * ((2 * Math.PI) / CONFIG.arms) +
        (rnd() - 0.5) * CONFIG.armJitter +
        (finalRadius - 1) * CONFIG.armTwist; /* spiral curvature */
      const delay =
        CONFIG.holdMs +
        ((finalRadius - 1) / (outerRadius - 1)) * CONFIG.waveMs +
        rnd() * CONFIG.jitterMs;
      const swirl = armSwirl[arm] + (rnd() - 0.5) * 0.12;
      clusters.push({
        theta: theta,
        rFinal: finalRadius,
        r0: ((0.2 + rnd() * 1.6) * cell) / Math.max(rx, ry),
        delay: delay,
        swirl: swirl,
        shape: clusterShape,
        color: pickWeighted(palette, rnd()).hex,
      });
    }
    return {
      width: width,
      height: height,
      cell: cell,
      rx: rx,
      ry: ry,
      clusters: clusters,
      cx: fieldCenterX,
      cy: fieldCenterY,
      ccx: place.ccx != null ? place.ccx : fieldCenterX,
      ccy: place.ccy != null ? place.ccy : fieldCenterY,
      clear: clearHalfX
        ? {
            hx: clearHalfX + CONFIG.dodgePad * cell,
            hy: (clearHalfY || height * 0.13) + CONFIG.dodgePad * cell,
          }
        : null,
      settleAt:
        CONFIG.holdMs + CONFIG.waveMs + CONFIG.jitterMs + CONFIG.burstMs,
    };
  }

  function sampleField(field, tMs, hideHeld) {
    const t = Math.floor(tMs / CONFIG.step) * CONFIG.step; /* quantized clock */
    const cx = field.cx,
      cy = field.cy,
      cell = field.cell;
    const copyCenterX = field.ccx,
      copyCenterY = field.ccy;
    const rects = [];
    for (let i = 0; i < field.clusters.length; i++) {
      const cluster = field.clusters[i];
      if (hideHeld && t < cluster.delay) continue; /* appears at its own beat */
      const p = clamp01((t - cluster.delay) / CONFIG.burstMs);
      const e = easeOutQuart(p);
      const r = cluster.r0 + (cluster.rFinal - cluster.r0) * e;
      const spin = t > field.settleAt ? (t - field.settleAt) * CONFIG.omega : 0;
      const angle = cluster.theta - cluster.swirl * (1 - e) + spin;
      const px = cx + r * Math.cos(angle) * field.rx;
      const py = cy + r * Math.sin(angle) * field.ry;
      /* snap so the shape's bbox is truly centered on the target */
      let gridX = Math.round(px / cell - cluster.shape.widthInCells / 2) * cell;
      let gridY =
        Math.round(py / cell - cluster.shape.heightInCells / 2) * cell;
      /* Copy keep-out: once the copy is up, a cluster whose snapped
         footprint would touch it steps outward, cell by cell, along
         its dominant radial axis, and flows back after passing. */
      if (field.clear && t >= CONFIG.dodgeFromMs) {
        let guard = 0;
        while (
          guard++ < 10 &&
          gridX < copyCenterX + field.clear.hx &&
          gridX + cluster.shape.widthInCells * cell >
            copyCenterX - field.clear.hx &&
          gridY < copyCenterY + field.clear.hy &&
          gridY + cluster.shape.heightInCells * cell >
            copyCenterY - field.clear.hy
        ) {
          const dx = Math.cos(angle) * field.rx,
            dy = Math.sin(angle) * field.ry;
          if (Math.abs(dx) >= Math.abs(dy)) gridX += dx >= 0 ? cell : -cell;
          else gridY += dy >= 0 ? cell : -cell;
        }
      }
      for (let k = 0; k < cluster.shape.cells.length; k++) {
        rects.push({
          x: gridX + cluster.shape.cells[k][0] * cell,
          y: gridY + cluster.shape.cells[k][1] * cell,
          w: cell,
          h: cell,
          color: cluster.color,
        });
      }
    }
    return rects;
  }

  return {
    buildField: buildField,
    sampleField: sampleField,
    CONFIG: CONFIG,
    PALETTE: PALETTE,
  };
}
