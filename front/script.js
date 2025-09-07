document.addEventListener('DOMContentLoaded', () => {
    
    // Elementos del DOM
    const canvas = document.getElementById('koch-canvas');
    const ctx = canvas.getContext('d');
    const drawButton = document.getElementById('draw-button');
    const recursionInput = document.getElementById('recursion');
    const isCompleteCheckbox = document.getElementById('is-complete');

    // --- CORRECCIÓN IMPORTANTE ---
    // Reemplaza esta URL con la URL de tu backend en Render cuando la tengas.
    // La obtendrás después de desplegar el "Web Service".
    const BACKEND_URL = 'https://SHINMON.onrender.com/generate_snowflake';

    function drawSnowflake(points) {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.strokeStyle = '#61dafb';
        ctx.lineWidth = 1.5;
        
        ctx.save();
        ctx.translate(canvas.width / 2, canvas.height / 2);
        
        ctx.beginPath();
        if (points.length > 0) {
            ctx.moveTo(points[0][0], points[0][1]);
            for (let i = 1; i < points.length; i++) {
                ctx.lineTo(points[i][0], points[i][1]);
            }
        }
        ctx.stroke();
        ctx.restore();
    }
    
    async function fetchAndDraw() {
        const order = parseInt(recursionInput.value, 10);
        const isComplete = isCompleteCheckbox.checked;

        try {
            const response = await fetch(BACKEND_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    order: order,
                    is_complete: isComplete 
                }),
            });

            if (!response.ok) {
                throw new Error(`Error del servidor: ${response.statusText}`);
            }

            const coordinates = await response.json();
            drawSnowflake(coordinates);

        } catch (error) {
            console.error('No se pudo obtener el copo de nieve:', error);
            alert('Error al conectar con el servidor. Revisa la URL en script.js y asegúrate de que el backend esté desplegado y funcionando.');
        }
    }

    drawButton.addEventListener('click', fetchAndDraw);
    isCompleteCheckbox.addEventListener('change', fetchAndDraw);
    
    fetchAndDraw();
});