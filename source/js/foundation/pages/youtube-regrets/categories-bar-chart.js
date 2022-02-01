import { Chart, registerables } from "chart.js";

/**
 * Using chart.js to render the regret category graph on the Youtube Regrets page.
 */

export const initYouTubeRegretsCategoriesBarChart = () => {
  Chart.register(...registerables);

  const labels = [
    gettext("MISINFORMATION"),
    gettext("VIOLENT OR GRAPHIC CONTENT"),
    gettext("COVID-19 MISINFORMATION"),
    gettext("HATE SPEECH"),
    gettext("SPAM, DECEPTIVE PRACTICES"),
    gettext("NUDITY & SEXUAL CONTENT"),
    gettext("CHILD SAFETY"),
    gettext("HARASSMENT & CYBERBULLYING"),
    gettext("HARMFUL OR DANGEROUS CONTENT"),
    gettext("OTHER"),
    gettext("FIREARMS"),
    gettext("IMPERSONATION"),
    gettext("ANIMAL ABUSE"),
    gettext("AGE-RESTRICTED CONTENT"),
    gettext("VIOLENT CRIMINAL ORGS"),
    gettext("FAKE ENGAGEMENT"),
  ];

  const data = [
    20, 14.6, 12.3, 12.3, 10.0, 6.9, 6.2, 3.8, 3.1, 2.3, 2.3, 1.5, 1.5, 1.5,
    0.8, 0.8,
  ];

  const categoriesChart = document.getElementById("categories-bar-chart");
  const ctx = categoriesChart.getContext("2d");
  const labelFormat = gettext("%s%");

  const chart = new Chart(ctx, {
    type: "bar",
    data: {
      labels,
      datasets: [
        {
          data,
          backgroundColor: [
            "#800000",
            "#BF0000",
            "#FF0000",
            "#FC666C",
            "#F99AB3",
            "#FFCFDB",
            "#DFDFDF",
            "#BFBFBF",
            "#808080",
            "#404040",
            "#2D2E7A",
            "#4345B6",
            "#595CF3",
            "#8F8BF0",
            "#ABADFC",
            "#E3E3FC",
          ],
        },
      ],
    },
    options: {
      responsive: true,
      scaleShowLabels: true,
      maintainAspectRatio: false,
      indexAxis: "y",
      plugins: {
        legend: {
          display: false,
        },
      },
      scales: {
        x: {
          grid: {
            color: "rgba(255, 255, 255, 0.5)",
          },
          ticks: {
            stepSize: 10,
            color: "white",
            font: {
              size: 12,
              family: "Nunito Sans",
            },
            callback: function (value) {
              return interpolate(labelFormat, [value]);
            },
          },
        },
        y: {
          gridLines: {
            zeroLineColor: "#ffcc33",
          },
          ticks: {
            color: "white",
            font: function (context) {
              var width = context.chart.width;
              const size = width >= 410 ? 12 : 8;

              return {
                family: "Nunito Sans",
                size: size,
              };
            },
          },
        },
      },
    },
  });
};
