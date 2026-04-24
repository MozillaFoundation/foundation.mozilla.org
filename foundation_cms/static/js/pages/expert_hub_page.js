import { forceSimulation, forceCollide, forceX, forceY } from "d3-force";
import { select } from "d3-selection";
import { timer } from "d3-timer";

// Golden angle for overflow phyllotaxis layout
const GOLDEN_ANGLE = Math.PI * (3 - Math.sqrt(5));

// ─── Seed positions (% of full container) ────────────────────────────────────
// Hand-tuned for the design composition: hero upper-center, others scattered
// to the right of the copy block. Only used for the first 12 nodes; beyond
// that, overflow nodes are placed via phyllotaxis in the available zone.
const TIER_CONFIG = [
  {
    tier: 1,
    positions: [[56, 55]],
  },
  {
    tier: 2,
    positions: [
      [37, 46],
      [60, 23],
      [78, 31],
      [92, 56],
      [76, 62],
      [22, 56],
    ],
  },
  {
    tier: 3,
    positions: [
      [16, 82],
      [93, 20],
      [64, 85],
      [34, 76],
      [7, 53],
    ],
  },
];

const SELECTORS = {
  viz: "#expert-hub-viz",
  bubble: "#expert-hub-bubble-list .expert-hub-bubble",
  copy: ".expert-hub-hero__copy",
  tooltipQuote: ".expert-hub-tooltip__quote",
  tooltipName: ".expert-hub-tooltip__name",
};

const CLASS_NAMES = {
  ready: "expert-hub-viz--ready",
  linesSvg: "expert-hub-viz__lines-svg",
  tooltip: "expert-hub-tooltip",
  overlayActive: "expert-hub-bubble--overlay-active",
  tier: (n) => `expert-hub-bubble--tier-${n}`,
};

const TIER_WEIGHT = { 1: 4, 2: 2, 3: 1 };

const TIER_BY_INDEX = TIER_CONFIG.flatMap(({ tier, positions }) =>
  positions.map((pos) => ({ tier, pos })),
);

const PACK_FACTOR = 0.3; // fraction of available area covered by bubble area

const FLOAT_RADIUS = [4, 9];           // [min, max] px orbit radius
const FLOAT_SPEED = [0.00025, 0.00045]; // [min, max] radians/ms
const FLOAT_Y_SPEED_RATIO = 0.65;       // y-axis drifts slower than x for elliptical motion

const COLLIDE_PADDING = 6;
const COLLIDE_STRENGTH = 0.9;
const COLLIDE_ITERATIONS = 3;
const ANCHOR_STRENGTH = 0.3;
const SIM_TICKS = 200;

const TOOLTIP_GAP = 12;
const TOOLTIP_EDGE_MARGIN = 8;
// Mirrors SCSS `@include breakpoint(large up)` — Foundation large = 64em
const VIZ_BREAKPOINT = "(min-width: 64em)";

/**
 * @param {number} min
 * @param {number} max
 * @returns {number}
 */
function randomFloat(min, max) {
  return min + Math.random() * (max - min);
}

/**
 * Returns the tier (1, 2, or 3) for node at index i.
 * Seeded nodes look up TIER_BY_INDEX; overflow nodes are assigned
 * proportionally (40% tier 2, 60% tier 3).
 *
 * @param {number} i - Node index (0-based)
 * @param {number} n - Total node count
 * @returns {1|2|3}
 */
function getTier(i, n) {
  if (i < TIER_BY_INDEX.length) return TIER_BY_INDEX[i].tier;
  const overflowIdx = i - TIER_BY_INDEX.length;
  const overflowCount = n - TIER_BY_INDEX.length;
  return overflowIdx < Math.round(overflowCount * 0.4) ? 2 : 3;
}

