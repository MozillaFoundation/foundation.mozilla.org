// Hover behaviour of LP's `wordmark` foundation (Figma 7224:378): the
// fifteen colored shapes scale in behind the ink in random order, and the
// twelve not tied to the M take a fresh palette colour on every hover in and
// after every hover out. Ported from the behaviour script in LP's
// components/foundations/logo/footer-logo/index.html.

const PALETTE_TOKENS = [
  "--color-accent-blue",
  "--color-accent-orange",
  "--color-accent-yellow",
  "--color-accent-green",
  "--color-accent-magenta",
];
const PALETTE_FALLBACK = [
  "#23A5E9",
  "#F06C13",
  "#EEC700",
  "#00A43D",
  "#EA5699",
];
// The red is a drawn value with no token behind it, so it is only ever a literal.
const PALETTE_RED = "#E44024";

const rand = (lo, hi) => lo + Math.random() * (hi - lo);

function shuffle(items) {
  const result = [...items];
  for (let i = result.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [result[i], result[j]] = [result[j], result[i]];
  }
  return result;
}

function readMotion(tokenStyles) {
  const ms = (name, fallback) => {
    const value = parseFloat(tokenStyles.getPropertyValue(name));
    return Number.isFinite(value) ? value : fallback;
  };
  return {
    easing:
      tokenStyles
        .getPropertyValue("--mzf-motion-easing-wordmark-shape")
        .trim() || "cubic-bezier(0.22, 1, 0.36, 1)",
    shapeIn: ms("--mzf-motion-duration-wordmark-shape-in", 200),
    shapeOut: ms("--mzf-motion-duration-wordmark-shape-out", 160),
    stagger: ms("--mzf-motion-duration-wordmark-stagger", 40),
  };
}

function readPalette(tokenStyles) {
  const colors = PALETTE_TOKENS.map(
    (name, i) =>
      tokenStyles.getPropertyValue(name).trim() || PALETTE_FALLBACK[i],
  );
  return [...colors, PALETTE_RED];
}

function writeFill(shape, color) {
  shape.setAttribute("fill", color);
  shape.style.fill = color;
}

function wireWordmark(root, tokenStyles) {
  if (root.dataset.wordmarkWired) return;
  root.dataset.wordmarkWired = "true";

  const shapes = [...root.querySelectorAll(".mzf-c-wordmark__shape")];
  if (!shapes.length) return;

  const isM = (shape) => shape.classList.contains("mzf-c-wordmark__shape--m");
  const mShapes = shapes.filter(isM);
  mShapes.forEach((shape) => {
    shape.dataset.wordmarkFill = shape.getAttribute("fill") || "";
  });

  const mutableShapes = shapes
    .filter((shape) => !isM(shape))
    .map((shape) => ({
      shape,
      letter: parseInt(shape.dataset.wordmarkLetter, 10),
    }))
    .filter(({ letter }) => Number.isFinite(letter))
    .sort((a, b) => a.letter - b.letter);

  const motion = readMotion(tokenStyles);
  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  const readFills = () =>
    mutableShapes
      .map(({ shape }) => (shape.getAttribute("fill") || "").toLowerCase())
      .join("|");

  // Neighbouring letters never share a colour, and the letter after the M
  // avoids the M's own three.
  const assignOnce = () => {
    const palette = readPalette(tokenStyles);
    const byLetter = new Map();
    const mColors = mShapes.map((shape) =>
      shape.dataset.wordmarkFill.toLowerCase(),
    );
    mutableShapes.forEach(({ shape, letter }) => {
      const blocked = new Set();
      if (byLetter.has(letter - 1)) blocked.add(byLetter.get(letter - 1));
      if (letter === 1) mColors.forEach((color) => blocked.add(color));
      const allowed = palette.filter(
        (color) => !blocked.has(color.toLowerCase()),
      );
      const pool = allowed.length ? allowed : palette;
      const color = pool[Math.floor(Math.random() * pool.length)];
      byLetter.set(letter, color.toLowerCase());
      writeFill(shape, color);
    });
  };

  const assignShapeColors = () => {
    const previous = readFills();
    let tries = 0;
    do {
      assignOnce();
      tries++;
    } while (readFills() === previous && tries < 32);
    mShapes.forEach((shape) => writeFill(shape, shape.dataset.wordmarkFill));
  };

  let live = [];
  let hoverGeneration = 0;

  const cancelAll = () => {
    live.forEach((animation) => animation.cancel());
    live = [];
    shapes.forEach((shape) =>
      shape.getAnimations().forEach((animation) => animation.cancel()),
    );
  };

  const resetShape = (shape) => {
    shape.style.opacity = "0";
    shape.style.transform = "";
  };

  root.addEventListener("mouseenter", () => {
    hoverGeneration++;
    assignShapeColors();
    cancelAll();

    if (reduced) {
      shapes.forEach((shape) => {
        shape.style.opacity = "1";
        shape.style.transform = "scale(1)";
      });
      return;
    }

    shapes.forEach(resetShape);
    let delay = 0;
    shuffle(shapes).forEach((shape) => {
      live.push(
        shape.animate(
          [
            { opacity: 0, transform: `scale(${rand(0.85, 0.9)})` },
            { opacity: 1, transform: "scale(1)" },
          ],
          {
            duration: rand(motion.shapeIn * 0.9, motion.shapeIn * 1.2),
            delay,
            easing: motion.easing,
            fill: "forwards",
          },
        ),
      );
      delay += rand(motion.stagger * 0.625, motion.stagger * 1.5);
    });
  });

  root.addEventListener("mouseleave", () => {
    const leaveGeneration = ++hoverGeneration;

    if (reduced) {
      cancelAll();
      shapes.forEach(resetShape);
      assignShapeColors();
      return;
    }

    // Freeze each shape where its entry animation left it, so the exit starts
    // from there rather than snapping to fully shown.
    shapes.forEach((shape) =>
      shape.getAnimations().forEach((animation) => animation.commitStyles()),
    );
    cancelAll();

    const exiting = [];
    shuffle(shapes).forEach((shape) => {
      const computed = getComputedStyle(shape);
      const opacity = parseFloat(computed.opacity);
      if (opacity < 0.02) {
        resetShape(shape);
        return;
      }
      exiting.push({
        shape,
        opacity,
        transform:
          computed.transform === "none" ? "scale(1)" : computed.transform,
      });
    });

    if (!exiting.length) {
      assignShapeColors();
      return;
    }

    let delay = 0;
    const exits = exiting.map(({ shape, opacity, transform }) => {
      const animation = shape.animate(
        [
          { opacity, transform },
          { opacity: 0, transform: "scale(0.87)" },
        ],
        {
          duration: rand(motion.shapeOut * 0.875, motion.shapeOut * 1.25),
          delay,
          easing: motion.easing,
          fill: "forwards",
        },
      );
      delay += rand(motion.stagger * 0.5, motion.stagger);
      live.push(animation);
      return animation.finished.catch(() => {});
    });

    Promise.all(exits).then(() => {
      if (leaveGeneration === hoverGeneration) assignShapeColors();
    });
  });
}

export function initWordmarkHover(root = document) {
  const wordmarks = root.querySelectorAll(".mzf-c-wordmark");
  if (!wordmarks.length) return;

  const tokenStyles = getComputedStyle(document.documentElement);
  wordmarks.forEach((wordmark) => wireWordmark(wordmark, tokenStyles));
}
