// Mostrar información adicional del medicamento seleccionado
document.getElementById('id_medicamento').addEventListener('change', function() {
    const selectedOption = this.options[this.selectedIndex];
    const infoDiv = document.getElementById('medicamentoInfo');
    
    if (selectedOption.value) {
        document.getElementById('medicamentoTipo').textContent = selectedOption.dataset.tipo;
        document.getElementById('medicamentoRef').textContent = selectedOption.dataset.referencia;
        infoDiv.style.display = 'block';
    } else {
        infoDiv.style.display = 'none';
    }
    
    updatePreview();
});

// Mostrar información adicional de la sede seleccionada
document.getElementById('id_sede').addEventListener('change', function() {
    const selectedOption = this.options[this.selectedIndex];
    const infoDiv = document.getElementById('sedeInfo');
    
    if (selectedOption.value) {
        document.getElementById('sedeCiudad').textContent = selectedOption.dataset.ciudad;
        document.getElementById('sedeUbicacion').textContent = selectedOption.dataset.ubicacion;
        infoDiv.style.display = 'block';
    } else {
        infoDiv.style.display = 'none';
    }
    
    updatePreview();
});

// Función de búsqueda
document.getElementById('searchInput').addEventListener('keyup', function() {
    const searchTerm = this.value.toLowerCase();
    const tableRows = document.querySelectorAll('#disponibilidadTable tbody tr');
    
    tableRows.forEach(function(row) {
        const text = row.textContent.toLowerCase();
        if (text.includes(searchTerm)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
});

// Auto-actualizar estado basado en stock
document.getElementById('stock').addEventListener('input', function() {
    const stock = parseInt(this.value);
    const estadoSelect = document.getElementById('estado');
    
    if (!isNaN(stock)) {
        if (stock === 0) {
            estadoSelect.value = 'agotado';
        } else if (stock <= 10) {
            estadoSelect.value = 'poco_stock';
        } else {
            estadoSelect.value = 'disponible';
        }
        
        // Mostrar indicador de cambio
        mostrarCambioStock(stock);
    }
});

// Función para mostrar cambio de stock
function mostrarCambioStock(stockNuevo) {
    const indicator = document.getElementById('stockChangeIndicator');
    const stockNuevoDiv = document.getElementById('stockNuevo');
    const stockDiferenciaDiv = document.getElementById('stockDiferencia');
    
    if (stockNuevo !== stockOriginal) {
        stockNuevoDiv.textContent = stockNuevo + ' unidades';
        
        const diferencia = stockNuevo - stockOriginal;
        if (diferencia > 0) {
            stockDiferenciaDiv.innerHTML = `<span class="text-success">+${diferencia} unidades</span>`;
        } else {
            stockDiferenciaDiv.innerHTML = `<span class="text-danger">${diferencia} unidades</span>`;
        }
        
        indicator.style.display = 'block';
    } else {
        indicator.style.display = 'none';
    }
}

// Funciones para acciones rápidas
function ajustarStock(cantidad) {
    const stockInput = document.getElementById('stock');
    const stockActual = parseInt(stockInput.value) || 0;
    const nuevoStock = Math.max(0, stockActual + cantidad);
    
    stockInput.value = nuevoStock;
    stockInput.dispatchEvent(new Event('input'));
}

function setStock(cantidad) {
    const stockInput = document.getElementById('stock');
    stockInput.value = cantidad;
    stockInput.dispatchEvent(new Event('input'));
}

// Validación del formulario
document.getElementById('editDisponibilidadForm').addEventListener('submit', function(e) {
    const stock = document.getElementById('stock').value;
    const estado = document.getElementById('estado').value;
    
    if (!stock || !estado) {
        e.preventDefault();
        alert('Todos los campos marcados con * son obligatorios.');
        return false;
    }
    
    if (parseInt(stock) < 0) {
        e.preventDefault();
        alert('El stock no puede ser negativo.');
        return false;
    }
});

// Función para confirmar eliminación
function confirmDelete(disponibilidadId, itemName) {
    document.getElementById('deleteItemName').textContent = itemName;
    document.getElementById('deleteForm').action = `/disponibilidad/${disponibilidadId}/delete`;
    const deleteModal = new bootstrap.Modal(document.getElementById('deleteModal'));
    deleteModal.show();
}

