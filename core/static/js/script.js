$(document).ready(function(){
	var iOS = navigator.userAgent.match(/iPhone|iPad|iPod/i);
	var clk = "click";
	if(iOS != null) clk = "touchstart";
	
	// Check if user is already logged in
	function checkAuthStatus() {
		// Check if there's a stored auth token or user data
		var authToken = localStorage.getItem('authToken');
		var userData = localStorage.getItem('userData');
		
		if (authToken && userData) {
			try {
				// Parse user data to check if it's valid
				var user = JSON.parse(userData);
				
				// Check if user data has required fields
				if (user && user.nick_in_game) {
					// User is logged in, update button to ACCOUNT
			$('#auth-button').text('ACCOUNT').attr('href', '/accounts/');
			$('#account-menu-item').show(); // Show account menu item
					return;
				}
			} catch (e) {
				// Invalid user data, clear it
				console.log('Invalid user data found, clearing...');
			}
		}
		
		// User is not logged in or data is invalid, clear everything and show LOGIN
		localStorage.removeItem('authToken');
		localStorage.removeItem('userData');
		$('#auth-button').text('LOGIN').attr('href', '#');
	}
	
	// Reset form to initial state
	function resetForm() {
		// Clear all input fields
		$('.drop_data_inp').val('').removeClass('error success');
		
		// Clear all icons and error messages
		$('.input-icon').removeClass('show').hide();
		$('.error-message').removeClass('show error-shake').hide();
		
		// Clear form messages
		$('.form-error').removeClass('show error-shake').hide();
		$('.form-success').removeClass('show').hide();
		
		// Reset platform selection
		$('.platform_item').removeClass('active');
		
		// Reset password field to password type
		$('input[name="password"]').attr('type', 'password');
		$('.password-toggle img').attr('src', '/static/img/ico_eye.svg');
		
		// Clear header states
		$('.form_inp_hd').removeClass('focus success error');
	}
	
	// Check auth status on page load
	checkAuthStatus();
	

	
	$('.answers_row').on(clk, function(){
		$(this).closest('.answers_item').toggleClass('active');
	});
	$('.opencase_botoom a.active').on(clk, function(e){
		e.preventDefault();
		$('#bg,.drop_popup').addClass('active');
	});
	$('#bg').on(clk, function(){
		$('#bg,.popup_block').removeClass('active');
		
		// Clear any errors when closing popup
		setTimeout(function() {
			$('.form-error').removeClass('show error-shake').hide();
			$('.form-success').removeClass('show').hide();
		}, 300);
	});
	$('#change_nick').on(clk, function(e){
		e.preventDefault();
		$('#bg,.chgname_popup').addClass('active');
	});
	$('.platform_item').on(clk, function(e){
		$('.platform_list .platform_item').removeClass('active');
		$(this).addClass('active');
		
		// Clear form error when platform is selected
		$('.form-error').removeClass('show error-shake').hide();
	});

	// Password toggle functionality
	$('.password-toggle').on(clk, function(e){
		e.preventDefault();
		var $input = $(this).siblings('input[name="password"]');
		var $icon = $(this).find('img');
		
		if ($input.attr('type') === 'password') {
			$input.attr('type', 'text');
			$icon.attr('src', '/static/img/ico_eye_slash.svg');
		} else {
			$input.attr('type', 'password');
			$icon.attr('src', '/static/img/ico_eye.svg');
		}
	});

	// Input focus handling
	$('.drop_data_inp').on('focus', function(){
		var $input = $(this);
		var $row = $input.closest('.chgname_inprow');
		var $header = $row.find('.form_inp_hd');
		
		$header.removeClass('success error').addClass('focus');
		
		// Clear form error when user starts typing
		$('.form-error').removeClass('show error-shake').hide();
	});

	// Input change handling
	$('.drop_data_inp').on('input', function(){
		var $input = $(this);
		var $row = $input.closest('.chgname_inprow');
		
		// Clear form error when user types
		$('.form-error').removeClass('show error-shake').hide();
	});

	// Input validation on blur
	$('.drop_data_inp').on('blur', function(){
		var $input = $(this);
		var $row = $input.closest('.chgname_inprow');
		var $successIcon = $row.find('.success-icon');
		var $errorIcon = $row.find('.error-icon');
		var $errorMessage = $row.find('.error-message');
		
		// Clear previous states
		$input.removeClass('error success');
		$successIcon.removeClass('show').hide();
		$errorIcon.removeClass('show').hide();
		$errorMessage.removeClass('show error-shake').hide();
		
		// Clear header states
		var $header = $row.find('.form_inp_hd');
		$header.removeClass('focus success error');
		
		var value = $input.val().trim();
		var isValid = true;
		var errorMsg = '';
		
		// Validation logic
		if ($input.attr('name') === 'email') {
			var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
			if (!value) {
				isValid = false;
				errorMsg = 'Email is required';
			} else if (!emailRegex.test(value)) {
				isValid = false;
				errorMsg = 'Please enter a valid email address';
			}
		} else if ($input.attr('name') === 'password') {
			if (!value) {
				isValid = false;
				errorMsg = 'Password is required';
			} else if (value.length < 6) {
				isValid = false;
				errorMsg = 'Password must be at least 6 characters';
			}
		} else if ($input.attr('name') === 'name') {
			if (!value) {
				isValid = false;
				errorMsg = 'Username is required';
			} else if (!value.startsWith('@')) {
				isValid = false;
				errorMsg = 'Username must start with @';
			}
		}
		
		// Show appropriate icon and message
		if (isValid && value) {
			$input.addClass('success');
			$successIcon.show().addClass('show');
			$header.addClass('success');
		} else if (!isValid) {
			$input.addClass('error');
			$errorIcon.show().addClass('show');
			$errorMessage.text(errorMsg).show().addClass('show').addClass('error-shake');
			$header.addClass('error');
		}
	});

	function getCookie(name){
		let value = `; ${document.cookie}`;
		let parts = value.split(`; ${name}=`);
		if(parts.length === 2) return parts.pop().split(';').shift();
	}

	// Platform mapping
	const platformMap = ['playstation', 'xbox', 'nintendo', 'apple', 'windows', 'android'];

	// Ensure CSRF cookie is set
	fetch('/accounts/csrf/', {credentials: 'same-origin'})
		.catch(function(){ /* ignore */ });

	$('.drop_mid_confirm').on(clk, function(e){
		e.preventDefault();
		
		var $button = $(this);
		
		// Disable button during submission
		$button.prop('disabled', true).text('Processing...');
		
		// Clear previous form messages
		$('.form-error').removeClass('show error-shake').hide();
		$('.form-success').removeClass('show').hide();
		
		var $form = $(this).closest('form');
		var email = $form.find('input[name="email"]').val().trim();
		var password = $form.find('input[name="password"]').val().trim();
		var nick_in_game = $form.find('input[name="name"]').val().trim();
		var platformIndex = $('.platform_list .platform_item').index($('.platform_list .platform_item.active'));
		var platform = platformIndex >= 0 ? platformMap[platformIndex] : '';

		// Validate all fields before submission
		var isValid = true;
		var errors = [];
		
		if (!email) {
			errors.push('Email is required');
			isValid = false;
		}
		if (!password) {
			errors.push('Password is required');
			isValid = false;
		}
		if (!nick_in_game) {
			errors.push('Username is required');
			isValid = false;
		}
		if (!platform) {
			errors.push('Please select a platform');
			isValid = false;
		}
		
		if (!isValid) {
			$('.form-error').removeClass('error-shake').text(errors.join(', ')).show().addClass('show');
			
			// Re-enable button on validation error
			$button.prop('disabled', false).text('Confirm');
			return;
		}

		var payload = { 
			email: email, 
			password: password, 
			name: nick_in_game, 
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
		}).then(function(res){
			return res.json().then(function(data){ return { ok: res.ok, status: res.status, data: data }; });
		}).then(function(result){
			if(result.ok && result.data && result.data.success){
				$('#bg,.popup_block').removeClass('active');
				
				// Store auth data in localStorage
				localStorage.setItem('authToken', 'logged_in');
				localStorage.setItem('userData', JSON.stringify(result.data.user));
				
				// Update button to ACCOUNT
				$('#auth-button').text('ACCOUNT').attr('href', '/account/');
				$('#account-menu-item').show(); // Show account menu item
				
				// Show success message in a nice way
				var successMsg = result.data.action === 'register' 
					? 'Account created successfully! Welcome, ' + result.data.user.nick_in_game
					: 'Welcome back, ' + result.data.user.nick_in_game;
				
				// Show success message
				$('.form-error').removeClass('show error-shake').hide();
				$('.form-success').text(successMsg).show().addClass('show');
				
				// Auto-hide success message after 3 seconds
				setTimeout(function() {
					$('.form-success').removeClass('show').fadeOut();
				}, 3000);
				
				// Close popup after success
				setTimeout(function() {
					$('#bg,.popup_block').removeClass('active');
					
					// Clear success message when closing
					setTimeout(function() {
						$('.form-success').removeClass('show').hide();
					}, 300);
				}, 2000);
			} else {
				// Show error message in form
				var errorMsg = result.data && result.data.error ? result.data.error : 'Login failed';
				
				// Check if error indicates authentication failure
				if (result.status === 401 || result.status === 403) {
					// Authentication error, clear auth data
					localStorage.removeItem('authToken');
					localStorage.removeItem('userData');
					$('#auth-button').text('LOGIN').attr('href', '#');
					errorMsg = 'Authentication failed. Please login again.';
				}
				
				$('.form-error').removeClass('error-shake').text(errorMsg).show().addClass('show');
				
				// Add shake animation to error message
				setTimeout(function() {
					$('.form-error').addClass('error-shake');
				}, 100);
			}
		}).catch(function(error){
			$('.form-error').removeClass('error-shake').text('Network error. Please try again.').show().addClass('show');
			
			// Add shake animation to error message
			setTimeout(function() {
				$('.form-error').addClass('error-shake');
			}, 100);
			
			// Check if it's an authentication-related network error
			if (error.name === 'TypeError' && error.message.includes('fetch')) {
				// Network error, but don't force logout for network issues
				console.log('Network error occurred:', error);
			}
		}).finally(function(){
			// Re-enable button
			$button.prop('disabled', false).text('Confirm');
		});
	});
})

