# scripts/test_caption_generator.py

from rmrbot.generator.post_text_generator import generate_caption

quote = "After all, if you run far enough, no one can catch you."
author = "V.E. Schwab"

caption = generate_caption(quote, author)

print("QUOTE:")
print(quote)
print("\nCAPTION:")
print(caption)

