function deselectAll() {
    const checkboxes = document.querySelectorAll('input[name="fractions"]');
    checkboxes.forEach(checkbox => checkbox.checked = false);
}

// Tooltip global
let tooltip;

window.addEventListener('DOMContentLoaded', () => {
    console.log("scripts.js cargado correctamente");

    const errorDiv = document.getElementById('floating-error');
    if (errorDiv) {
        const message = errorDiv.getAttribute('data-message');
        errorDiv.textContent = message;

        setTimeout(() => {
            errorDiv.remove();
        }, 3000);
    }

    // Crear tooltip global y agregar al body
    tooltip = document.createElement('div');
    tooltip.className = 'tooltip';
    tooltip.style.position = 'fixed';
    tooltip.style.top = '0';
    tooltip.style.left = '0';
    tooltip.style.opacity = '0';
    tooltip.style.visibility = 'hidden';
    tooltip.style.pointerEvents = 'none';
    document.body.appendChild(tooltip);

    const dates = document.querySelectorAll('.date-circle[data-tooltip]');
    dates.forEach(el => {
        el.addEventListener('mouseenter', () => {
            tooltip.textContent = el.getAttribute('data-tooltip');
            tooltip.style.visibility = 'visible';
            tooltip.style.opacity = '1';
        });

        el.addEventListener('mousemove', (event) => {
            // Posicionar tooltip cerca del cursor, ajustando para no salir de pantalla
            const padding = 10;
            let x = event.clientX;
            let y = event.clientY - 40; // un poco arriba del cursor

            const tooltipRect = tooltip.getBoundingClientRect();
            const screenWidth = window.innerWidth;
            const screenHeight = window.innerHeight;

            if (x + tooltipRect.width + padding > screenWidth) {
                x = screenWidth - tooltipRect.width - padding;
            }
            if (y - tooltipRect.height - padding < 0) {
                y = event.clientY + 20; // debajo si no cabe arriba
            }

            tooltip.style.transform = `translate(${x}px, ${y}px)`;
        });

        el.addEventListener('mouseleave', () => {
            tooltip.style.opacity = '0';
            tooltip.style.visibility = 'hidden';
        });
    });
});
