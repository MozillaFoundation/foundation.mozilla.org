// Ported from LP studio/heroes/galaxy.html, final handoff 804c5fd.
// LP geometry and timing stay here; GalaxyHero owns the DOM and animation clock.
// The studio's alternate transitions and editable palette/rotation controls are
// omitted: this component uses the delivered Default transition and Logo palette.
import { createGalaxyField } from "./galaxy_field.js";
// The reduced-motion still uses the settled field, with rotation disabled.
const SETTLED_GALAXY_TIME_MS = 10_000_000;
// Scroll ranges, as fractions of the sticky stage's travel. LP captures wheel
// input on a fixed stage; here the page keeps scrolling, so the counters get
// the first range and the timed cover and galaxy reveal get their own ranges,
// leaving the settled scene on screen for the rest of the sticky travel.
const COUNTER_SCROLL_END = 0.4;
const COVER_SCROLL_RANGE = [0.4, 0.48];
const REVEAL_SCROLL_RANGE = [0.48, 0.8];
// Halfway through the counters' range, as before the scroll ranges.
const REDUCED_MOTION_SECOND_BEAT = COUNTER_SCROLL_END / 2;
const FIRST_COPY_EXIT_PROGRESS = 0.035;
const COUNTER_FADE_SECONDS = 0.45;
const WIPE_GALAXY_START_PROGRESS = 0.68;

