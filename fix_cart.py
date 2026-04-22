from pathlib import Path
import re

root = Path(r"d:\VS Projects\Maxi's Boutique\Boutique")

# Home page fixes
home_path = root / 'Home.html'
text = home_path.read_text(encoding='utf-8')
text = text.replace("background-image: url('images/img1.jpg')", "background-image: url('../images/img1.jpg')")
text = re.sub(r'src="images/([^"]+)"', r'src="../images/\1"', text)
# fix incorrect filenames
text = text.replace('src="../images/pic13.jpg"', 'src="../images/img13.jpg"')
# fix navigation and add cart link if missing
text = text.replace(
    '<nav>\n            <a href="Shop.html">Shop</a>\n            <a href="About.html">About</a>\n            <a href="Contact.html">Contact</a>\n        </nav>',
    '<nav>\n            <a href="Home.html">Home</a>\n            <a href="Shop.html">Shop</a>\n            <a href="About.html">About</a>\n            <a href="Contact.html">Contact</a>\n            <a href="Cart.html">Cart</a>\n        </nav>'
)
text = text.replace('<button type="submit">', '<button type="button">')

home_script = '''    <script>
        const cartKey = 'boutiqueCart';
        function getCart() {
            return JSON.parse(localStorage.getItem(cartKey) || '[]');
        }
        function saveCart(cart) {
            localStorage.setItem(cartKey, JSON.stringify(cart));
        }
        function updateCartCount() {
            const count = getCart().reduce((sum, item) => sum + item.quantity, 0);
            const counter = document.getElementById('cart-count-display');
            if (counter) counter.textContent = count;
        }
        function addToCart(productName, productPrice) {
            const cart = getCart();
            const existing = cart.find(item => item.name === productName);
            if (existing) {
                existing.quantity += 1;
            } else {
                cart.push({ name: productName, price: productPrice, quantity: 1 });
            }
            saveCart(cart);
            updateCartCount();
            alert(`${productName} has been added to your cart!`);
        }
        function attachCartButtons() {
            document.querySelectorAll('.product-card').forEach(card => {
                const btn = card.querySelector('.contact-form button');
                if (!btn || btn.disabled) return;
                const name = card.querySelector('.product-info h3').textContent.trim();
                const priceText = card.querySelector('.price').textContent.trim();
                const price = parseFloat(priceText.replace(/[^0-9.]/g, '')) || 0;
                btn.addEventListener('click', () => addToCart(name, price));
            });
        }
        document.addEventListener('DOMContentLoaded', () => {
            updateCartCount();
            attachCartButtons();
        });
    </script>'''

if '</script>' not in text:
    text = text.replace('    <footer>', home_script + '\n    <footer>', 1)
home_path.write_text(text, encoding='utf-8')
print('Home.html updated')

# Shop page fixes
shop_path = root / 'Shop.html'
text = shop_path.read_text(encoding='utf-8')
text = text.replace("background-image: url('images/img1.jpg')", "background-image: url('../images/img1.jpg')")
text = re.sub(r'src="images/([^"]+)"', r'src="../images/\1"', text)
text = text.replace('src="../images/pic14.jpg"', 'src="../images/img14.jpg"')
text = text.replace(
    '<nav>\n            <a href="Home.html">Home</a>\n            <a href="About.html">About</a>\n            <a href="Contact.html">Contact</a>\n        </nav>',
    '<nav>\n            <a href="Home.html">Home</a>\n            <a href="Shop.html">Shop</a>\n            <a href="About.html">About</a>\n            <a href="Contact.html">Contact</a>\n            <a href="Cart.html">Cart</a>\n        </nav>'
)

shop_script = '''    <script>
        const cartKey = 'boutiqueCart';
        function getCart() {
            return JSON.parse(localStorage.getItem(cartKey) || '[]');
        }
        function saveCart(cart) {
            localStorage.setItem(cartKey, JSON.stringify(cart));
        }
        function updateCartCount() {
            const count = getCart().reduce((sum, item) => sum + item.quantity, 0);
            const counter = document.getElementById('cart-count');
            if (counter) counter.textContent = count;
        }
        function addToCart(productName, productPrice) {
            const cart = getCart();
            const existing = cart.find(item => item.name === productName);
            if (existing) {
                existing.quantity += 1;
            } else {
                cart.push({ name: productName, price: productPrice, quantity: 1 });
            }
            saveCart(cart);
            updateCartCount();
            alert(`${productName} has been added to your cart!`);
        }
        function attachCartButtons() {
            document.querySelectorAll('.product-card .contact-form button').forEach(btn => {
                if (!btn || btn.disabled) return;
                const card = btn.closest('.product-card');
                const name = card.querySelector('.product-info h3').textContent.trim();
                const priceText = card.querySelector('.price').textContent.trim();
                const price = parseFloat(priceText.replace(/[^0-9.]/g, '')) || 0;
                if (!btn.onclick) {
                    btn.addEventListener('click', () => addToCart(name, price));
                }
            });
        }
        document.addEventListener('DOMContentLoaded', () => {
            updateCartCount();
            attachCartButtons();
        });
    </script>'''

text = re.sub(r'<script>.*?</script>', shop_script, text, flags=re.S)
shop_path.write_text(text, encoding='utf-8')
print('Shop.html updated')

# Cart page fixes
cart_path = root / 'Cart.html'
text = cart_path.read_text(encoding='utf-8')
text = text.replace('<tbody>\n                <tr>\n                    <td>Red Dress</td>\n                    <td>$50</td>\n                    <td>1</td>\n                    <td>$50</td>\n                </tr>\n                <tr>\n                    <td>Blue Scarf</td>\n                    <td>$20</td>\n                    <td>2</td>\n                    <td>$40</td>\n                </tr>\n                <tr>\n                    <td>White Shoes</td>\n                    <td>$30</td>\n                    <td>1</td>\n                    <td>$30</td>\n                </tr>\n            </tbody>', '<tbody id="cart-body"></tbody>')
text = text.replace('<h3>Total: $120</h3>', '<h3>Total: <span id="cart-total">$0</span></h3>')
text = text.replace('href="Payment.py"', 'href="Pay.html"')
text = text.replace('&copy; 2025 Boutique Store | All Rights Reserved', '&copy; 2026 Boutique Store | All Rights Reserved')
text = text.replace('</body>', '''    <script>
        const cartKey = 'boutiqueCart';
        function getCart() {
            return JSON.parse(localStorage.getItem(cartKey) || '[]');
        }
        function formatCurrency(value) {
            return '$' + value.toFixed(2);
        }
        function renderCart() {
            const cart = getCart();
            const body = document.getElementById('cart-body');
            const totalEl = document.getElementById('cart-total');
            body.innerHTML = '';
            if (!cart.length) {
                body.innerHTML = '<tr><td colspan="4" style="text-align:center;">Your cart is empty.</td></tr>';
                totalEl.textContent = '$0';
                return;
            }
            let total = 0;
            cart.forEach(item => {
                const row = document.createElement('tr');
                const itemTotal = item.price * item.quantity;
                total += itemTotal;
                row.innerHTML = `<td>${item.name}</td><td>${formatCurrency(item.price)}</td><td>${item.quantity}</td><td>${formatCurrency(itemTotal)}</td>`;
                body.appendChild(row);
            });
            totalEl.textContent = formatCurrency(total);
        }
        document.addEventListener('DOMContentLoaded', renderCart);
    </script>
</body>''')
cart_path.write_text(text, encoding='utf-8')
print('Cart.html updated')
