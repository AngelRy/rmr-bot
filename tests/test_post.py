import os

dotenv_path = "/home/angels/rmr-bot/.env"

with open(dotenv_path, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()
            os.environ[key] = value

# Now access the variables
ACCESS_TOKEN = os.getenv("FACEBOOK_PAGE_TOKEN")
PAGE_ID = os.getenv("FACEBOOK_PAGE_ID")

print("ACCESS_TOKEN:", repr(ACCESS_TOKEN))
print("PAGE_ID:", repr(PAGE_ID))

if ACCESS_TOKEN:
    print("✅ Token loaded successfully!")
else:
    print("❌ Token not found.")