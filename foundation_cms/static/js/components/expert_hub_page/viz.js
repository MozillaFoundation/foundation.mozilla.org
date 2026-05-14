import { forceSimulation, forceCollide, forceX, forceY } from "d3-force";
import { select } from "d3-selection";
import { setupLightbox } from "./lightbox";
import { BREAKPOINTS, CONFIGS } from "./viz-configs";

// Golden angle for overflow phyllotaxis layout
const GOLDEN_ANGLE = Math.PI * (3 - Math.sqrt(5));

const SELECTORS = {
  viz: "#expert-hub-viz",
  hero: ".expert-hub-hero",
  bubbleList: "#expert-hub-bubble-list",
  bubble: "#expert-hub-bubble-list .expert-hub-bubble",
  copy: ".expert-hub-hero__copy",
  tooltipBlurb: ".expert-hub-tooltip__blurb",
  tooltipName: ".expert-hub-tooltip__name",
  card: "#expert-hub-card",
};

const CLASS_NAMES = {
  ready: "expert-hub-viz--ready",
  linesSvg: "expert-hub-viz__lines-svg",
  tooltip: "expert-hub-tooltip",
  overlayActive: "expert-hub-bubble--overlay-active",
  tier: (n) => `expert-hub-bubble--tier-${n}`,
};

const COLLIDE_PADDING = 6;
const COLLIDE_STRENGTH = 0.9;
const COLLIDE_ITERATIONS = 3;
const ANCHOR_STRENGTH = 0.3;
const SIM_TICKS = 200;

const TOOLTIP_GAP = -5;
const TOOLTIP_EDGE_MARGIN = 8;

const COMPUTED_HEIGHT_PADDING = 40;
// Fraction of the available zone's smaller dimension used as the spiral radius for overflow
// bubbles. 0.5 would place the outermost centre at the zone edge (clipping since bubbles
// have physical size); 0.38 was tuned visually to keep them clear of the edge.
const OVERFLOW_SPREAD = 0.38;
const LINES_STROKE_COLOR = "#f06c13"; // orange 300

const IS_TOUCH = !window.matchMedia("(hover: hover) and (pointer: fine)")
  .matches;

/**
 * Returns the active breakpoint key for the current viewport.
 *
 * @returns {"xl"|"lg"|"md"|"sm"}
 */
function getBreakpoint() {
  const w = window.innerWidth;
  if (w >= BREAKPOINTS.xl) return "xl";
  if (w >= BREAKPOINTS.lg) return "lg";
  if (w >= BREAKPOINTS.md) return "md";
  return "sm";
}

/**
 * Returns the tier for node at index i.
 * Configured nodes use tierByIndex; overflow nodes are tier 2 or 3 only
 * (40% tier 2, 60% tier 3).
 *
 * @param {number} i           - Node index (0-based)
 * @param {number} n           - Total node count
 * @param {Array}  tierByIndex - Flattened position list for the active config
 */
function getTier(i, n, tierByIndex) {
  if (i < tierByIndex.length) return tierByIndex[i].tier;
  const overflowIdx = i - tierByIndex.length;
  const overflowCount = n - tierByIndex.length;
  return overflowIdx < Math.round(overflowCount * 0.4) ? 2 : 3;
}

/**
 * Initialises the bubble viz for the given breakpoint config.
 * Computes bubble sizes from available area, then runs a static force simulation
 * to resolve collisions.
 *
 * @param {HTMLElement}      viz   - The `#expert-hub-viz` container element
 * @param {HTMLElement|null} hero  - The `.expert-hub-hero` wrapper; used to
 *   measure the copy block on desktop to determine the bubble placement zone
 * @param {object}           config - CONFIGS entry for the active breakpoint
 * @returns {() => void} Teardown function — removes the SVG and resets all
 *   bubble styles so the viz can be re-initialised cleanly.
 */
