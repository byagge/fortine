// Account API integration
class AccountAPI {
	constructor() {
		this.baseURL = '/accounts/';
		this.csrfToken = null;
		this.init();
	}

	async init() {
		await this.getCSRFToken();
		this.loadAccountInfo();
		this.loadUserSkins();
		this.setupEventListeners();
	}

	async getCSRFToken() {
		try {
			const response = await fetch(this.baseURL + 'csrf/');
			const data = await response.json();
			this.csrfToken = data.csrfToken;
		} catch (error) {
			console.error('Error getting CSRF token:', error);
		}
	}

	async loadAccountInfo() {
		try {
			const response = await fetch(this.baseURL + 'account-info/', {
				headers: {
					'X-CSRFToken': this.csrfToken,
					'Content-Type': 'application/json',
				},
			});

			if (response.ok) {
				const data = await response.json();
				if (data.success) {
					this.updateAccountUI(data.user);
				}
			} else if (response.status === 401) {
				alert('Нужно зарегистрироваться или войти. Выполняется переход на главную.');
				window.location.href = '/';
			}
		} catch (error) {
			console.error('Error loading account info:', error);
		}
	}

	async loadUserSkins() {
		try {
			const response = await fetch(this.baseURL + 'user-skins/', {
				headers: {
					'X-CSRFToken': this.csrfToken,
					'Content-Type': 'application/json',
				},
			});

			if (response.ok) {
				const data = await response.json();
				if (data.success) {
					this.updateSkinsUI(data.skins);
				}
			} else if (response.status === 401) {
				alert('Нужно зарегистрироваться или войти. Выполняется переход на главную.');
				window.location.href = '/';
			}
		} catch (error) {
			console.error('Error loading user skins:', error);
		}
	}

	updateAccountUI(user) {
		// Update user email instead of username
		const emailElement = document.querySelector('.user-email');
		if (emailElement) {
			emailElement.textContent = user.email || 'No email';
		}

		// Update nickname
		const nickElement = document.querySelector('.user_nickname');
		if (nickElement) {
			nickElement.textContent = user.nick_in_game || 'Not set';
		}

		const regDateElement = document.querySelector('.user_regdate');
		if (regDateElement && user.registration_date) {
			regDateElement.textContent = user.registration_date;
		}

		const balanceElement = document.querySelector('.balance_money');
		if (balanceElement && user.balance) {
			balanceElement.textContent = `${user.balance} $`;
		}

		const headerBalanceElement = document.querySelector('.header_balance');
		if (headerBalanceElement && user.balance) {
			headerBalanceElement.textContent = user.balance;
		}

		const usernameElement = document.querySelector('.acc_name');
		if (usernameElement && user.nick_in_game) {
			usernameElement.textContent = user.nick_in_game;
		}

		// Update avatar if exists
		if (user.avatar) {
			const avatarElements = document.querySelectorAll('.profile-avatar, .profile-avatar-small, .acc_img img');
			avatarElements.forEach(img => {
				img.src = user.avatar;
			});
		}
	}

	updateSkinsUI(skins) {
		const caseList = document.querySelector('.case_list');
		if (!caseList) return;

		// Clear existing items
		caseList.innerHTML = '';

		// Add new skins
		skins.forEach(skin => {
			const skinElement = this.createSkinElement(skin);
			caseList.appendChild(skinElement);
		});
	}

	getRarityClass(rarity) {
		const map = {
			'common': 'blue',
			'uncommon': 'blue',
			'rare': 'pink',
			'epic': 'pink',
			'legendary': 'yel'
		};
		return map[rarity] || 'blue';
	}

	getRarityLabel(rarity) {
		const map = {
			'common': 'Common',
			'uncommon': 'Uncommon',
			'rare': 'Rare',
			'epic': 'Epic',
			'legendary': 'Legendary'
		};
		return map[rarity] || 'Common';
	}

	createSkinElement(skin) {
		const div = document.createElement('div');
		div.className = `case_item item_${this.getRarityClass(skin.rarity)}`;
		
		div.innerHTML = `
			<div class="item_top_plank"></div>
			<p class="item_mod">${skin.name}</p>
			<p class="item_name">${skin.case_name || ''}</p>
			<p class="item_descr">${this.getRarityLabel(skin.rarity)}</p>
			<div class="item_img"><img src="${skin.image}"></div>
		`;
		
		return div;
	}

