// Ported from LP studio/heroes/galaxy.html, final handoff 804c5fd.
// The seeded field and sampling math stay independent of the browser.
/**
 * @param {(name: string) => string} colorToken - Resolves a colour token name,
 *   such as `--color-accent-blue`, to its colour value.
 * @returns {{buildField: Function, sampleField: Function, CONFIG: object, PALETTE: {hex: string, weight: number}[]}}
 */
export function createGalaxyField(colorToken) {
  // Spectrum weights preserve LP's reference composition.
  const PALETTE = [
    {
      hex: colorToken("--color-spectrum-yellow-600"),
      weight: 30,
    },
    { hex: colorToken("--color-spectrum-cyan"), weight: 23 },
    {
      hex: colorToken("--color-spectrum-apricot"),
      weight: 10,
    },
    { hex: colorToken("--color-accent-blue"), weight: 10 },
    { hex: colorToken("--color-spectrum-crimson"), weight: 9 },
    { hex: colorToken("--color-accent-orange"), weight: 8 },
    { hex: colorToken("--color-card-pink"), weight: 7 },
    { hex: colorToken("--color-card-lime"), weight: 3 },
  ];

  /* Cluster shapes on the square grid; cells are offsets from the
     anchor and each shape carries its bounds so it can be centered. */
  function createClusterShape(weight, cells) {
    let maxX = 0,
      maxY = 0;
    for (let i = 0; i < cells.length; i++) {
      if (cells[i][0] > maxX) maxX = cells[i][0];
      if (cells[i][1] > maxY) maxY = cells[i][1];
    }
    const widthInCells = maxX + 1,
      heightInCells = maxY + 1; /* bounding box, cells */
    /* symmetric overhang past the true center per axis, in cells,
       incl. 0.5 cell grid-snap slop */
    return {
      weight,
      cells,
      widthInCells,
      heightInCells,
      halfWidthWithSnap: widthInCells / 2 + 0.5,
      halfHeightWithSnap: heightInCells / 2 + 0.5,
    };
  }
  const SHAPES = [
    createClusterShape(24, [[0, 0]]),
    createClusterShape(14, [
      [0, 0],
      [1, 0],
    ]),
    createClusterShape(14, [
      [0, 0],
      [0, 1],
    ]),
    createClusterShape(10, [
      [0, 0],
      [1, 0],
      [1, 1],
    ]),
    createClusterShape(10, [
      [0, 0],
      [0, 1],
      [1, 1],
    ]),
    createClusterShape(8, [
      [0, 0],
      [1, 0],
      [0, 1],
    ]),
    createClusterShape(6, [
      [0, 0],
      [1, 0],
      [2, 0],
    ]),
    createClusterShape(6, [
      [0, 0],
      [0, 1],
      [0, 2],
    ]),
    createClusterShape(8, [
      [0, 0],
      [1, 0],
      [0, 1],
      [1, 1],
    ]),
  ];

  const CONFIG = {
    clusterCount: 64 /* clusters */,
    arms: 8 /* spiral arms — fewer, denser chains */,
    armJitter: 0.12 /* angular scatter within an arm (rad) */,
    armTwist: 1.7 /* arm curvature: angle advance per unit radius */,
    cellSizeRatio: 0.0725 /* cellSize = cellSizeRatio * min(W,H)  (0.073 in reference) */,
    innerRadiusXRatio: 0.727 /* inner ellipse semi-x = innerRadiusXRatio * W/2 */,
    innerRadiusYRatio: 1.089 /* inner ellipse semi-y = innerRadiusYRatio * H/2 */,
    outerCornerScale: 1.1 /* outer band reaches corner distance * outerCornerScale */,
    radialBias: 1.6 /* >1 packs clusters toward inner edge */,
    headlineAvoidanceStartMs: 1150 /* copy keep-out engages just before the fade */,
    headlinePaddingCells: 0.4 /* clearance around copy, cells */,
    tickMs: 110 /* quantized clock, ms */,
    holdMs: 320 /* dense pinwheel hold before burst */,
    burstMs: 1500 /* per-cluster radial travel */,
    waveMs: 520 /* emanation wavefront (delay grows with radius) */,
    jitterMs: 180 /* per-cluster delay jitter */,
    swirlMin: 0.65 /* rad unwound during burst */,
    swirlMax: 1.15,
    rotationRadiansPerMs:
      (2 * Math.PI) / 140000 /* settled rotation: 1 rev / 140 s */,
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
  function pickWeighted(items, randomValue) {
    let totalWeight = 0;
    for (const item of items) totalWeight += item.weight;
    let remainingWeight = randomValue * totalWeight;
    for (const item of items) {
      remainingWeight -= item.weight;
      if (remainingWeight <= 0) return item;
    }
    return items[items.length - 1];
  }
  function easeOutQuart(t) {
    t = 1 - t;
    return 1 - t * t * t * t;
  }
  function clamp01(t) {
    return t < 0 ? 0 : t > 1 ? 1 : t;
  }

  /**
   * Build a repeatable arrangement once, then sample it at any animation time.
   * Width, height and headline half-sizes are CSS pixels. Placement overrides
   * the field/copy centers and inner ellipse radii, also in CSS pixels.
   * Keep random draws in order: changing their order changes the composition.
   *
   * @param {object} options
   * @param {number} options.seed
   * @param {number} options.width
   * @param {number} options.height
   * @param {number} [options.headlineHalfWidth] - Omit to skip headline avoidance.
   * @param {number} [options.headlineHalfHeight]
   * @param {{hex: string, weight: number}[]} [options.palette] - Defaults to PALETTE.
   * @param {{centerX?: number, centerY?: number, copyCenterX?: number, copyCenterY?: number, ellipseRadiusX?: number, ellipseRadiusY?: number}} [options.placement]
   * @returns {object} The field for sampleField(): its size, cell size,
   *   centres, clusters, headline bounds (or null) and `settledAtMs`.
   */
  function buildField({
    seed,
    width,
    height,
    headlineHalfWidth,
    headlineHalfHeight,
    palette = PALETTE,
    placement = {},
  }) {
    const random = mulberry32(seed);
    const shortSide = Math.min(width, height);
    const cellSize = Math.max(8, Math.round(shortSide * CONFIG.cellSizeRatio));
    const ellipseRadiusX =
      placement.ellipseRadiusX ||
      (CONFIG.innerRadiusXRatio * width) / 2; /* inner ellipse semi-axes */
    const ellipseRadiusY =
      placement.ellipseRadiusY || (CONFIG.innerRadiusYRatio * height) / 2;
    const fieldCenterX =
      placement.centerX != null ? placement.centerX : width / 2;
    const fieldCenterY =
      placement.centerY != null ? placement.centerY : height / 2;
    /* outer band pinned to the farthest viewport corner */
    const cornerRadiusX =
        Math.max(fieldCenterX, width - fieldCenterX) / ellipseRadiusX,
      cornerRadiusY =
        Math.max(fieldCenterY, height - fieldCenterY) / ellipseRadiusY;
    const outerRadius =
      Math.sqrt(cornerRadiusX * cornerRadiusX + cornerRadiusY * cornerRadiusY) *
      CONFIG.outerCornerScale;
    /* Each arm is a chain: members stratified along the radial band,
       tight angular scatter, strong shared twist — the arm stays
       legible through burst, settle, and rotation. */
    const clustersPerArm = Math.ceil(CONFIG.clusterCount / CONFIG.arms);
    const armSwirls = [];
    for (let a = 0; a < CONFIG.arms; a++)
      armSwirls.push(
        CONFIG.swirlMin + random() * (CONFIG.swirlMax - CONFIG.swirlMin),
      );
    const clusters = [];
    for (let i = 0; i < CONFIG.clusterCount; i++) {
      const arm = i % CONFIG.arms;
      const member = Math.floor(i / CONFIG.arms);
      const clusterShape = pickWeighted(SHAPES, random());
      const armProgress =
        (member + random() * 0.7) / clustersPerArm; /* 0..1 along the arm */
      const finalRadius =
        1 + (outerRadius - 1) * Math.pow(armProgress, CONFIG.radialBias);
      const angle =
        arm * ((2 * Math.PI) / CONFIG.arms) +
        (random() - 0.5) * CONFIG.armJitter +
        (finalRadius - 1) * CONFIG.armTwist; /* spiral curvature */
      const delayMs =
        CONFIG.holdMs +
        ((finalRadius - 1) / (outerRadius - 1)) * CONFIG.waveMs +
        random() * CONFIG.jitterMs;
      const swirl = armSwirls[arm] + (random() - 0.5) * 0.12;
      clusters.push({
        angle,
        finalRadius,
        initialRadius:
          ((0.2 + random() * 1.6) * cellSize) /
          Math.max(ellipseRadiusX, ellipseRadiusY),
        delayMs,
        swirl,
        shape: clusterShape,
        color: pickWeighted(palette, random()).hex,
      });
    }
    return {
      width,
      height,
      cellSize,
      ellipseRadiusX,
      ellipseRadiusY,
      clusters,
      centerX: fieldCenterX,
      centerY: fieldCenterY,
      copyCenterX:
        placement.copyCenterX != null ? placement.copyCenterX : fieldCenterX,
      copyCenterY:
        placement.copyCenterY != null ? placement.copyCenterY : fieldCenterY,
      headlineBounds: headlineHalfWidth
        ? {
            halfWidth:
              headlineHalfWidth + CONFIG.headlinePaddingCells * cellSize,
            halfHeight:
              (headlineHalfHeight || height * 0.13) +
              CONFIG.headlinePaddingCells * cellSize,
          }
        : null,
      settledAtMs:
        CONFIG.holdMs + CONFIG.waveMs + CONFIG.jitterMs + CONFIG.burstMs,
    };
  }

  // Move a snapped cluster outward until it clears the headline, at most
  // ten cells along its dominant radial axis. The limit is LP's original cap.
  function avoidHeadline(field, clusterShape, angle, tickTimeMs, gridX, gridY) {
    const { cellSize, copyCenterX, copyCenterY } = field;
    if (field.headlineBounds && tickTimeMs >= CONFIG.headlineAvoidanceStartMs) {
      let guard = 0;
      while (
        guard++ < 10 &&
        gridX < copyCenterX + field.headlineBounds.halfWidth &&
        gridX + clusterShape.widthInCells * cellSize >
          copyCenterX - field.headlineBounds.halfWidth &&
        gridY < copyCenterY + field.headlineBounds.halfHeight &&
        gridY + clusterShape.heightInCells * cellSize >
          copyCenterY - field.headlineBounds.halfHeight
      ) {
        const dx = Math.cos(angle) * field.ellipseRadiusX,
          dy = Math.sin(angle) * field.ellipseRadiusY;
        if (Math.abs(dx) >= Math.abs(dy))
          gridX += dx >= 0 ? cellSize : -cellSize;
        else gridY += dy >= 0 ? cellSize : -cellSize;
      }
    }
    return { gridX, gridY };
  }

  /**
   * Return ordered CSS-pixel rectangles without mutating the seeded field.
   *
   * @param {object} field - From buildField().
   * @param {number} elapsedMs - Time since the burst started.
   * @param {boolean} hideDelayedClusters - Skip clusters whose delay hasn't passed.
   * @returns {{x: number, y: number, w: number, h: number, color: string}[]}
   */
  function sampleField(field, elapsedMs, hideDelayedClusters) {
    const tickTimeMs =
      Math.floor(elapsedMs / CONFIG.tickMs) *
      CONFIG.tickMs; /* quantized clock */
    const centerX = field.centerX,
      centerY = field.centerY,
      cellSize = field.cellSize;
    const rects = [];
    for (let i = 0; i < field.clusters.length; i++) {
      const cluster = field.clusters[i];
      if (hideDelayedClusters && tickTimeMs < cluster.delayMs)
        continue; /* appears at its own beat */
      const burstProgress = clamp01(
        (tickTimeMs - cluster.delayMs) / CONFIG.burstMs,
      );
      const easedProgress = easeOutQuart(burstProgress);
      const radius =
        cluster.initialRadius +
        (cluster.finalRadius - cluster.initialRadius) * easedProgress;
      const rotation =
        tickTimeMs > field.settledAtMs
          ? (tickTimeMs - field.settledAtMs) * CONFIG.rotationRadiansPerMs
          : 0;
      const angle =
        cluster.angle - cluster.swirl * (1 - easedProgress) + rotation;
      const pixelX = centerX + radius * Math.cos(angle) * field.ellipseRadiusX;
      const pixelY = centerY + radius * Math.sin(angle) * field.ellipseRadiusY;
      /* snap so the shape's bbox is truly centered on the target */
      let gridX =
        Math.round(pixelX / cellSize - cluster.shape.widthInCells / 2) *
        cellSize;
      let gridY =
        Math.round(pixelY / cellSize - cluster.shape.heightInCells / 2) *
        cellSize;
      ({ gridX, gridY } = avoidHeadline(
        field,
        cluster.shape,
        angle,
        tickTimeMs,
        gridX,
        gridY,
      ));
      for (let k = 0; k < cluster.shape.cells.length; k++) {
        rects.push({
          x: gridX + cluster.shape.cells[k][0] * cellSize,
          y: gridY + cluster.shape.cells[k][1] * cellSize,
          w: cellSize,
          h: cellSize,
          color: cluster.color,
        });
      }
    }
    return rects;
  }

  return {
    buildField,
    sampleField,
    CONFIG,
    PALETTE,
  };
}
