// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Navbar scroll effect
const navbar = document.querySelector('.navbar');
let lastScroll = 0;

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    
    if (currentScroll <= 0) {
        navbar.classList.remove('scroll-up');
        return;
    }
    
    if (currentScroll > lastScroll && !navbar.classList.contains('scroll-down')) {
        // Scroll Down
        navbar.classList.remove('scroll-up');
        navbar.classList.add('scroll-down');
    } else if (currentScroll < lastScroll && navbar.classList.contains('scroll-down')) {
        // Scroll Up
        navbar.classList.remove('scroll-down');
        navbar.classList.add('scroll-up');
    }
    lastScroll = currentScroll;
});

// Newsletter form submission
const newsletterForm = document.querySelector('.newsletter-form');
if (newsletterForm) {
    newsletterForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const email = newsletterForm.querySelector('input[type="email"]').value;
        
        if (email) {
            // Here you would typically send the email to your server
            showNotification('Thank you for subscribing to our newsletter!', 'success');
            newsletterForm.reset();
        }
    });
}

// Login Form Submission
const loginForm = document.querySelector('.login-form');
if (loginForm) {
    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const email = document.querySelector('#email').value;
        const password = document.querySelector('#password').value;
        const remember = document.querySelector('#remember').checked;

        // Basic validation
        if (!email || !password) {
            showNotification('Please fill in all fields', 'error');
            return;
        }

        // Here you would typically send the login data to your server
        // For demo purposes, we'll simulate a successful login
        showNotification('Login successful! Redirecting...', 'success');
        
        // Store login state if remember me is checked
        if (remember) {
            localStorage.setItem('isLoggedIn', 'true');
            localStorage.setItem('userEmail', email);
        }

        // Redirect to shop page after successful login
        setTimeout(() => {
            window.location.href = 'shop.html';
        }, 1500);
    });
}

// Signup Form Submission
const signupForm = document.querySelector('.signup-form');
if (signupForm) {
    signupForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const fullname = document.querySelector('#fullname').value;
        const email = document.querySelector('#email').value;
        const password = document.querySelector('#password').value;
        const confirmPassword = document.querySelector('#confirm-password').value;
        const terms = document.querySelector('#terms').checked;

        // Basic validation
        if (!fullname || !email || !password || !confirmPassword) {
            showNotification('Please fill in all fields', 'error');
            return;
        }

        if (password !== confirmPassword) {
            showNotification('Passwords do not match', 'error');
            return;
        }

        if (!terms) {
            showNotification('Please agree to the Terms & Conditions', 'error');
            return;
        }

        // Here you would typically send the signup data to your server
        // For demo purposes, we'll simulate a successful signup
        showNotification('Account created successfully! Redirecting to login...', 'success');
        
        // Redirect to login page after successful signup
        setTimeout(() => {
            window.location.href = 'login.html';
        }, 1500);
    });
}

// Password visibility toggle
const togglePasswordBtns = document.querySelectorAll('.toggle-password');
togglePasswordBtns.forEach(btn => {
    btn.addEventListener('click', function() {
        const passwordInput = this.previousElementSibling;
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
        this.classList.toggle('fa-eye');
        this.classList.toggle('fa-eye-slash');
    });
});

// Password strength checker
const passwordInput = document.querySelector('#password');
const strengthMeter = document.querySelector('.strength-meter');
const strengthValue = document.querySelector('#strength-value');

if (passwordInput && strengthMeter && strengthValue) {
    passwordInput.addEventListener('input', function() {
        const password = this.value;
        let strength = 0;
        let feedback = '';

        // Length check
        if (password.length >= 8) strength += 1;
        
        // Contains number
        if (/\d/.test(password)) strength += 1;
        
        // Contains lowercase
        if (/[a-z]/.test(password)) strength += 1;
        
        // Contains uppercase
        if (/[A-Z]/.test(password)) strength += 1;
        
        // Contains special character
        if (/[^A-Za-z0-9]/.test(password)) strength += 1;

        // Update strength meter
        strengthMeter.className = 'strength-meter';
        if (strength > 0) {
            if (strength <= 2) {
                strengthMeter.classList.add('weak');
                feedback = 'Weak';
            } else if (strength <= 3) {
                strengthMeter.classList.add('medium');
                feedback = 'Medium';
            } else if (strength <= 4) {
                strengthMeter.classList.add('strong');
                feedback = 'Strong';
            } else {
                strengthMeter.classList.add('very-strong');
                feedback = 'Very Strong';
            }
        }
        strengthValue.textContent = feedback;
    });
}

