import {
  forceSimulation,
  forceLink,
  forceManyBody,
  forceCollide,
} from "d3-force";
import { select } from "d3-selection";
import { drag } from "d3-drag";

const SELECTORS = {
  network: "#expertHubNetwork",
  dataEl: "#expertHubData",
};

const CLASS_NAMES = {
  ready: "is-ready",
  panLayer: "expert-hub-network__pan-layer",
  card: "expert-hub-card",
  cardActive: "is-active",
  cardFaded: "is-faded",
  topicTag: "expert-hub-topic-tag",
  cardInner: "expert-hub-card__inner",
  cardPhotoWrap: "expert-hub-card__photo-wrap",
  cardPhoto: "expert-hub-card__photo",
  cardInfo: "expert-hub-card__info",
  cardName: "expert-hub-card__name",
  cardTitle: "expert-hub-card__title",
  center: "expert-hub-center",
  svg: "expert-hub-network__svg",
  link: "expert-hub-link",
};

const CENTER_H = 172; // center block height in px, used for positioning
const NETWORK_H = 800; // fixed height of the simulation space in px
const LINK_STRENGTH = 0.25; // how strongly topic-anchor links pull person nodes toward their cluster
const COLLIDE_RADIUS = 140; // collision radius for person nodes to prevent overlap
const WARMUP_ALPHA = 0.005; // simulation alpha threshold below which warmup stops early
const WARMUP_MAX_TICKS = 300; // maximum synchronous ticks to run before showing the initial layout

// --- Pure helpers ---

function getInitials(name) {
  return name
    .split(" ")
    .map((w) => w[0])
    .join("")
    .slice(0, 2)
    .toUpperCase();
}

function createCardEl(node) {
  const el = document.createElement("div");
  el.className = CLASS_NAMES.card;
  el.innerHTML = `
    <div class="${CLASS_NAMES.cardInner}">
      <div class="${CLASS_NAMES.topicTag}">${node.topics[0]}</div>
      <div class="${CLASS_NAMES.cardPhotoWrap}">
        <div class="${CLASS_NAMES.cardPhoto}" style="background-color:${node.bg_color}">${getInitials(node.name)}</div>
      </div>
      <div class="${CLASS_NAMES.cardInfo}">
        <strong class="${CLASS_NAMES.cardName}">${node.name}</strong>
        <span class="${CLASS_NAMES.cardTitle}">${node.title}</span>
      </div>
    </div>
  `;
  return el;
}

function buildNodes(experts, allTopics, W, H, topicOrbitR) {
  return [
    { id: "center", type: "center", fx: W / 2, fy: H / 2 },
    ...allTopics.map((topic, i) => {
      const angle = (i / allTopics.length) * 2 * Math.PI - Math.PI / 2;
      return {
        id: `topic-${topic}`,
        type: "topic-anchor",
        label: topic,
        fx: W / 2 + topicOrbitR * Math.cos(angle),
        fy: H / 2 + topicOrbitR * Math.sin(angle),
      };
    }),
    ...experts.map((e, i) => {
      const anchorIdx = allTopics.indexOf(e.topics[0]);
      const angle = (anchorIdx / allTopics.length) * 2 * Math.PI - Math.PI / 2;
      const jitter = 20;
      return {
        id: `person-${i}`,
        type: "person",
        ...e,
        x:
          W / 2 +
          topicOrbitR * Math.cos(angle) +
          (Math.random() - 0.5) * jitter,
        y:
          H / 2 +
          topicOrbitR * Math.sin(angle) +
          (Math.random() - 0.5) * jitter,
      };
    }),
  ];
}

function buildLinks(experts) {
  return experts.map((e, i) => ({
    source: `person-${i}`,
    target: `topic-${e.topics[0]}`,
  }));
}

// --- Main ---

