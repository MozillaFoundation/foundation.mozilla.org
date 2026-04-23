import { forceSimulation, forceCollide, forceX, forceY } from "d3-force";
import { select } from "d3-selection";
import { timer } from "d3-timer";

// Tier configuration — defines how many bubbles each tier holds and their
// predefined [x%, y%] positions (center, relative to stage).
// Top-left is reserved for intro copy (roughly x<35% AND y<65%).
// To add a new tier: add an entry here and update TIER_WEIGHT below.
const TIER_CONFIG = [
  {
    tier: 1,
    positions: [
      [57, 56], // center-right
    ],
  },
  {
    tier: 2,
    positions: [
      [38, 48], // upper-left of viz (just right of copy)
      [56, 23], // upper-center
      [73, 33], // right-center
      [90, 52], // far-right
      [75, 62], // lower-right
    ],
  },
  {
    tier: 3,
    positions: [
      [22, 58], // left, below copy block
      [26, 82], // lower-left
      [90, 20], // upper-far-right
      [64, 85], // lower-center
      [42, 76], // center-lower
      [7, 55], // far lower-left
      [11, 81], // bottom-left
    ],
  },
];

const SELECTORS = {
  stage: "#ehbStage",
  bubbleList: "#ehbBubbleList",
  bubble: "#ehbBubbleList .ehb-bubble",
  copy: ".ehb-hero__copy",
  bubbleInitials: ".ehb-bubble__initials",
  linesSvg: "ehb-stage__lines-svg",
};

const CLASS_NAMES = {
  ready: "ehb-stage--ready",
  active: "ehb-bubble--active",
  tier: (n) => `ehb-bubble--tier-${n}`,
};

// Area weight per tier — controls relative bubble size.
// tier-1 gets 3× the circle area of a tier-3 bubble.
const TIER_WEIGHT = { 1: 2.5, 2: 1.5, 3: 1 };

// Derive tier lookup and flat position list from TIER_CONFIG.
// Each bubble index maps to a tier and a position within that tier's list.
const TIER_BY_INDEX = TIER_CONFIG.flatMap(({ tier, positions }) =>
  positions.map((pos) => ({ tier, pos })),
);

// Given n experts (6–13), compute how many belong to each tier.
// Always 1 tier-1 (featured). Remaining split ~40% tier-2, ~60% tier-3.
// Falls back to the last defined tier for any index beyond TIER_BY_INDEX.
function computeTierBoundaries(n) {
  const remaining = n - 1;
  const tier2Count = Math.round(remaining * 0.4);
  return { tier2Count };
}

function getTier(i, n) {
  // If explicit positions exist for this index, use them.
  if (i < TIER_BY_INDEX.length) return TIER_BY_INDEX[i].tier;
  // Otherwise derive tier from dynamic boundaries.
  const { tier2Count } = computeTierBoundaries(n);
  if (i === 0) return 1;
  if (i <= tier2Count) return 2;
  return 3;
}

function getPosition(i) {
  return TIER_BY_INDEX[i]?.pos ?? [50, 50];
}

// What fraction of the available (non-copy) stage area the bubbles should
// collectively occupy.
const PACK_DENSITY = 0.6;
// Scale factor applied to bubble diameters (0.8 = 80% of base size; area scales by 0.8² = 0.64).
const BUBBLE_SIZE_SCALE = 0.7;
const PACK_FACTOR = PACK_DENSITY * BUBBLE_SIZE_SCALE ** 2;

// Float animation — gentle sine/cosine drift applied to each bubble every frame.
const FLOAT_RADIUS_MIN = 4; // px — minimum drift distance
const FLOAT_RADIUS_MAX = 9; // px — maximum drift distance
const FLOAT_SPEED_MIN = 0.00025; // radians/ms — slowest oscillation
const FLOAT_SPEED_MAX = 0.00045; // radians/ms — fastest oscillation

