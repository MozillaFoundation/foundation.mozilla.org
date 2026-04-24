import { forceSimulation, forceCollide, forceX, forceY } from "d3-force";
import { select } from "d3-selection";

// Golden angle for overflow phyllotaxis layout
const GOLDEN_ANGLE = Math.PI * (3 - Math.sqrt(5));

// ─── Breakpoints (match SCSS customized-settings.scss) ───────────────────────
const BREAKPOINTS = {
  large: 1024,
  xlarge: 1200,
};

// ─── Per-breakpoint starting positions (% of full container) ─────────────────
// Each config is hand-tuned for that viewport's available zone.
// Overflow nodes beyond the configured count use phyllotaxis in the right-of-copy zone.
const TIER_CONFIGS = {
  // ≥ 1200px
  xlarge: {
    packFactor: 0.3,
    tiers: [
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
          [22, 58],
        ],
      },
      {
        tier: 3,
        positions: [
          [22, 84],
          [93, 20],
          [64, 85],
          [36, 76],
          [7, 54],
          [8, 77],
        ],
      },
    ],
  },
  // 1024–1199px
  large: {
    packFactor: 0.25,
    tiers: [
      {
        tier: 1,
        positions: [[58, 49]],
      },
      {
        tier: 2,
        positions: [
          [37, 49],
          [60, 18],
          [78, 31],
          [92, 56],
          [76, 62],
          [23, 61],
        ],
      },
      {
        tier: 3,
        positions: [
          [22, 84],
          [93, 20],
          [62, 78],
          [40, 74],
          [7, 56],
          [8, 77],
        ],
      },
    ],
  },
};

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

const COLLIDE_PADDING = 6;
const COLLIDE_STRENGTH = 0.9;
const COLLIDE_ITERATIONS = 3;
const ANCHOR_STRENGTH = 0.3;
const SIM_TICKS = 200;

const TOOLTIP_GAP = -12;
const TOOLTIP_EDGE_MARGIN = 8;

/**
 * Returns the active breakpoint key for the current viewport,
 * or null for touch devices and viewports below 1024px (both use the mobile layout).
 *
 * @returns {"xlarge"|"large"|null}
 */
function getBreakpoint() {
  if (!window.matchMedia("(hover: hover) and (pointer: fine)").matches)
    return null;
  const w = window.innerWidth;
  if (w >= BREAKPOINTS.xlarge) return "xlarge";
  if (w >= BREAKPOINTS.large) return "large";
  return null;
}

/**
 * Returns the tier (1, 2, or 3) for node at index i.
 * Configured nodes look up tierByIndex; overflow nodes are assigned
 * proportionally (40% tier 2, 60% tier 3).
 *
 * @param {number} i           - Node index (0-based)
 * @param {number} n           - Total node count
 * @param {Array}  tierByIndex - Flattened position list for the active config
 * @returns {1|2|3}
 */
function getTier(i, n, tierByIndex) {
  if (i < tierByIndex.length) return tierByIndex[i].tier;
  const overflowIdx = i - tierByIndex.length;
  const overflowCount = n - tierByIndex.length;
  return overflowIdx < Math.round(overflowCount * 0.4) ? 2 : 3;
}

/**
 * Returns the absolute [x, y] starting position for node at index i.
 * Configured nodes use the per-breakpoint percentage table.
 * Overflow nodes use a golden-angle phyllotaxis spiral centred in the
 * available zone to the right of the copy block.
 *
 * @param {number} i           - Node index (0-based)
 * @param {number} n           - Total node count
 * @param {number} zoneLeft    - Left edge of available zone (px)
 * @param {number} vizW        - Viz container width (px)
 * @param {number} vizH        - Viz container height (px)
 * @param {Array}  tierByIndex - Flattened position list for the active config
 * @returns {[number, number]} [x, y] in px relative to the viz container
 */
function getInitialPosition(i, n, zoneLeft, vizW, vizH, tierByIndex) {
  if (i < tierByIndex.length) {
    const [xPct, yPct] = tierByIndex[i].pos;
    return [(xPct / 100) * vizW, (yPct / 100) * vizH];
  }
  const zoneW = vizW - zoneLeft;
  const cx = zoneLeft + zoneW / 2;
  const cy = vizH / 2;
  const maxR = 0.38 * Math.min(zoneW, vizH);
  const overflowIdx = i - tierByIndex.length;
  const overflowCount = n - tierByIndex.length;
  const r = Math.sqrt((overflowIdx + 1) / overflowCount) * maxR;
  const θ = overflowIdx * GOLDEN_ANGLE;
  return [cx + r * Math.cos(θ), cy + r * Math.sin(θ)];
}

/**
 * Initialises the bubble viz for the given breakpoint config.
 * Computes bubble sizes from available area, then runs a static force simulation
 * to resolve collisions.
 *
 * @param {HTMLElement} viz        - The `#expert-hub-viz` container element
 * @param {object}      tierConfig - TIER_CONFIGS entry for the active breakpoint
 * @returns {() => void} Teardown function — removes the SVG and resets all
 *   bubble styles so the viz can be re-initialised cleanly.
 */
function init(viz, tierConfig) {
  const { packFactor, tiers } = tierConfig;
  const tierByIndex = tiers.flatMap(({ tier, positions }) =>
    positions.map((pos) => ({ tier, pos })),
  );

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
    (sum, _, i) => sum + TIER_WEIGHT[getTier(i, n, tierByIndex)],
    0,
  );

  const areaPerUnit = (availableArea * packFactor) / totalWeightedUnits;
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
    const tier = getTier(i, n, tierByIndex);
    const size = Math.round(tierRadius[tier] * 2);
    const [baseX, baseY] = getInitialPosition(
      i,
      n,
      zoneLeft,
      vizW,
      vizH,
      tierByIndex,
    );

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

  nodes.forEach((node, i) => {
    node.el.style.animationDelay = `${i * 80}ms`;
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
    tooltip.querySelector(SELECTORS.tooltipName).textContent =
      `[${node.index + 1}] ${node.name}`;
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
        const style = getComputedStyle(node.el);
        const color = style.getPropertyValue("--bubble-color").trim();
        const tooltipColor = style
          .getPropertyValue("--bubble-color-light")
          .trim();
        updateLines(i);
        applyOverlays(i, color);
        showTooltip(node, tooltipColor);
      },
      { signal },
    );

    node.el.addEventListener(
      "mouseleave",
      () => {
        updateLines(null);
        clearOverlays();
        hideTooltip();
      },
      { signal },
    );
  });

  viz.classList.add(CLASS_NAMES.ready);

  // ─── Teardown ──────────────────────────────────────────────────────────────

  return () => {
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
 * so layout measurements stay accurate.
 *
 * The active breakpoint config is resolved on each run, so resizing across
 * a breakpoint boundary automatically picks up the right starting positions.
 * Touch devices and viewports below 1024px return null from getBreakpoint() and get no viz.
 */
export function setupViz() {
  const viz = document.querySelector(SELECTORS.viz);
  if (!viz) return;

  let cleanup = null;
  let resizeTimer = null;

  function run() {
    if (cleanup) {
      cleanup();
      cleanup = null;
    }
    const bp = getBreakpoint();
    if (bp) {
      cleanup = init(viz, TIER_CONFIGS[bp]);
    }
  }

  let initialFire = true;
  const ro = new ResizeObserver(() => {
    if (initialFire) {
      initialFire = false;
      return;
    }
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(run, 150);
  });

  ro.observe(viz);
  run();
}