export function createGalaxyRenderer(
  canvas,
  { headline, secondHeadline, background, colors },
) {
  const colorToken = (name) => colors[name];
  const galaxyField = createGalaxyField(colorToken);

  const paperColor = colorToken("--color-gray-100"),
    defaultInk = colorToken("--color-text-default");
  const blue = colorToken("--color-accent-blue"),
    orange = colorToken("--color-accent-orange"),
    yellow = colorToken("--color-spectrum-yellow-600");

  const counterPaths = {
    L: "M0.5996 730H218.696L612.514 2596.84H0.5996V730Z",
    M: "M1223.365 -1634.84H217.225L611.043 232H829.547L1223.365 -1634.84Z",
    R: "M1221.904 730H1440V2596.84H828.076L1221.904 730Z",
  };
  const hasPath2D = typeof Path2D === "function";
  const paths = hasPath2D
    ? {
        L: new Path2D(counterPaths.L),
        M: new Path2D(counterPaths.M),
        R: new Path2D(counterPaths.R),
      }
    : counterPaths;
  // Preserve LP's 1440px design coordinates. Height and travel adapt to the
  // viewport while the counters meet at the same centred contact point.
  const DESKTOP_FONT_SIZE = 65;
  let geometry = null;
  function computeGeometry() {
    // Cap design height so the counters' wide ends stay outside the viewport.
    const scale = Math.max(width / 1440, height / 1780);
    const designHeight = height / scale;
    // Leave 72px around desktop copy and 48px on mobile before convergence.
    const headlineClearance = (width < 760 ? 48 : 72) / scale;
    const designFontSize =
      Math.min(DESKTOP_FONT_SIZE, DESKTOP_FONT_SIZE * scale) / scale; // hero size, design px
    let headlineHalfHeight = designFontSize * 1.32; // two lines, half height
    if (isMobile()) {
      // the re-wrapped block, half height
      const lineCount = fitLines(firstHeadlineLines, MOBILE_FONT_SIZE).length;
      headlineHalfHeight =
        designFontSize * (((lineCount - 1) * LINE_HEIGHT + 1) / 2 + 0.22);
    }
    const middleRestOffset =
      designHeight / 2 - headlineHalfHeight - headlineClearance - 232; // M bottom at the zone
    const outerStartTop =
      designHeight / 2 + headlineHalfHeight + headlineClearance; // sides' tops at the zone
    const convergedTop = designHeight / 2 - 1866.84 / 2;
    const outerTravel = convergedTop - outerStartTop; // negative: outer pair rises
    const middleEndOffset = convergedTop + 1634.84; // positive: middle drops
    const combinedTravel = -outerTravel + (middleEndOffset - middleRestOffset);
    return {
      scale: scale,
      designHeight: designHeight,
      offsetX: (width - 1440 * scale) / 2, // centres the crop under zoom
      outerRestOffset: outerStartTop - 730, // sides' rest offset
      middleRestOffset: middleRestOffset, // middle's rest offset
      outerTravel: outerTravel,
      middleEndOffset: middleEndOffset,
      convergedTop: convergedTop,
      convergenceProgress: 1 - 6.9735 / Math.max(60, combinedTravel),
    };
  }

  // polygon vertex lists (for centroids, seams, complements)
  const counterVertices = {
    L: [
      [0.5996, 730],
      [218.696, 730],
      [612.514, 2596.84],
      [0.5996, 2596.84],
    ],
    M: [
      [1223.365, -1634.84],
      [217.225, -1634.84],
      [611.043, 232],
      [829.547, 232],
    ],
    R: [
      [1221.904, 730],
      [1440, 730],
      [1440, 2596.84],
      [828.076, 2596.84],
    ],
  };
  function centroid(v) {
    let x = 0,
      y = 0;
    for (let i = 0; i < v.length; i++) {
      x += v[i][0];
      y += v[i][1];
    }
    return [x / v.length, y / v.length];
  }
  const counterCentroids = {
    L: centroid(counterVertices.L),
    M: centroid(counterVertices.M),
    R: centroid(counterVertices.R),
  };

  // magnetic journey: fast out of the gate, resistance as the gap closes,
  // then the snap. The hold sits at 90% of travel; the remaining 10% of
  // both travels closes in the final stretch of scroll.
  function counterJourney(p) {
    if (p < 0.84) {
      const u = p / 0.84;
      return 0.9 * (1 - Math.pow(1 - u, 2.2));
    }
    const v = (p - 0.84) / 0.16;
    return 0.9 + 0.1 * v * v * (3 - 2 * v);
  }

  // The two-beat copy: line one shows at rest and leaves as the scroll
  // begins, line two arrives once the galaxy is up.
  const firstHeadlineLines = copyLines(headline);
  const secondHeadlineLines = copyLines(secondHeadline);
  // Explicit desktop line breaks are preserved; mobile reflows the words.
  function copyLines(str) {
    const out = String(str)
      .split("\n")
      .map(function (l) {
        return l.trim();
      })
      .filter(function (l) {
        return l.length;
      });
    return out.length ? out : [""];
  }
  const FONT_FAMILY = '"Mozilla Headline", "Helvetica Neue", Arial, sans-serif';
  let reducedMotionEnabled = false;
  const context = canvas.getContext("2d");
  let width = 0,
    height = 0,
    pixelRatio = 1;
  function resize(nextWidth, nextHeight, nextPixelRatio) {
    width = nextWidth;
    height = nextHeight;
    pixelRatio = nextPixelRatio;
    canvas.width = Math.round(width * pixelRatio);
    canvas.height = Math.round(height * pixelRatio);
    context.setTransform(pixelRatio, 0, 0, pixelRatio, 0, 0);
  }

  // Words fade and rise 6px on a 90ms stagger. Replaying a beat resets it.
  const copyStates = [];
  let copyInk = null; // per-frame override; null uses defaultInk
  function copyState(key, elapsedSeconds) {
    // Track each beat separately so rewrapping does not restart the stagger.
    for (let i = 0; i < copyStates.length; i++) {
      if (copyStates[i].key === key) return copyStates[i];
    }
    const state = { key: key, startedAt: elapsedSeconds, visible: false };
    copyStates.push(state);
    return state;
  }
  // The two-beat copy: line one departs as the scroll begins; line two
  // arrives once the galaxy has started.
  const SECOND_COPY_DELAY_SECONDS = 1.25;
  // Use LP's h1 metrics, scaling desktop copy down but never up.
  function headlineFontSize() {
    return isMobile()
      ? MOBILE_FONT_SIZE
      : Math.min(DESKTOP_FONT_SIZE, DESKTOP_FONT_SIZE * geometry.scale);
  }
  const FONT_WEIGHT = 400,
    LINE_HEIGHT = 1.1,
    DESKTOP_TRACKING = -0.02;
  function setHeadlineFont(fontSize) {
    context.font = FONT_WEIGHT + " " + fontSize + "px " + FONT_FAMILY;
    const track = isMobile() ? MOBILE_TRACKING : DESKTOP_TRACKING;
    if ("letterSpacing" in context)
      context.letterSpacing = (fontSize * track).toFixed(2) + "px";
  }
  // Keep all three counters visible and the galaxy close to the mobile copy.
  const MOBILE_BREAKPOINT = 760,
    MOBILE_GUTTER = 24;
  // Figma mobile/h1: 38px, minus 1.5 percent (components/tokens.css)
  const MOBILE_FONT_SIZE = 38,
    MOBILE_TRACKING = -0.015;
  function isMobile() {
    return width < MOBILE_BREAKPOINT;
  }
  // Mobile reflows the words instead of preserving desktop line breaks.
  function fitLines(lines, fontSize) {
    if (!isMobile()) return lines;
    const maxWidth = width - 2 * MOBILE_GUTTER,
      out = [];
    const words = lines.join(" ").split(" ");
    let currentLine = "";
    context.save();
    setHeadlineFont(fontSize);
    for (let j = 0; j < words.length; j++) {
      const next = currentLine ? currentLine + " " + words[j] : words[j];
      if (currentLine && context.measureText(next).width > maxWidth) {
        out.push(currentLine);
        currentLine = words[j];
      } else currentLine = next;
    }
    out.push(currentLine);
    context.restore();
    return out;
  }

  function drawHeadlines(
    scene,
    entranceSeconds,
    elapsedSeconds,
    journeyProgress,
    countersConverged,
    secondCopyReady,
  ) {
    const out = journeyProgress >= FIRST_COPY_EXIT_PROGRESS;
    const inn = countersConverged && secondCopyReady;
    // on scroll-back, line one holds offstage until line two has fully
    // left — the two beats never share the stage in either direction
    const outHold = out || scene.secondCopyOpacity > 0.06;
    if (reducedMotionEnabled) {
      scene.firstCopyExit = out ? 1 : 0;
      scene.secondCopyOpacity = inn ? 1 : 0;
    } else {
      // exits are brisk, arrivals stay gentle
      const tA = outHold ? 1 : 0,
        tB = inn ? 1 : 0;
      scene.firstCopyExit +=
        (tA - scene.firstCopyExit) * (tA > scene.firstCopyExit ? 0.22 : 0.1);
      scene.secondCopyOpacity +=
        (tB - scene.secondCopyOpacity) *
        (tB < scene.secondCopyOpacity ? 0.22 : 0.1);
    }
    const gate = headlineEntranceOpacity(entranceSeconds);
    // fades hold their ground: no drift out or in — the words simply
    // appear and disappear in place
    drawCopy(
      firstHeadlineLines,
      (1 - scene.firstCopyExit) * gate,
      elapsedSeconds,
      "beatA",
    );
    drawCopy(
      secondHeadlineLines,
      scene.secondCopyOpacity * gate,
      elapsedSeconds,
      "beatB",
    );
  }

  function drawCopy(lines, alpha, elapsedSeconds, key) {
    const copy = copyState(key, elapsedSeconds);
    // Replay the stagger each time a beat becomes visible, not after a slow frame.
    if (alpha <= 0.004) {
      copy.visible = false;
      return;
    }
    if (!copy.visible) copy.startedAt = elapsedSeconds;
    copy.visible = true;

    context.save();
    context.fillStyle = copyInk || defaultInk;
    context.textAlign = "left";
    context.textBaseline = "middle";
    let fontSize = headlineFontSize();
    lines = fitLines(lines, fontSize);
    setHeadlineFont(fontSize);
    let widest = 0;
    for (let i = 0; i < lines.length; i++)
      widest = Math.max(widest, context.measureText(lines[i]).width);
    if (widest > width * 0.86) fontSize = (fontSize * (width * 0.86)) / widest;
    fontSize = Math.min(
      fontSize,
      (height * 0.86) / (lines.length * LINE_HEIGHT),
    );
    // the block's top must clear the nav band on short viewports
    const half = ((lines.length - 1) * LINE_HEIGHT + 1) / 2; // half-height in fs units
    fontSize = Math.max(12, Math.min(fontSize, (height / 2 - 48) / half));
    setHeadlineFont(fontSize.toFixed(1));
    const lineHeight = fontSize * LINE_HEIGHT,
      spaceWidth = context.measureText(" ").width;
    let wordIndex = 0;
    for (let i = 0; i < lines.length; i++) {
      const words = lines[i].split(" ");
      let total = 0;
      const wordWidths = [];
      for (let j = 0; j < words.length; j++) {
        wordWidths.push(context.measureText(words[j]).width);
        total += wordWidths[j];
      }
      total += spaceWidth * (words.length - 1);
      let x = width / 2 - total / 2;
      const y = height / 2 + (i - (lines.length - 1) / 2) * lineHeight;
      for (let j = 0; j < words.length; j++) {
        let wordProgress = reducedMotionEnabled
          ? 1
          : Math.min(
              1,
              Math.max(
                0,
                (elapsedSeconds - copy.startedAt - wordIndex * 0.09) / 0.32,
              ),
            );
        wordProgress = 1 - Math.pow(1 - wordProgress, 3);
        if (wordProgress > 0.004) {
          context.globalAlpha = alpha * wordProgress;
          context.fillText(words[j], x, y + (1 - wordProgress) * 6);
        }
        x += wordWidths[j] + spaceWidth;
        wordIndex++;
      }
    }
    context.restore();
  }

  const entranceOffsets = { lr: 0, m: 0 };

  // Draws in design space: 1440 wide, scaled and centred by computeGeometry(),
  // clipped to the design height.
  function withDesignCoordinates(fn) {
    context.save();
    if (isMobile())
      context.scale(width / 1440, geometry.scale); // all three counters in frame
    else {
      context.translate(geometry.offsetX, 0);
      context.scale(geometry.scale, geometry.scale);
    }
    context.beginPath();
    context.rect(0, 0, 1440, geometry.designHeight);
    context.clip();
    fn();
    context.restore();
  }

  function clampCounterOffset(key, dy) {
    // Keep outer bottoms below the stage and the middle top above it.
    if (key === "M") return Math.min(dy, 1634.84);
    return Math.max(dy, geometry.designHeight - 2596.84);
  }
  // Draw one counter at its vertical offset, plus any entrance offset.
  function drawCounter(key, dy, fill) {
    dy = clampCounterOffset(key, dy);
    const enter = key === "M" ? entranceOffsets.m : entranceOffsets.lr;
    context.save();
    context.translate(0, dy + enter);
    context.fillStyle = fill;
    context.fill(paths[key]);
    context.restore();
  }

  // The counters enter from opposite edges before the first headline appears.
  function updateCounterEntrance(entranceSeconds) {
    let a = reducedMotionEnabled
      ? 1
      : Math.min(1, Math.max(0, (entranceSeconds - 0.15) / 0.9));
    a = 1 - Math.pow(1 - a, 3);
    // Start each shape fully outside the stage at every viewport height.
    const outerEntranceDistance =
      geometry.designHeight - 730 - geometry.outerRestOffset + 40;
    const middleEntranceDistance = 232 + 40;
    entranceOffsets.lr = (1 - a) * outerEntranceDistance;
    entranceOffsets.m = -(1 - a) * middleEntranceDistance;
  }
  function headlineEntranceOpacity(entranceSeconds) {
    if (reducedMotionEnabled) return 1;
    return Math.min(1, Math.max(0, (entranceSeconds - 0.45) / 0.2));
  }

  // ---- Beat 2: the pixel galaxy (arms) ----
  // Measure the second headline before building the seeded field so cells
  // stay outside its clear area, including after a viewport resize.
  const GALAXY_SEED = 7;
  // The middle counter expands uniformly to become the second background.
  // Swap counter colours so it always carries the selected ground colour.
  const BACKGROUND_SCHEMES = {
    Gray: {
      bg: null,
      fills: { L: blue, M: orange, R: yellow },
      ink: defaultInk,
    },
    Orange: {
      bg: orange,
      fills: { L: blue, M: orange, R: yellow },
      ink: colorToken("--color-text-inverse"),
    },
    Yellow: {
      bg: yellow,
      fills: { L: blue, M: yellow, R: orange },
      ink: defaultInk,
    },
    Blue: {
      bg: blue,
      fills: { L: orange, M: blue, R: yellow },
      ink: colorToken("--color-text-inverse"),
    },
  };
  const scheme = BACKGROUND_SCHEMES[background] || BACKGROUND_SCHEMES.Gray;
  const WIPE_DURATION_SECONDS = 0.7;
  function wipeCoverScale(middleEndOffset) {
    // smallest uniform scale about the mid counter's kiss centroid that
    // covers the design viewport (convex quad: binary search + inclusion)
    const poly = counterVertices.M.map(function (v) {
      return [v[0], v[1] + middleEndOffset];
    });
    const cx = counterCentroids.M[0],
      cy = counterCentroids.M[1] + middleEndOffset;
    function inside(px, py, k) {
      const q = poly.map(function (v) {
        return [cx + (v[0] - cx) * k, cy + (v[1] - cy) * k];
      });
      let sgn = 0;
      for (let i = 0; i < q.length; i++) {
        const a = q[i],
          b = q[(i + 1) % q.length];
        const cr = (b[0] - a[0]) * (py - a[1]) - (b[1] - a[1]) * (px - a[0]);
        if (cr !== 0) {
          if (sgn === 0) sgn = cr > 0 ? 1 : -1;
          else if ((cr > 0 ? 1 : -1) !== sgn) return false;
        }
      }
      return true;
    }
    const corners = [
      [0, 0],
      [1440, 0],
      [0, geometry.designHeight],
      [1440, geometry.designHeight],
    ];
    let lo = 1,
      hi = 64;
    for (let n = 0; n < 26; n++) {
      const mid = (lo + hi) / 2;
      let ok = true;
      for (let ci = 0; ci < 4; ci++)
        if (!inside(corners[ci][0], corners[ci][1], mid)) {
          ok = false;
          break;
        }
      if (ok) hi = mid;
      else lo = mid;
    }
    return hi;
  }
  const LOGO_PALETTE = [
    { hex: colorToken("--color-spectrum-yellow-600"), weight: 30 },
    { hex: colorToken("--color-accent-blue"), weight: 10 },
    { hex: colorToken("--color-accent-orange"), weight: 8 },
  ];
  function secondHeadlineBounds() {
    // line two's rendered box, from the shared fit
    let fontSize = headlineFontSize();
    const lines = fitLines(secondHeadlineLines, fontSize);
    context.save();
    setHeadlineFont(fontSize);
    let widest = 0;
    for (let i = 0; i < lines.length; i++)
      widest = Math.max(widest, context.measureText(lines[i]).width);
    context.restore();
    if (widest > width * 0.86) {
      fontSize = (fontSize * (width * 0.86)) / widest;
      widest = width * 0.86;
    }
    fontSize = Math.min(
      fontSize,
      (height * 0.86) / (lines.length * LINE_HEIGHT),
    );
    if (isMobile()) {
      const hy =
        ((lines.length - 1) * fontSize * LINE_HEIGHT + fontSize) / 2 + 6;
      return { hx: widest / 2, hy: hy, n: lines.length, fontSize: fontSize };
    }
    // half-height: half the leaded block, plus the line's own half-body
    // margin, plus the arrival drift (line two lands from +26·s below)
    return {
      hx: widest / 2,
      hy:
        ((secondHeadlineLines.length - 1) * fontSize * LINE_HEIGHT + fontSize) /
          2 +
        26 * geometry.scale +
        6,
    };
  }
  function buildGalaxy(scene) {
    const box = secondHeadlineBounds();
    let palette = null;
    if (scheme.bg) {
      // coloured ground: Spectrum only, with the ground's colour omitted
      palette = galaxyField.PALETTE.filter(function (p) {
        return p.hex !== scheme.bg;
      });
    } else palette = LOGO_PALETTE;
    let place = null;
    // the hole hugs the copy, so the arms fill above and below it
    if (isMobile())
      place = {
        ellipseRadiusX: width * 0.42,
        ellipseRadiusY: Math.max(box.hy * 1.9, width * 0.62),
      };
    scene.field = galaxyField.buildField({
      seed: GALAXY_SEED,
      width,
      height,
      headlineHalfWidth: box.hx,
      headlineHalfHeight: box.hy,
      palette,
      placement: place || {},
    });
  }

  function drawCounters(
    scene,
    entranceSeconds,
    countersConverged,
    counterProgress,
    convergenceSeconds,
  ) {
    if (!countersConverged) {
      withDesignCoordinates(function () {
        updateCounterEntrance(entranceSeconds);
        drawCounter(
          "L",
          geometry.outerRestOffset + geometry.outerTravel * counterProgress,
          scheme.fills.L,
        );
        if (!(scheme.bg && scene.wipeProgress > 0.05))
          drawCounter(
            "M",
            geometry.middleRestOffset +
              (geometry.middleEndOffset - geometry.middleRestOffset) *
                counterProgress,
            scheme.fills.M,
          );
        drawCounter(
          "R",
          geometry.outerRestOffset + geometry.outerTravel * counterProgress,
          scheme.fills.R,
        );
      });
    } else {
      // Coloured backgrounds cover opaque counters; fading would flash paper.
      const hold = scheme.bg
        ? scene.wipeProgress >= 0.999
          ? 0
          : 1
        : reducedMotionEnabled
          ? 0
          : Math.max(0, 1 - convergenceSeconds / COUNTER_FADE_SECONDS);
      if (hold > 0.004) {
        context.save();
        context.globalAlpha = hold;
        withDesignCoordinates(function () {
          updateCounterEntrance(entranceSeconds);
          drawCounter(
            "L",
            geometry.outerRestOffset + geometry.outerTravel,
            scheme.fills.L,
          );
          if (!scheme.bg)
            drawCounter("M", geometry.middleEndOffset, scheme.fills.M);
          drawCounter(
            "R",
            geometry.outerRestOffset + geometry.outerTravel,
            scheme.fills.R,
          );
        });
        context.restore();
      }
    }
  }

  function drawBackgroundWipe(
    scene,
    countersConverged,
    counterProgress,
    convergenceSeconds,
  ) {
    // the wipe: forward on the kiss clock; on scroll-back it recedes
    if (scheme.bg) {
      if (countersConverged)
        scene.wipeProgress = reducedMotionEnabled
          ? 1
          : Math.min(1, convergenceSeconds / WIPE_DURATION_SECONDS);
      else
        scene.wipeProgress = reducedMotionEnabled
          ? 0
          : scene.wipeProgress * 0.7;
      if (scene.wipeProgress > 0.004) {
        const easedWipeProgress =
          scene.wipeProgress < 0.5
            ? 4 * scene.wipeProgress * scene.wipeProgress * scene.wipeProgress
            : 1 - Math.pow(-2 * scene.wipeProgress + 2, 3) / 2;
        if (
          scene.wipeDesignHeight !== geometry.designHeight ||
          scene.wipeMiddleOffset !== geometry.middleEndOffset
        ) {
          scene.wipeFullScale = wipeCoverScale(geometry.middleEndOffset);
          scene.wipeDesignHeight = geometry.designHeight;
          scene.wipeMiddleOffset = geometry.middleEndOffset;
        }
        const wipeScale = 1 + (scene.wipeFullScale - 1) * easedWipeProgress;
        const middleOffset = clampCounterOffset(
          "M",
          geometry.middleRestOffset +
            (geometry.middleEndOffset - geometry.middleRestOffset) *
              (countersConverged ? 1 : counterProgress),
        ); // rides the rewind
        withDesignCoordinates(function () {
          context.globalAlpha = 1; // never fades: it covers, or it recedes
          if (easedWipeProgress >= 0.999) {
            context.fillStyle = scheme.bg;
            context.fillRect(0, 0, 1440, geometry.designHeight);
          } else {
            const cx = counterCentroids.M[0],
              cy = counterCentroids.M[1] + middleOffset;
            context.translate(cx, cy);
            context.scale(wipeScale, wipeScale);
            context.translate(-cx, -cy);
            context.translate(0, middleOffset);
            context.fillStyle = scheme.bg;
            context.fill(paths.M);
          }
          context.globalAlpha = 1;
        });
      }
    } else scene.wipeProgress = 0;
    copyInk = scheme.bg && scene.wipeProgress > 0.55 ? scheme.ink : null;
  }

  // Called only while the galaxy is visible. Keep the burst clock separate
  // from accumulated rotation, so reversing can freeze the departing field.
  function advanceGalaxyClock(scene, elapsedSeconds) {
    const burstElapsedMs =
      scene.galaxyStartedAt !== null
        ? Math.max(0, (elapsedSeconds - scene.galaxyStartedAt) * 1000)
        : (scene.galaxyFrozenMs ?? 0);
    scene.galaxyLastMs = burstElapsedMs;
    const settledAtMs = scene.field.settledAtMs;
    const deltaMs = Math.max(
      0,
      (elapsedSeconds - scene.galaxyLastSeconds) * 1000,
    );
    scene.galaxyLastSeconds = elapsedSeconds;
    if (burstElapsedMs > settledAtMs) scene.rotationMs += deltaMs;
    if (reducedMotionEnabled) return SETTLED_GALAXY_TIME_MS;
    if (burstElapsedMs <= settledAtMs) return burstElapsedMs;
    return settledAtMs + scene.rotationMs;
  }

  function drawGalaxy(scene, elapsedSeconds, countersConverged) {
    if (!scene.field) return;
    // Rebuild on resize so the field stays centred and its clear area
    // follows the rewrapped headline. The seed preserves its arrangement.
    if (scene.field.width !== width || scene.field.height !== height)
      buildGalaxy(scene);
    const target = countersConverged && scene.galaxyStartedAt !== null ? 1 : 0;
    if (reducedMotionEnabled) scene.galaxyOpacity = target;
    else
      scene.galaxyOpacity +=
        (target - scene.galaxyOpacity) * (countersConverged ? 0.25 : 0.22);
    if (
      scene.galaxyOpacity > 0.004 &&
      scene.galaxyFrozenMs === null &&
      scene.galaxyStartedAt === null
    )
      scene.galaxyFrozenMs = scene.galaxyLastMs;
    if (scene.galaxyStartedAt !== null) scene.galaxyFrozenMs = null;
    if (scene.galaxyOpacity > 0.004) {
      const sampleMs = advanceGalaxyClock(scene, elapsedSeconds);
      const rects = galaxyField.sampleField(
        scene.field,
        sampleMs,
        !reducedMotionEnabled,
      );
      context.save();
      context.globalAlpha = scene.galaxyOpacity;
      for (let rectIndex = 0; rectIndex < rects.length; rectIndex++) {
        const rect = rects[rectIndex];
        context.fillStyle = rect.color;
        const x = Math.round(rect.x * pixelRatio) / pixelRatio;
        const y = Math.round(rect.y * pixelRatio) / pixelRatio;
        context.fillRect(
          x,
          y,
          Math.round((rect.x + rect.w) * pixelRatio) / pixelRatio - x,
          Math.round((rect.y + rect.h) * pixelRatio) / pixelRatio - y,
        );
      }
      context.restore();
    }
  }

  // Frame order matters: retire the first copy, converge the counters, cover
  // the background, then burst the galaxy and reveal the second copy.
  // Times are scene seconds; null means "not yet" for this pass forward.
  function createSceneState() {
    return {
      clockOffsetSeconds: 0, // scroll pacing's fast-forward
      born: null,
      firstCopyExit: 0,
      secondCopyOpacity: 0,
      wasConverged: false,
      convergedAt: null,
      coveredAt: null,
      wipeProgress: 0,
      wipeFullScale: null, // cached for wipeDesignHeight/wipeMiddleOffset
      wipeDesignHeight: null,
      wipeMiddleOffset: null,
      field: null,
      galaxyStartedAt: null,
      galaxyOpacity: 0,
      galaxyFrozenMs: null, // burst time held while reversing
      galaxyLastMs: 0,
      galaxyLastSeconds: 0,
      rotationMs: 0,
    };
  }

  function scrollRangeProgress(progress, [start, end]) {
    return Math.min(1, Math.max(0, (progress - start) / (end - start)));
  }

  // Continued scrolling fast-forwards, but never rewinds, the timed cover and
  // galaxy reveal so each finishes within its scroll range. Slower scrolling
  // or stopping leaves LP's wall-clock timing unchanged.
  function paceRevealToScroll(scene, progress, elapsedSeconds) {
    const coverSeconds = scheme.bg
      ? WIPE_GALAXY_START_PROGRESS * WIPE_DURATION_SECONDS
      : COUNTER_FADE_SECONDS;
    let pacedSeconds =
      scene.convergedAt +
      coverSeconds * scrollRangeProgress(progress, COVER_SCROLL_RANGE);
    if (scene.galaxyStartedAt !== null) {
      // The burst settles after the second headline's word stagger ends.
      const revealSeconds = scene.field.settledAtMs / 1000;
      pacedSeconds = Math.max(
        pacedSeconds,
        scene.galaxyStartedAt +
          revealSeconds * scrollRangeProgress(progress, REVEAL_SCROLL_RANGE),
      );
    }
    if (pacedSeconds <= elapsedSeconds) return elapsedSeconds;
    scene.clockOffsetSeconds += pacedSeconds - elapsedSeconds;
    return pacedSeconds;
  }

  function drawScene(progress, scene, clockSeconds) {
    let elapsedSeconds = clockSeconds + scene.clockOffsetSeconds;
    if (scene.born === null) scene.born = elapsedSeconds;
    const entranceSeconds = elapsedSeconds - scene.born;
    const journeyProgress = counterJourney(
      Math.min(1, progress / COUNTER_SCROLL_END),
    );
    // Hold the counters until the first headline has mostly faded out.
    const copyExitGate = reducedMotionEnabled
      ? 1
      : Math.max(0, Math.min(1, (scene.firstCopyExit - 0.55) / 0.4));
    const counterProgress = journeyProgress * copyExitGate;
    const countersConverged = counterProgress >= geometry.convergenceProgress;
    if (countersConverged && !scene.wasConverged) {
      scene.convergedAt = elapsedSeconds;
      // Wait for coverage before starting the burst; reversing resets its clock.
      if (!scene.field) buildGalaxy(scene);
    }
    scene.wasConverged = countersConverged;
    context.fillStyle = paperColor;
    context.fillRect(0, 0, width, height);

    if (countersConverged && !reducedMotionEnabled)
      elapsedSeconds = paceRevealToScroll(scene, progress, elapsedSeconds);
    const convergenceSeconds = countersConverged
      ? elapsedSeconds - scene.convergedAt
      : 0;

    // Gray waits for the counters to fade. Coloured backgrounds start the
    // burst near the end of the wipe, at about 93% viewport coverage.
    // Read the preceding frame's coverage, preserving LP's frame ordering.
    const covered = scheme.bg
      ? scene.wipeProgress >= WIPE_GALAXY_START_PROGRESS
      : countersConverged && convergenceSeconds >= COUNTER_FADE_SECONDS;
    if (covered && scene.coveredAt === null) scene.coveredAt = elapsedSeconds;
    if (!covered) scene.coveredAt = null;
    const backgroundCovered = scene.coveredAt !== null;
    if (backgroundCovered && scene.galaxyStartedAt === null) {
      scene.galaxyStartedAt = elapsedSeconds;
      scene.rotationMs = 0;
      scene.galaxyLastSeconds = elapsedSeconds;
    }
    if (!countersConverged) scene.galaxyStartedAt = null;

    drawCounters(
      scene,
      entranceSeconds,
      countersConverged,
      counterProgress,
      convergenceSeconds,
    );
    drawBackgroundWipe(
      scene,
      countersConverged,
      counterProgress,
      convergenceSeconds,
    );
    drawGalaxy(scene, elapsedSeconds, countersConverged);

    const secondCopyReady =
      scene.galaxyStartedAt !== null &&
      elapsedSeconds - scene.galaxyStartedAt > SECOND_COPY_DELAY_SECONDS;
    drawHeadlines(
      scene,
      entranceSeconds,
      elapsedSeconds,
      journeyProgress,
      countersConverged,
      reducedMotionEnabled ? countersConverged : secondCopyReady,
    );
  }

  let state = createSceneState();
  return {
    resize,
    draw(progress, elapsedMs, reducedMotion) {
      if (!width || !height) return;
      if (reducedMotionEnabled !== reducedMotion) {
        state = createSceneState();
        copyStates.length = 0;
      }
      reducedMotionEnabled = reducedMotion;
      geometry = computeGeometry();
      if (reducedMotionEnabled) {
        // LP reads coverage from the preceding frame. Resolve the entrance,
        // coverage and settled field in order, without scheduling animation.
        // Ten seconds between samples exceeds every entrance/wipe delay.
        state = createSceneState();
        copyStates.length = 0;
        const beat = progress >= REDUCED_MOTION_SECOND_BEAT ? 1 : 0;
        drawScene(beat, state, 0);
        drawScene(beat, state, 10);
        drawScene(beat, state, 20);
      } else {
        drawScene(
          Math.min(1, Math.max(0, progress || 0)),
          state,
          elapsedMs / 1000,
        );
      }
      return copyInk || defaultInk;
    },
  };
}
