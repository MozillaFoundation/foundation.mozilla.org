import { forceSimulation, forceCollide, forceX, forceY } from "d3-force";
import { select } from "d3-selection";
import { drag } from "d3-drag";

const SELECTORS = {
  network: "#expertHubNetwork",
  dataEl: "#expertHubData",
};

const CLASS_NAMES = {
  ready: "is-ready",
  layer: "expert-hub-network__layer",
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

const NETWORK_H = 800; // fixed height of the simulation space in px
const CLUSTER_STRENGTH = 0.4; // how strongly forceX/Y pulls each person directly toward their topic anchor position
// Orbit radius multipliers per topic, cycling if there are more topics than entries.
// Vary these to control how much edge-length variety there is (1.0 = base topicOrbitR).
const ORBIT_FACTORS = [1.6, 1.3, 1.4, 0.8, 1.8, 1.8, 0.85];
const COLLIDE_RADIUS = 100; // collision radius for person nodes to prevent overlap
const EDGE_PADDING = 16; // min px between bounding box and container edges
const GOLDEN_ANGLE = 2.399963; // radians ≈ 137.5° — spaces anchors so the layout never looks like a regular polygon
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
      // Golden angle spacing breaks the equal-angular-interval look that makes radial
      // layouts feel circular even when radii vary.
      const angle = i * GOLDEN_ANGLE;
      const r = topicOrbitR * ORBIT_FACTORS[i % ORBIT_FACTORS.length];
      return {
        id: `topic-${topic}`,
        type: "topic-anchor",
        label: topic,
        fx: W / 2 + r * Math.cos(angle),
        fy: H / 2 + r * Math.sin(angle),
      };
    }),
    ...experts.map((e, i) => {
      const anchorIdx = allTopics.indexOf(e.topics[0]);
      const angle = anchorIdx * GOLDEN_ANGLE;
      const r = topicOrbitR * ORBIT_FACTORS[anchorIdx % ORBIT_FACTORS.length];
      const jitter = 20;
      return {
        id: `person-${i}`,
        type: "person",
        ...e,
        x: W / 2 + r * Math.cos(angle) + (Math.random() - 0.5) * jitter,
        y: H / 2 + r * Math.sin(angle) + (Math.random() - 0.5) * jitter,
      };
    }),
  ];
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
  const topicOrbitR = Math.min(W, containerH) * 0.38;

  // Graph data
  const allTopics = [...new Set(experts.map((e) => e.topics[0]))].sort();
  const nodes = buildNodes(experts, allTopics, W, H, topicOrbitR);
  const personNodes = nodes.filter((n) => n.type === "person");
  const centerNode = nodes.find((n) => n.id === "center");

  // Layer div: holds cards and SVG so a single transform centres the whole graph vertically
  const layerEl = document.createElement("div");
  layerEl.className = CLASS_NAMES.layer;
  container.appendChild(layerEl);

  // DOM setup
  const { svg, lineEls } = setupSVGLayer();
  const centerEl = setupCenterEl();
  // Heights are measured from the DOM after rendering so they adapt to actual CSS dimensions.
  const CENTER_H = centerEl.offsetHeight;
  centerEl.style.transform = `translate(${centerNode.fx - CENTER_W / 2}px, ${centerNode.fy - CENTER_H / 2}px)`;
  const cardEls = personNodes.map((node) => {
    const el = createCardEl(node);
    layerEl.appendChild(el);
    return { node, el };
  });
  const cardH = cardEls[0]?.el.offsetHeight ?? 0;

  // Behaviors
  let selectedIdx = null;
  setupSelectionBehavior();
  const simulation = setupSimulation();
  warmupAndStart();
  setupDragBehavior();
  setupResizeObserver();

  // --- Tick & layout helpers ---

  function centerInViewport() {
    // Centre the settled bounding box both horizontally and vertically in the viewport
    // so no cards are clipped by overflow: hidden.
    let minX = Infinity,
      maxX = -Infinity,
      minY = Infinity,
      maxY = -Infinity;
    personNodes.forEach((n) => {
      minX = Math.min(minX, n.x - CARD_W / 2);
      maxX = Math.max(maxX, n.x + CARD_W / 2);
      minY = Math.min(minY, n.y - cardH / 2);
      maxY = Math.max(maxY, n.y + cardH / 2);
    });
    minX = Math.min(minX, centerNode.fx - CENTER_W / 2);
    maxX = Math.max(maxX, centerNode.fx + CENTER_W / 2);
    minY = Math.min(minY, centerNode.fy - CENTER_H / 2);
    maxY = Math.max(maxY, centerNode.fy + CENTER_H / 2);
    const bboxW = maxX - minX;
    const bboxH = maxY - minY;
    const availW = W - EDGE_PADDING * 2;
    const availH = containerH - EDGE_PADDING * 2;
    // Scale down only if the bbox is larger than the available area; never scale up
    const scale = Math.min(1, availW / bboxW, availH / bboxH);
    // Centre the scaled bbox in the container
    const offsetX = Math.round(W / 2 - ((minX + maxX) / 2) * scale);
    const offsetY = Math.round(containerH / 2 - ((minY + maxY) / 2) * scale);
    layerEl.style.transform = `translate(${offsetX}px, ${offsetY}px) scale(${scale})`;
  }

  function ticked() {
    lineEls.attr("x2", (d) => d.x).attr("y2", (d) => d.y);
    cardEls.forEach(({ node, el }) => {
      el.style.transform = `translate(${node.x - CARD_W / 2}px, ${node.y - cardH / 2}px)`;
    });
    centerInViewport();
  }

  // --- Setup functions ---

  function setupSVGLayer() {
    // SVG layer for connection lines (person → center), lives inside the layer div
    const svg = select(layerEl)
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
    // Center block (pre-rendered in the Django template, moved into the layer here).
    // Transform is applied after CENTER_H is measured — see call site.
    const el = document.getElementById("expertHubCenter");
    layerEl.appendChild(el);
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
        "collide",
        forceCollide((d) => {
          if (d.type === "person") return COLLIDE_RADIUS;
          if (d.type === "center") return CENTER_W / 2 + 20;
          return 0;
        }),
      )
      .force(
        "clusterX",
        forceX((d) => {
          if (d.type !== "person") return d.fx ?? W / 2;
          const anchor = nodes.find((n) => n.id === `topic-${d.topics[0]}`);
          return anchor ? anchor.fx : W / 2;
        }).strength(CLUSTER_STRENGTH),
      )
      .force(
        "clusterY",
        forceY((d) => {
          if (d.type !== "person") return d.fy ?? H / 2;
          const anchor = nodes.find((n) => n.id === `topic-${d.topics[0]}`);
          return anchor ? anchor.fy : H / 2;
        }).strength(CLUSTER_STRENGTH),
      )
      .on("tick", ticked);
  }

  function setupDragBehavior() {
    // Card drag: freeze the simulation while dragging so only the dragged node moves,
    // then release and let it spring back to its cluster anchor.
    const nodeDrag = drag()
      .on("start", (event, d) => {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        // Fix every other node so only the dragged one moves
        personNodes.forEach((n) => {
          if (n !== d) {
            n.fx = n.x;
            n.fy = n.y;
          }
        });
        d.fx = d.x;
        d.fy = d.y;
      })
      .on("drag", (event, d) => {
        d.fx = event.x;
        d.fy = event.y;
      })
      .on("end", (event, _d) => {
        if (!event.active) simulation.alphaTarget(0);
        // Release all nodes so they spring back to their cluster anchors
        personNodes.forEach((n) => {
          n.fx = null;
          n.fy = null;
        });
      });

    cardEls.forEach(({ node, el }) => select(el).datum(node).call(nodeDrag));
  }

  function warmupAndStart() {
    // Run a brief synchronous warmup so the initial positions are roughly settled,
    // then let the simulation finish animating live so the intro feels dynamic.
    simulation.stop();
    let tick = 0;
    while (simulation.alpha() > WARMUP_ALPHA && tick < WARMUP_MAX_TICKS) {
      simulation.tick();
      tick++;
    }
    ticked(); // also calls centerInViewport
    // Restart with a small residual alpha so nodes animate gently into their final positions
    simulation.alpha(0.3).restart();
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
        const angle = i * GOLDEN_ANGLE;
        const r = topicOrbitR * ORBIT_FACTORS[i % ORBIT_FACTORS.length];
        const anchor = nodes.find((n) => n.id === `topic-${topic}`);
        if (anchor) {
          anchor.fx = newW / 2 + r * Math.cos(angle);
          anchor.fy = H / 2 + r * Math.sin(angle);
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
