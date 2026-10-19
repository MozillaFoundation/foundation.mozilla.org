// Ported from LP studio/heroes/galaxy.html, final handoff 804c5fd.
// The seeded field and sampling math stay independent of the browser.
export function createGalaxyField(TOK) {
  /* Spectrum palette (Figma 4LGXunuoHeSygfrdHwr8D3 / 9269:14712),
     weighted per the vectorized reference composition. */
  /* Weighted spectrum, all design-system colours. Keep these in step with
     the GAL_PRIM_SRC keys — that map is keyed by the same hex values. */
  var PALETTE = [
    {
      hex: TOK("--color-spectrum-yellow-600"),
      w: 30,
    } /* core-yellow */,
    { hex: TOK("--color-spectrum-cyan"), w: 23 } /* cyan        */,
    {
      hex: TOK("--color-spectrum-apricot"),
      w: 10,
    } /* apricot     */,
    { hex: TOK("--color-accent-blue"), w: 10 } /* core-blue   */,
    { hex: TOK("--color-spectrum-crimson"), w: 9 } /* crimson     */,
    { hex: TOK("--color-accent-orange"), w: 8 } /* core-orange */,
    { hex: TOK("--color-card-pink"), w: 7 } /* pink        */,
    { hex: TOK("--color-card-lime"), w: 3 } /* lime        */,
  ];

  /* Cluster shapes on the square grid; cells are offsets from the
     anchor and each shape carries its bbox so it can be centered. */
  function shape(w, cells) {
    var maxX = 0,
      maxY = 0;
    for (var i = 0; i < cells.length; i++) {
      if (cells[i][0] > maxX) maxX = cells[i][0];
      if (cells[i][1] > maxY) maxY = cells[i][1];
    }
    var bw = maxX + 1,
      bh = maxY + 1; /* bbox, cells */
    /* symmetric overhang past the true center per axis, in cells,
       incl. 0.5 cell grid-snap slop */
    return {
      w: w,
      cells: cells,
      bw: bw,
      bh: bh,
      mx: bw / 2 + 0.5,
      my: bh / 2 + 0.5,
    };
  }
  var SHAPES = [
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

  var CFG = {
    n: 64 /* clusters                                      */,
    arms: 8 /* spiral arms — fewer, denser chains            */,
    armJitter: 0.12 /* angular scatter within an arm (rad)           */,
    armTwist: 1.7 /* arm curvature: theta advance per unit radius  */,
    cellK: 0.0725 /* cell = cellK * min(W,H)  (0.073 in reference) */,
    innerKX: 0.727 /* inner ellipse semi-x = innerKX * W/2          */,
    innerKY: 1.089 /* inner ellipse semi-y = innerKY * H/2          */,
    cornerK: 1.1 /* outer band reaches corner distance * cornerK  */,
    radialBias: 1.6 /* >1 packs clusters toward inner edge           */,
    dodgeFromMs: 1150 /* copy keep-out engages just before the fade    */,
    dodgePad: 0.4 /* clearance around copy, cells                  */,
    step: 110 /* quantized clock, ms                           */,
    holdMs: 320 /* dense pinwheel hold before burst              */,
    burstMs: 1500 /* per-cluster radial travel                     */,
    waveMs: 520 /* emanation wavefront (delay grows w/ radius)   */,
    jitterMs: 180 /* per-cluster delay jitter                      */,
    swirlMin: 0.65 /* rad unwound during burst                      */,
    swirlMax: 1.15,
    omega:
      (2 * Math.PI) / 140000 /* settled rotation: 1 rev / 140 s          */,
  };

  function mulberry32(a) {
    return function () {
      a |= 0;
      a = (a + 0x6d2b79f5) | 0;
      var t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  function pickWeighted(list, r) {
    var total = 0,
      i;
    for (i = 0; i < list.length; i++) total += list[i].w;
    var x = r * total;
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
  function buildField(seed, W, H, clearHalfX, clearHalfY, palette, place) {
    palette = palette || PALETTE;
    place = place || {};
    var rnd = mulberry32(seed);
    var minD = Math.min(W, H);
    var cell = Math.max(8, Math.round(minD * CFG.cellK));
    var rx = place.rx || (CFG.innerKX * W) / 2; /* inner ellipse semi-axes */
    var ry = place.ry || (CFG.innerKY * H) / 2;
    var fcx = place.cx != null ? place.cx : W / 2;
    var fcy = place.cy != null ? place.cy : H / 2;
    /* outer band pinned to the farthest viewport corner */
    var cW = Math.max(fcx, W - fcx) / rx,
      cH = Math.max(fcy, H - fcy) / ry;
    var rOuter = Math.sqrt(cW * cW + cH * cH) * CFG.cornerK;
    /* Each arm is a chain: members stratified along the radial band,
       tight angular scatter, strong shared twist — the arm stays
       legible through burst, settle, and rotation. */
    var perArm = Math.ceil(CFG.n / CFG.arms);
    var armSwirl = [];
    for (var a = 0; a < CFG.arms; a++)
      armSwirl.push(CFG.swirlMin + rnd() * (CFG.swirlMax - CFG.swirlMin));
    var clusters = [];
    for (var i = 0; i < CFG.n; i++) {
      var arm = i % CFG.arms;
      var member = Math.floor(i / CFG.arms);
      var sh = pickWeighted(SHAPES, rnd());
      var along = (member + rnd() * 0.7) / perArm; /* 0..1 along the arm */
      var rN = 1 + (rOuter - 1) * Math.pow(along, CFG.radialBias);
      var theta =
        arm * ((2 * Math.PI) / CFG.arms) +
        (rnd() - 0.5) * CFG.armJitter +
        (rN - 1) * CFG.armTwist; /* spiral curvature */
      var delay =
        CFG.holdMs +
        ((rN - 1) / (rOuter - 1)) * CFG.waveMs +
        rnd() * CFG.jitterMs;
      var swirl = armSwirl[arm] + (rnd() - 0.5) * 0.12;
      clusters.push({
        theta: theta,
        rFinal: rN,
        r0: ((0.2 + rnd() * 1.6) * cell) / Math.max(rx, ry),
        delay: delay,
        swirl: swirl,
        shape: sh,
        color: pickWeighted(palette, rnd()).hex,
      });
    }
    return {
      W: W,
      H: H,
      cell: cell,
      rx: rx,
      ry: ry,
      clusters: clusters,
      cx: fcx,
      cy: fcy,
      ccx: place.ccx != null ? place.ccx : fcx,
      ccy: place.ccy != null ? place.ccy : fcy,
      clear: clearHalfX
        ? {
            hx: clearHalfX + CFG.dodgePad * cell,
            hy: (clearHalfY || H * 0.13) + CFG.dodgePad * cell,
          }
        : null,
      settleAt: CFG.holdMs + CFG.waveMs + CFG.jitterMs + CFG.burstMs,
    };
  }

  function sampleField(field, tMs, hideHeld) {
    var t = Math.floor(tMs / CFG.step) * CFG.step; /* quantized clock */
    var cx = field.cx,
      cy = field.cy,
      cell = field.cell;
    var kx = field.ccx,
      ky = field.ccy;
    var rects = [];
    for (var i = 0; i < field.clusters.length; i++) {
      var c = field.clusters[i];
      if (hideHeld && t < c.delay) continue; /* appears at its own beat */
      var p = clamp01((t - c.delay) / CFG.burstMs);
      var e = easeOutQuart(p);
      var r = c.r0 + (c.rFinal - c.r0) * e;
      var spin = t > field.settleAt ? (t - field.settleAt) * CFG.omega : 0;
      var th = c.theta - c.swirl * (1 - e) + spin;
      var px = cx + r * Math.cos(th) * field.rx;
      var py = cy + r * Math.sin(th) * field.ry;
      /* snap so the shape's bbox is truly centered on the target */
      var gx = Math.round(px / cell - c.shape.bw / 2) * cell;
      var gy = Math.round(py / cell - c.shape.bh / 2) * cell;
      /* Copy keep-out: once the copy is up, a cluster whose snapped
         footprint would touch it steps outward, cell by cell, along
         its dominant radial axis, and flows back after passing. */
      if (field.clear && t >= CFG.dodgeFromMs) {
        var guard = 0;
        while (
          guard++ < 10 &&
          gx < kx + field.clear.hx &&
          gx + c.shape.bw * cell > kx - field.clear.hx &&
          gy < ky + field.clear.hy &&
          gy + c.shape.bh * cell > ky - field.clear.hy
        ) {
          var dx = Math.cos(th) * field.rx,
            dy = Math.sin(th) * field.ry;
          if (Math.abs(dx) >= Math.abs(dy)) gx += dx >= 0 ? cell : -cell;
          else gy += dy >= 0 ? cell : -cell;
        }
      }
      for (var k = 0; k < c.shape.cells.length; k++) {
        rects.push({
          x: gx + c.shape.cells[k][0] * cell,
          y: gy + c.shape.cells[k][1] * cell,
          w: cell,
          h: cell,
          color: c.color,
        });
      }
    }
    return rects;
  }

  return {
    buildField: buildField,
    sampleField: sampleField,
    CFG: CFG,
    PALETTE: PALETTE,
  };
}
