import { Chart, registerables } from 'chart.js';

document.addEventListener('DOMContentLoaded', () => {
  Chart.register(...registerables);

  const labels = [
    'MISINFORMATION',
    'VIOLENT OR GRAPHIC CONTENT',
    'COVID-19 MISINFORMATION',
    'HATE SPEECH',
    'SPAM',
    'NUDITY & SEXUAL CONTENT',
    'CHILD SAFETY',
    'HARASSMENT & CYBERBULLYING',
    'HARMFUL OR DANGEROUS',
    'OTHER',
    'FIREARMS',
    'IMPERSONATION',
    'ANIMAL ABUSE',
    'AGE-RESTRICTED CONTENT',
    'VIOLENT CRIMINAL ORGS',
    'FAKE ENGAGEMENT'
  ]

  const data = [
    26,
    19,
    16,
    16,
    13,
    9,
    8,
    5,
    4,
    3,
    3,
    2,
    2,
    2,
    1,
    1,
  ]

  const categoriesChart = document.getElementById('categories-bar-chart');
  const ctx = categoriesChart.getContext('2d');

  const chart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        data,
          backgroundColor: [
            '#800000',
            '#BF0000',
            '#FF0000',
            '#FC666C',
            '#F9CBD7',
            '#FFF1F5',
            '#BFBFBF',
            '#808080',
            '#404040',
            '#2D2E7A',
            '#4345B6',
            '#595CF3',
            '#A0A2F8',
            '#E7E7FC',
            '#FFFFFF',
          ],
        }]
      },
    options: {
      indexAxis: 'y',
      plugins: {
        legend: {
          display: false
        }
      },
      scales: {
        x: {
          grid: {
            color: 'rgba(255, 255, 255, 0.5)'
          },
          ticks: {
            stepSize: 10,
            color: "white",
            font: {
              size: 12,
              family: "Nunito Sans",
            },
            callback: function(value) {
              return `${value}%`;
            },
          }
        },
        y: {
          gridLines: {
            zeroLineColor: '#ffcc33'
          },
          ticks: {
            color: "white",
            font: {
              size: 12,
              family: "Nunito Sans",
            },
          }
        }
      }
    }
  });
});
