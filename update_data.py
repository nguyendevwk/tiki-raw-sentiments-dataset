import pandas as pd
import os
import requests
import time
from tqdm import tqdm
import random

# Hàm lấy thông tin sản phẩm từ API Tiki dựa trên product_id
def get_product_info_from_api(product_id):
    product_api_url = f'https://tiki.vn/api/v2/products/{product_id}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    try:
        response = requests.get(product_api_url, headers=headers)

        # Kiểm tra mã trạng thái HTTP
        if response.status_code != 200:
            print(f"Error fetching data for product ID {product_id}: HTTP {response.status_code}")
            return {'image_url': '', 'category_name': ''}  # Trả về thông tin mặc định nếu có lỗi HTTP

        data = response.json()

        # Kiểm tra nếu dữ liệu không đầy đủ
        if 'thumbnail_url' not in data or ('categories' not in data and 'breadcrumbs' not in data):
            print(f"Error fetching data for product ID {product_id}: Missing fields")
            return {'image_url': '', 'category_name': ''}

        # Trích xuất category_name từ categories nếu có, nếu không lấy từ breadcrumbs
        if 'categories' in data and data['categories']:
            category_name = data['categories'].get('name', '')  # Lấy tên danh mục từ categories
        elif 'breadcrumbs' in data and data['breadcrumbs']:
            category_name = data['breadcrumbs'][0].get('name', '')  # Lấy tên từ breadcrumbs
        else:
            category_name = ''

        # Trả về các trường cần thiết
        thumbnail_url = data.get('thumbnail_url', '')  # Lấy URL ảnh

        return {
            'image_url': thumbnail_url,
            'category_name': category_name
        }
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for product ID {product_id}: {e}")
        return {'image_url': '', 'category_name': ''}  # Nếu lỗi kết nối hoặc exception khác

# Hàm bổ sung dữ liệu thiếu cho các sản phẩm
def add_missing_data(df):
    for index, row in tqdm(df.iterrows(), total=len(df), desc="Đang bổ sung dữ liệu"):
        # Nếu đã có đủ dữ liệu thì bỏ qua
        if row['image_url'] and row['category_name']:
            continue

        product_id = row['product_id']
        product_info = get_product_info_from_api(product_id)

        df.at[index, 'image_url'] = product_info['image_url']
        df.at[index, 'category_name'] = product_info['category_name']

        # Chờ để tránh quá tải API
        time.sleep(random.uniform(1, 3))

    return df

# Đọc dữ liệu từ file CSV đã gộp
folder_path = "data"  # Thư mục chứa file đã gộp
merged_file_path = os.path.join(folder_path, "merged_tiki_products.csv")
df = pd.read_csv(merged_file_path)

# Kiểm tra nếu thiếu 2 cột cần bổ sung
if 'image_url' not in df.columns or 'category_name' not in df.columns:
    # Thêm 2 cột nếu chưa có
    if 'image_url' not in df.columns:
        df['image_url'] = ''
    if 'category_name' not in df.columns:
        df['category_name'] = ''

    # Bổ sung dữ liệu thiếu
    df = add_missing_data(df)

    # Lưu lại file CSV đã bổ sung dữ liệu
    df.to_csv('merged_tiki_products.csv', index=False)
    print(f"Đã bổ sung dữ liệu và lưu lại tại: {merged_file_path}")
else:
    print("Không cần bổ sung dữ liệu vì các trường đã đầy đủ.")
