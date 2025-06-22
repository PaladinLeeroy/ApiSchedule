// Функции для работы с cookies
function setCookie(name, value, days) {
    let expires = "";
    if (days) {
        const date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
}

function getCookie(name) {
    const nameEQ = name + "=";
    const ca = document.cookie.split(';');
    for(let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) === ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

function deleteCookie(name) {
    document.cookie = name + '=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
}

// Функция проверки авторизации
async function checkAuth() {
    const token = getCookie('access_token');
    const currentPath = window.location.pathname;
    
    // Если мы на странице входа и есть токен
    if (currentPath === '/unauthorized' && token) {
        // Проверяем валидность токена
        try {
            const response = await fetch('/api/users/me', {
                headers: addAuthHeader()
            });
            if (response.ok) {
                window.location.replace('/');
                return true;
            } else {
                // Если токен невалиден, удаляем его
                deleteCookie('access_token');
                return false;
            }
        } catch (error) {
            console.error('Auth check error:', error);
            deleteCookie('access_token');
            return false;
        }
    }
    
    // Если мы не на странице входа и нет токена
    if (!token && currentPath !== '/unauthorized' && !currentPath.startsWith('/static/')) {
        window.location.replace('/unauthorized');
        return false;
    }
    
    return !!token;
}

// Функция для добавления заголовка авторизации
function addAuthHeader(headers = {}) {
    const token = getCookie('access_token');
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    return headers;
}

// Перехватчик для fetch
const originalFetch = window.fetch;
window.fetch = async function(url, options = {}) {
    // Не добавляем заголовок авторизации для запросов к /api/token
    if (!url.includes('/api/token')) {
        options.headers = addAuthHeader(options.headers || {});
    }
    
    try {
        const response = await originalFetch(url, options);
        // Проверяем 401 только для API запросов
        if (response.status === 401 && url.startsWith('/api/')) {
            deleteCookie('access_token');
            if (window.location.pathname !== '/unauthorized') {
                window.location.replace('/unauthorized');
            }
        }
        return response;
    } catch (error) {
        console.error('Fetch error:', error);
        throw error;
    }
};

// Перехватчик для XMLHttpRequest
const originalXHROpen = XMLHttpRequest.prototype.open;
const originalXHRSend = XMLHttpRequest.prototype.send;

XMLHttpRequest.prototype.open = function(method, url, ...args) {
    this._url = url;
    return originalXHROpen.apply(this, [method, url, ...args]);
};

XMLHttpRequest.prototype.send = function(data) {
    if (!this._url.includes('/api/token')) {
        const token = getCookie('access_token');
        if (token) {
            this.setRequestHeader('Authorization', `Bearer ${token}`);
        }
    }
    return originalXHRSend.apply(this, [data]);
};

// Функция выхода
function handleLogout() {
    deleteCookie('access_token');
    // Используем replace для предотвращения возврата в историю браузера
    window.location.replace('/unauthorized');
}

// Проверка авторизации при загрузке страницы
document.addEventListener('DOMContentLoaded', async () => {
    const currentPath = window.location.pathname;
    // Проверяем авторизацию только если мы не на странице входа
    // и не на странице с ошибкой и не загружаем статические файлы
    if (currentPath !== '/unauthorized' && 
        !currentPath.startsWith('/error') && 
        !currentPath.startsWith('/static/')) {
        await checkAuth();
    }
});

// Обработка кликов по ссылкам
document.addEventListener('click', async (event) => {
    const link = event.target.closest('a');
    if (!link) return;
    
    const href = link.getAttribute('href');
    // Пропускаем внешние ссылки, ссылки на API и страницу входа
    if (!href || href.startsWith('http') || href.includes('/api/') || href === '/unauthorized') {
        return;
    }
    
    const token = getCookie('access_token');
    if (!token) {
        event.preventDefault();
        window.location.replace('/unauthorized');
    }
});

// Обработчик формы входа
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        // Удаляем существующий обработчик, если он есть
        const newLoginForm = loginForm.cloneNode(true);
        loginForm.parentNode.replaceChild(newLoginForm, loginForm);
        
        newLoginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const form = e.target;
            if (!form.checkValidity()) {
                e.stopPropagation();
                form.classList.add('was-validated');
                return;
            }

            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;

            try {
                const formData = new FormData();
                formData.append('username', username);
                formData.append('password', password);

                const response = await fetch('/api/token', {
                    method: 'POST',
                    body: formData,
                    redirect: 'manual'
                });

                if (response.ok) {
                    const data = await response.json();
                    document.cookie = `access_token=${data.access_token}; path=/; max-age=${60 * 60 * 24}; SameSite=Strict`;
                    window.location.replace('/');
                } else if (response.status === 401) {
                    const error = await response.json();
                    alert(error.detail || 'Неверное имя пользователя или пароль');
                } else {
                    alert('Произошла ошибка при авторизации');
                }
            } catch (error) {
                console.error('Ошибка:', error);
                alert('Произошла ошибка при авторизации');
            }
        });
    }
}); 