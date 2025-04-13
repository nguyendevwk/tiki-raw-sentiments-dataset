import requests
import json
import pandas as pd
import time
import random
from bs4 import BeautifulSoup
from tqdm import tqdm

class TikiSentimentScraper:
    def __init__(self, user_agent=None):
        self.headers = {
            'User-Agent': user_agent or 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept': 'application/json, text/plain, */*',
            'Origin': 'https://tiki.vn',
            'Referer': 'https://tiki.vn/'
        }
        self.base_url = 'https://tiki.vn'
        self.api_url = 'https://tiki.vn/api/v2/reviews'
        self.product_api_url = 'https://tiki.vn/api/v2/products'
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def get_product_info(self, product_id):
        """Lấy thông tin sản phẩm từ API của Tiki"""
        url = f"{self.product_api_url}/{product_id}"

        try:
            response = self.session.get(url)
            response.raise_for_status()
            data = response.json()

            product_info = {
                'product_id': product_id,
                'name': data.get('name', ''),
                'short_description': data.get('short_description', ''),
                'price': data.get('price', 0),
                'original_price': data.get('original_price', 0),
                'discount_rate': data.get('discount_rate', 0),
                'rating_average': data.get('rating_average', 0),
                'review_count': data.get('review_count', 0),
                'category_name': data.get('categories', {}).get('name', ''),
                'brand_name': data.get('brand', {}).get('name', ''),
                'url': data.get('url_path', ''),
                'image_url': data.get('thumbnail_url', ''),
            }

            return product_info
        except Exception as e:
            print(f"Lỗi khi lấy thông tin sản phẩm {product_id}: {e}")
            return None

    def get_reviews(self, product_id: str, limit=500):
        """Lấy đánh giá sản phẩm từ API của Tiki"""
        reviews = []
        page = 1
        total_pages = 1

        while page <= total_pages and len(reviews) < limit:
            params = {
                'product_id': product_id,
                'page': page,
                'limit': 20,  # Số lượng đánh giá trên mỗi trang
                'include': 'comments,contribute_info,attribute_vote_summary'
            }

            try:
                response = self.session.get(self.api_url, params=params)
                response.raise_for_status()
                data = response.json()

                # Cập nhật số trang tổng cộng
                total_pages = data.get('paging', {}).get('last_page', 1)

                # Thêm đánh giá vào danh sách
                reviews.extend(data.get('data', []))

                # Tăng số trang
                page += 1

                # Thêm độ trễ để tránh bị chặn
                # time.sleep(random.uniform(0.5, 1.5))

            except Exception as e:
                print(f"Lỗi khi lấy đánh giá trang {page} cho sản phẩm {product_id}: {e}")
                break

        return reviews[:limit]

    def process_reviews(self, reviews):
        """Xử lý dữ liệu đánh giá thô thành dạng cấu trúc"""
        processed_reviews = []

        for review in reviews:
            try:
                processed_review = {
                    'review_id': review.get('id', ''),
                    'title': review.get('title', ''),
                    'content': review.get('content', ''),
                    'rating': review.get('rating', 0),
                    'created_at': review.get('created_at', ''),
                    'customer_name': review.get('created_by', {}).get('name', ''),
                    'product_id': review.get('product_id', ''),
                    'is_verified': review.get('is_verified', False),
                    'number_of_likes': review.get('number_of_likes', 0),
                    'number_of_replies': review.get('number_of_replies', 0)
                }

                # Thêm nhãn sentiment dựa trên số sao
                if processed_review['rating'] >= 4:
                    processed_review['sentiment'] = 'positive'
                elif processed_review['rating'] <= 2:
                    processed_review['sentiment'] = 'negative'
                else:
                    processed_review['sentiment'] = 'neutral'

                processed_reviews.append(processed_review)
            except Exception as e:
                print(f"Lỗi khi xử lý đánh giá: {e}")
                continue

        return processed_reviews

    def search_products(self, keyword: str, limit=20):
        """Tìm kiếm sản phẩm theo từ khóa"""
        search_url = f"{self.base_url}/api/v2/products?limit={limit}&q={keyword}"

        try:
            response = self.session.get(search_url)
            response.raise_for_status()
            data = response.json()

            products = data.get('data', [])

            result = []
            for product in products:
                product_info = {
                    'product_id': product.get('id', ''),
                    'name': product.get('name', ''),
                    'price': product.get('price', 0),
                    'rating_average': product.get('rating_average', 0),
                    'review_count': product.get('review_count', 0),
                    'url': product.get('url_path', '')
                }
                result.append(product_info)

            return result
        except Exception as e:
            print(f"Lỗi khi tìm kiếm sản phẩm với từ khóa '{keyword}': {e}")
            return []

    def get_product_ids_by_category(self, category_url:str, limit=50):
        """Lấy danh sách ID sản phẩm từ một danh mục"""
        product_ids = []

        try:
            response = self.session.get(f"{self.base_url}/{category_url}")
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Tìm các sản phẩm trong danh mục
            product_elements = soup.select('div[data-view-id="product_list_container"] > div')

            for element in product_elements[:limit]:
                try:
                    # Lấy ID sản phẩm từ thuộc tính data-id
                    product_id = element.get('data-id', '')
                    if product_id and product_id.isdigit():
                        product_ids.append(product_id)
                except Exception as e:
                    continue

            return product_ids
        except Exception as e:
            print(f"Lỗi khi lấy danh sách sản phẩm từ danh mục '{category_url}': {e}")
            return []

    def create_sentiment_dataset(self, product_ids, reviews_per_product=100):
        """Tạo bộ dữ liệu sentiment từ danh sách ID sản phẩm"""
        all_reviews = []
        product_info_list = []

        for product_id in tqdm(product_ids, desc="Đang lấy dữ liệu từ sản phẩm"):
            # Lấy thông tin sản phẩm
            product_info = self.get_product_info(product_id)
            if product_info:
                product_info_list.append(product_info)

                # Lấy đánh giá
                # reviews = self.get_reviews(product_id, limit=reviews_per_product)
                # processed_reviews = self.process_reviews(reviews)
                # all_reviews.extend(processed_reviews)

                # Thêm độ trễ để tránh bị chặn
                # time.sleep(random.uniform(1, 2))

        # Tạo DataFrame
        # reviews_df = pd.DataFrame(all_reviews)
        products_df = pd.DataFrame(product_info_list)

        reviews_df = []
        return reviews_df, products_df

    def save_dataset(self, reviews_df, products_df, output_dir='.'):
        """Lưu bộ dữ liệu ra file"""
        # Lưu thành file CSV
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        reviews_df.to_csv(f"{output_dir}/tiki_reviews_{timestamp}.csv", index=False, encoding='utf-8-sig')
        products_df.to_csv(f"{output_dir}/tiki_products_{timestamp}.csv", index=False, encoding='utf-8-sig')

        # Lưu thành file JSON
        reviews_df.to_json(f"{output_dir}/tiki_reviews_{timestamp}.json", orient='records', force_ascii=False)
        products_df.to_json(f"{output_dir}/tiki_products_{timestamp}.json", orient='records', force_ascii=False)

        print(f"Đã lưu bộ dữ liệu gồm {len(reviews_df)} đánh giá từ {len(products_df)} sản phẩm")

        return {
            'reviews_csv': f"{output_dir}/tiki_reviews_{timestamp}.csv",
            'products_csv': f"{output_dir}/tiki_products_{timestamp}.csv",
            'reviews_json': f"{output_dir}/tiki_reviews_{timestamp}.json",
            'products_json': f"{output_dir}/tiki_products_{timestamp}.json"
        }
