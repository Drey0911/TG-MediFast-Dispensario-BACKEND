// Validación básica del formulario
document.getElementById('addSedeForm').addEventListener('submit', function(e) {
    const nombreSede = document.getElementById('nombreSede').value.trim();
    const ciudad = document.getElementById('ciudad').value.trim();
    const ubicacion = document.getElementById('ubicacion').value.trim();
    
    if (!nombreSede || !ciudad || !ubicacion) {
        e.preventDefault();
        alert('Todos los campos marcados con * son obligatorios.');
        return false;
    }
});

// Validación básica del formulario
document.getElementById('editSedeForm').addEventListener('submit', function(e) {
    const nombreSede = document.getElementById('nombreSede').value.trim();
    const ciudad = document.getElementById('ciudad').value.trim();
    const ubicacion = document.getElementById('ubicacion').value.trim();
    
    if (!nombreSede || !ciudad || !ubicacion) {
        e.preventDefault();
        alert('Todos los campos marcados con * son obligatorios.');
        return false;
    }
});

// Función de búsqueda
document.getElementById('searchInput').addEventListener('keyup', function() {
    const searchTerm = this.value.toLowerCase();
    const tableRows = document.querySelectorAll('#sedesTable tbody tr');
    
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
function confirmDelete(sedeId, sedeName) {
    document.getElementById('deleteSedeName').textContent = sedeName;
    document.getElementById('deleteForm').action = `/sedes/${sedeId}/delete`;
    const deleteModal = new bootstrap.Modal(document.getElementById('deleteModal'));
    deleteModal.show();
}