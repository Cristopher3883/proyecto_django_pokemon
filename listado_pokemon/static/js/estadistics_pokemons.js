const MAX_STAT = 255;

document.addEventListener("DOMContentLoaded", () => {
    const bars = document.querySelectorAll('.progress-bar');

    bars.forEach(bar => {
        const value = parseInt(bar.dataset.value);
        const percentage = (value / MAX_STAT) * 100;

        // Reinicia a 0%
        bar.style.width = '0%';

        // Pequeño retraso para permitir que la transición se vea
        setTimeout(() => {
            bar.style.width = `${percentage}%`;
        }, 200);

        bar.setAttribute('aria-valuenow', value);
        bar.setAttribute('aria-valuemin', 0);
        bar.setAttribute('aria-valuemax', MAX_STAT);
    });
    // Ver mas
    const btnVerMas = document.getElementById('btn-ver-mas');
    const evolutionsContainer = document.getElementById('evolutions-container');

    btnVerMas.addEventListener('click', () => {
        evolutionsContainer.classList.toggle('hidden');
    });
});