/**
 * Returns absolute [x, y] seed coordinates for node at index i.
 * Seeded nodes (i < 12) use the hand-tuned TIER_CONFIG percentage table.
 * Overflow nodes use a golden-angle phyllotaxis spiral centred in the
 * available zone to the right of the copy block.
 *
 * @param {number} i        - Node index (0-based)
 * @param {number} n        - Total node count
 * @param {number} zoneLeft - Left edge of the available zone (px), i.e. copy block right edge
 * @param {number} vizW     - Viz container width (px)
 * @param {number} vizH     - Viz container height (px)
 * @returns {[number, number]} [x, y] in px relative to the viz container
 */
function getSeedPosition(i, n, zoneLeft, vizW, vizH) {
  if (i < TIER_BY_INDEX.length) {
    const [xPct, yPct] = TIER_BY_INDEX[i].pos;
    return [(xPct / 100) * vizW, (yPct / 100) * vizH];
  }
  const zoneW = vizW - zoneLeft;
  const cx = zoneLeft + zoneW / 2;
  const cy = vizH / 2;
  const maxR = 0.38 * Math.min(zoneW, vizH);
  const overflowIdx = i - TIER_BY_INDEX.length;
  const overflowCount = n - TIER_BY_INDEX.length;
  const r = Math.sqrt((overflowIdx + 1) / overflowCount) * maxR;
  const θ = overflowIdx * GOLDEN_ANGLE;
  return [cx + r * Math.cos(θ), cy + r * Math.sin(θ)];
}

/**
 * Initialises the bubble viz inside the given container element.
 * Computes bubble sizes from available area, runs a static force simulation
 * to resolve collisions, then starts the float animation loop.
 *
 * @param {HTMLElement} viz - The `#expert-hub-viz` container element
 * @returns {() => void} Teardown function — stops the timer, removes the SVG,
 *   and resets all bubble styles so the viz can be re-initialised cleanly.
 */
