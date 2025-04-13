from tiki_sentiment_scraper import TikiSentimentScraper
import pandas as pd
from imblearn.over_sampling import SMOTE

# Khởi tạo scraper
scraper = TikiSentimentScraper()

### 🔹 PHƯƠNG PHÁP 1: Lấy dữ liệu từ tìm kiếm sản phẩm
# 🔹 Danh sách từ khóa tìm kiếm
search_keywords = [
    # Thiết bị di động & Phụ kiện
    "điện thoại", "điện thoại thông minh", "điện thoại cũ", "điện thoại giá rẻ",
    "smartphone cao cấp", "ốp lưng điện thoại", "kính cường lực", "pin sạc dự phòng",
    "cáp sạc nhanh", "củ sạc nhanh", "thẻ nhớ microSD", "bút cảm ứng", "tai nghe bluetooth",
    "smartwatch", "vỏ điện thoại", "cáp sạc lightning", "cáp USB-C", "quai đeo smartwatch",
    "miếng dán màn hình", "màn hình điện thoại", "phụ kiện smartphone", "sạc không dây",
    "màn hình gập", "smartphone màn hình cong", "pin điện thoại", "camera điện thoại", "smartphone màn hình phẳng",

    # Máy tính & Linh kiện
    "laptop", "laptop gaming", "laptop văn phòng", "laptop sinh viên", "macbook",
    "chuột không dây", "bàn phím cơ", "bàn phím không dây", "bàn phím cơ RGB",
    "màn hình máy tính", "RAM DDR4", "RAM DDR5", "ổ cứng SSD", "ổ cứng HDD",
    "card đồ họa RTX", "card đồ họa AMD", "mainboard gaming", "CPU Intel", "CPU AMD",
    "máy tính để bàn", "máy tính xách tay", "case máy tính", "card màn hình", "ổ đĩa quang",
    "bộ nhớ ngoài", "tản nhiệt CPU", "quạt máy tính", "bộ nguồn máy tính", "tản nhiệt nước",
    "phụ kiện laptop", "bộ chuyển đổi USB", "dock máy tính", "ổ cứng ngoài", "bộ phát wifi",

    # Thiết bị Âm thanh
    "tai nghe", "tai nghe bluetooth", "tai nghe gaming", "tai nghe chống ồn",
    "loa bluetooth", "loa bluetooth mini", "loa bluetooth công suất lớn",
    "dàn âm thanh gia đình", "soundbar TV", "âm ly", "mic không dây", "tai nghe in-ear",
    "mic thu âm", "loa kéo", "bộ loa 5.1", "loa siêu trầm", "tai nghe chụp tai",
    "loa ngoài", "tai nghe thể thao", "tai nghe chống ồn chủ động", "microphone gaming",
    "tai nghe true wireless", "dàn karaoke gia đình", "loa ngoài trời", "loa bluetooth chống nước",

    # Thiết bị Gia dụng
    "máy giặt", "máy giặt cửa ngang", "máy giặt cửa trên", "máy sấy quần áo",
    "tủ lạnh inverter", "tủ lạnh mini", "bếp từ đôi", "bếp hồng ngoại",
    "nồi chiên không dầu", "robot hút bụi", "máy hút bụi", "máy xay sinh tố",
    "máy ép trái cây", "máy pha cà phê", "bình đun siêu tốc", "máy rửa bát",
    "máy làm sữa chua", "bình nóng lạnh", "máy lọc không khí", "tủ đông",
    "máy xay thịt", "bàn là", "máy sấy tóc", "máy làm kem", "máy chiết rót",
    "quạt làm mát", "máy nướng bánh", "tủ lạnh side-by-side", "nồi cơm điện",

    # Thiết bị Giải trí & Hình ảnh
    "tivi", "tivi 4K", "tivi OLED", "tivi thông minh",
    "máy chiếu mini", "máy ảnh", "máy ảnh DSLR", "máy ảnh mirrorless", "máy quay phim",
    "gimbal", "camera hành trình", "camera thể thao", "camera an ninh", "đầu phát Bluray",
    "máy tính bảng", "máy chiếu mini xách tay", "kính thực tế ảo VR", "dựng phim 4K",
    "phụ kiện máy ảnh", "lens máy ảnh", "bộ lọc máy ảnh", "dụng cụ chụp ảnh chuyên nghiệp",
    "máy quay 360 độ", "quay phim drone", "máy chiếu phim", "tivi thông minh 8K",
    "kính thực tế ảo", "máy chiếu 4K", "tivi LED", "phụ kiện quay phim", "tai nghe chơi game",

    # Sản phẩm điện tử khác
    "máy tính bảng", "smartwatch", "máy đo huyết áp", "máy đo nhiệt độ", "camera 360 độ",
    "dụng cụ đo lường", "máy chiếu", "phụ kiện máy tính bảng", "thiết bị smart home",
    "thiết bị an ninh", "thiết bị theo dõi sức khỏe", "máy tạo ion âm", "sạc dự phòng",
    "bộ phát wifi", "router wifi", "đầu ghi camera", "màn hình LED", "phụ kiện chơi game",
    "phụ kiện điện thoại", "thiết bị âm thanh không dây", "tủ bảo quản máy ảnh", "đầu thu tín hiệu",
    "máy chơi game cầm tay", "máy chơi game console", "thiết bị VR",

    # Các thiết bị văn phòng khác
    "máy in", "máy photocopy", "máy scan", "máy tính tiền", "bàn làm việc",
    "ghế văn phòng", "máy chấm công", "bút ký", "bảng trắng", "bảng từ",
    "thiết bị hội nghị", "máy chiếu projector", "dụng cụ văn phòng", "máy cắt giấy",
    "thẻ nhớ", "khóa thông minh", "sổ tay", "thiết bị giáo dục", "máy lạnh",

    # Dụng cụ thể thao & Ngoài trời
    "dụng cụ thể thao", "xe đạp", "giày thể thao", "bóng đá", "bóng rổ",
    "gậy golf", "thảm tập yoga", "tạ tay", "dụng cụ bơi lội", "mũ bảo hiểm",
    "túi ngủ", "lều cắm trại", "dụng cụ leo núi", "dụng cụ tập gym", "đồng hồ thể thao",
    "áo thể thao", "quần thể thao", "bình nước thể thao", "ba lô du lịch", "bộ đồ câu cá",
    "gậy câu cá", "thảm lót yoga", "kính bơi", "gậy chống", "đệm du lịch", "cần câu",

    # Thiết bị sức khỏe & Làm đẹp
    "máy massage", "máy xông mặt", "máy triệt lông", "máy rửa mặt", "máy xông hơi",
    "máy chăm sóc da", "máy tăm nước", "bộ làm đẹp", "máy nâng cơ", "máy sấy tóc",
    "máy làm sạch da", "bàn chải điện", "máy chạy bộ", "máy ép trái cây", "máy đếm bước chân",
    "máy giảm mỡ bụng", "máy giúp ngủ ngon", "thảm massage", "máy điều trị mụn", "máy xông mặt ozone",
]


