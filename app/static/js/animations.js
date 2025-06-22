// Функция для показа уведомлений
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast ${type} animate__animated animate__fadeInRight`;
    toast.innerHTML = `
        <div class="toast-content">${message}</div>
        <div class="toast-close">&times;</div>
    `;
    
    const container = document.querySelector('.toast-container') || (() => {
        const cont = document.createElement('div');
        cont.className = 'toast-container';
        document.body.appendChild(cont);
        return cont;
    })();
    
    container.appendChild(toast);
    
    // Обработчик закрытия
    toast.querySelector('.toast-close').addEventListener('click', () => {
        toast.classList.remove('animate__fadeInRight');
        toast.classList.add('animate__fadeOutRight');
        setTimeout(() => toast.remove(), 300);
    });
    
    // Автоматическое закрытие через 3 секунды
    setTimeout(() => {
        if (toast.parentElement) {
            toast.classList.remove('animate__fadeInRight');
            toast.classList.add('animate__fadeOutRight');
            setTimeout(() => toast.remove(), 300);
        }
    }, 3000);
}

// Функция для анимации добавления строки
function animateAddRow(row) {
    row.classList.add('animate__animated', 'animate__fadeIn');
}

// Функция для анимации удаления строки
function animateDeleteRow(row) {
    row.classList.add('animate__animated', 'animate__fadeOutLeft');
    return new Promise(resolve => setTimeout(resolve, 300));
}

// Функция для анимации обновления строки
function animateUpdateRow(row) {
    row.classList.add('animate__animated', 'animate__pulse');
    return new Promise(resolve => setTimeout(resolve, 500));
}

// Функция для анимации модального окна
function animateModal(modal, type = 'show') {
    const modalElement = modal._element;
    if (type === 'show') {
        modalElement.classList.add('animate__animated', 'animate__fadeIn');
    }
} 