function init(viz, hero, config) {
  const { computeHeight, containerAspect, tierRadiusPercent, tiers } = config;
  const tierByIndex = tiers.flatMap(({ tier, positions }) =>
    positions.map((pos) => ({ tier, pos })),
  );

  const bubbleList = viz.querySelector(SELECTORS.bubbleList);
  const els = Array.from(viz.querySelectorAll(SELECTORS.bubble));
  const n = els.length;

  if (n === 0) {
    return () => {};
  }

  if (computeHeight && !bubbleList) {
    console.warn(
      "expert-hub viz: missing bubble list for computeHeight layout",
    );
    return () => {};
  }

  const vizRect = viz.getBoundingClientRect();
  const vizW = vizRect.width;

  // Mobile: set provisional height on the bubble list so positions can be
  // calculated before the sim resolves. Synchronous — browser never paints this.
  if (computeHeight) {
    bubbleList.style.height = `${vizW * containerAspect}px`;
  }
  const vizH = computeHeight ? vizW * containerAspect : vizRect.height;

  // On mobile the copy stacks above the viz in normal flow — no overlap to
  // subtract. On desktop the copy is absolutely positioned over the left of the
  // hero; measure it to find the right-hand zone where bubbles are placed.
  const copyEl = computeHeight
    ? null
    : (hero?.querySelector(SELECTORS.copy) ?? null);
  const copyRect = copyEl ? copyEl.getBoundingClientRect() : null;
  const zoneLeft = copyRect ? copyRect.right - vizRect.left : vizW * 0.4;

  const tierRadius = Object.fromEntries(
    Object.entries(tierRadiusPercent).map(([t, pct]) => [
      t,
      (pct / 100) * vizW,
    ]),
  );

  // Lines SVG is desktop-only; mobile has no tooltip or lines interaction.
  const svg = computeHeight
    ? null
    : select(viz)
        .append("svg")
        .attr("class", CLASS_NAMES.linesSvg)
        .attr("width", vizW)
        .attr("height", vizH);

  const linesGroup = svg ? svg.append("g") : null;

  const tooltip = viz.querySelector(`.${CLASS_NAMES.tooltip}`);
  const tooltipBlurb = tooltip?.querySelector(SELECTORS.tooltipBlurb);
  const tooltipName = tooltip?.querySelector(SELECTORS.tooltipName);
  const tooltipTailRaw = tooltip
    ? parseFloat(
        getComputedStyle(tooltip).getPropertyValue("--tooltip-tail-width"),
      )
    : NaN;
  const tooltipTailHalfWidth = Number.isFinite(tooltipTailRaw)
    ? tooltipTailRaw / 2
    : 6;
  const lightbox = setupLightbox(document.querySelector(SELECTORS.card));

  /**
   * Returns the absolute [x, y] starting position for node at index i.
   * Configured nodes use the per-breakpoint percentage table.
   * Overflow nodes use a golden-angle phyllotaxis spiral centred in the
   * available zone to the right of the copy block.
   *
   * @param {number} i - Node index (0-based)
   * @returns {[number, number]} [x, y] in px relative to the viz container
   */
  function getInitialPosition(i) {
    if (i < tierByIndex.length) {
      const [xPct, yPct] = tierByIndex[i].pos;
      return [(xPct / 100) * vizW, (yPct / 100) * vizH];
    }
    const zoneW = vizW - zoneLeft;
    const cx = zoneLeft + zoneW / 2;
    const cy = vizH / 2;
    const maxR = OVERFLOW_SPREAD * Math.min(zoneW, vizH);
    const overflowIdx = i - tierByIndex.length;
    const overflowCount = n - tierByIndex.length;
    const r = Math.sqrt((overflowIdx + 1) / overflowCount) * maxR;
    const θ = overflowIdx * GOLDEN_ANGLE;
    return [cx + r * Math.cos(θ), cy + r * Math.sin(θ)];
  }

  const nodes = els.map((el, i) => {
    const tier = getTier(i, n, tierByIndex);
    const size = Math.round(tierRadius[tier] * 2);
    const [baseX, baseY] = getInitialPosition(i);

    const topic = (el.dataset.topic ?? "").trim();

    el.classList.add(CLASS_NAMES.tier(tier));
    el.style.width = `${size}px`;
    el.style.height = `${size}px`;
    el.style.left = `${baseX}px`;
    el.style.top = `${baseY}px`;
    el.setAttribute("role", "button");
    el.setAttribute("tabindex", "0");
    const label = el.dataset.name?.trim();
    if (label) el.setAttribute("aria-label", label);

    return {
      el,
      tier,
      size,
      topic,
      blurb: el.dataset.blurb || "",
      name: el.dataset.name || "",
      cx: baseX,
      cy: baseY,
    };
  });

  // Resolve collisions with a static force sim
  const simNodes = nodes.map((node) => ({
    x: node.cx,
    y: node.cy,
    r: node.size / 2,
  }));

  forceSimulation(simNodes)
    .force(
      "collide",
      forceCollide((d) => d.r + COLLIDE_PADDING)
        .strength(COLLIDE_STRENGTH)
        .iterations(COLLIDE_ITERATIONS),
    )
    .force("x", forceX((_, i) => nodes[i].cx).strength(ANCHOR_STRENGTH))
    .force("y", forceY((_, i) => nodes[i].cy).strength(ANCHOR_STRENGTH))
    .stop()
    .tick(SIM_TICKS);

  simNodes.forEach((sn, i) => {
    nodes[i].cx = sn.x;
    nodes[i].cy = sn.y;
    nodes[i].el.style.left = `${sn.x}px`;
    nodes[i].el.style.top = `${sn.y}px`;
    nodes[i].el.style.animationDelay = `${i * 80}ms`;
  });

  // Mobile: snap bubble list height to actual bubble extents
  if (computeHeight && simNodes.length > 0) {
    const maxBottom = Math.max(...simNodes.map((sn) => sn.y + sn.r));
    bubbleList.style.height = `${maxBottom + COMPUTED_HEIGHT_PADDING}px`;
  }

  // ─── Tooltip ───────────────────────────────────────────────────────────────

  function positionTooltip(node) {
    if (!tooltip) return;
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

    // Align tail with bubble centre, clamped so it stays within the tooltip
    const tailRight = tipW - (node.cx - x) - tooltipTailHalfWidth;
    const tailRightClamped = Math.max(
      tooltipTailHalfWidth,
      Math.min(tailRight, tipW - tooltipTailHalfWidth * 3),
    );

    tooltip.style.left = `${x}px`;
    tooltip.style.top = `${y}px`;
    tooltip.style.setProperty("--tooltip-tail-right", `${tailRightClamped}px`);
    tooltip.dataset.tail = tail;
  }

  function showTooltip(node, color) {
    if (!tooltip || !tooltipBlurb || !tooltipName) return;
    tooltip.style.setProperty("--tooltip-color", color);
    tooltipBlurb.textContent = node.blurb;
    tooltipName.textContent = node.name;
    tooltip.removeAttribute("hidden");
    positionTooltip(node);
  }

  function hideTooltip() {
    tooltip?.setAttribute("hidden", "");
  }

  // ─── Lines ─────────────────────────────────────────────────────────────────

  function clearLines() {
    updateLines(null);
  }

  function updateLines(hoveredIndex) {
    if (!linesGroup) return;
    if (hoveredIndex === null) {
      linesGroup.selectAll("line").data([]).join("line");
      return;
    }
    const hovered = nodes[hoveredIndex];
    const targets = nodes.filter((node, i) => {
      if (i === hoveredIndex) return false;
      return (
        Boolean(hovered.topic) &&
        Boolean(node.topic) &&
        hovered.topic === node.topic
      );
    });

    linesGroup
      .selectAll("line")
      .data(targets, (d) => d.el) // key by DOM element — never misaligns
      .join("line")
      .attr("stroke", LINES_STROKE_COLOR)
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
        if (IS_TOUCH) {
          lightbox?.open(node.el);
        } else {
          window.location.href = node.el.dataset.url;
        }
      },
      { signal },
    );

    node.el.addEventListener(
      "keydown",
      (e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          node.el.click();
        }
      },
      { signal },
    );
  });

  if (!computeHeight) {
    let hideTimer = null;

    nodes.forEach((node, i) => {
      node.el.addEventListener(
        "mouseenter",
        () => {
          clearTimeout(hideTimer);
          const style = getComputedStyle(node.el);
          const color = style.getPropertyValue("--bubble-color").trim();
          const tooltipColor = style
            .getPropertyValue("--bubble-color-light")
            .trim();
          updateLines(i);
          applyOverlays(i, color);
          if (node.blurb) showTooltip(node, tooltipColor);
        },
        { signal },
      );

      node.el.addEventListener(
        "mouseleave",
        () => {
          hideTimer = setTimeout(() => {
            clearLines();
            clearOverlays();
            hideTooltip();
          }, 80);
        },
        { signal },
      );
    });
  }

  if (IS_TOUCH && lightbox) {
    lightbox.bindListeners(signal);
  }

  viz.classList.add(CLASS_NAMES.ready);

  // ─── Teardown ──────────────────────────────────────────────────────────────

  return () => {
    ac.abort();
    svg?.remove();
    if (tooltip) {
      tooltip.setAttribute("hidden", "");
      tooltip.style.removeProperty("--tooltip-color");
      tooltip.style.removeProperty("--tooltip-tail-right");
      delete tooltip.dataset.tail;
    }
    lightbox?.close();
    viz.classList.remove(CLASS_NAMES.ready);
    if (computeHeight) {
      bubbleList.style.removeProperty("height");
    }
    nodes.forEach(({ el, tier }) => {
      el.removeAttribute("style");
      el.removeAttribute("role");
      el.removeAttribute("tabindex");
      el.removeAttribute("aria-label");
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
 */
export function setupViz() {
  const viz = document.querySelector(SELECTORS.viz);
  if (!viz) return;
  const hero = viz.closest(SELECTORS.hero);

  let cleanup = null;
  let resizeTimer = null;

  function run() {
    if (cleanup) {
      cleanup();
      cleanup = null;
    }
    const bp = getBreakpoint();
    cleanup = init(viz, hero, CONFIGS[bp]);
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

  const root = document.documentElement;
  const updateParallax = () => {
    const y = window.scrollY;
    root.style.setProperty("--parallax-y-left", `${y * 0.3}px`);
    root.style.setProperty("--parallax-y-right", `${y * 0.5}px`);
  };
  window.addEventListener("scroll", updateParallax, { passive: true });
  updateParallax();
}