// Shop Page Functionality
document.addEventListener('DOMContentLoaded', function() {
    // Quick View Modal
    const quickViewBtns = document.querySelectorAll('.quick-view-btn');
    const modal = document.querySelector('.modal');
    const closeModal = document.querySelector('.close-modal');

    if (quickViewBtns.length > 0) {
        quickViewBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                const productCard = this.closest('.product-card');
                const productName = productCard.querySelector('h3').textContent;
                const productPrice = productCard.querySelector('.product-price').textContent;
                const productImage = productCard.querySelector('.product-image img').src;
                const productRating = productCard.querySelector('.product-rating').innerHTML;

                const modalContent = document.querySelector('.modal-content');
                modalContent.innerHTML = `
                    <span class="close-modal">&times;</span>
                    <div class="modal-product">
                        <div class="modal-product-image">
                            <img src="${productImage}" alt="${productName}">
                        </div>
                        <div class="modal-product-info">
                            <h2>${productName}</h2>
                            <div class="modal-product-rating">${productRating}</div>
                            <div class="modal-product-price">${productPrice}</div>
                            <p class="modal-product-description">
                                Experience the perfect blend of style and comfort with our premium collection. 
                                Each piece is crafted with attention to detail and quality materials.
                            </p>
                            <div class="modal-product-actions">
                                <div class="quantity-selector">
                                    <button class="quantity-btn minus">-</button>
                                    <input type="number" value="1" min="1" max="10">
                                    <button class="quantity-btn plus">+</button>
                                </div>
                                <button class="add-to-cart-btn">
                                    <i class="fas fa-shopping-cart"></i>
                                    Add to Cart
                                </button>
                            </div>
                        </div>
                    </div>
                `;

                modal.style.display = 'block';
                document.body.style.overflow = 'hidden';

                // Add event listeners for the new modal elements
                const newCloseModal = modalContent.querySelector('.close-modal');
                const quantityInput = modalContent.querySelector('.quantity-selector input');
                const minusBtn = modalContent.querySelector('.quantity-btn.minus');
                const plusBtn = modalContent.querySelector('.quantity-btn.plus');

                newCloseModal.addEventListener('click', closeModalHandler);
                minusBtn.addEventListener('click', () => updateQuantity(quantityInput, -1));
                plusBtn.addEventListener('click', () => updateQuantity(quantityInput, 1));
            });
        });
    }

    if (closeModal) {
        closeModal.addEventListener('click', closeModalHandler);
    }

    // Close modal when clicking outside
    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            closeModalHandler();
        }
    });

    function closeModalHandler() {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }

    function updateQuantity(input, change) {
        const newValue = parseInt(input.value) + change;
        if (newValue >= 1 && newValue <= 10) {
            input.value = newValue;
        }
    }

    // Add to Cart Functionality
    const addToCartBtns = document.querySelectorAll('.add-to-cart-btn');
    addToCartBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const productCard = this.closest('.product-card');
            const productName = productCard.querySelector('h3').textContent;
            const productPrice = productCard.querySelector('.product-price').textContent;
            
            // Check if user is logged in
            if (!localStorage.getItem('isLoggedIn')) {
                showNotification('Please login to add items to cart', 'error');
                setTimeout(() => {
                    window.location.href = 'login.html';
                }, 1500);
                return;
            }
            
            // Show success message
            showNotification(`${productName} added to cart!`, 'success');
        });
    });

    // Price Range Filter
    const priceSlider = document.querySelector('.price-slider');
    const minPriceInput = document.querySelector('.min-price');
    const maxPriceInput = document.querySelector('.max-price');

    if (priceSlider && minPriceInput && maxPriceInput) {
        priceSlider.addEventListener('input', function() {
            const value = this.value;
            maxPriceInput.value = value;
            filterProducts();
        });

        minPriceInput.addEventListener('change', function() {
            if (parseInt(this.value) > parseInt(maxPriceInput.value)) {
                this.value = maxPriceInput.value;
            }
            filterProducts();
        });

        maxPriceInput.addEventListener('change', function() {
            if (parseInt(this.value) < parseInt(minPriceInput.value)) {
                this.value = minPriceInput.value;
            }
            filterProducts();
        });
    }

    // Category Filter
    const categoryCheckboxes = document.querySelectorAll('.filter-list input[type="checkbox"]');
    categoryCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', filterProducts);
    });

    // Search Functionality
    const searchForm = document.querySelector('.search-bar');
    const searchInput = document.querySelector('.search-bar input');

    if (searchForm && searchInput) {
        searchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            filterProducts();
        });

        searchInput.addEventListener('input', filterProducts);
    }
});

