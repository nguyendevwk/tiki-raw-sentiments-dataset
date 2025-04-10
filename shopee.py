import requests

url = "https://shopee.vn/api/v4/item/get?itemid=7891011&shopid=123456"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://shopee.vn/",
}

response = requests.get(url, headers=headers)

print(response.json())
