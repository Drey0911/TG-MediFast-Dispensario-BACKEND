/**
 * Gestión de edición de disponibilidad
 * Funcionalidad completa para el formulario de edición de disponibilidad
 */

class EditDisponibilidad {
    constructor() {
        this.stockOriginal = disponibilidadData.stockOriginal;
        this.estadoOriginal = disponibilidadData.estadoOriginal;
        this.init();
    }

    init() {
        this.bindEvents();
        this.setupQuickActions();
    }

    bindEvents() {
        // Auto-actualizar estado basado en stock
        document.getElementById('stock').addEventListener('input', (e) => {
            this.handleStockChange(e.target.value);
        });

        // Validación del formulario
        document.getElementById('editDisponibilidadForm').addEventListener('submit', (e) => {
            this.handleFormSubmit(e);
        });

        // Inicializar indicador de cambio si hay diferencia al cargar
        const stockActual = parseInt(document.getElementById('stock').value);
        if (stockActual !== this.stockOriginal) {
            this.mostrarCambioStock(stockActual);
        }
    }

    setupQuickActions() {
        // Configurar eventos para botones de acciones rápidas
        const quickActionButtons = document.querySelectorAll('.quick-action-btn');
        quickActionButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                const action = e.target.closest('.quick-action-btn').dataset.action;
                const amount = parseInt(e.target.closest('.quick-action-btn').dataset.amount);
                this.handleQuickAction(action, amount);
            });
        });
    }

    handleStockChange(stockValue) {
        const stock = parseInt(stockValue);
        const estadoSelect = document.getElementById('estado');
        
        if (!isNaN(stock)) {
            // Actualizar estado automáticamente basado en el stock
            if (stock === 0) {
                estadoSelect.value = 'agotado';
            } else if (stock <= 10) {
                estadoSelect.value = 'poco_stock';
            } else {
                estadoSelect.value = 'disponible';
            }
            
            // Mostrar indicador de cambio
            this.mostrarCambioStock(stock);
        }
    }

    handleQuickAction(action, amount) {
        const stockInput = document.getElementById('stock');
        let stockActual = parseInt(stockInput.value) || 0;
        let nuevoStock;

        switch (action) {
            case 'add':
                nuevoStock = stockActual + amount;
                break;
            case 'subtract':
                nuevoStock = Math.max(0, stockActual - amount);
                break;
            case 'set':
                nuevoStock = amount;
                break;
            default:
                nuevoStock = stockActual;
        }

        stockInput.value = nuevoStock;
        
        // Disparar evento input para actualizar estado y mostrar cambios
        const event = new Event('input', { bubbles: true });
        stockInput.dispatchEvent(event);
    }

    mostrarCambioStock(stockNuevo) {
        const indicator = document.getElementById('stockChangeIndicator');
        const stockNuevoDiv = document.getElementById('stockNuevo');
        const stockDiferenciaDiv = document.getElementById('stockDiferencia');
        
        if (stockNuevo !== this.stockOriginal) {
            stockNuevoDiv.textContent = stockNuevo + ' unidades';
            
            const diferencia = stockNuevo - this.stockOriginal;
            if (diferencia > 0) {
                stockDiferenciaDiv.innerHTML = `<span class="text-success">+${diferencia} unidades (incremento)</span>`;
            } else if (diferencia < 0) {
                stockDiferenciaDiv.innerHTML = `<span class="text-danger">${diferencia} unidades (decremento)</span>`;
            } else {
                stockDiferenciaDiv.innerHTML = `<span class="text-muted">Sin cambios</span>`;
            }
            
            indicator.style.display = 'block';
        } else {
            indicator.style.display = 'none';
        }
    }

    handleFormSubmit(e) {
        const stock = document.getElementById('stock').value;
        const estado = document.getElementById('estado').value;
        
        // Validaciones
        if (!stock || !estado) {
            e.preventDefault();
            this.showAlert('Todos los campos marcados con * son obligatorios.', 'error');
            return false;
        }
        
        if (parseInt(stock) < 0) {
            e.preventDefault();
            this.showAlert('El stock no puede ser negativo.', 'error');
            return false;
        }

        // Validación adicional: estado coherente con stock
        const stockNum = parseInt(stock);
        if (stockNum === 0 && estado !== 'agotado') {
            if (!confirm('El stock es 0 pero el estado no está marcado como "Agotado". ¿Desea continuar?')) {
                e.preventDefault();
                return false;
            }
        } else if (stockNum > 0 && stockNum <= 10 && estado !== 'poco_stock') {
            if (!confirm('El stock es bajo (≤10) pero el estado no está marcado como "Poco Stock". ¿Desea continuar?')) {
                e.preventDefault();
                return false;
            }
        } else if (stockNum > 10 && estado !== 'disponible') {
            if (!confirm('El stock es suficiente (>10) pero el estado no está marcado como "Disponible". ¿Desea continuar?')) {
                e.preventDefault();
                return false;
            }
        }

        // Mostrar resumen de cambios antes de enviar
        const cambios = this.getResumenCambios();
        if (cambios.hayCambios) {
            console.log('Enviando formulario con cambios:', cambios);
        }
        
        return true;
    }

    getResumenCambios() {
        const stockActual = parseInt(document.getElementById('stock').value);
        const estadoActual = document.getElementById('estado').value;
        
        return {
            hayCambios: stockActual !== this.stockOriginal || estadoActual !== this.estadoOriginal,
            stock: {
                anterior: this.stockOriginal,
                nuevo: stockActual,
                diferencia: stockActual - this.stockOriginal
            },
            estado: {
                anterior: this.estadoOriginal,
                nuevo: estadoActual,
                cambio: estadoActual !== this.estadoOriginal
            }
        };
    }

    showAlert(message, type = 'error') {
        // Puedes implementar un sistema de alertas más sofisticado aquí
        alert(message);
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    new EditDisponibilidad();
});

// Funciones globales para compatibilidad con onclick (opcional)
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