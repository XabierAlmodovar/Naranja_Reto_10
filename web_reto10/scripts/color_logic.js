// Este script asume que las variables COMBINATION_LOOKUP (el diccionario) 
// y UNIQUE_COLORS (la lista) han sido definidas en el HTML.

// Variables de estado
let selectedTopColor = null;
let selectedBottomColor = null;
let currentTarget = 'top'; // 'top' o 'bottom'

// Elementos del DOM
const palette = document.getElementById('color-palette');
const previewTop = document.getElementById('preview-top');
const previewBottom = document.getElementById('preview-bottom');
const hexTop = document.getElementById('hex-top');
const hexBottom = document.getElementById('hex-bottom');
const resultMessage = document.getElementById('result-message');
const selectionTargetDisplay = document.getElementById('current-selection-target');
const checkButton = document.getElementById('checkCombination');


// --- Helper Functions ---

function getContrastColor(hexcolor) {
    if (!hexcolor || hexcolor.length !== 7) return '#000000';
    const r = parseInt(hexcolor.substring(1, 3), 16);
    const g = parseInt(hexcolor.substring(3, 5), 16);
    const b = parseInt(hexcolor.substring(5, 7), 16);
    const yiq = ((r * 299) + (g * 587) + (b * 114)) / 1000;
    return (yiq >= 140) ? '#000000' : '#FFFFFF';
}

function updateSelection(colorHex) {
    // La data ya está en el scope, podemos usar COMBINATION_LOOKUP y UNIQUE_COLORS
    
    let targetElement, hexElement;
    
    if (currentTarget === 'top') {
        selectedTopColor = colorHex;
        targetElement = previewTop;
        hexElement = hexTop;
    } else {
        selectedBottomColor = colorHex;
        targetElement = previewBottom;
        hexElement = hexBottom;
    }

    // Aplicar color al preview
    targetElement.style.backgroundColor = colorHex;
    targetElement.style.color = getContrastColor(colorHex);
    hexElement.textContent = colorHex;

    // Cambiar objetivo para el siguiente clic
    currentTarget = (currentTarget === 'top') ? 'bottom' : 'top';
    selectionTargetDisplay.textContent = (currentTarget === 'top') ? 'Prenda Superior' : 'Prenda Inferior';
    
    // Habilitar botón
    if (selectedTopColor && selectedBottomColor) {
        checkButton.disabled = false;
        resultMessage.classList.remove('empty', 'success', 'error');
        resultMessage.classList.add('info');
        resultMessage.innerHTML = '¡Listo para verificar! Presiona el botón.';
    }
}

function checkCombination() {
    if (!selectedTopColor || !selectedBottomColor) return;

    // 1. Crear la clave canónica (ordenada alfabéticamente y en mayúsculas)
    // Esto asegura que (Blanco, Negro) y (Negro, Blanco) busquen la misma clave: #000000_#FFFFFF
    const colorPair = [selectedTopColor.toUpperCase(), selectedBottomColor.toUpperCase()].sort();
    const canonicalKey = `${colorPair[0]}_${colorPair[1]}`;

    // 2. Buscar en la data
    const label = COMBINATION_LOOKUP[canonicalKey];

    // 3. Mostrar Resultado
    resultMessage.classList.remove('empty', 'success', 'error', 'info');
    
    if (label === 1) {
        resultMessage.classList.add('success');
        resultMessage.innerHTML = '✅ <strong>¡Combinan!</strong> Esta combinación está validada por el sistema Lookiero.';
    } else if (label === 0) {
        resultMessage.classList.add('error');
        resultMessage.innerHTML = '❌ <strong>¡No combinan!</strong> La etiqueta de esta combinación en la data es "0".';
    } else {
        // Esto captura cualquier par que no estuviera en las 1378 entradas del CSV
        resultMessage.classList.add('info');
        resultMessage.innerHTML = '⚠️ Combinación no encontrada. (Este par no fue evaluado en el CSV original).';
    }
}


// --- Inicialización ---

function initializePalette() {
    // Si la data no existe en el scope, algo falló en la carga del HTML.
    if (!palette || !UNIQUE_COLORS || UNIQUE_COLORS.length === 0) {
        console.error("Error: UNIQUE_COLORS no se cargó correctamente. Verifique el HTML.");
        return;
    }
    
    // 1. Insertar swatches
    UNIQUE_COLORS.forEach(color => {
        const swatch = document.createElement('div');
        swatch.className = 'color-swatch';
        swatch.style.backgroundColor = color;
        
        swatch.addEventListener('click', () => {
            document.querySelectorAll('.color-swatch').forEach(s => s.classList.remove('active'));
            swatch.classList.add('active');
            updateSelection(color);
        });

        palette.appendChild(swatch);
    });
    
    // 2. Asignar evento al botón de verificar
    checkButton.addEventListener('click', checkCombination);

    // Inicializar previsualización con colores base
    previewTop.style.backgroundColor = '#FFFFFF';
    previewBottom.style.backgroundColor = '#FFFFFF';
}

document.addEventListener('DOMContentLoaded', initializePalette);