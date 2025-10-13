// Valor máximo de estadística base
const MAX_STAT = 255;

// Asignar ancho proporcional
document.querySelectorAll('.progress-bar').forEach(bar => {
    const value = parseInt(bar.dataset.value);
    const percentage = (value / MAX_STAT) * 100;
    bar.style.width = `${percentage}%`;
    bar.setAttribute('aria-valuenow', value);
    bar.setAttribute('aria-valuemin', 0);
    bar.setAttribute('aria-valuemax', MAX_STAT);
});