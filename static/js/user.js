function togglePassword(fieldId, iconId) {
    const passwordInput = document.getElementById(fieldId);
    const toggleIcon = document.getElementById(iconId);
    
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        toggleIcon.classList.replace('fa-eye', 'fa-eye-slash');
    } else {
        passwordInput.type = 'password';
        toggleIcon.classList.replace('fa-eye-slash', 'fa-eye');
    }
}

// Validación en tiempo real de la contraseña
document.getElementById('password').addEventListener('input', function() {
    const password = this.value;
    
    // Verificar longitud
    updateRequirement('length-req', password.length >= 8);
    
    // Verificar mayúscula
    updateRequirement('uppercase-req', /[A-Z]/.test(password));
    
    // Verificar número
    updateRequirement('number-req', /[0-9]/.test(password));
    
    // Verificar símbolo
    updateRequirement('symbol-req', /[!@#$%^&*(),.?":{}|<>]/.test(password));
});

function updateRequirement(elementId, isValid) {
    const element = document.getElementById(elementId);
    const icon = element.querySelector('i');
    
    if (isValid) {
        icon.className = 'fas fa-check-circle text-success me-2';
        element.classList.remove('text-danger');
        element.classList.add('text-success');
    } else {
        icon.className = 'fas fa-times-circle text-danger me-2';
        element.classList.remove('text-success');
        element.classList.add('text-danger');
    }
}

// Validación del formulario
document.getElementById('addUserForm').addEventListener('submit', function(e) {
    const password = document.getElementById('password').value;
    
    // Verificar todos los requisitos
    const isValidLength = password.length >= 8;
    const hasUppercase = /[A-Z]/.test(password);
    const hasNumber = /[0-9]/.test(password);
    const hasSymbol = /[!@#$%^&*(),.?":{}|<>]/.test(password);
    
    if (!isValidLength || !hasUppercase || !hasNumber || !hasSymbol) {
        e.preventDefault();
        alert('La contraseña no cumple con todos los requisitos de seguridad.');
        return false;
    }
});

function togglePassword(fieldId, iconId) {
    const passwordInput = document.getElementById(fieldId);
    const toggleIcon = document.getElementById(iconId);
    
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        toggleIcon.classList.replace('fa-eye', 'fa-eye-slash');
    } else {
        passwordInput.type = 'password';
        toggleIcon.classList.replace('fa-eye-slash', 'fa-eye');
    }
}

// Mostrar/ocultar requisitos de contraseña
const passwordField = document.getElementById('password');
const requirementsCard = document.getElementById('passwordRequirements');

passwordField.addEventListener('input', function() {
    const password = this.value;
    
    if (password.length > 0) {
        requirementsCard.style.display = 'block';
        
        // Verificar requisitos
        updateRequirement('length-req', password.length >= 8);
        updateRequirement('uppercase-req', /[A-Z]/.test(password));
        updateRequirement('number-req', /[0-9]/.test(password));
        updateRequirement('symbol-req', /[!@#$%^&*(),.?":{}|<>]/.test(password));
    } else {
        requirementsCard.style.display = 'none';
    }
});

function updateRequirement(elementId, isValid) {
    const element = document.getElementById(elementId);
    const icon = element.querySelector('i');
    
    if (isValid) {
        icon.className = 'fas fa-check-circle text-success me-2';
        element.classList.remove('text-danger');
        element.classList.add('text-success');
    } else {
        icon.className = 'fas fa-times-circle text-danger me-2';
        element.classList.remove('text-success');
        element.classList.add('text-danger');
    }
}

// Validación del formulario
document.getElementById('editUserForm').addEventListener('submit', function(e) {
    const password = document.getElementById('password').value;
    
    // Solo validar si se está cambiando la contraseña
    if (password.length > 0) {
        const isValidLength = password.length >= 8;
        const hasUppercase = /[A-Z]/.test(password);
        const hasNumber = /[0-9]/.test(password);
        const hasSymbol = /[!@#$%^&*(),.?":{}|<>]/.test(password);
        
        if (!isValidLength || !hasUppercase || !hasNumber || !hasSymbol) {
            e.preventDefault();
            alert('La nueva contraseña no cumple con todos los requisitos de seguridad.');
            return false;
        }
    }
});

// Función de búsqueda
document.getElementById('searchInput').addEventListener('keyup', function() {
    const searchTerm = this.value.toLowerCase();
    const tableRows = document.querySelectorAll('#usersTable tbody tr');
    
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
function confirmDelete(userId, userName) {
    document.getElementById('deleteUserName').textContent = userName;
    document.getElementById('deleteForm').action = `/users/${userId}/delete`;
    const deleteModal = new bootstrap.Modal(document.getElementById('deleteModal'));
    deleteModal.show();
}