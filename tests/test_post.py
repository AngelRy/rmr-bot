import requests, os

page_id = os.getenv("FB_PAGE_ID")        # numeric page ID
page_token = os.getenv("FB_PAGE_TOKEN")  # Page Access Token
image_path = "output/quote_20260311_102124_351834.png"   # your generated image
caption = "Test post from RMR Bot"

with open(image_path, "rb") as f:
    files = {"source": f}
    data = {"caption": caption, "access_token": page_token}
    r = requests.post(f"https://graph.facebook.com/v19.0/{page_id}/photos", files=files, data=data)

print(r.status_code, r.text)