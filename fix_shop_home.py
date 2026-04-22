from pathlib import Path
import re

root = Path(r"d:\VS Projects\Maxi's Boutique\Boutique")

files = [root / 'Home.html', root / 'Shop.html']
for path in files:
    text = path.read_text(encoding='utf-8')
    text = text.replace("background-image: url('images/", "background-image: url('../images/")
    text = text.replace('src="images/', 'src="../images/')
    text = text.replace('src="../images/pic13.jpg"', 'src="../images/img13.jpg"')
    text = text.replace('src="../images/pic14.jpg"', 'src="../images/img14.jpg"')
    if path.name == 'Home.html':
        text = re.sub(r'<form action="#" method="POST">\s*<button type="submit">', '<button type="button">', text)
        text = re.sub(r'</button>\s*</form>', '</button>', text)
        text = text.replace(
            '<nav>\n            <a href="Shop.html">Shop</a>\n            <a href="About.html">About</a>\n            <a href="Contact.html">Contact</a>\n        </nav>',
            '<nav>\n            <a href="Home.html">Home</a>\n            <a href="Shop.html">Shop</a>\n            <a href="About.html">About</a>\n            <a href="Contact.html">Contact</a>\n            <a href="Cart.html">Cart</a>\n        </nav>'
        )
    if path.name == 'Shop.html':
        text = text.replace(
            '<nav>\n            <a href="Home.html">Home</a>\n\n            <a href="About.html">About</a>\n            <a href="Contact.html">Contact</a>\n        </nav>',
            '<nav>\n            <a href="Home.html">Home</a>\n            <a href="Shop.html">Shop</a>\n            <a href="About.html">About</a>\n            <a href="Contact.html">Contact</a>\n            <a href="Cart.html">Cart</a>\n        </nav>'
        )
    path.write_text(text, encoding='utf-8')
print('done')