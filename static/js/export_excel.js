function exportToExcel(canvasId, nombreArchivo = "datos_chart.xlsx") {
  const canvas = document.getElementById(canvasId);

  if (!canvas) {
    console.error("No se encontró el canvas:", canvasId);
    return;
  }

  // Extraer datos del dataset
  const labels = JSON.parse(canvas.dataset.labels);
  const vida = JSON.parse(canvas.dataset.vida);
  const ataque = JSON.parse(canvas.dataset.ataque);
  const defensa = JSON.parse(canvas.dataset.defensa);
  const velocidad = JSON.parse(canvas.dataset.velocidad);
  const defensaEsp = JSON.parse(canvas.dataset.defensaEspecial);
  const ataqueEsp = JSON.parse(canvas.dataset.ataqueEspecial);
  const numPokemon = JSON.parse(canvas.dataset.numPokemon);

  // Prepara los datos para Excel
  const filas = labels.map((nombre, i) => ({
    Tipo: nombre,
    Vida: vida[i],
    Ataque: ataque[i],
    Defensa: defensa[i],
    Velocidad: velocidad[i],
    "Defensa Especial": defensaEsp[i],
    "Ataque Especial": ataqueEsp[i],
    "N° Pokémon": numPokemon[i]
  }));

  // Generar y descargar Excel
  const hoja = XLSX.utils.json_to_sheet(filas);
  const libro = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(libro, hoja, "Datos");
  XLSX.writeFile(libro, nombreArchivo);
}