// Validación básica del formulario
document.getElementById('editRecoleccionForm').addEventListener('submit', function(e) {
    const cumplimiento = document.getElementById('cumplimiento').value;

    if (cumplimiento === '') {
        e.preventDefault();
        alert('Por favor selecciona un estado de cumplimiento.');
    }
});

// Función de búsqueda
document.getElementById('searchInput').addEventListener('keyup', function() {
    const searchTerm = this.value.toLowerCase();
    const tableRows = document.querySelectorAll('#recoleccionesTable tbody tr');
    
    tableRows.forEach(function(row) {
        const text = row.textContent.toLowerCase();
        if (text.includes(searchTerm)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
});

// Función para confirmar eliminación
function confirmDelete(norecoleccion, userName) {
    document.getElementById('deleteRecName').textContent = userName + ' (' + norecoleccion + ')';
    document.getElementById('deleteForm').action = `/recolecciones/${norecoleccion}/delete`;
    const deleteModal = new bootstrap.Modal(document.getElementById('deleteModal'));
    deleteModal.show();
}