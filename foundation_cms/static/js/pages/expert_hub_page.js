import { forceSimulation, forceCollide, forceX, forceY } from "d3-force";
import { select } from "d3-selection";
import { timer } from "d3-timer";

const TIER_CONFIG = [
  {
    tier: 1,
    positions: [[57, 56]],
  },
  {
    tier: 2,
    positions: [
      [38, 48],
      [56, 23],
      [73, 33],
      [90, 52],
      [75, 62],
    ],
  },
  {
    tier: 3,
    positions: [
      [22, 58],
      [26, 82],
      [90, 20],
      [64, 85],
      [42, 76],
      [7, 55],
      [11, 81],
    ],
  },
];

const SELECTORS = {
  viz: "#expert-hub-viz",
  bubbleList: "#expert-hub-bubble-list",
  bubble: "#expert-hub-bubble-list .expert-hub-bubble",
  copy: ".expert-hub-hero__copy",
  linesSvg: "expert-hub-viz__lines-svg",
};

const CLASS_NAMES = {
  ready: "expert-hub-viz--ready",
  overlayActive: "expert-hub-bubble--overlay-active",
  tier: (n) => `expert-hub-bubble--tier-${n}`,
};

const TIER_WEIGHT = { 1: 2.5, 2: 1.5, 3: 1 };

const TIER_BY_INDEX = TIER_CONFIG.flatMap(({ tier, positions }) =>
  positions.map((pos) => ({ tier, pos })),
);

function computeTierBoundaries(n) {
  const remaining = n - 1;
  const tier2Count = Math.round(remaining * 0.4);
  return { tier2Count };
}

function getTier(i, n) {
  if (i < TIER_BY_INDEX.length) return TIER_BY_INDEX[i].tier;
  const { tier2Count } = computeTierBoundaries(n);
  if (i === 0) return 1;
  if (i <= tier2Count) return 2;
  return 3;
}

function getPosition(i) {
  return TIER_BY_INDEX[i]?.pos ?? [50, 50];
}

const PACK_DENSITY = 0.6;
const BUBBLE_SIZE_SCALE = 0.7;
const PACK_FACTOR = PACK_DENSITY * BUBBLE_SIZE_SCALE ** 2;

const FLOAT_RADIUS_MIN = 4;
const FLOAT_RADIUS_MAX = 9;
const FLOAT_SPEED_MIN = 0.00025;
const FLOAT_SPEED_MAX = 0.00045;

const COLLIDE_PADDING = 6;
const COLLIDE_STRENGTH = 0.9;
const COLLIDE_ITERATIONS = 3;
const ANCHOR_STRENGTH = 0.3;
const SIM_TICKS = 200;

function randomFloat(min, max) {
  return min + Math.random() * (max - min);
}

function init() {
  const viz = document.querySelector(SELECTORS.viz);
  if (!viz) return;

  const vizRect = viz.getBoundingClientRect();
  const vizW = vizRect.width;
  const vizH = vizRect.height;

  const copyEl = viz.querySelector(SELECTORS.copy);
  const copyRect = copyEl ? copyEl.getBoundingClientRect() : null;
  const copyArea = copyRect ? copyRect.width * copyRect.height : 0;
  const availableArea = vizW * vizH - copyArea;

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
    .attr("class", SELECTORS.linesSvg)
    .attr("width", vizW)
    .attr("height", vizH)
    .style("position", "absolute")
    .style("inset", "0")
    .style("pointer-events", "none");

  const linesGroup = svg.append("g");

  const nodes = els.map((el, i) => {
    const tier = getTier(i, n);
    const size = Math.round(tierRadius[tier] * 2);
    const [xPct, yPct] = getPosition(i);
    const baseX = (xPct / 100) * vizW;
    const baseY = (yPct / 100) * vizH;
    const topics = el.dataset.topics
      ? el.dataset.topics.split(",").map((t) => t.trim())
      : [];

    const floatR = randomFloat(FLOAT_RADIUS_MIN, FLOAT_RADIUS_MAX);
    const floatSpeed = randomFloat(FLOAT_SPEED_MIN, FLOAT_SPEED_MAX);
    const phaseX = randomFloat(0, Math.PI * 2);
    const phaseY = randomFloat(0, Math.PI * 2);

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
      floatR,
      floatSpeed,
      phaseX,
      phaseY,
      cx: baseX,
      cy: baseY,
    };
  });

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

  simNodes.forEach((sn, i) => {
    nodes[i].baseX = sn.x;
    nodes[i].baseY = sn.y;
    nodes[i].cx = sn.x;
    nodes[i].cy = sn.y;
    nodes[i].el.style.left = `${sn.x}px`;
    nodes[i].el.style.top = `${sn.y}px`;
  });

  let hoverIndex = null;

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
        .attr("stroke", "#f06c13") // color(orange, "300")
        .attr("stroke-width", 1)
        .style("opacity", 1);
    });
  }

  function clearLines() {
    linesGroup.selectAll("line").remove();
  }

  function applyOverlays(sourceIndex) {
    const color = getComputedStyle(nodes[sourceIndex].el)
      .getPropertyValue("--bubble-color")
      .trim();
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

  nodes.forEach((node, i) => {
    node.el.addEventListener("click", () => {
      window.location.href = node.el.dataset.url;
    });

    node.el.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") node.el.click();
    });

    node.el.addEventListener("mouseenter", () => {
      hoverIndex = i;
      drawLines(i);
      applyOverlays(i);
    });
    node.el.addEventListener("mouseleave", () => {
      hoverIndex = null;
      clearLines();
      clearOverlays();
    });
  });

  timer((elapsed) => {
    nodes.forEach((node) => {
      const dx =
        node.floatR * Math.sin(elapsed * node.floatSpeed + node.phaseX);
      const dy =
        node.floatR * Math.cos(elapsed * node.floatSpeed * 0.65 + node.phaseY);

      node.cx = node.baseX + dx;
      node.cy = node.baseY + dy;

      node.el.style.transform = `translate(calc(-50% + ${dx}px), calc(-50% + ${dy}px))`;
    });

    const displayIndex = hoverIndex;
    if (displayIndex !== null) {
      const hovered = nodes[displayIndex];
      linesGroup.selectAll("line").each(function (_, lineIdx) {
        const connectedLines = linesGroup.selectAll("line").nodes();
        const connectedNodes = nodes.filter((node, i) => {
          if (i === displayIndex) return false;
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

  viz.classList.add(CLASS_NAMES.ready);
}

// Only run the viz on large screens
const mediaQuery = window.matchMedia("(min-width: 64em)");
if (mediaQuery.matches) {
  init();
}