function init(viz) {
  const vizRect = viz.getBoundingClientRect();
  const vizW = vizRect.width;
  const vizH = vizRect.height;

  const copyEl = viz.querySelector(SELECTORS.copy);
  const copyRect = copyEl ? copyEl.getBoundingClientRect() : null;
  const copyArea = copyRect ? copyRect.width * copyRect.height : 0;
  const availableArea = vizW * vizH - copyArea;
  const zoneLeft = copyRect ? copyRect.right - vizRect.left : vizW * 0.4;

  const els = Array.from(document.querySelectorAll(SELECTORS.bubble));
  const n = els.length;

  const totalWeightedUnits = els.reduce(
    (sum, _, i) => sum + TIER_WEIGHT[getTier(i, n)],
    0,
  );

  const areaPerUnit = (availableArea * PACK_FACTOR) / totalWeightedUnits;
  const tierRadius = {
    1: Math.sqrt((areaPerUnit * TIER_WEIGHT[1]) / Math.PI),
    2: Math.sqrt((areaPerUnit * TIER_WEIGHT[2]) / Math.PI),
    3: Math.sqrt((areaPerUnit * TIER_WEIGHT[3]) / Math.PI),
  };

  const svg = select(viz)
    .append("svg")
    .attr("class", CLASS_NAMES.linesSvg)
    .attr("width", vizW)
    .attr("height", vizH)
    .style("position", "absolute")
    .style("inset", "0")
    .style("pointer-events", "none");

  const linesGroup = svg.append("g");

  const tooltip = viz.querySelector(`.${CLASS_NAMES.tooltip}`);

  const nodes = els.map((el, i) => {
    const tier = getTier(i, n);
    const size = Math.round(tierRadius[tier] * 2);
    const [baseX, baseY] = getSeedPosition(i, n, zoneLeft, vizW, vizH);

    const topics = el.dataset.topics
      ? el.dataset.topics.split(",").map((t) => t.trim())
      : [];

    el.classList.add(CLASS_NAMES.tier(tier));
    el.style.width = `${size}px`;
    el.style.height = `${size}px`;
    el.style.position = "absolute";
    el.style.left = `${baseX}px`;
    el.style.top = `${baseY}px`;
    el.style.transform = "translate(-50%, -50%)";
    el.setAttribute("role", "button");
    el.setAttribute("tabindex", "0");

    return {
      el,
      tier,
      size,
      baseX,
      baseY,
      topics,
      index: i,
      quote: el.dataset.quote || "",
      name: el.dataset.name || "",
      floatR: randomFloat(...FLOAT_RADIUS),
      floatSpeed: randomFloat(...FLOAT_SPEED),
      phaseX: randomFloat(0, Math.PI * 2),
      phaseY: randomFloat(0, Math.PI * 2),
      cx: baseX,
      cy: baseY,
    };
  });

  // Resolve collisions with a static force sim
  const simNodes = nodes.map((node) => ({
    x: node.baseX,
    y: node.baseY,
    r: node.size / 2,
  }));

  forceSimulation(simNodes)
    .force(
      "collide",
      forceCollide((d) => d.r + COLLIDE_PADDING)
        .strength(COLLIDE_STRENGTH)
        .iterations(COLLIDE_ITERATIONS),
    )
    .force("x", forceX((_, i) => nodes[i].baseX).strength(ANCHOR_STRENGTH))
    .force("y", forceY((_, i) => nodes[i].baseY).strength(ANCHOR_STRENGTH))
    .stop()
    .tick(SIM_TICKS);

  simNodes.forEach((sn, i) => {
    nodes[i].baseX = sn.x;
    nodes[i].baseY = sn.y;
    nodes[i].cx = sn.x;
    nodes[i].cy = sn.y;
    nodes[i].el.style.left = `${sn.x}px`;
    nodes[i].el.style.top = `${sn.y}px`;
  });

  // ─── Tooltip ───────────────────────────────────────────────────────────────

  function positionTooltip(node) {
    const r = node.size / 2;
    const tipW = tooltip.offsetWidth;
    const tipH = tooltip.offsetHeight;

    let x = node.cx - tipW / 2;
    let y = node.cy - r - tipH - TOOLTIP_GAP;
    let tail = "bottom";

    if (y < TOOLTIP_EDGE_MARGIN) {
      y = node.cy + r + TOOLTIP_GAP;
      tail = "top";
    }

    x = Math.max(
      TOOLTIP_EDGE_MARGIN,
      Math.min(x, vizW - tipW - TOOLTIP_EDGE_MARGIN),
    );

    tooltip.style.left = `${x}px`;
    tooltip.style.top = `${y}px`;
    tooltip.dataset.tail = tail;
  }

  function showTooltip(node, color) {
    tooltip.style.setProperty("--tooltip-color", color);
    tooltip.querySelector(SELECTORS.tooltipQuote).textContent = node.quote;
    tooltip.querySelector(SELECTORS.tooltipName).textContent = `[${node.index + 1}] ${node.name}`;
    tooltip.removeAttribute("hidden");
    positionTooltip(node);
  }

  function hideTooltip() {
    tooltip.setAttribute("hidden", "");
  }

  // ─── Lines ─────────────────────────────────────────────────────────────────

  function updateLines(hoveredIndex) {
    if (hoveredIndex === null) {
      linesGroup.selectAll("line").data([]).join("line");
      return;
    }
    const hovered = nodes[hoveredIndex];
    const targets = nodes.filter((node, i) => {
      if (i === hoveredIndex) return false;
      return hovered.topics.some((t) => node.topics.includes(t));
    });

    linesGroup
      .selectAll("line")
      .data(targets, (d) => d.el) // key by DOM element — never misaligns
      .join("line")
      .attr("stroke", "#f06c13") // orange 300
      .attr("stroke-width", 1)
      .attr("x1", hovered.cx)
      .attr("y1", hovered.cy)
      .attr("x2", (d) => d.cx)
      .attr("y2", (d) => d.cy);
  }

  // ─── Overlays ──────────────────────────────────────────────────────────────

  function applyOverlays(sourceIndex, color) {
    nodes.forEach((node, i) => {
      if (i === sourceIndex) return;
      node.el.style.setProperty("--overlay-color", color);
      node.el.classList.add(CLASS_NAMES.overlayActive);
    });
  }

  function clearOverlays() {
    nodes.forEach((node) => {
      node.el.classList.remove(CLASS_NAMES.overlayActive);
      node.el.style.removeProperty("--overlay-color");
    });
  }

  // ─── Events ────────────────────────────────────────────────────────────────

  let hoverIndex = null;
  const ac = new AbortController();
  const { signal } = ac;

  nodes.forEach((node, i) => {
    node.el.addEventListener(
      "click",
      () => {
        window.location.href = node.el.dataset.url;
      },
      { signal },
    );

    node.el.addEventListener(
      "keydown",
      (e) => {
        if (e.key === "Enter" || e.key === " ") node.el.click();
      },
      { signal },
    );

    node.el.addEventListener(
      "mouseenter",
      () => {
        hoverIndex = i;
        const color = getComputedStyle(node.el)
          .getPropertyValue("--bubble-color")
          .trim();
        updateLines(i);
        applyOverlays(i, color);
        showTooltip(node, color);
      },
      { signal },
    );

    node.el.addEventListener(
      "mouseleave",
      () => {
        hoverIndex = null;
        updateLines(null);
        clearOverlays();
        hideTooltip();
      },
      { signal },
    );
  });

  // ─── Animation loop ────────────────────────────────────────────────────────

  const t = timer((elapsed) => {
    nodes.forEach((node) => {
      const dx =
        node.floatR * Math.sin(elapsed * node.floatSpeed + node.phaseX);
      const dy =
        node.floatR * Math.cos(elapsed * node.floatSpeed * FLOAT_Y_SPEED_RATIO + node.phaseY);

      node.cx = node.baseX + dx;
      node.cy = node.baseY + dy;
      node.el.style.transform = `translate(calc(-50% + ${dx}px), calc(-50% + ${dy}px))`;
    });

    if (hoverIndex !== null) {
      const hovered = nodes[hoverIndex];
      linesGroup
        .selectAll("line")
        .attr("x1", hovered.cx)
        .attr("y1", hovered.cy)
        .attr("x2", (d) => d.cx)
        .attr("y2", (d) => d.cy);
      positionTooltip(nodes[hoverIndex]);
    }
  });

  viz.classList.add(CLASS_NAMES.ready);

  // ─── Teardown ──────────────────────────────────────────────────────────────

  return () => {
    t.stop();
    ac.abort();
    svg.remove();
    tooltip.setAttribute("hidden", "");
    tooltip.style.removeProperty("--tooltip-color");
    viz.classList.remove(CLASS_NAMES.ready);
    nodes.forEach(({ el, tier }) => {
      el.removeAttribute("style");
      el.removeAttribute("role");
      el.removeAttribute("tabindex");
      el.classList.remove(CLASS_NAMES.tier(tier));
    });
  };
}

/**
 * Entry point. Queries the viz container, then starts and manages the viz
 * lifecycle via ResizeObserver — tearing down and re-initialising on resize
 * so layout measurements stay accurate. Only runs the viz when the viewport
 * matches VIZ_BREAKPOINT (large and up).
 */
function setup() {
  const viz = document.querySelector(SELECTORS.viz);
  if (!viz) return;

  let cleanup = null;
  let resizeTimer = null;

  function run() {
    if (cleanup) {
      cleanup();
      cleanup = null;
    }
    if (window.matchMedia(VIZ_BREAKPOINT).matches) {
      cleanup = init(viz);
    }
  }

  const ro = new ResizeObserver(() => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(run, 150);
  });

  ro.observe(viz);
  run();
}

setup();
