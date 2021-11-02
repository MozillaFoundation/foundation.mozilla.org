import { Chart, registerables } from "chart.js";

export const initYouTubeRegretsRegretRatesChart = () => {
  Chart.register(...registerables);

  const labels = [
    gettext("Brazil"),
    gettext("Germany"),
    gettext("France"),
    gettext("Japan"),
    gettext("Poland"),
    gettext("India"),
    gettext("Spain"),
    gettext("Mexico"),
    gettext("United States"),
    gettext("Turkey"),
    gettext("Finland"),
    gettext("Sweden"),
    gettext("Netherlands"),
    gettext("Norway"),
    gettext("New Zealand"),
    gettext("United Kingdom"),
    gettext("Ireland"),
    gettext("South Africa"),
    gettext("Italy"),
    gettext("Portugal"),
    gettext("Indonesia"),
    gettext("Australia"),
    gettext("Switzerland"),
    gettext("Bangladesh"),
    gettext("Czechia"),
    gettext("Canada"),
    gettext("Austria"),
    gettext("Denmark"),
  ];

  const data = [
    21.89752274, 21.09878711, 20.15801721, 18.43997787, 16.55023432,
    15.30387998, 15.04163309, 13.67011526, 13.34734649, 12.84698325,
    12.63802049, 12.30419762, 11.1181114, 9.55535737, 9.171212048, 8.968666115,
    8.778530223, 8.430062901, 8.371703642, 8.064922627, 8.044435932,
    7.742360596, 7.347047823, 7.221259388, 7.1864894, 7.01534607, 5.290538753,
    4.871869824,
  ];

  const primaryEnglish = [
    gettext("United States"),
    gettext("New Zealand"),
    gettext("United Kingdom"),
    gettext("Ireland"),
    gettext("Australia"),
    gettext("Canada"),
  ];

  const bgColors = {
    dark: "#FC4147",
    light: "#FBD5D7",
  };

  const categoriesChart = document.getElementById("regret-rates-chart");
  const ctx = categoriesChart.getContext("2d");

  const chart = new Chart(ctx, {
    type: "bar",
    data: {
      labels,
      datasets: [
        {
          data,
          backgroundColor: labels.map((label) =>
            primaryEnglish.includes(label) ? bgColors.dark : bgColors.light
          ),
        },
      ],
    },
    options: {
      maintainAspectRatio: false,
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
            text: gettext("Regrets Per 10000 Videos"),
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
