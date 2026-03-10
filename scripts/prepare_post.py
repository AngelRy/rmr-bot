# scripts/prepare_post.py

from rmrbot.database.models import get_unused_quote, mark_used
from rmrbot.generator.quote_parser import parse_quote
from rmrbot.generator.image_generator import generate_image
from rmrbot.generator.post_text_generator import generate_caption


def main():
    raw_quote = get_unused_quote()

    if not raw_quote:
        print("No unused quotes available.")
        return

    parsed = parse_quote(raw_quote)

    quote_text = parsed["quote"]
    author = parsed["author"]

    # ⬇⬇⬇ PASS AUTHOR INTO IMAGE GENERATOR ⬇⬇⬇
    image_path = generate_image(quote_text, author)

    caption = generate_caption(quote_text, author)

    mark_used(raw_quote)

    print("=" * 60)
    print("POST PREPARED")
    print("=" * 60)
    print("\nQUOTE:")
    print(quote_text)

    if author:
        print(f"\nAUTHOR: {author}")

    print("\nCAPTION:")
    print(caption)

    print("\nIMAGE PATH:")
    print(image_path)
    print("=" * 60)


if __name__ == "__main__":
    main()
