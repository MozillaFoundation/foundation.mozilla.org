// ─── Breakpoints (match SCSS customized-settings.scss) ───────────────────────
export const BREAKPOINTS = { sm: 375, md: 640, lg: 1024, xl: 1200 };

// ─── Per-breakpoint configs ───────────────────────────────────────────────────
// Mobile configs (xs–lg): computeHeight=true, JS sets viz height from simulation output.
// Desktop configs (xl–xxl): computeHeight=false, CSS sets viz height.
// All entries use the same d3-force simulation; only starting positions differ.
// tierRadiusPercent: fixed bubble radius per tier as a percentage of vizW (e.g. 7 = 7%).
export const CONFIGS = {
  // ≥ 1200px
  xl: {
    computeHeight: false,
    tierRadiusPercent: { 1: 10, 2: 6.5, 3: 4.5 },
    tiers: [
      {
        tier: 1,
        positions: [[59, 50]],
      },
      {
        tier: 2,
        positions: [
          [40, 46],
          [63, 15],
          [78, 32],
          [92, 57],
          [77, 65],
          [25, 54],
        ],
      },
      {
        tier: 3,
        positions: [
          [21, 81],
          [90, 21],
          [50, 80],
          [37, 76],
          [11, 53],
          [9, 78],
        ],
      },
    ],
  },
  // 1024–1199px
  lg: {
    computeHeight: false,
    tierRadiusPercent: { 1: 10, 2: 7, 3: 5 },
    tiers: [
      {
        tier: 1,
        positions: [[58, 50]],
      },
      {
        tier: 2,
        positions: [
          [38, 51],
          [60, 18],
          [78, 31],
          [92, 56],
          [76, 71],
          [23, 59],
        ],
      },
      {
        tier: 3,
        positions: [
          [24, 84],
          [93, 20],
          [60, 80],
          [40, 78],
          [7, 59],
          [8, 83],
        ],
      },
    ],
  },
  // 640–1023px
  md: {
    computeHeight: true,
    containerAspect: 2.5,
    tierRadiusPercent: { 1: 18, 2: 13, 3: 11, 4: 9 },
    tiers: [
      {
        tier: 1,
        positions: [[52, 32]],
      },
      {
        tier: 2,
        positions: [
          [49, 11],
          [81, 13],
        ],
      },
      {
        tier: 3,
        positions: [
          [21, 15],
          [20, 31],
          [26, 47],
          [84, 30],
        ],
      },
      {
        tier: 4,
        positions: [
          [79, 44],
          [42, 65],
          [52, 49],
          [73, 59],
          [19, 62],
          [64, 73],
        ],
      },
    ],
  },
  // < 640px
  sm: {
    computeHeight: true,
    containerAspect: 3,
    tierRadiusPercent: { 1: 23, 2: 18, 3: 15, 4: 12 },
    tiers: [
      {
        tier: 1,
        positions: [[69, 34]],
      },
      {
        tier: 2,
        positions: [[30, 9]],
      },
      {
        tier: 3,
        positions: [
          [69, 13],
          [22, 33],
          [28, 52],
          [23, 71],
          [68, 55],
        ],
      },
      {
        tier: 4,
        positions: [
          [73, 72],
          [16, 91],
          [50, 87],
          [78, 94],
          [35, 107],
          [68, 111],
        ],
      },
    ],
  },
};