function initExpertHub() {
  const dataEl = document.querySelector(SELECTORS.dataEl);
  if (!dataEl) return;
  const experts = JSON.parse(dataEl.textContent);
  if (!experts.length) return;
  const container = document.querySelector(SELECTORS.network);
  if (!container) return;

  // Dimensions & force distances derived from the initial viewport
  const CARD_W = parseFloat(
    getComputedStyle(container).getPropertyValue("--expert-hub-card-width"),
  );
  const CENTER_W = parseFloat(
    getComputedStyle(container).getPropertyValue("--expert-hub-center-width"),
  );
  let W = container.clientWidth;
  const H = NETWORK_H;
  const containerH = container.clientHeight;
  const topicOrbitR = Math.min(W, containerH) * 0.28;
  const linkDistance = topicOrbitR * 0.6;
  const chargeStrength = -(topicOrbitR * 0.85);

  // Graph data
  const allTopics = [...new Set(experts.map((e) => e.topics[0]))].sort();
  const nodes = buildNodes(experts, allTopics, W, H, topicOrbitR);
  const links = buildLinks(experts);
  const personNodes = nodes.filter((n) => n.type === "person");
  const centerNode = nodes.find((n) => n.id === "center");

  // Pan layer: all visual elements live here so a single CSS translate pans everything
  const panLayerEl = document.createElement("div");
  panLayerEl.className = CLASS_NAMES.panLayer;
  container.appendChild(panLayerEl);
  let panX = 0;
  let panY = 0;

  // DOM setup
  const { svg, lineEls } = setupSVGLayer();
  const centerEl = setupCenterEl();
  const cardEls = personNodes.map((node) => {
    const el = createCardEl(node);
    panLayerEl.appendChild(el);
    return { node, el };
  });
  // Card height is measured from the DOM after rendering so it adapts to actual CSS dimensions.
  let cardH = cardEls[0]?.el.offsetHeight ?? 0;

  // Behaviors
  let selectedIdx = null;
  setupSelectionBehavior();
  const simulation = setupSimulation();
  setupDragBehavior();
  warmupAndStart();
  setupResizeObserver();

  // --- Tick & layout helpers ---

  function centerInViewport() {
    // Centre the settled bounding box vertically in the viewport.
    // Horizontal pan is omitted: the simulation is radially symmetric around W/2.
    let minY = Infinity,
      maxY = -Infinity;
    personNodes.forEach((n) => {
      minY = Math.min(minY, n.y - cardH / 2);
      maxY = Math.max(maxY, n.y + cardH / 2);
    });
    minY = Math.min(minY, centerNode.fy - CENTER_H / 2);
    maxY = Math.max(maxY, centerNode.fy + CENTER_H / 2);
    const bboxCY = (minY + maxY) / 2;
    panX = 0;
    panY = Math.round(containerH / 2 - bboxCY);
    panLayerEl.style.transform = `translate(${panX}px, ${panY}px)`;
  }

  function ticked() {
    lineEls.attr("x2", (d) => d.x).attr("y2", (d) => d.y);
    cardEls.forEach(({ node, el }) => {
      el.style.transform = `translate(${node.x - CARD_W / 2}px, ${node.y - cardH / 2}px)`;
    });
  }

  // --- Setup functions ---

  function setupSVGLayer() {
    // SVG layer for connection lines (person → center), lives inside pan layer
    const svg = select(panLayerEl)
      .append("svg")
      .attr("class", CLASS_NAMES.svg)
      .attr("width", W)
      .attr("height", H)
      .attr("aria-hidden", "true");

    const lineEls = svg
      .selectAll("line")
      .data(personNodes)
      .join("line")
      .attr("class", CLASS_NAMES.link)
      .attr("x1", centerNode.fx)
      .attr("y1", centerNode.fy);

    return { svg, lineEls };
  }

  function setupCenterEl() {
    // Center block (pre-rendered in the Django template, moved into the pan layer here)
    const el = document.getElementById("expertHubCenter");
    el.style.transform = `translate(${centerNode.fx - CENTER_W / 2}px, ${centerNode.fy - CENTER_H / 2}px)`;
    panLayerEl.appendChild(el);
    return el;
  }

  function clearSelection() {
    selectedIdx = null;
    cardEls.forEach(({ el }) =>
      el.classList.remove(CLASS_NAMES.cardActive, CLASS_NAMES.cardFaded),
    );
    lineEls.classed(CLASS_NAMES.cardFaded, false);
  }

  function selectCard(idx) {
    if (selectedIdx === idx) {
      clearSelection();
      return;
    }
    selectedIdx = idx;
    cardEls.forEach(({ el }, i) => {
      el.classList.toggle(CLASS_NAMES.cardActive, i === idx);
      el.classList.toggle(CLASS_NAMES.cardFaded, i !== idx);
    });
    lineEls.classed(CLASS_NAMES.cardFaded, (_d, i) => i !== idx);
  }

  function setupSelectionBehavior() {
    // Clicking a card fades all others; clicking again or the background clears it
    cardEls.forEach(({ el }, idx) =>
      el.addEventListener("click", () => selectCard(idx)),
    );
    container.addEventListener("click", (e) => {
      if (!e.target.closest(`.${CLASS_NAMES.card}`)) clearSelection();
    });
  }

  function setupSimulation() {
    return forceSimulation(nodes)
      .force(
        "link",
        forceLink(links)
          .id((d) => d.id)
          .distance(linkDistance)
          .strength(LINK_STRENGTH),
      )
      .force("charge", forceManyBody().strength(chargeStrength))
      .force(
        "collide",
        forceCollide((d) => {
          if (d.type === "person") return COLLIDE_RADIUS;
          if (d.type === "center") return CENTER_W / 2 + 20;
          return 0;
        }),
      )
      .on("tick", ticked);
  }

  function setupDragBehavior() {
    // Card drag: fixes node position on drag, releases on dragend
    const nodeDrag = drag()
      .on("start", (event, d) => {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
      })
      .on("drag", (event, d) => {
        d.fx = event.x;
        d.fy = event.y;
      })
      .on("end", (event, d) => {
        if (!event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
      });

    cardEls.forEach(({ node, el }) => select(el).datum(node).call(nodeDrag));
  }

  function warmupAndStart() {
    // Warm up synchronously so the initial render is already settled
    simulation.stop();
    let tick = 0;
    while (simulation.alpha() > WARMUP_ALPHA && tick < WARMUP_MAX_TICKS) {
      simulation.tick();
      tick++;
    }
    ticked();
    centerInViewport();
    simulation.restart();
    requestAnimationFrame(() => container.classList.add(CLASS_NAMES.ready));
  }

  function setupResizeObserver() {
    // Re-layout on width change (same pattern as gallery.js ResizeObserver)
    let lastW = W;
    new ResizeObserver((entries) => {
      const newW = entries[0].contentRect.width;
      if (newW === lastW) return;
      lastW = newW;
      W = newW;

      centerNode.fx = newW / 2;
      allTopics.forEach((topic, i) => {
        const angle = (i / allTopics.length) * 2 * Math.PI - Math.PI / 2;
        const anchor = nodes.find((n) => n.id === `topic-${topic}`);
        if (anchor) {
          anchor.fx = newW / 2 + topicOrbitR * Math.cos(angle);
          anchor.fy = H / 2 + topicOrbitR * Math.sin(angle);
        }
      });

      svg.attr("width", newW);
      lineEls.attr("x1", centerNode.fx).attr("y1", centerNode.fy);
      centerEl.style.transform = `translate(${centerNode.fx - CENTER_W / 2}px, ${centerNode.fy - CENTER_H / 2}px)`;

      simulation.alpha(0.3).restart();
      centerInViewport();
    }).observe(container);
  }
}

initExpertHub();
