// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

// Bar Chart Example
var ctx = document.getElementById("myBarChart");
var myLineChart = new Chart(ctx, {
  type: 'bar',
  data: {
    labels: JSON.parse(ctx.dataset.labels),
    datasets: [{
      label: "Vida",
      backgroundColor: "rgba(2,117,216,1)",
      borderColor: "rgba(2,117,216,1)",
      data: JSON.parse(ctx.dataset.vida),
    }],
  },
  options: {
    scales: {
      xAxes: [{
        gridLines: { display: false },
        ticks: {
          autoSkip: false,
          maxRotation: 60,
          minRotation: 30,
          fontSize: 16
        }
      }],
      yAxes: [{
        ticks: {
          beginAtZero: true
        }
      }]
    },
    legend: {
      display: false
    }
  }
});

document.getElementById("statSelect").addEventListener("change", function () {
  const selected = this.value;
  let label = "";
  let color = "";
  let data = [];

  switch (selected) {
    case "vida":
      label = "Vida (HP)";
      color = "rgba(2,117,216,1)";
      data = JSON.parse(ctx.dataset.vida);
      break;
    case "ataque":
      label = "Ataque";
      color = "rgba(220,53,69,1)";
      data = JSON.parse(ctx.dataset.ataque);
      break;
    case "defensa":
      label = "Defensa";
      color = "rgba(40,167,69,1)";
      data = JSON.parse(ctx.dataset.defensa);
      break;
    case "velocidad":
      label = "Velocidad";
      color = "rgba(255,193,7,1)";
      data = JSON.parse(ctx.dataset.velocidad);
      break;
    case "defensa-especial":
      label = "Defensa Especial";
      color = "rgba(255,193,7,1)";
      data = JSON.parse(ctx.dataset.defensaEspecial); // ✅ camelCase
      break;

    case "ataque-especial":
      label = "Ataque Especial";
      color = "rgba(255,99,132,1)";
      data = JSON.parse(ctx.dataset.ataqueEspecial); // ✅ camelCase
      break;
    case "num-pokemon":
      label = "Numero Pokemon";
      color = "rgba(255,99,132,1)";
      data = JSON.parse(ctx.dataset.numPokemon); // ✅ camelCase
      break;

  }

  myLineChart.data.datasets[0].label = label;
  myLineChart.data.datasets[0].backgroundColor = color;
  myLineChart.data.datasets[0].borderColor = color;
  myLineChart.data.datasets[0].data = data;
  myLineChart.update(); // 👈 esto actualiza las barras
});
