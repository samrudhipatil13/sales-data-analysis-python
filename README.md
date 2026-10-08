# Sales Data Analysis & Business Insights

## 📌 Project Overview

This project performs an end-to-end analysis of sales transaction data using Python, Pandas, and Matplotlib.

The project focuses on data cleaning, feature engineering, exploratory data analysis (EDA), revenue analysis, data visualization, and generating actionable business insights.

## 🎯 Objectives

- Clean and prepare raw sales transaction data
- Handle duplicate and invalid records
- Handle missing values
- Calculate revenue from transaction-level data
- Analyze sales performance across categories and regions
- Identify top-performing products
- Analyze payment method usage
- Identify monthly revenue trends
- Calculate monthly revenue growth
- Generate business recommendations

## 📊 Dataset

The project analyzes **5,100 raw sales records** containing information such as:

- Order ID
- Order Date
- Region
- Category
- Product
- Quantity
- Unit Price
- Discount
- Payment Method
- Customer Age

After data cleaning, **4,701 records** were retained for analysis.

## 🧹 Data Cleaning

The following data preparation steps were performed:

- Removed **100 duplicate orders**
- Corrected **25 negative quantity values**
- Removed records with missing Unit Price or Quantity
- Filled missing discount values with `0`
- Filled missing customer ages using the median age
- Standardized text fields such as Region, Category, Product, and Payment Method

## ⚙️ Feature Engineering

A new `Revenue` column was calculated using:

```text
Revenue = UnitPrice × Quantity × (1 - DiscountPct / 100)
```

Additional date-based features were created:

- Year
- Month
- Month Name

## 🔎 Exploratory Data Analysis

The analysis covers:

### Revenue Analysis

- Total revenue
- Total orders
- Average order value
- Revenue by category
- Revenue by region

### Product Analysis

- Top 5 products by revenue

### Customer & Payment Analysis

- Orders by payment method
- Average revenue per transaction by category

### Time-Series Analysis

- Monthly revenue
- Best-performing month
- Worst-performing month
- Monthly revenue growth

### Business Analysis

The project also calculates:

- Category revenue contribution
- Region revenue contribution
- Monthly revenue growth
- Business recommendations based on analysis results

## 📈 Key Results

From the analysis:

| Metric | Result |
|---|---:|
| Raw Records | 5,100 |
| Clean Records | 4,701 |
| Total Revenue | $5.82M |
| Total Orders | 4,701 |
| Average Order Value | $1,238.55 |
| Highest Revenue Category | Toys |
| Highest Revenue Region | North |
| Best Month | September 2024 |
| Top Product | Bed Frame |

## 📊 Visualizations

The project generates six visualizations:

1. Monthly Revenue Trend
2. Revenue by Category
3. Revenue Share by Region
4. Top 5 Products by Revenue
5. Orders by Payment Method
6. Monthly Revenue Growth

All generated charts are available in the `charts/` directory.

## 💡 Business Recommendations

Based on the analysis:

- Focus on high-performing product categories to maximize revenue.
- Strengthen sales strategies in high-performing regions.
- Promote top-performing products.
- Monitor low-performing months and plan targeted promotional campaigns.
- Track monthly revenue growth to identify changes in sales performance.

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Git
- GitHub

## 📁 Project Structure

```text
sales-data-analysis-python/
│
├── analysis.py
├── generate_data.py
├── LinearRegCarprice.ipynb
├── README.md
├── sales_report.txt
│
├── data/
│   ├── sales_data_raw.csv
│   └── sales_data_cleaned.csv
│
└── charts/
    ├── monthly_revenue_trend.png
    ├── revenue_by_category.png
    ├── revenue_by_region.png
    ├── top_5_products.png
    ├── payment_method_distribution.png
    └── monthly_revenue_growth.png
```

## ▶️ How to Run

### 1. Clone the repository

```bash
git clone https://github.com/samrudhipatil13/sales-data-analysis-python.git
```

### 2. Navigate to the project

```bash
cd sales-data-analysis-python
```

### 3. Generate the sales data

```bash
py generate_data.py
```

### 4. Run the analysis

```bash
py analysis.py
```

The cleaned dataset, report, and visualizations will be generated automatically.

## 📄 Output Files

After running the project, the following outputs are generated:

- `data/sales_data_cleaned.csv`
- `sales_report.txt`
- Six visualization files inside `charts/`

## 👩‍💻 Skills Demonstrated

This project demonstrates practical experience with:

- Data Cleaning
- Data Preprocessing
- Exploratory Data Analysis
- Feature Engineering
- Data Visualization
- Aggregation and GroupBy
- Time-Series Analysis
- Business Insight Generation
- Python Programming
- Git & GitHub

---

**Author:** Samrudhi Patil