import { Chart, registerables } from "chart.js";

export const initYouTubeRegretsRegretRatesChart = () => {
  Chart.register(...registerables);

  const labels = [
    "Brazil",
    "Germany",
    "France",
    "Japan",
    "Poland",
    "India",
    "Spain",
    "Mexico",
    "United States",
    "Turkey",
    "Finland",
    "Sweden",
    "Netherlands",
    "Norway",
    "New Zealand",
    "United Kingdom",
    "Ireland",
    "South Africa",
    "Italy",
    "Portugal",
    "Indonesia",
    "Australia",
    "Switzerland",
    "Bangladesh",
    "Czechia",
    "Canada",
    "Austria",
    "Denmark",
  ];

  const data = [
    21.89752274,
    21.09878711,
    20.15801721,
    18.43997787,
    16.55023432,
    15.30387998,
    15.04163309,
    13.67011526,
    13.34734649,
    12.84698325,
    12.63802049,
    12.30419762,
    11.1181114,
    9.55535737,
    9.171212048,
    8.968666115,
    8.778530223,
    8.430062901,
    8.371703642,
    8.064922627,
    8.044435932,
    7.742360596,
    7.347047823,
    7.221259388,
    7.1864894,
    7.01534607,
    5.290538753,
    4.871869824,
  ];

  const categoriesChart = document.getElementById("regret-rates-chart");
  const ctx = categoriesChart.getContext("2d");

  const chart = new Chart(ctx, {
    type: "bar",
    data: {
      labels,
      datasets: [
        {
          data,
          backgroundColor: [
            "#FBD5D7",
            "#FBD5D7",
            "#FBD5D7",
            "#FBD5D7",
            "#FBD5D7",
            "#FBD5D7",
            "#FBD5D7",
            "#FC4147",
            "#FBD5D7",
            "#FBD5D7",
            "#FBD5D7",
            "#FBD5D7",
            "#FBD5D7",
            "#FBD5D7",
            "#FC4147",
            "#FC4147",
            "#FBD5D7",
            "#FC4147",
            "#FBD5D7",
            "#FBD5D7",
            "#FBD5D7",
            "#FBD5D7",
            "#FC4147",
            "#FC4147",
            "#FBD5D7",
            "#FBD5D7",
            "#FC4147",
            "#FBD5D7",
            "#FBD5D7",
          ],
        },
      ],
    },
    options: {
      indexAxis: "y",
      plugins: {
        legend: {
          display: false,
        },
      },
      scales: {
        x: {
          title: {
            display: true,
            text: "Regrets Per 10000 Videos",
            padding: {
              top: 20,
            },
            font: {
              size: 18,
              family: "Nunito Sans",
              weight: "400",
              color: "#263238",
            },
          },
          grid: {
            color: "#e5e5e5",
          },
          ticks: {
            stepSize: 5,
            color: "#000",
            font: {
              size: 12,
              family: "Nunito Sans",
            },
          },
        },
        y: {
          grid: {
            color: "transparent",
          },
          ticks: {
            display: true,
            color: "#000",
            font: {
              size: 12,
              family: "Nunito Sans",
              weight: "700",
            },
          },
          pointLabels: {
            fontStyle: "bold",
          },
        },
      },
    },
  });
};
