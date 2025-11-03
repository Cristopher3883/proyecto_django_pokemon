document.addEventListener("DOMContentLoaded", () => {
  const select = document.getElementById("tipoDescarga");
  const boton = document.getElementById("btnDescargar");

  boton.addEventListener("click", async () => {
    const tipo = select.value;

    if (tipo === "pdf") {
      await exportToPDF("chartData", "grafico.pdf");
    } else if (tipo === "excel") {
      exportToExcel("myBarChart", "datos_chart.xlsx");
    } else {
      alert("Selecciona un tipo de descarga válido.");
    }
  });
});