from rmrbot.database.models import get_unused_quote, mark_used
from rmrbot.generator.image_generator import generate_image


quote = get_unused_quote()

if not quote:
    print("No unused quotes available.")
    exit()

image_path = generate_image(quote)
mark_used(quote)

print("Image generated:")
print(image_path)
print()
print("QUOTE:")
print(quote)