// Helper function to filter products
function filterProducts() {
    const searchTerm = document.querySelector('.search-bar input')?.value.toLowerCase() || '';
    const minPrice = parseInt(document.querySelector('.min-price')?.value) || 0;
    const maxPrice = parseInt(document.querySelector('.max-price')?.value) || Infinity;
    const selectedCategories = Array.from(document.querySelectorAll('.filter-list input[type="checkbox"]:checked'))
        .map(checkbox => checkbox.value);

    const productCards = document.querySelectorAll('.product-card');

    productCards.forEach(card => {
        const productName = card.querySelector('h3').textContent.toLowerCase();
        const productPrice = parseFloat(card.querySelector('.product-price').textContent.replace('$', ''));
        const productCategory = card.dataset.category;

        const matchesSearch = productName.includes(searchTerm);
        const matchesPrice = productPrice >= minPrice && productPrice <= maxPrice;
        const matchesCategory = selectedCategories.length === 0 || selectedCategories.includes(productCategory);

        card.style.display = matchesSearch && matchesPrice && matchesCategory ? 'block' : 'none';
    });
}

// Notification system
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Trigger animation
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);
    
    // Remove notification after 3 seconds
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

// Add notification styles
const style = document.createElement('style');
style.textContent = `
    .notification {
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 25px;
        border-radius: 5px;
        color: white;
        font-weight: 500;
        transform: translateX(120%);
        transition: transform 0.3s ease;
        z-index: 1000;
    }
    
    .notification.show {
        transform: translateX(0);
    }
    
    .notification.success {
        background-color: #4CAF50;
    }
    
    .notification.error {
        background-color: #f44336;
    }
`;
document.head.appendChild(style);

// Cart functionality
class ShoppingCart {
    constructor() {
        this.items = [];
        this.modal = document.getElementById('cart-modal');
        this.cartItems = document.getElementById('cart-items');
        this.cartCount = document.getElementById('cart-count');
        this.cartTotal = document.getElementById('cart-total');
        this.initializeEventListeners();
        this.loadCart(); // Load cart items when page loads
    }

