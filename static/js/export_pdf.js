async function exportToPDF(contenedorId, nombreArchivo = "contenedor.pdf") {
  const { jsPDF } = window.jspdf;
  const contenedor = document.getElementById(contenedorId);

  if (!contenedor) {
    console.error("No se encontró el contenedor:", contenedorId);
    return;
  }

  // Renderiza el contenedor en alta resolución
  const canvas = await html2canvas(contenedor, { scale: 4, useCORS: true });
  const imgData = canvas.toDataURL("image/png", 1.0);

  // Crea y guarda el PDF
  const pdf = new jsPDF("p", "mm", "a4");
  const pdfWidth = pdf.internal.pageSize.getWidth();
  const pdfHeight = (canvas.height * pdfWidth) / canvas.width;

  pdf.addImage(imgData, "PNG", 0, 0, pdfWidth, pdfHeight);
  pdf.save(nombreArchivo);
}