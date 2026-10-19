// Ported from LP studio/heroes/galaxy.html, final handoff 804c5fd.
// LP geometry and timing stay here; GalaxyHero owns the DOM and animation clock.
// The studio's alternate transitions and editable palette/rotation controls are
// omitted: this component uses the delivered Default transition and Logo palette.
import { createGalaxyField } from "./galaxy_field.js";
// The reduced-motion still uses the settled field, with rotation disabled.
const SETTLED_GALAXY_TIME_MS = 10_000_000;
const REDUCED_MOTION_SECOND_BEAT = 0.5;
const FIRST_COPY_EXIT_PROGRESS = 0.035;
const COUNTER_FADE_SECONDS = 0.45;
const WIPE_GALAXY_START_PROGRESS = 0.68;

export function createGalaxyRenderer(
  canvas,
  { headline, secondHeadline, background, colors },
) {
  const TOK = (name) => colors[name];
  const GALAXY = createGalaxyField(TOK);

  // ------------------------------------------------------------- constants
  var PAPER = TOK("--color-gray-100"),
    INK = TOK("--color-text-default");
  var SKY = TOK("--color-accent-blue"),
    ORG = TOK("--color-accent-orange"),
    YEL = TOK("--color-spectrum-yellow-600");

  var SRC = {
    L: "M0.5996 730H218.696L612.514 2596.84H0.5996V730Z",
    M: "M1223.365 -1634.84H217.225L611.043 232H829.547L1223.365 -1634.84Z",
    R: "M1221.904 730H1440V2596.84H828.076L1221.904 730Z",
  };
  var HASP2D = typeof Path2D === "function";
  var P = HASP2D
    ? { L: new Path2D(SRC.L), M: new Path2D(SRC.M), R: new Path2D(SRC.R) }
    : SRC;
  // Responsive geometry: the design width is fixed at 1440 (the whole
  // composition is always visible across), and the design HEIGHT flexes to
  // fill the stage exactly — no letterbox in either axis. Anchors follow
  // the mock's construction: the outer pair peeks 230 design px above the
  // bottom edge (tops at 730 in the 960 mock), the middle hangs from the
  // top as drawn (bottom edge at 232), and the kiss — the fixed 1866.84
  // band — lands centred. Travels and the contact point derive per layout;
  // the contact closed form generalises the measured p* = 0.99705 at 960:
  // p* = 1 − (1.471 · 4.7404) / (|T_LR| + T_M).
  // The hero's type is the library's h1 — 65px at the 1440 design width
  // (components/tokens.css, --font-size-h1); the rest of the style sits
  // with heroFont() below.
  var HERO_FS = 65;
  var GEO = null;
  function computeGeo() {
    // Full-bleed at any aspect: the counters' wide ends must never enter
    // the viewport. At the kiss the sides' bottoms sit at dh/2 + 933.4,
    // so any dh beyond 1866.8 exposes them — the scale takes a floor
    // (a uniform zoom, angles untouched) that caps the design height.
    var s = Math.max(W / 1440, H / 1780);
    var dh = H / s;
    // Rest sits close to the centre: the shapes' leading edges hold a
    // safe zone above and below the hero text (72px desktop, 48px
    // mobile), so the scroll is short and the words always own their
    // ground at rest.
    var safe = (W < 760 ? 48 : 72) / s;
    var fsD = Math.min(HERO_FS, HERO_FS * s) / s; // hero size, design px
    var halfBlock = fsD * 1.32; // two lines, half height
    if (mobileOpt()) {
      // the re-wrapped block, half height
      var nA = fitLines(COPY_A, HERO_FS_MOBILE).length;
      halfBlock = fsD * (((nA - 1) * HERO_LEAD + 1) / 2 + 0.22);
    }
    var mRest = dh / 2 - halfBlock - safe - 232; // M bottom at the zone
    var startTopLR = dh / 2 + halfBlock + safe; // sides' tops at the zone
    var endTop = dh / 2 - 1866.84 / 2;
    var tLR = endTop - startTopLR; // negative: outer pair rises
    var tM = endTop + 1634.84; // positive: middle drops
    var D = -tLR + (tM - mRest);
    return {
      s: s,
      dh: dh,
      ox: (W - 1440 * s) / 2, // centres the crop under zoom
      dLR0: startTopLR - 730, // sides' rest offset
      mRest: mRest, // middle's rest offset
      tLR: tLR,
      tM: tM,
      endTop: endTop,
      pstar: 1 - 6.9735 / Math.max(60, D),
    };
  }

  // polygon vertex lists (for centroids, seams, complements)
  var VERT = {
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
    var x = 0,
      y = 0;
    for (var i = 0; i < v.length; i++) {
      x += v[i][0];
      y += v[i][1];
    }
    return [x / v.length, y / v.length];
  }
  var CEN = { L: centroid(VERT.L), M: centroid(VERT.M), R: centroid(VERT.R) };

  // magnetic journey: fast out of the gate, resistance as the gap closes,
  // then the snap. The hold sits at 90% of travel; the remaining 10% of
  // both travels closes in the final stretch of scroll.
  function magJ(p) {
    if (p < 0.84) {
      var u = p / 0.84;
      return 0.9 * (1 - Math.pow(1 - u, 2.2));
    }
    var v = (p - 0.84) / 0.16;
    return 0.9 + 0.1 * v * v * (3 - 2 * v);
  }

  // The two-beat copy: line one shows at rest and leaves as the scroll
  // begins, line two arrives once the galaxy is up.
  var COPY_A = copyLines(headline);
  var COPY_B = copyLines(secondHeadline);
  // Explicit desktop line breaks are preserved; mobile reflows the words.
  function copyLines(str) {
    var out = String(str)
      .split("\n")
      .map(function (l) {
        return l.trim();
      })
      .filter(function (l) {
        return l.length;
      });
    return out.length ? out : [""];
  }
  var FACE = '"Mozilla Headline", "Helvetica Neue", Arial, sans-serif';
  var REDUCED = false;
  var c = canvas.getContext("2d");
  var W = 0,
    H = 0,
    dpr = 1;
  function resize(width, height, pixelRatio) {
    W = width;
    H = height;
    dpr = pixelRatio;
    canvas.width = Math.round(W * dpr);
    canvas.height = Math.round(H * dpr);
    c.setTransform(dpr, 0, 0, dpr, 0, 0);
  }

  // -------------------------------------------------------------- headline
  // The copy appears word by word: each word fades (and rises 6px) on a
  // 90ms stagger. Appearance timing is managed here, keyed on the lines
  // array itself: whenever a copy comes back after being invisible — or
  // hasn't been drawn for a beat — its stagger replays.
  var COPY_STATE = [];
  var COPY_INK = null; // per-frame override; null = INK
  function copyState(key, e) {
    // keyed by beat role, not array identity: a text change swaps the
    // words in place without refiring the word stagger
    for (var i = 0; i < COPY_STATE.length; i++) {
      if (COPY_STATE[i].key === key) return COPY_STATE[i];
    }
    var st2 = { key: key, t0: e, lastDrawn: -1 };
    COPY_STATE.push(st2);
    return st2;
  }
  // The two-beat copy: line one departs as the scroll begins; line two
  // arrives once the galaxy has started.
  var COPY_AFTER = 1.25; // line two lands this long after the galaxy clock starts
  // The hero is set in the library's h1 — Mozilla Headline, regular, 65px
  // at the 1440 design width, 110 percent leading, minus 2 percent
  // tracking (components/tokens.css) — scaling down proportionally on
  // narrower viewports (GEO.s < 1); never larger on wide screens.
  function heroFs() {
    return mobileOpt() ? HERO_FS_MOBILE : Math.min(HERO_FS, HERO_FS * GEO.s);
  }
  var HERO_WEIGHT = 400,
    HERO_LEAD = 1.1,
    HERO_TRACK = -0.02;
  function heroFont(fs) {
    c.font = HERO_WEIGHT + " " + fs + "px " + FACE;
    var track = mobileOpt() ? HERO_TRACK_MOBILE : HERO_TRACK;
    if ("letterSpacing" in c) c.letterSpacing = (fs * track).toFixed(2) + "px";
  }
  // LP's mobile layout
  // Below 760px the counters squeeze to the width so all three stay in
  // frame, and the galaxy's inner hole hugs the copy.
  var MOBILE_BP = 760,
    MOBILE_GUTTER = 24;
  // Figma mobile/h1: 38px, minus 1.5 percent (components/tokens.css)
  var HERO_FS_MOBILE = 38,
    HERO_TRACK_MOBILE = -0.015;
  function mobileOpt() {
    return W < MOBILE_BP;
  }
  // At the mobile size the copy re-wraps to the column instead of
  // shrinking. The desktop line breaks are dropped, so a short last word
  // never strands on a line of its own.
  function fitLines(lines, fs) {
    if (!mobileOpt()) return lines;
    var maxW = W - 2 * MOBILE_GUTTER,
      out = [];
    var words = lines.join(" ").split(" "),
      cur = "";
    c.save();
    heroFont(fs);
    for (var j = 0; j < words.length; j++) {
      var next = cur ? cur + " " + words[j] : words[j];
      if (cur && c.measureText(next).width > maxW) {
        out.push(cur);
        cur = words[j];
      } else cur = next;
    }
    out.push(cur);
    c.restore();
    return out;
  }

  function drawCopyTwoBeat(st, tb, e, f, isMagic, innReady) {
    var out = f >= FIRST_COPY_EXIT_PROGRESS;
    var inn = isMagic && innReady;
    if (st.copyKA === undefined) {
      st.copyKA = 0;
      st.copyKB = 0;
    }
    // on scroll-back, line one holds offstage until line two has fully
    // left — the two beats never share the stage in either direction
    var outHold = out || st.copyKB > 0.06;
    if (REDUCED) {
      st.copyKA = out ? 1 : 0;
      st.copyKB = inn ? 1 : 0;
    } else {
      // exits are brisk, arrivals stay gentle
      var tA = outHold ? 1 : 0,
        tB = inn ? 1 : 0;
      st.copyKA += (tA - st.copyKA) * (tA > st.copyKA ? 0.22 : 0.1);
      st.copyKB += (tB - st.copyKB) * (tB < st.copyKB ? 0.22 : 0.1);
    }
    var gate = copyGate(tb);
    // fades hold their ground: no drift out or in — the words simply
    // appear and disappear in place
    drawCopy(COPY_A, (1 - st.copyKA) * gate, e, 0, null, "beatA");
    drawCopy(COPY_B, st.copyKB * gate, e, 0, null, "beatB");
  }

  function drawCopy(lines, alpha, e, yOff, fsIn, key) {
    yOff = yOff || 0;
    var cs = copyState(key || lines.join("\u0001"), e);
    if (alpha <= 0.004) {
      cs.t0 = e;
      return;
    } // invisible: rearm
    if (e - cs.lastDrawn > 0.3) cs.t0 = e; // returning: replay
    cs.lastDrawn = e;

    c.save();
    c.fillStyle = COPY_INK || INK;
    c.textAlign = "left";
    c.textBaseline = "middle";
    var fs = fsIn || heroFs(),
      i,
      j; // scales down to fit
    if (!fsIn) {
      lines = fitLines(lines, fs);
      heroFont(fs);
      var widest = 0;
      for (i = 0; i < lines.length; i++)
        widest = Math.max(widest, c.measureText(lines[i]).width);
      if (widest > W * 0.86) fs = (fs * (W * 0.86)) / widest;
      fs = Math.min(fs, (H * 0.86) / (lines.length * HERO_LEAD));
      // the block's top must clear the nav band on short viewports
      var half = ((lines.length - 1) * HERO_LEAD + 1) / 2; // half-height in fs units
      fs = Math.max(12, Math.min(fs, (H / 2 - 48) / half));
    }
    heroFont(fs.toFixed(1));
    var lead = fs * HERO_LEAD,
      sp = c.measureText(" ").width;
    var wi = 0; // word index, global
    for (i = 0; i < lines.length; i++) {
      var words = lines[i].split(" ");
      var total = 0,
        wids = [];
      for (j = 0; j < words.length; j++) {
        wids.push(c.measureText(words[j]).width);
        total += wids[j];
      }
      total += sp * (words.length - 1);
      var x = W / 2 - total / 2;
      var y = H / 2 + yOff + (i - (lines.length - 1) / 2) * lead;
      for (j = 0; j < words.length; j++) {
        var wt = REDUCED
          ? 1
          : Math.min(1, Math.max(0, (e - cs.t0 - wi * 0.09) / 0.32));
        wt = 1 - Math.pow(1 - wt, 3);
        if (wt > 0.004) {
          c.globalAlpha = alpha * wt;
          c.fillText(words[j], x, y + (1 - wt) * 6);
        }
        x += wids[j] + sp;
        wi++;
      }
    }
    c.restore();
  }

  var ENTER = { lr: 0, m: 0 };

  // ---------------------------------------------------------- draw helpers
  // Draws in design space: 1440 wide, scaled and centred by computeGeo(),
  // clipped to the design height.
  function withDesign(fn) {
    c.save();
    if (mobileOpt())
      c.scale(W / 1440, GEO.s); // all three counters in frame
    else {
      c.translate(GEO.ox, 0);
      c.scale(GEO.s, GEO.s);
    } // ox 0 on desktop; centres phones
    c.beginPath();
    c.rect(0, 0, 1440, GEO.dh);
    c.clip();
    fn(GEO.s);
    c.restore();
    return GEO.s;
  }

  // one counter, with optional rotation about its centroid and an extra
  // offset
  function clampBleed(key, dy) {
    // full-bleed is a law, not a tuning: the sides' bottoms (design y
    // 2596.84) stay at/below the stage floor, the middle's top (design
    // y -1634.84) stays at/above the ceiling — for every offset anyone
    // ever asks for
    if (key === "M") return Math.min(dy, 1634.84);
    return Math.max(dy, GEO.dh - 2596.84);
  }
  function counter(key, dy, opts) {
    dy = clampBleed(key, dy);
    opts = opts || {};
    var enter = key === "M" ? ENTER.m : ENTER.lr;
    c.save();
    c.translate(opts.ox || 0, dy + (opts.oy || 0) + enter);
    if (opts.rot) {
      c.translate(CEN[key][0], CEN[key][1]);
      c.rotate(opts.rot);
      c.translate(-CEN[key][0], -CEN[key][1]);
    }
    c.fillStyle = opts.fill;
    c.fill(P[key]);
    c.restore();
  }

  // The counters enter from opposite edges before the first headline appears.
  function enterShapes(tb) {
    var a = REDUCED ? 1 : Math.min(1, Math.max(0, (tb - 0.15) / 0.9));
    a = 1 - Math.pow(1 - a, 3);
    // viewport-true amplitude: the shapes BEGIN fully off the stage —
    // the sides below the bottom edge, the mid above the top — and
    // travel in; thresholds derived live so it holds at any height
    var eLR = GEO.dh - 730 - GEO.dLR0 + 40;
    var eM = 232 + 40;
    ENTER.lr = (1 - a) * eLR;
    ENTER.m = -(1 - a) * eM;
  }
  function copyGate(tb) {
    if (REDUCED) return 1;
    return Math.min(1, Math.max(0, (tb - 0.45) / 0.2));
  }

  // ---- Beat 2: the pixel galaxy (arms) ----
  // Measure the second headline before building the seeded field so cells
  // stay outside its clear area, including after a viewport resize.
  var GALAXY_SEED = 7;
  // Galaxy bg: beat two's ground can be one of the logo colours. The
  // transition is the middle counter itself — at the kiss it scales up
  // UNIFORMLY about its centroid (the trapezoid's angles are the M's
  // counterform; they never distort) until it covers the stage, and the
  // colour it wears becomes the ground. Counters permute per scheme so
  // the middle always carries the target colour.
  var BG_SCHEMES = {
    Gray: { bg: null, fills: { L: SKY, M: ORG, R: YEL }, ink: INK },
    Orange: {
      bg: ORG,
      fills: { L: SKY, M: ORG, R: YEL },
      ink: TOK("--color-text-inverse"),
    },
    Yellow: { bg: YEL, fills: { L: SKY, M: YEL, R: ORG }, ink: INK },
    Blue: {
      bg: SKY,
      fills: { L: ORG, M: SKY, R: YEL },
      ink: TOK("--color-text-inverse"),
    },
  };
  var WIPE_S = 0.7; // the wipe's duration, s
  function wipeCoverK(tM) {
    // smallest uniform scale about the mid counter's kiss centroid that
    // covers the design viewport (convex quad: binary search + inclusion)
    var poly = VERT.M.map(function (v) {
      return [v[0], v[1] + tM];
    });
    var cx = CEN.M[0],
      cy = CEN.M[1] + tM;
    function inside(px, py, k) {
      var q = poly.map(function (v) {
        return [cx + (v[0] - cx) * k, cy + (v[1] - cy) * k];
      });
      var sgn = 0;
      for (var i = 0; i < q.length; i++) {
        var a = q[i],
          b = q[(i + 1) % q.length];
        var cr = (b[0] - a[0]) * (py - a[1]) - (b[1] - a[1]) * (px - a[0]);
        if (cr !== 0) {
          if (sgn === 0) sgn = cr > 0 ? 1 : -1;
          else if ((cr > 0 ? 1 : -1) !== sgn) return false;
        }
      }
      return true;
    }
    var corners = [
      [0, 0],
      [1440, 0],
      [0, GEO.dh],
      [1440, GEO.dh],
    ];
    var lo = 1,
      hi = 64;
    for (var n = 0; n < 26; n++) {
      var mid = (lo + hi) / 2,
        ok = true;
      for (var ci = 0; ci < 4; ci++)
        if (!inside(corners[ci][0], corners[ci][1], mid)) {
          ok = false;
          break;
        }
      if (ok) hi = mid;
      else lo = mid;
    }
    return hi;
  }
  var GALAXY_LOGO = [
    { hex: TOK("--color-spectrum-yellow-600"), w: 30 },
    { hex: TOK("--color-accent-blue"), w: 10 },
    { hex: TOK("--color-accent-orange"), w: 8 },
  ];
  function galaxyCopyBox() {
    // line two's rendered box, from the shared fit
    var fs = heroFs();
    var lines = fitLines(COPY_B, fs);
    c.save();
    heroFont(fs);
    var widest = 0;
    for (var i = 0; i < lines.length; i++)
      widest = Math.max(widest, c.measureText(lines[i]).width);
    c.restore();
    if (widest > W * 0.86) {
      fs = (fs * (W * 0.86)) / widest;
      widest = W * 0.86;
    }
    fs = Math.min(fs, (H * 0.86) / (lines.length * HERO_LEAD));
    if (mobileOpt()) {
      var hy = ((lines.length - 1) * fs * HERO_LEAD + fs) / 2 + 6;
      return { hx: widest / 2, hy: hy, n: lines.length, fs: fs };
    }
    // half-height: half the leaded block, plus the line's own half-body
    // margin, plus the arrival drift (line two lands from +26·s below)
    return {
      hx: widest / 2,
      hy: ((COPY_B.length - 1) * fs * HERO_LEAD + fs) / 2 + 26 * GEO.s + 6,
    };
  }
  function galaxyBuild(st, bg) {
    var box = galaxyCopyBox();
    var scheme = BG_SCHEMES[bg] || BG_SCHEMES.Gray;
    var palette = null;
    if (scheme.bg) {
      // coloured ground: Spectrum only, with the ground's colour omitted
      palette = GALAXY.PALETTE.filter(function (p) {
        return p.hex !== scheme.bg;
      });
    } else palette = GALAXY_LOGO;
    var mob = mobileOpt(),
      place = null;
    // the hole hugs the copy, so the arms fill above and below it
    if (mob) place = { rx: W * 0.42, ry: Math.max(box.hy * 1.9, W * 0.62) };
    st.gal = GALAXY.buildField(
      GALAXY_SEED,
      W,
      H,
      box.hx,
      box.hy,
      palette,
      place,
    );
    st.galBg = bg;
    st.galMob = mob;
  }

  function drawCounters(
    scene,
    scheme,
    entranceSeconds,
    countersConverged,
    counterProgress,
    convergenceSeconds,
  ) {
    if (!countersConverged) {
      withDesign(function () {
        enterShapes(entranceSeconds);
        counter("L", GEO.dLR0 + GEO.tLR * counterProgress, {
          fill: scheme.fills.L,
        });
        if (!(scheme.bg && scene.wipeK > 0.05))
          counter("M", GEO.mRest + (GEO.tM - GEO.mRest) * counterProgress, {
            fill: scheme.fills.M,
          });
        counter("R", GEO.dLR0 + GEO.tLR * counterProgress, {
          fill: scheme.fills.R,
        });
      });
    } else {
      // Gray fades the three; a coloured ground fades NOTHING — the
      // sides hold full ink at their kiss positions and the wipe covers
      // them, so paper never flashes through the transition
      var hold = scheme.bg
        ? scene.wipeK >= 0.999
          ? 0
          : 1
        : REDUCED
          ? 0
          : Math.max(0, 1 - convergenceSeconds / COUNTER_FADE_SECONDS);
      if (hold > 0.004) {
        c.save();
        c.globalAlpha = hold;
        withDesign(function () {
          enterShapes(entranceSeconds);
          counter("L", GEO.dLR0 + GEO.tLR, { fill: scheme.fills.L });
          if (!scheme.bg) counter("M", GEO.tM, { fill: scheme.fills.M });
          counter("R", GEO.dLR0 + GEO.tLR, { fill: scheme.fills.R });
        });
        c.restore();
      }
    }
  }

  function drawBackgroundWipe(
    scene,
    scheme,
    countersConverged,
    counterProgress,
    convergenceSeconds,
  ) {
    // the wipe: forward on the kiss clock; on scroll-back it recedes
    if (scene.wipeK === undefined) scene.wipeK = 0;
    if (scheme.bg) {
      if (countersConverged)
        scene.wipeK = REDUCED ? 1 : Math.min(1, convergenceSeconds / WIPE_S);
      else scene.wipeK = REDUCED ? 0 : scene.wipeK * 0.7;
      if (scene.wipeK > 0.004) {
        var wu =
          scene.wipeK < 0.5
            ? 4 * scene.wipeK * scene.wipeK * scene.wipeK
            : 1 - Math.pow(-2 * scene.wipeK + 2, 3) / 2;
        if (scene.wipeDh !== GEO.dh || scene.wipeTm !== GEO.tM) {
          scene.wipeKstar = wipeCoverK(GEO.tM);
          scene.wipeDh = GEO.dh;
          scene.wipeTm = GEO.tM;
        }
        var wk = 1 + (scene.wipeKstar - 1) * wu;
        var midOff = clampBleed(
          "M",
          GEO.mRest +
            (GEO.tM - GEO.mRest) * (countersConverged ? 1 : counterProgress),
        ); // rides the rewind
        withDesign(function () {
          c.globalAlpha = 1; // never fades: it covers, or it recedes
          if (wu >= 0.999) {
            c.fillStyle = scheme.bg;
            c.fillRect(0, 0, 1440, GEO.dh);
          } else {
            var cx = CEN.M[0],
              cy = CEN.M[1] + midOff;
            c.translate(cx, cy);
            c.scale(wk, wk);
            c.translate(-cx, -cy);
            c.translate(0, midOff);
            c.fillStyle = scheme.bg;
            c.fill(P.M);
          }
          c.globalAlpha = 1;
        });
      }
    } else scene.wipeK = 0;
    COPY_INK = scheme.bg && scene.wipeK > 0.55 ? scheme.ink : null;
  }

  function drawGalaxy(scene, settings, elapsedSeconds, countersConverged) {
    if (scene.gal) {
      // Rebuild on resize so the field stays centred and its clear area
      // follows the rewrapped headline. The seed preserves its arrangement.
      if (
        scene.galBg !== settings.bg ||
        scene.galMob !== mobileOpt() ||
        scene.gal.W !== W ||
        scene.gal.H !== H
      )
        galaxyBuild(scene, settings.bg);
      var target = countersConverged && scene.galT0 !== null ? 1 : 0;
      if (REDUCED) scene.galA = target;
      else
        scene.galA += (target - scene.galA) * (countersConverged ? 0.25 : 0.22);
      if (
        scene.galA > 0.004 &&
        scene.galFreeze === undefined &&
        scene.galT0 === null
      )
        scene.galFreeze = scene.galLastT || 0;
      if (scene.galT0 !== null) scene.galFreeze = undefined;
      if (scene.galA > 0.004) {
        var realMs =
          scene.galT0 !== null
            ? Math.max(0, (elapsedSeconds - scene.galT0) * 1000)
            : scene.galFreeze || 0;
        scene.galLastT = realMs;
        var settleAt = scene.gal.settleAt;
        if (scene.rotAcc === undefined) {
          scene.rotAcc = 0;
          scene.galLastE = elapsedSeconds;
        }
        var dtMs = Math.max(0, (elapsedSeconds - scene.galLastE) * 1000);
        scene.galLastE = elapsedSeconds;
        if (realMs > settleAt) scene.rotAcc += dtMs;
        var tMs = REDUCED
          ? SETTLED_GALAXY_TIME_MS
          : realMs <= settleAt
            ? realMs
            : settleAt + scene.rotAcc;
        var rects = GALAXY.sampleField(scene.gal, tMs, !REDUCED);
        c.save();
        c.globalAlpha = scene.galA;
        for (var rn = 0; rn < rects.length; rn++) {
          var rr = rects[rn];
          c.fillStyle = rr.color;
          var x = Math.round(rr.x * dpr) / dpr;
          var y = Math.round(rr.y * dpr) / dpr;
          c.fillRect(
            x,
            y,
            Math.round((rr.x + rr.w) * dpr) / dpr - x,
            Math.round((rr.y + rr.h) * dpr) / dpr - y,
          );
        }
        c.restore();
      }
    }
  }

  // Frame order matters: retire the first copy, converge the counters, cover
  // the background, then burst the galaxy and reveal the second copy.
  function createSceneState() {
    // LP state names: magicT is convergence time; galT0 starts the burst;
    // galA is galaxy opacity; coverT records when the background is ready.
    return {
      wasMagic: false,
      gal: null,
      galT0: null,
      galA: 0,
      magicT: null,
      coverT: undefined,
    };
  }

  function drawScene(settings, scene, elapsedSeconds) {
    if (scene.born === undefined) scene.born = elapsedSeconds;
    var entranceSeconds = elapsedSeconds - scene.born;
    var progress = Math.min(1, Math.max(0, settings.progress || 0));
    var journeyProgress = magJ(progress);
    // Hold the counters until the first headline has mostly faded out.
    var copyExitGate = REDUCED
      ? 1
      : Math.max(0, Math.min(1, ((scene.copyKA || 0) - 0.55) / 0.4));
    var counterProgress = journeyProgress * copyExitGate;
    var countersConverged = counterProgress >= GEO.pstar;
    if (countersConverged && !scene.wasMagic) {
      scene.magicT = elapsedSeconds;
      // Wait for coverage before starting the burst; reversing resets its clock.
      if (!scene.gal || scene.galBg !== settings.bg)
        galaxyBuild(scene, settings.bg);
    }
    scene.wasMagic = countersConverged;
    c.fillStyle = PAPER;
    c.fillRect(0, 0, W, H);

    var convergenceSeconds = countersConverged
      ? elapsedSeconds - scene.magicT
      : 0;
    var scheme = BG_SCHEMES[settings.bg] || BG_SCHEMES.Gray;

    // Gray waits for the counters to fade. Coloured backgrounds start the
    // burst near the end of the wipe, at about 93% viewport coverage.
    // Read the preceding frame's coverage, preserving LP's frame ordering.
    var covered = scheme.bg
      ? scene.wipeK >= WIPE_GALAXY_START_PROGRESS
      : countersConverged && convergenceSeconds >= COUNTER_FADE_SECONDS;
    if (covered && scene.coverT === undefined) scene.coverT = elapsedSeconds;
    if (!covered) scene.coverT = undefined;
    var backgroundCovered = scene.coverT !== undefined;
    if (backgroundCovered && scene.galT0 === null) {
      scene.galT0 = elapsedSeconds;
      scene.rotAcc = 0;
      scene.galLastE = elapsedSeconds;
    }
    if (!countersConverged) scene.galT0 = null;

    drawCounters(
      scene,
      scheme,
      entranceSeconds,
      countersConverged,
      counterProgress,
      convergenceSeconds,
    );
    drawBackgroundWipe(
      scene,
      scheme,
      countersConverged,
      counterProgress,
      convergenceSeconds,
    );
    drawGalaxy(scene, settings, elapsedSeconds, countersConverged);

    var secondCopyReady =
      scene.galT0 !== null && elapsedSeconds - scene.galT0 > COPY_AFTER;
    drawCopyTwoBeat(
      scene,
      entranceSeconds,
      elapsedSeconds,
      journeyProgress,
      countersConverged,
      REDUCED ? countersConverged : secondCopyReady,
    );
  }

  var state = createSceneState();
  return {
    resize,
    draw(progress, elapsedMs, reducedMotion) {
      if (!W || !H) return;
      if (REDUCED !== reducedMotion) {
        state = createSceneState();
        COPY_STATE.length = 0;
      }
      REDUCED = reducedMotion;
      GEO = computeGeo();
      const settings = {
        progress,
        bg: background,
      };
      if (REDUCED) {
        // LP reads coverage from the preceding frame. Resolve the entrance,
        // coverage and settled field in order, without scheduling animation.
        // Ten seconds between samples exceeds every entrance/wipe delay.
        state = createSceneState();
        COPY_STATE.length = 0;
        settings.progress = progress >= REDUCED_MOTION_SECOND_BEAT ? 1 : 0;
        drawScene(settings, state, 0);
        drawScene(settings, state, 10);
        drawScene(settings, state, 20);
      } else {
        drawScene(settings, state, elapsedMs / 1000);
      }
      return COPY_INK || INK;
    },
  };
}