    initializeEventListeners() {
        // Cart button click
        const cartBtn = document.getElementById('cart-btn');
        if (cartBtn) {
            cartBtn.addEventListener('click', () => this.openModal());
        }

        // Close modal
        const closeBtn = this.modal.querySelector('.close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => this.closeModal());
        }

        // Clear cart
        const clearCartBtn = document.getElementById('clear-cart');
        if (clearCartBtn) {
            clearCartBtn.addEventListener('click', () => this.clearCart());
        }

        // Checkout
        const checkoutBtn = document.getElementById('checkout');
        if (checkoutBtn) {
            checkoutBtn.addEventListener('click', () => this.checkout());
        }

        // Add to cart buttons
        document.querySelectorAll('.add-to-cart-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const productCard = e.target.closest('.product-card');
                const product = {
                    id: productCard.dataset.id,
                    name: productCard.querySelector('h3').textContent,
                    price: parseFloat(productCard.querySelector('.product-price').textContent.replace('$', '')),
                    quantity: 1
                };
                this.addToCart(product);
            });
        });
    }

    async loadCart() {
        const userId = localStorage.getItem('userId');
        if (!userId) {
            this.items = [];
            this.updateCart();
            return;
        }
        try {
            const response = await fetch(`/get_cart?user_id=${userId}`);
            if (response.ok) {
                const data = await response.json();
                this.items = data.items || [];
                this.updateCart();
            }
        } catch (error) {
            console.error('Error loading cart:', error);
        }
    }

    async addToCart(product) {
        const userId = localStorage.getItem('userId');
        if (!userId) {
            alert('Please log in to add items to your cart.');
            return;
        }
        const payload = {
            ...product,
            user_id: userId
        };
        const response = await fetch('/add_to_cart', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (response.ok) {
            const data = await response.json();
            this.items = data.items;
            this.updateCart();
            showNotification('Product added to cart!', 'success');
        } else {
            showNotification('Failed to add product to cart', 'error');
        }
    }

    async removeFromCart(productId) {
        const userId = localStorage.getItem('userId');
        if (!userId) {
            alert('Please log in to remove items from your cart.');
            return;
        }
        try {
            const response = await fetch('/remove_from_cart', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ productId, user_id: userId })
            });

            if (response.ok) {
                const data = await response.json();
                this.items = data.items;
                this.updateCart();
                showNotification('Product removed from cart', 'success');
            } else {
                showNotification('Failed to remove product', 'error');
            }
        } catch (error) {
            console.error('Error removing from cart:', error);
            showNotification('Error removing from cart', 'error');
        }
    }

    async updateCart() {
        this.renderCartItems();
        this.updateCartCount();
        this.updateCartTotal();
    }

    updateCartCount() {
        const totalItems = this.items.reduce((sum, item) => sum + item.quantity, 0);
        this.cartCount.textContent = totalItems;
    }

    updateCartTotal() {
        const total = this.items.reduce((sum, item) => sum + (item.price * item.quantity), 0);
        this.cartTotal.textContent = total.toFixed(2);
    }

    renderCartItems() {
        this.cartItems.innerHTML = '';
        
        if (this.items.length === 0) {
            this.cartItems.innerHTML = '<p class="empty-cart">Your cart is empty</p>';
            return;
        }

        this.items.forEach(item => {
            const cartItem = document.createElement('div');
            cartItem.className = 'cart-item';
            cartItem.innerHTML = `
                <div class="cart-item-info">
                    <h4>${item.name}</h4>
                    <p class="cart-item-price">$${item.price.toFixed(2)}</p>
                </div>
                <div class="cart-item-quantity">
                    <button class="quantity-btn minus" data-id="${item.id}">-</button>
                    <span>${item.quantity}</span>
                    <button class="quantity-btn plus" data-id="${item.id}">+</button>
                </div>
                <button class="remove-item" data-id="${item.id}">
                    <i class="fas fa-trash"></i>
                </button>
            `;

            // Add event listeners for quantity buttons
            const minusBtn = cartItem.querySelector('.minus');
            const plusBtn = cartItem.querySelector('.plus');
            const removeBtn = cartItem.querySelector('.remove-item');

            minusBtn.addEventListener('click', () => this.updateItemQuantity(item.id, -1));
            plusBtn.addEventListener('click', () => this.updateItemQuantity(item.id, 1));
            removeBtn.addEventListener('click', () => this.removeFromCart(item.id));

            this.cartItems.appendChild(cartItem);
        });
    }

    async updateItemQuantity(productId, change) {
        const userId = localStorage.getItem('userId');
        if (!userId) {
            alert('Please log in to update your cart.');
            return;
        }
        const item = this.items.find(item => item.id === productId);
        if (!item) return;

        const newQuantity = item.quantity + change;
        if (newQuantity < 1) {
            await this.removeFromCart(productId);
            return;
        }

        try {
            const response = await fetch('/update_cart', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    productId,
                    quantity: newQuantity,
                    user_id: userId
                })
            });

            if (response.ok) {
                const data = await response.json();
                this.items = data.items;
                this.updateCart();
            } else {
                showNotification('Failed to update quantity', 'error');
            }
        } catch (error) {
            console.error('Error updating quantity:', error);
            showNotification('Error updating quantity', 'error');
        }
    }

    async clearCart() {
        const userId = localStorage.getItem('userId');
        if (!userId) {
            alert('Please log in to clear your cart.');
            return;
        }
        try {
            const response = await fetch('/clear_cart', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ user_id: userId })
            });

            if (response.ok) {
                this.items = [];
                this.updateCart();
                showNotification('Cart cleared successfully', 'success');
            } else {
                showNotification('Failed to clear cart', 'error');
            }
        } catch (error) {
            console.error('Error clearing cart:', error);
            showNotification('Error clearing cart', 'error');
        }
    }

    checkout() {
        if (this.items.length === 0) {
            showNotification('Your cart is empty', 'error');
            return;
        }
        // Implement checkout logic here
        showNotification('Checkout functionality coming soon!', 'info');
    }

    openModal() {
        this.modal.style.display = 'block';
        document.body.style.overflow = 'hidden';
    }

    closeModal() {
        this.modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
}

// Initialize cart when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.cart = new ShoppingCart();
}); 