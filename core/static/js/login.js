$(document).ready(function() {
	// Проверяем, что jQuery загружен
	if (typeof $ === 'undefined') {
		console.error('jQuery is not loaded!');
		return;
	}
	
	console.log('Login.js loaded successfully');
	
	var iOS = navigator.userAgent.match(/iPhone|iPad|iPod/i);
	var clk = "click";
	if(iOS != null) clk = "touchstart";
	
	// Переключение между вкладками
	$('.tab_button').on(clk, function() {
		var tab = $(this).data('tab');
		
		// Обновляем активную вкладку
		$('.tab_button').removeClass('active');
		$(this).addClass('active');
		
		// Показываем соответствующую форму
		$('.login_form, .register_form').removeClass('active');
		if (tab === 'login') {
			$('.login_form').addClass('active');
		} else {
			$('.register_form').addClass('active');
		}
		
		// Очищаем сообщения
		$('.form-error, .form-success').hide();
	});
	
	// Переключение видимости пароля
	$(document).on('click', 'button.password-toggle', function(e) {
		e.preventDefault();
		e.stopPropagation();
		
		var input = $(this).siblings('input[type="password"], input[type="text"]');
		var eyeIcon = $(this).find('img.eye-icon');
		
		console.log('Password toggle clicked');
		console.log('Current input type:', input.attr('type'));
		console.log('Current icon src:', eyeIcon.attr('src'));
		console.log('Input found:', input.length);
		console.log('Icon found:', eyeIcon.length);
		
		if (input.attr('type') === 'password') {
			input.attr('type', 'text');
			eyeIcon.attr('src', '/static/img/ico_eye_slash.svg');
			console.log('Password shown, icon changed to slash');
		} else {
			input.attr('type', 'password');
			eyeIcon.attr('src', '/static/img/ico_eye.svg');
			console.log('Password hidden, icon changed to eye');
		}
	});
	
	// Выбор платформы
	$('.platform_item').on(clk, function() {
		$('.platform_item').removeClass('active');
		$(this).addClass('active');
	});
	
	// Валидация email
	function validateEmail(email) {
		var re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
		return re.test(email);
	}
	
	// Валидация пароля
	function validatePassword(password) {
		return password.length >= 6;
	}
	
	// Валидация username
	function validateUsername(username) {
		var re = /^@[a-zA-Z0-9_]{2,19}$/;
		return re.test(username);
	}
	
	// Показ/скрытие иконок валидации
	function showValidationIcon(input, isValid, message) {
		var container = input.closest('.input_container');
		var successIcon = container.find('.success-icon');
		var errorIcon = container.find('.error-icon');
		var errorMessage = container.siblings('.error-message');
		
		// Скрываем все иконки
		successIcon.hide();
		errorIcon.hide();
		errorMessage.hide();
		
		// Показываем соответствующую иконку
		if (isValid) {
			successIcon.show();
			input.removeClass('error').addClass('success');
		} else {
			errorIcon.show();
			input.removeClass('success').addClass('error');
			if (message) {
				errorMessage.text(message).show();
			}
		}
	}
	
	// Валидация в реальном времени
	$('.form_input').on('input blur', function() {
		var input = $(this);
		var value = input.val().trim();
		var name = input.attr('name');
		var isValid = false;
		var message = '';
		
		switch(name) {
			case 'email':
				isValid = validateEmail(value);
				message = isValid ? '' : 'Please enter a valid email address';
				break;
			case 'password':
				isValid = validatePassword(value);
				message = isValid ? '' : 'Password must be at least 6 characters';
				break;
			case 'name':
				isValid = validateUsername(value);
				message = isValid ? '' : 'Username must start with @ and be 2-19 characters';
				break;
		}
		
		if (value === '') {
			input.removeClass('success error');
			input.closest('.input_container').find('.success-icon, .error-icon').hide();
			input.siblings('.error-message').hide();
		} else {
			showValidationIcon(input, isValid, message);
		}
	});
	
	// Обработка формы входа
	$('#login-form').on('submit', function(e) {
		e.preventDefault();
		
		var form = $(this);
		var submitBtn = form.find('.submit_button');
		var email = form.find('input[name="email"]').val().trim();
		var password = form.find('input[name="password"]').val().trim();
		
		// Валидация
		if (!validateEmail(email)) {
			showMessage('Please enter a valid email address', 'error');
			return;
		}
		
		if (!validatePassword(password)) {
			showMessage('Please enter your password', 'error');
			return;
		}
		
		// Отправка формы
		submitBtn.prop('disabled', true).text('Logging in...');
		
		var payload = { email: email, password: password };
		var csrfToken = getCookie('csrftoken');
		
		fetch('/accounts/login-or-register/', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': csrfToken || ''
			},
			credentials: 'same-origin',
			body: JSON.stringify(payload)
		}).then(function(res) {
			return res.json().then(function(data) { 
				return { ok: res.ok, status: res.status, data: data }; 
			});
		}).then(function(result) {
			if (result.ok && result.data && result.data.success) {
				// Успешный вход
				localStorage.setItem('authToken', 'logged_in');
				localStorage.setItem('userData', JSON.stringify(result.data.user));
				
				showMessage('Welcome back! Redirecting...', 'success');
				
				// Перенаправление на главную страницу
				setTimeout(function() {
					window.location.href = '/';
				}, 1500);
			} else {
				// Ошибка входа
				var errorMsg = result.data && result.data.error ? result.data.error : 'Login failed';
				showMessage(errorMsg, 'error');
			}
		}).catch(function(error) {
			showMessage('Network error. Please try again.', 'error');
		}).finally(function() {
			submitBtn.prop('disabled', false).text('Login');
		});
	});
	
	// Обработка формы регистрации
	$('#register-form').on('submit', function(e) {
		e.preventDefault();
		
		var form = $(this);
		var submitBtn = form.find('.submit_button');
		var email = form.find('input[name="email"]').val().trim();
		var password = form.find('input[name="password"]').val().trim();
		var username = form.find('input[name="name"]').val().trim();
		var platform = $('.platform_item.active').data('platform');
		
		// Валидация
		if (!validateEmail(email)) {
			showMessage('Please enter a valid email address', 'error');
			return;
		}
		
		if (!validatePassword(password)) {
			showMessage('Password must be at least 6 characters', 'error');
			return;
		}
		
		if (!validateUsername(username)) {
			showMessage('Username must start with @ and be 2-19 characters', 'error');
			return;
		}
		
		if (!platform) {
			showMessage('Please select a platform', 'error');
			return;
		}
		
		// Отправка формы
		submitBtn.prop('disabled', true).text('Creating account...');
		
		var payload = { 
			email: email, 
			password: password, 
			name: username, 
			platform: platform 
		};
		var csrfToken = getCookie('csrftoken');
		
		fetch('/accounts/login-or-register/', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': csrfToken || ''
			},
			credentials: 'same-origin',
			body: JSON.stringify(payload)
		}).then(function(res) {
			return res.json().then(function(data) { 
				return { ok: res.ok, status: res.status, data: data }; 
			});
		}).then(function(result) {
			if (result.ok && result.data && result.data.success) {
				// Успешная регистрация
				localStorage.setItem('authToken', 'logged_in');
				localStorage.setItem('userData', JSON.stringify(result.data.user));
				
				showMessage('Account created successfully! Welcome, ' + result.data.user.nick_in_game, 'success');
				
				// Перенаправление на главную страницу
				setTimeout(function() {
					window.location.href = '/';
				}, 2000);
			} else {
				// Ошибка регистрации
				var errorMsg = result.data && result.data.error ? result.data.error : 'Registration failed';
				showMessage(errorMsg, 'error');
			}
		}).catch(function(error) {
			showMessage('Network error. Please try again.', 'error');
		}).finally(function() {
			submitBtn.prop('disabled', false).text('Register');
		});
	});
	
	// Показ сообщений
	function showMessage(message, type) {
		var errorDiv = $('.form-error');
		var successDiv = $('.form-success');
		
		// Скрываем все сообщения
		errorDiv.hide();
		successDiv.hide();
		
		// Показываем соответствующее сообщение
		if (type === 'error') {
			errorDiv.text(message).show().addClass('error-shake');
			setTimeout(function() {
				errorDiv.removeClass('error-shake');
			}, 500);
		} else {
			successDiv.text(message).show();
		}
	}
	
	// Получение CSRF токена
	function getCookie(name) {
		var cookieValue = null;
		if (document.cookie && document.cookie !== '') {
			var cookies = document.cookie.split(';');
			for (var i = 0; i < cookies.length; i++) {
				var cookie = cookies[i].trim();
				if (cookie.substring(0, name.length + 1) === (name + '=')) {
					cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
					break;
				}
			}
		}
		return cookieValue;
	}
	
	// Проверка авторизации при загрузке страницы
	function checkAuthStatus() {
		var authToken = localStorage.getItem('authToken');
		var userData = localStorage.getItem('userData');
		
		if (authToken && userData) {
			try {
				var user = JSON.parse(userData);
				if (user && user.nick_in_game) {
					// Пользователь уже авторизован, перенаправляем
					window.location.href = '/';
					return;
				}
			} catch (e) {
				// Очищаем невалидные данные
				localStorage.removeItem('authToken');
				localStorage.removeItem('userData');
			}
		}
	}
	
	// Проверяем статус при загрузке
	checkAuthStatus();
}); 