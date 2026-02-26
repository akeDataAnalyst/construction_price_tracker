# Construction Materials Price Tracker Dashboard

A full-stack Python portfolio project demonstrating web scraping, data cleaning, database integration, report generation, machine learning validation, and an interactive Streamlit dashboard — built for tracking real-time construction and interior material prices in Ethiopia.



## Project Highlights

- **Source**: Scraped from https://con.2merkato.com/prices (Construction Market Watch)
- **Categories scraped**: Concrete Work, Finishing, Roofing, Painting
- **Total items extracted**: 177 records (after scraping & cleaning)
- **Outliers detected**: 15 price anomalies (8.5% of valid prices) using Isolation Forest
- **ML techniques used**:
  - Unsupervised outlier detection (Isolation Forest on price + data freshness)
  - Text similarity (TF-IDF + cosine similarity) for material name grouping/matching
- **Dashboard**: Interactive Streamlit app with filters, dark theme, charts, highlighted outliers & CSV export

## Tech Stack & Tools

| Layer                 | Tools / Libraries                              |
|-----------------------|------------------------------------------------|
| Language              | Python 3.10+                                   |
| Scraping              | requests + BeautifulSoup                       |
| Data Processing       | pandas                                         |
| Database              | MySQL (SQLAlchemy + pymysql)                   |
| Visualization         | matplotlib, seaborn, plotly                    |
| Machine Learning      | scikit-learn (IsolationForest, TfidfVectorizer, cosine_similarity) |
| Dashboard             | Streamlit                                      |
| Environment           | venv, python-dotenv (secure MySQL credentials) |
| Reports               | ReportLab (PDF generation in Phase 4)          |



A complete Python portfolio project that scrapes real-time material prices from 2merkato.com, cleans and validates data, applies ML for outlier detection & material matching, stores in MySQL, generates PDF reports, and delivers everything through an interactive dark-mode Streamlit dashboard with live filters, charts, highlighted anomalies, and CSV export.
177 records scraped · 15 price outliers detected (8.5%) · Built for Ethiopia's construction & interiors market.

#Python #WebScraping #DataAutomation #MachineLearning #Streamlit #OutlierDetection #DataEngineering #ConstructionTech #EthiopiaTech #PortfolioProject