	async updateNickname(newNickname) {
		try {
			const response = await fetch(this.baseURL + 'update-profile/', {
				method: 'POST',
				headers: {
					'X-CSRFToken': this.csrfToken,
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({
					nick_in_game: newNickname
				})
			});

			if (response.ok) {
				const data = await response.json();
				if (data.success) {
					this.loadAccountInfo(); // Reload account info
					this.showMessage('Nickname updated successfully!', 'success');
					return true; // Indicate success
				} else {
					this.showMessage(data.error || 'Failed to update nickname', 'error');
					return false; // Indicate failure
				}
			} else if (response.status === 401) {
				alert('Нужно зарегистрироваться или войти. Выполняется переход на главную.');
				window.location.href = '/';
				return false;
			} else {
				this.showMessage('Failed to update nickname', 'error');
				return false; // Indicate failure
			}
			
		} catch (error) {
			console.error('Error updating nickname:', error);
			this.showMessage('Error updating nickname', 'error');
			return false; // Indicate failure
		}
	}

	async uploadAvatar(file) {
		try {
			const formData = new FormData();
			formData.append('avatar', file);

			const response = await fetch(this.baseURL + 'upload-avatar/', {
				method: 'POST',
				headers: {
					'X-CSRFToken': this.csrfToken,
				},
				body: formData
			});

			if (response.ok) {
				const data = await response.json();
				if (data.success) {
					this.showMessage('Avatar uploaded successfully!', 'success');
					this.loadAccountInfo(); // Reload account info to show new avatar
				} else {
					this.showMessage(data.error || 'Failed to upload avatar', 'error');
				}
			} else if (response.status === 401) {
				alert('Нужно зарегистрироваться или войти. Выполняется переход на главную.');
				window.location.href = '/';
			} else {
				this.showMessage('Failed to upload avatar', 'error');
			}
		} catch (error) {
			console.error('Error uploading avatar:', error);
			this.showMessage('Error uploading avatar', 'error');
		}
	}

	async logout() {
		try {
			const response = await fetch(this.baseURL + 'logout/', {
				method: 'POST',
				headers: {
					'X-CSRFToken': this.csrfToken,
					'Content-Type': 'application/json',
				},
			});

			if (response.ok) {
				const data = await response.json();
				if (data.success) {
					// Clear local storage
					localStorage.removeItem('authToken');
					localStorage.removeItem('userData');
					
					// Redirect to home page
					window.location.href = '/';
				} else {
					this.showMessage(data.error || 'Failed to logout', 'error');
				}
			} else {
				this.showMessage('Failed to logout', 'error');
			}
		} catch (error) {
			console.error('Error logging out:', error);
			this.showMessage('Error logging out', 'error');
		}
	}

	showMessage(message, type = 'info') {
		// Remove existing messages first
		const existingMessages = document.querySelectorAll('.message');
		existingMessages.forEach(msg => {
			if (msg.parentNode) {
				msg.parentNode.removeChild(msg);
			}
		});

		// Create a new message display
		const messageDiv = document.createElement('div');
		messageDiv.className = `message ${type}`;
		messageDiv.textContent = message;

		document.body.appendChild(messageDiv);

		// Remove message after 4 seconds
		setTimeout(() => {
			if (messageDiv.parentNode) {
				messageDiv.style.animation = 'messageSlideOut 0.3s ease forwards';
				setTimeout(() => {
					if (messageDiv.parentNode) {
						messageDiv.parentNode.removeChild(messageDiv);
					}
				}, 300);
			}
		}, 4000);
	}

	setupEventListeners() {
		// Handle nickname change
		document.addEventListener('click', (e) => {
			if (e.target.closest('#change_nick')) {
				e.preventDefault();
				this.showNicknamePopup();
			}
		});

		// Handle popup confirm button
		document.addEventListener('click', (e) => {
			if (e.target.closest('.drop_mid_confirm')) {
				e.preventDefault();
				this.confirmNicknameChange();
			}
		});

		// Handle logout button
		document.addEventListener('click', (e) => {
			if (e.target.closest('#logout-btn')) {
				e.preventDefault();
				this.logout();
			}
		});

		// Handle avatar upload
		const avatarUpload = document.getElementById('avatar-upload');
		if (avatarUpload) {
			avatarUpload.addEventListener('change', (e) => {
				const file = e.target.files[0];
				if (file) {
					this.uploadAvatar(file);
					// Reset input
					e.target.value = '';
				}
			});
		}

		// Handle nickname input validation in real-time
		document.addEventListener('input', (e) => {
			if (e.target.name === 'new_name') {
				this.validateNicknameInput(e.target);
			}
		});

		// Handle nickname input focus for auto-@
		document.addEventListener('focus', (e) => {
			if (e.target.name === 'new_name') {
				this.handleNicknameFocus(e.target);
			}
		}, true);

		// Handle nickname input blur for auto-@
		document.addEventListener('blur', (e) => {
			if (e.target.name === 'new_name') {
				this.handleNicknameBlur(e.target);
			}
		}, true);

		// Handle nickname input enter key
		document.addEventListener('keypress', (e) => {
			if (e.target.name === 'new_name' && e.key === 'Enter') {
				e.preventDefault();
				this.confirmNicknameChange();
			}
		});

		// Handle background click to close popup
		document.addEventListener('click', (e) => {
			if (e.target.id === 'bg') {
				this.closeNicknamePopup();
			}
		});

		// Handle escape key to close popup
		document.addEventListener('keydown', (e) => {
			if (e.key === 'Escape') {
				this.closeNicknamePopup();
			}
		});
	}

	handleNicknameFocus(input) {
		// If input is empty or doesn't start with @, add @
		if (!input.value || !input.value.startsWith('@')) {
			input.value = '@' + (input.value || '');
			// Move cursor after @
			setTimeout(() => {
				input.setSelectionRange(1, input.value.length);
			}, 0);
		}
	}

	handleNicknameBlur(input) {
		// Ensure @ is present when leaving the field
		if (input.value && !input.value.startsWith('@')) {
			input.value = '@' + input.value;
		}
		// Validate after ensuring @ is present
		this.validateNicknameInput(input);
	}

	validateNicknameInput(input) {
		let value = input.value.trim();
		const checkIcon = input.nextElementSibling;
		const confirmButton = input.closest('.chgname_popup').querySelector('.drop_mid_confirm');
		
		// Auto-add @ if not present
		if (value && !value.startsWith('@')) {
			value = '@' + value;
			input.value = value;
		}
		
		// Basic validation: nickname should be 3-20 characters (excluding @), alphanumeric and underscore only
		// Remove @ for length calculation
		const nicknameWithoutAt = value.startsWith('@') ? value.substring(1) : value;
		const isValid = nicknameWithoutAt.length >= 2 && nicknameWithoutAt.length <= 19 && 
					  /^[a-zA-Z0-9_]+$/.test(nicknameWithoutAt) && value.startsWith('@');
		
		if (isValid && value) {
			input.classList.add('valid');
			checkIcon.style.display = 'block';
			confirmButton.disabled = false;
			confirmButton.style.opacity = '1';
			confirmButton.style.cursor = 'pointer';
		} else {
			input.classList.remove('valid');
			checkIcon.style.display = 'none';
			confirmButton.disabled = true;
			confirmButton.style.opacity = '0.5';
			confirmButton.style.cursor = 'not-allowed';
		}
	}

	showNicknamePopup() {
		const popup = document.querySelector('.chgname_popup');
		const background = document.getElementById('bg');
		
		if (popup) {
			popup.style.display = 'block';
			
			// Activate background blur
			if (background) {
				background.classList.add('active');
			}
			
			// Focus on input
			const input = popup.querySelector('input[name="new_name"]');
			const confirmButton = popup.querySelector('.drop_mid_confirm');
			
			if (input) {
				input.focus();
				// Set current nickname as default value
				const currentNick = document.querySelector('.user_nickname').textContent;
				if (currentNick && currentNick !== 'Not set') {
					// Ensure @ is present in the input
					if (currentNick.startsWith('@')) {
						input.value = currentNick;
					} else {
						input.value = '@' + currentNick;
					}
				} else {
					input.value = '@';
				}
				
				// Validate initial value
				this.validateNicknameInput(input);
			}
			
			// Initially disable confirm button
			if (confirmButton) {
				confirmButton.disabled = true;
				confirmButton.style.opacity = '0.5';
				confirmButton.style.cursor = 'not-allowed';
			}
		}
	}

	async confirmNicknameChange() {
		const input = document.querySelector('input[name="new_name"]');
		if (input && input.value.trim() && input.classList.contains('valid')) {
			let nickname = input.value.trim();
			
			// Ensure @ is present
			if (!nickname.startsWith('@')) {
				nickname = '@' + nickname;
			}
			
			// Show success message first
			this.showMessage('Updating nickname...', 'info');
			
			// Update nickname and check result
			const success = await this.updateNickname(nickname);
			
			if (success) {
				// Close popup after a short delay to show the success message
				setTimeout(() => {
					// Hide popup and background
					const popup = document.querySelector('.chgname_popup');
					const background = document.getElementById('bg');
					
					if (popup) {
						popup.style.display = 'none';
						// Clear input and reset validation
						input.value = '@';
						input.classList.remove('valid');
						const checkIcon = input.nextElementSibling;
						if (checkIcon) {
							checkIcon.style.display = 'none';
						}
					}
					
					// Remove background blur
					if (background) {
						background.classList.remove('active');
					}
				}, 500);
			}
			// If not successful, popup stays open and error message is shown
		} else {
			this.showMessage('Please enter a valid nickname (2-19 characters after @, alphanumeric and underscore only)', 'error');
		}
	}

	closeNicknamePopup() {
		const popup = document.querySelector('.chgname_popup');
		const background = document.getElementById('bg');
		
		if (popup && popup.style.display !== 'none') {
			popup.style.display = 'none';
			// Reset input and validation
			const input = popup.querySelector('input[name="new_name"]');
			if (input) {
				input.value = '@';
				input.classList.remove('valid');
				const checkIcon = input.nextElementSibling;
				if (checkIcon) {
					checkIcon.style.display = 'none';
				}
			}
			// Reset confirm button
			const confirmButton = popup.querySelector('.drop_mid_confirm');
			if (confirmButton) {
				confirmButton.disabled = true;
				confirmButton.style.opacity = '0.5';
				confirmButton.style.cursor = 'not-allowed';
			}
		}
		
		// Remove background blur
		if (background) {
			background.classList.remove('active');
		}
	}
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
	new AccountAPI();
}); 