// Collision resolution simulation settings
const COLLIDE_PADDING = 6; // px — minimum gap between bubble edges
const COLLIDE_STRENGTH = 0.9; // how aggressively overlaps are resolved (0–1)
const COLLIDE_ITERATIONS = 3; // collision constraint iterations per tick
const ANCHOR_STRENGTH = 0.3; // how strongly bubbles are pulled back toward their target position
const SIM_TICKS = 200; // synchronous ticks to run before first paint

function getInitials(name) {
  return name
    .split(" ")
    .map((w) => w[0])
    .join("")
    .slice(0, 2)
    .toUpperCase();
}

function randomFloat(min, max) {
  return min + Math.random() * (max - min);
}

function init() {
  const stage = document.querySelector(SELECTORS.stage);
  if (!stage) return;

  const stageRect = stage.getBoundingClientRect();
  const stageW = stageRect.width;
  const stageH = stageRect.height;

  // Subtract the copy block's footprint from available area
  const copyEl = stage.querySelector(SELECTORS.copy);
  const copyRect = copyEl ? copyEl.getBoundingClientRect() : null;
  const copyArea = copyRect ? copyRect.width * copyRect.height : 0;
  const availableArea = stageW * stageH - copyArea;

  // Build node elements once — reused below for both size calc and node mapping
  const els = Array.from(document.querySelectorAll(SELECTORS.bubble));
  const n = els.length;

  // Total weighted units across all bubbles
  const totalWeightedUnits = els.reduce(
    (sum, _, i) => sum + TIER_WEIGHT[getTier(i, n)],
    0,
  );

  // Area per unit weight, scaled by pack factor
  const areaPerUnit = (availableArea * PACK_FACTOR) / totalWeightedUnits;

  // Radius for each tier: r = √(areaPerUnit × weight / π)
  const tierRadius = {
    1: Math.sqrt((areaPerUnit * TIER_WEIGHT[1]) / Math.PI),
    2: Math.sqrt((areaPerUnit * TIER_WEIGHT[2]) / Math.PI),
    3: Math.sqrt((areaPerUnit * TIER_WEIGHT[3]) / Math.PI),
  };

  // SVG overlay for connection lines — sits below the bubbles
  const svg = select(stage)
    .append("svg")
    .attr("class", SELECTORS.linesSvg)
    .attr("width", stageW)
    .attr("height", stageH)
    .style("position", "absolute")
    .style("inset", "0")
    .style("pointer-events", "none");

  const linesGroup = svg.append("g");

  // Build node data from existing <li> elements
  const nodes = els.map((el, i) => {
    const tier = getTier(i, n);
    const size = Math.round(tierRadius[tier] * 2);
    const [xPct, yPct] = getPosition(i);
    const baseX = (xPct / 100) * stageW;
    const baseY = (yPct / 100) * stageH;
    const name = el.dataset.name ?? "";
    const topics = el.dataset.topics
      ? el.dataset.topics.split(",").map((t) => t.trim())
      : [];

    // Unique float params per bubble
    const floatR = randomFloat(FLOAT_RADIUS_MIN, FLOAT_RADIUS_MAX);
    const floatSpeed = randomFloat(FLOAT_SPEED_MIN, FLOAT_SPEED_MAX);
    const phaseX = randomFloat(0, Math.PI * 2);
    const phaseY = randomFloat(0, Math.PI * 2);

    // Apply static styles
    el.classList.add(CLASS_NAMES.tier(tier));
    el.style.width = `${size}px`;
    el.style.height = `${size}px`;
    el.style.backgroundColor = el.dataset.bgColor;
    el.style.position = "absolute";
    // left/top set once as the static base position; float drift is applied
    // via transform only so the browser can handle it on the compositor thread
    // without triggering layout recalculation every frame.
    el.style.left = `${baseX}px`;
    el.style.top = `${baseY}px`;
    el.style.transform = "translate(-50%, -50%)";

    const initialsEl = el.querySelector(SELECTORS.bubbleInitials);
    if (initialsEl) initialsEl.textContent = getInitials(name);

    el.setAttribute("role", "button");
    el.setAttribute("tabindex", "0");

    return {
      el,
      tier,
      size,
      baseX,
      baseY,
      topics,
      floatR,
      floatSpeed,
      phaseX,
      phaseY,
      // mutable current position (updated each frame)
      cx: baseX,
      cy: baseY,
    };
  });

  // ── Collision resolution — nudges baseX/baseY so bubbles don't overlap ──
  // Run synchronously to completion before first paint.
  const simNodes = nodes.map((n) => ({
    x: n.baseX,
    y: n.baseY,
    r: n.size / 2,
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

  // Write settled positions back as the new base positions
  simNodes.forEach((sn, i) => {
    nodes[i].baseX = sn.x;
    nodes[i].baseY = sn.y;
    nodes[i].cx = sn.x;
    nodes[i].cy = sn.y;
    // Update left/top to the post-sim base — only written here, not in the
    // animation loop.
    nodes[i].el.style.left = `${sn.x}px`;
    nodes[i].el.style.top = `${sn.y}px`;
  });

  // ── Topic connection lines ──────────────────────────────────────────────

  let activeIndex = null;

  function drawLines(hoveredIndex) {
    linesGroup.selectAll("line").remove();

    const hovered = nodes[hoveredIndex];
    if (!hovered) return;

    nodes.forEach((node, i) => {
      if (i === hoveredIndex) return;
      const shared = hovered.topics.filter((t) => node.topics.includes(t));
      if (shared.length === 0) return;

      linesGroup
        .append("line")
        .attr("x1", hovered.cx)
        .attr("y1", hovered.cy)
        .attr("x2", node.cx)
        .attr("y2", node.cy)
        .attr("stroke", "rgba(0,0,0,0.35)")
        .attr("stroke-width", 1.5)
        .attr("stroke-dasharray", "5,4")
        .style("opacity", 1);
    });
  }

  function clearLines() {
    linesGroup.selectAll("line").remove();
  }

  nodes.forEach((node, i) => {
    node.el.addEventListener("click", () => {
      if (activeIndex === i) {
        // clicking the active bubble deselects it
        activeIndex = null;
        node.el.classList.remove(CLASS_NAMES.active);
        clearLines();
      } else {
        if (activeIndex !== null) {
          nodes[activeIndex].el.classList.remove(CLASS_NAMES.active);
        }
        activeIndex = i;
        node.el.classList.add(CLASS_NAMES.active);
        drawLines(i);
      }
    });

    node.el.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") node.el.click();
    });

    // Scale is set via el.style.scale (individual transform property) so it
    // composes with the JS-driven transform on el.style.transform without
    // overwriting it.
    node.el.addEventListener("mouseenter", () => { node.el.style.scale = "1.06"; });
    node.el.addEventListener("mouseleave", () => { node.el.style.scale = ""; });
  });

  // ── Float animation ─────────────────────────────────────────────────────

  timer((elapsed) => {
    nodes.forEach((node) => {
      const dx =
        node.floatR * Math.sin(elapsed * node.floatSpeed + node.phaseX);
      const dy =
        node.floatR * Math.cos(elapsed * node.floatSpeed * 0.65 + node.phaseY);

      node.cx = node.baseX + dx;
      node.cy = node.baseY + dy;

      // Compositor-only update — no layout recalculation triggered.
      node.el.style.transform = `translate(calc(-50% + ${dx}px), calc(-50% + ${dy}px))`;
    });

    // Keep connection lines tracking the moving bubbles
    if (activeIndex !== null) {
      const hovered = nodes[activeIndex];
      linesGroup.selectAll("line").each(function (_, lineIdx) {
        // Find which target node this line connects to by DOM order
        const connectedLines = linesGroup.selectAll("line").nodes();
        const connectedNodes = nodes.filter((node, i) => {
          if (i === activeIndex) return false;
          return hovered.topics.some((t) => node.topics.includes(t));
        });

        const lineEl = connectedLines[lineIdx];
        const targetNode = connectedNodes[lineIdx];
        if (lineEl && targetNode) {
          select(lineEl)
            .attr("x1", hovered.cx)
            .attr("y1", hovered.cy)
            .attr("x2", targetNode.cx)
            .attr("y2", targetNode.cy);
        }
      });
    }
  });

  stage.classList.add(CLASS_NAMES.ready);
}

init();