# 🔹 Danh sách danh mục sản phẩm
category_urls = [
    'dien-thoai-smartphone/c1795', 'laptop/c1846', 'tivi/c1882',
    'may-giat/c1883', 'may-anh/c1801', 'dong-ho-thoi-trang/c8379',
    'tai-nghe/c1788', 'may-tinh-bang/c1803', 'loa-bluetooth/c1811',
    'camera-giam-sat/c4077', 'camera-hanh-trinh-action-camera-va-phu-kien/c28834',
    'thiet-bi-quay-phim/c28822', 'thiet-bi-choi-game-va-phu-kien/c2667',
    'phu-kien-gaming/c6742', 'thiet-bi-deo-thong-minh-va-phu-kien/c8039',
    'phu-kien-dien-thoai-va-may-tinh-bang/c8214'
]



product_ids = []
for keyword in search_keywords:
    print(f"🔍 Đang tìm kiếm sản phẩm: {keyword}...")
    search_results = scraper.search_products(keyword, limit=1000)
    product_ids.extend([product['product_id'] for product in search_results])

### 🔹 PHƯƠNG PHÁP 2: Lấy dữ liệu từ danh mục sản phẩm
for category_url in category_urls:
    print(f"📂 Đang lấy sản phẩm từ danh mục: {category_url}...")
    product_ids.extend(scraper.get_product_ids_by_category(category_url, limit=1000))

### 🔹 PHƯƠNG PHÁP 3: Chỉ định ID sản phẩm (tùy chọn)
# product_ids.extend(['123456', '789012', '345678'])

# Loại bỏ trùng lặp ID
product_ids = list(set(product_ids))
print(f"✅ Tổng số sản phẩm thu thập: {len(product_ids)}")

# 🔹 Tạo dataset sentiment từ danh sách sản phẩm
print("📡 Đang thu thập dữ liệu đánh giá...")
reviews_df, products_df = scraper.create_sentiment_dataset(product_ids, reviews_per_product=5000)

# 🔹 Thống kê dữ liệu thu thập được
print(f"📊 Số lượng sản phẩm: {len(products_df)}")
print(f"📊 Số lượng đánh giá: {len(reviews_df)}")
print("\n📌 Phân bố sentiment ban đầu:")
print(reviews_df['sentiment'].value_counts())

# 🔹 Cân bằng dữ liệu sentiment
sentiment_counts = reviews_df['sentiment'].value_counts()
min_count = sentiment_counts.min()

balanced_reviews = (
    reviews_df.groupby('sentiment')
    .apply(lambda x: x.sample(min_count))
    .reset_index(drop=True)
)

print("\n✅ Sau khi cân bằng sentiment:")
print(balanced_reviews['sentiment'].value_counts())

# 🔹 Lưu dữ liệu ra file
output_files = scraper.save_dataset(balanced_reviews, products_df, output_dir='./data')

# 🔹 Hiển thị một số đánh giá mẫu
print("\n📢 Một số đánh giá mẫu:")
print(balanced_reviews[['content', 'rating', 'sentiment']].sample(5))

# 🔹 Thống kê số sao
print("\n⭐ Số lượng đánh giá theo số sao:")
print(reviews_df['rating'].value_counts().sort_index())

# 🔹 Thống kê sentiment
print("\n🔍 Số lượng đánh giá theo sentiment:")
print(balanced_reviews['sentiment'].value_counts())

# 🔹 Xem thông tin sản phẩm
print("\n📦 Thông tin sản phẩm thu thập:")
print(products_df[['name', 'price', 'rating_average', 'review_count']].head())

