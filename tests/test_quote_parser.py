# scripts/test_quote_parser.py

from rmrbot.generator.quote_parser import parse_quote

TEST_QUOTES = [
    'After all, if you run far enough, no one can catch you.”―V.E. Schwab,A Gathering of Shadows',
    'If you build the guts to do something, anything, then you better save enough to face the consequences.”―Criss Jami,Killosophy',
    'Run when you can, walk if you have to, crawl if you must; just never give up.'
]

for raw in TEST_QUOTES:
    parsed = parse_quote(raw)
    print("-" * 60)
    print("RAW:")
    print(raw)
    print("\nPARSED:")
    for k, v in parsed.items():
        print(f"{k}: {v}")