// Мобильное меню функциональность
$(document).ready(function() {
	// Проверяем, есть ли мобильное меню на странице
	if ($('#mobile-menu').length === 0) {
		return; // Мобильное меню не найдено на этой странице
	}
	
	// Открытие мобильного меню
	$('#mobile-menu-toggle').on('click', function() {
		$('#mobile-menu').addClass('active');
		$(this).addClass('active');
		$('body').addClass('menu-open');
	});
	
	// Закрытие мобильного меню
	$('#mobile-menu-close').on('click', function() {
		$('#mobile-menu').removeClass('active');
		$(this).removeClass('active');
		$('body').removeClass('menu-open');
	});
	
	// Закрытие меню при клике на пункт меню
	$('.mobile_nav_item').on('click', function() {
		$('#mobile-menu').removeClass('active');
		$('#mobile-menu-toggle').removeClass('active');
		$('body').removeClass('menu-open');
	});
	
	// Закрытие меню при клике вне его
	$(document).on('click', function(e) {
		if (!$(e.target).closest('#mobile-menu, #mobile-menu-toggle').length) {
			$('#mobile-menu').removeClass('active');
			$('#mobile-menu-toggle').removeClass('active');
			$('body').removeClass('menu-open');
		}
	});
	
	// Закрытие меню при свайпе влево
	let startX = 0;
	let currentX = 0;
	
	$('#mobile-menu').on('touchstart', function(e) {
		startX = e.originalEvent.touches[0].clientX;
	});
	
	$('#mobile-menu').on('touchmove', function(e) {
		currentX = e.originalEvent.touches[0].clientX;
	});
	
	$('#mobile-menu').on('touchend', function() {
		const diffX = startX - currentX;
		if (diffX > 50) { // Свайп влево более 50px
			$('#mobile-menu').removeClass('active');
			$('#mobile-menu-toggle').removeClass('active');
			$('body').removeClass('menu-open');
		}
	});
	
	// Синхронизация состояния авторизации для мобильного меню
	function updateMobileAuthStatus() {
		var authToken = localStorage.getItem('authToken');
		var userData = localStorage.getItem('userData');
		
		if (authToken && userData) {
			try {
				var user = JSON.parse(userData);
				if (user && user.nick_in_game) {
					$('#mobile-auth-button').text('ACCOUNT').attr('href', '/accounts/');
				}
			} catch (e) {
				console.log('Invalid user data found, clearing...');
			}
		} else {
			$('#mobile-auth-button').text('LOGIN').attr('href', '/login/');
		}
	}
	
	// Обновление статуса при загрузке страницы
	updateMobileAuthStatus();
	
	// Обработка клика по мобильной кнопке депозита
	$(document).on('click', '.mobile_deposit_btn', function(e) {
		// Закрываем мобильное меню перед переходом
		$('#mobile-menu').removeClass('active');
		$('#mobile-menu-toggle').removeClass('active');
		$('body').removeClass('menu-open');
	});
	
	// Обработка logout в мобильном меню
	$(document).on('click', '.mobile_logout', function(e) {
		e.preventDefault();
		
		// Закрываем мобильное меню
		$('#mobile-menu').removeClass('active');
		$('#mobile-menu-toggle').removeClass('active');
		$('body').removeClass('menu-open');
		
		// Очищаем localStorage
		localStorage.removeItem('authToken');
		localStorage.removeItem('userData');
		
		// Мгновенно перенаправляем на главную страницу
		window.location.href = '/';
		
		// В фоне выполняем logout через API (без ожидания)
		fetch('/accounts/logout/', {
			method: 'GET',
			credentials: 'same-origin'
		}).catch(function(error) {
			console.error('Logout API error:', error);
		});
	});
});