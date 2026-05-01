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
    tierRadiusPercent: { 1: 8.4, 2: 6.3, 3: 4.6 },
    tiers: [
      {
        tier: 1,
        positions: [[59, 46]],
      },
      {
        tier: 2,
        positions: [
          [41, 46],
          [63, 15],
          [78, 31],
          [92, 57],
          [77, 65],
          [25, 51],
          [36, 78],
        ],
      },
      {
        tier: 3,
        positions: [
          [90, 21],
          [64, 77],
          [50, 74],
          [11, 53],
          [19, 75],
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
        positions: [[52, 28]],
      },
      {
        tier: 2,
        positions: [
          [49, 9],
          [81, 11],
        ],
      },
      {
        tier: 3,
        positions: [
          [15, 13],
          [20, 29],
          [17, 44],
          [84, 26],
        ],
      },
      {
        tier: 4,
        positions: [
          [83, 45],
          [60, 46],
          [41, 44],
          [77, 55],
          [19, 57],
          [42, 58],
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
        positions: [[42, 9]],
      },
      {
        tier: 3,
        positions: [
          [79, 13],
          [22, 26],
          [28, 45],
          [23, 63],
          [68, 58],
        ],
      },
      {
        tier: 4,
        positions: [
          [75, 73],
          [16, 79],
          [50, 82],
          [78, 90],
          [21, 95],
          [53, 98],
        ],
      },
    ],
  },
};
