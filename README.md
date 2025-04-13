# Sentiment Analysis for Tiki Reviews

This project collects and analyzes sentiment from product reviews on the Tiki e-commerce platform.

#### Phạm Nguyễn - nguyendevwk

## Requirements

-   Python 3.8+
-   Required packages:

```bash
pip install -r install.txt
```

## Project Structure

```
sentiment_reviews_tiki/
│
├── data/                  # Folder containing collected data
├── raw_app.py             # Main script for data collection
├── tiki_sentiment_scraper.py  # Scraper class implementation
└── README.md
```

## Usage

1. Clone the repository:

```bash
git clone https://github.com/nguyendevwk/tiki-raw-sentiments-dataset.git
cd sentiment_reviews_tiki
```

2. Create and activate a virtual environment (optional but recommended):

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Linux/Mac
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r install.txt
```

4. Run the data collection script:

```bash
python raw_app.py
```

The script will:

-   Search for products using predefined keywords
-   Collect products from specified categories
-   Gather reviews and analyze sentiment
-   Balance the dataset
-   Save results to CSV and JSON files in the `data` folder

## Output Files

The program generates the following files in the `data` directory:

-   `tiki_reviews_[timestamp].csv` - Collected reviews with sentiment
-   `tiki_reviews_[timestamp].json` - Reviews in JSON format
-   `tiki_products_[timestamp].csv` - Product information
-   `tiki_products_[timestamp].json` - Products in JSON format

## Configuration

You can modify the following in `raw_app.py`:

-   `search_keywords`: List of keywords to search for products
-   `category_urls`: List of category URLs to collect products from
-   `reviews_per_product`: Number of reviews to collect per product (default: 5000)
-   Add specific product IDs in the commented section

## Limitations

-   Be mindful of Tiki's rate limiting
-   Large datasets may take significant time to collect
-   Keep reasonable limits on `reviews_per_product` to avoid overload

## License

This project is licensed under the MIT License.
