// Vista previa de la imagen
document.getElementById('foto').addEventListener('change', function(e) {
    const file = e.target.files[0];
    const preview = document.getElementById('previewImage');
    const previewContainer = document.getElementById('imagePreview');
    
    if (file) {
        const reader = new FileReader();
        
        reader.onload = function(e) {
            preview.src = e.target.result;
            previewContainer.style.display = 'block';
        }
        
        reader.readAsDataURL(file);
    } else {
        previewContainer.style.display = 'none';
    }
});

// Validación básica del formulario
document.getElementById('addMedicamentoForm').addEventListener('submit', function(e) {
    const nombreMedicamento = document.getElementById('nombreMedicamento').value.trim();
    const tipo = document.getElementById('tipo').value.trim();
    const referencia = document.getElementById('referencia').value.trim();
    const foto = document.getElementById('foto').files[0];
    
    if (!nombreMedicamento || !tipo || !referencia) {
        e.preventDefault();
        alert('Los campos marcados con * son obligatorios.');
        return false;
    }
    
    // Validar tamaño de archivo si se subió uno
    if (foto && foto.size > 5 * 1024 * 1024) {
        e.preventDefault();
        alert('La imagen no puede superar los 5MB.');
        return false;
    }
});

// Vista previa de la imagen
document.getElementById('foto').addEventListener('change', function(e) {
    const file = e.target.files[0];
    const preview = document.getElementById('previewImage');
    const previewContainer = document.getElementById('imagePreview');
    
    if (file) {
        const reader = new FileReader();
        
        reader.onload = function(e) {
            preview.src = e.target.result;
            previewContainer.style.display = 'block';
        }
        
        reader.readAsDataURL(file);
    } else {
        previewContainer.style.display = 'none';
    }
});

// Validación básica del formulario
document.getElementById('editMedicamentoForm').addEventListener('submit', function(e) {
    const nombreMedicamento = document.getElementById('nombreMedicamento').value.trim();
    const tipo = document.getElementById('tipo').value.trim();
    const referencia = document.getElementById('referencia').value.trim();
    const foto = document.getElementById('foto').files[0];
    
    if (!nombreMedicamento || !tipo || !referencia) {
        e.preventDefault();
        alert('Los campos marcados con * son obligatorios.');
        return false;
    }
    
    // Validar tamaño de archivo si se subió uno
    if (foto && foto.size > 5 * 1024 * 1024) {
        e.preventDefault();
        alert('La imagen no puede superar los 5MB.');
        return false;
    }
});

// Función de búsqueda
document.getElementById('searchInput').addEventListener('keyup', function() {
    const searchTerm = this.value.toLowerCase();
    const tableRows = document.querySelectorAll('#medicamentosTable tbody tr');
    
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
function confirmDelete(medicamentoId, medicamentoName) {
    document.getElementById('deleteMedicamentoName').textContent = medicamentoName;
    document.getElementById('deleteForm').action = `/medicamentos/${medicamentoId}/delete`;
    const deleteModal = new bootstrap.Modal(document.getElementById('deleteModal'));
    deleteModal.show();
}

// Función para establecer el tipo desde los badges
function setTipo(tipo) {
    document.getElementById('tipo').value = tipo;
    document.getElementById('tipo').focus();
}

document.addEventListener('DOMContentLoaded', function() {
    const nombreField = document.getElementById('nombre');
    if (nombreField && !nombreField.value) {
        nombreField.focus();
    }
});

// Función para confirmar eliminación
function confirmDelete(medicamentoId, medicamentoName) {
    document.getElementById('deleteMedicamentoName').textContent = medicamentoName;
    document.getElementById('deleteForm').action = `/medicamentos/${medicamentoId}/delete`;
    const deleteModal = new bootstrap.Modal(document.getElementById('deleteModal'));
    deleteModal.show();
}