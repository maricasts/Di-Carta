// Global JavaScript functions for the Dicarta Livraria application

// Book Management Functions
function editBook(id, titulo, autor, editora, ano, genero, preco, estoque) {
    document.getElementById('edit_titulo').value = titulo;
    document.getElementById('edit_autor').value = autor;
    document.getElementById('edit_editora').value = editora || '';
    document.getElementById('edit_ano').value = ano || '';
    document.getElementById('edit_genero').value = genero || '';
    document.getElementById('edit_preco').value = preco;
    document.getElementById('edit_estoque').value = estoque;
    
    // Set the form action to update the specific book
    document.getElementById('editBookForm').action = `/tecnico/books/update/${id}`;
}

// Order Management Functions
function editOrder(id, descricao, status, dataFechamento) {
    document.getElementById('edit_descricao').value = descricao;
    document.getElementById('edit_status').value = status;
    document.getElementById('edit_dataFechamento').value = dataFechamento || '';
    
    // Set the form action to update the specific order
    document.getElementById('editOrderForm').action = `/tecnico/orders/update/${id}`;
}

// Format currency values
function formatCurrency(value) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(value);
}

// Format CPF input
function formatCPF(input) {
    // Remove all non-digit characters
    let value = input.value.replace(/\D/g, '');
    
    // Limit to 11 digits
    value = value.substring(0, 11);
    
    // Apply CPF formatting
    if (value.length >= 3) {
        value = value.replace(/(\d{3})(\d)/, '$1.$2');
    }
    if (value.length >= 7) {
        value = value.replace(/(\d{3})\.(\d{3})(\d)/, '$1.$2.$3');
    }
    if (value.length >= 11) {
        value = value.replace(/(\d{3})\.(\d{3})\.(\d{3})(\d{2})/, '$1.$2.$3-$4');
    }
    
    input.value = value;
}

// Add input event listeners when document is ready
document.addEventListener('DOMContentLoaded', function() {
    // CPF formatting for registration forms
    const cpfInputs = document.querySelectorAll('input[name="cpf"]');
    cpfInputs.forEach(input => {
        input.addEventListener('input', function() {
            formatCPF(this);
        });
    });
    
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
    
    // Initialize tooltips if Bootstrap tooltips are needed
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// Shopping cart utilities
const Cart = {
    // Add item to cart (this would typically make an AJAX call)
    addItem: function(bookId) {
        // This is handled by the server-side route
        window.location.href = `/cart/add/${bookId}`;
    },
    
    // Remove item from cart
    removeItem: function(bookId) {
        if (confirm('Remover este item do carrinho?')) {
            window.location.href = `/cart/remove/${bookId}`;
        }
    },
    
    // Update cart item quantity (for future implementation)
    updateQuantity: function(bookId, quantity) {
        // This would make an AJAX call to update quantity
        console.log(`Update book ${bookId} quantity to ${quantity}`);
    }
};

// Utility functions
const Utils = {
    // Show loading spinner
    showLoading: function(element) {
        if (element) {
            element.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Carregando...';
            element.disabled = true;
        }
    },
    
    // Hide loading spinner
    hideLoading: function(element, originalText) {
        if (element) {
            element.innerHTML = originalText;
            element.disabled = false;
        }
    },
    
    // Validate form inputs
    validateForm: function(formId) {
        const form = document.getElementById(formId);
        if (form) {
            return form.checkValidity();
        }
        return false;
    }
};

// Book search functionality (for future implementation)
function searchBooks(searchTerm) {
    // This would filter the books display based on search term
    console.log('Searching for:', searchTerm);
}

// Form validation helpers
function validateBookForm() {
    const titulo = document.querySelector('input[name="titulo"]').value;
    const autor = document.querySelector('input[name="autor"]').value;
    const preco = document.querySelector('input[name="preco"]').value;
    
    if (!titulo || !autor || !preco) {
        alert('Por favor, preencha todos os campos obrigatórios.');
        return false;
    }
    
    if (parseFloat(preco) <= 0) {
        alert('O preço deve ser maior que zero.');
        return false;
    }
    
    return true;
}

// Initialize page-specific functionality
function initializePage() {
    const currentPage = window.location.pathname;
    
    if (currentPage.includes('/book_management')) {
        // Initialize book management specific features
        console.log('Book management page loaded');
    } else if (currentPage.includes('/cart')) {
        // Initialize cart specific features
        console.log('Shopping cart page loaded');
    }
}

// Call initialization when page loads
document.addEventListener('DOMContentLoaded', initializePage);
