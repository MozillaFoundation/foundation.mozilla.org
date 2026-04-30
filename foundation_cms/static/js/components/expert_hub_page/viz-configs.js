// ─── Breakpoints (match SCSS customized-settings.scss) ───────────────────────
export const BREAKPOINTS = { sm: 375, md: 480, lg: 768, xl: 1024, xxl: 1200 };

// Shared tier weights for xl and xxl desktop configs
const WEIGHTS_DESKTOP = { 1: 4, 2: 2, 3: 1 };

// ─── Per-breakpoint configs ───────────────────────────────────────────────────
// Mobile configs (xs–lg): computeHeight=true, JS sets viz height from simulation output.
// Desktop configs (xl–xxl): computeHeight=false, CSS sets viz height.
// All entries use the same d3-force simulation; only starting positions differ.
export const CONFIGS = {
  // ≥ 1200px
  xxl: {
    computeHeight: false,
    packFactor: 0.3,
    tierWeights: WEIGHTS_DESKTOP,
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
  xl: {
    computeHeight: false,
    packFactor: 0.25,
    tierWeights: WEIGHTS_DESKTOP,
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
  // 768–1023px
  lg: {
    computeHeight: true,
    containerAspect: 2.2,
    packFactor: 0.4,
    tierWeights: { 1: 3.2, 2: 2.5, 3: 1.5, 4: 0.7 },
    tiers: [
      {
        tier: 1,
        positions: [[75, 36]],
      },
      {
        tier: 2,
        positions: [[40, 12]],
      },
      {
        tier: 3,
        positions: [
          [82, 13],
          [18, 30],
          [32, 50],
          [48, 88],
          [55, 69],
        ],
      },
      {
        tier: 4,
        positions: [
          [18, 67],
          [82, 57],
          [15, 82],
          [82, 80],
          [20, 98],
          [80, 96],
        ],
      },
    ],
  },
  // 480–767px
  md: {
    computeHeight: true,
    containerAspect: 2.5,
    packFactor: 0.33,
    tierWeights: { 1: 3.2, 2: 2.5, 3: 1.5, 4: 0.7 },
    tiers: [
      {
        tier: 1,
        positions: [[74, 34]],
      },
      {
        tier: 2,
        positions: [[40, 12]],
      },
      {
        tier: 3,
        positions: [
          [80, 10],
          [18, 28],
          [32, 47],
          [48, 88],
          [56, 68],
        ],
      },
      {
        tier: 4,
        positions: [
          [18, 64],
          [76, 55],
          [15, 79],
          [78, 82],
          [20, 98],
          [80, 96],
        ],
      },
    ],
  },
  // 375–479px
  sm: {
    computeHeight: true,
    containerAspect: 2.8,
    packFactor: 0.22,
    tierWeights: { 1: 4, 2: 2.5, 3: 1.5, 4: 0.7 },
    tiers: [
      {
        tier: 1,
        positions: [[70, 29]],
      },
      {
        tier: 2,
        positions: [[40, 9]],
      },
      {
        tier: 3,
        positions: [
          [80, 9],
          [18, 27],
          [28, 43],
          [48, 83],
          [55, 62],
        ],
      },
      {
        tier: 4,
        positions: [
          [18, 58],
          [72, 47],
          [14, 73],
          [80, 76],
          [20, 96],
          [80, 92],
        ],
      },
    ],
  },
  // < 375px
  xs: {
    computeHeight: true,
    containerAspect: 3,
    packFactor: 0.22,
    tierWeights: { 1: 4, 2: 2.5, 3: 1.5, 4: 0.8 },
    tiers: [
      {
        tier: 1,
        positions: [[72, 31]],
      },
      {
        tier: 2,
        positions: [[40, 9]],
      },
      {
        tier: 3,
        positions: [
          [80, 12],
          [18, 27],
          [28, 45],
          [43, 80],
          [68, 64],
        ],
      },
      {
        tier: 4,
        positions: [
          [18, 61],
          [72, 49],
          [13, 74],
          [77, 83],
          [17, 94],
          [65, 97],
        ],
      },
    ],
  },
};
