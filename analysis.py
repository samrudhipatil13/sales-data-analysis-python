
"""
analysis.py
-----------
End-to-end Sales Data Analysis Project
Python + pandas + matplotlib

Pipeline:
1. Load raw data
2. Clean data
3. Feature engineering
4. Exploratory Data Analysis
5. Business insights
6. Additional business analysis
7. Save charts and cleaned dataset
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# ---------------------------------------------------------------
# SETUP
# ---------------------------------------------------------------

# Create required folders automatically
os.makedirs("data", exist_ok=True)
os.makedirs("charts", exist_ok=True)

pd.set_option("display.max_columns", None)

# ---------------------------------------------------------------
# 1. LOAD DATA
# ---------------------------------------------------------------

df = pd.read_csv(
    "data/sales_data_raw.csv",
    parse_dates=["OrderDate"]
)

print(f"Raw data loaded: {df.shape[0]} rows, {df.shape[1]} columns")

# ---------------------------------------------------------------
# 2. DATA CLEANING
# ---------------------------------------------------------------

# Standardize text columns
text_cols = ["Region", "Category", "PaymentMethod", "Product"]

for col in text_cols:
    df[col] = (
        df[col]
        .astype(str)
        .str.strip()
        .str.title()
    )

# Remove duplicate orders
before = len(df)

df = df.drop_duplicates(
    subset=["OrderID"],
    keep="first"
)

print(f"Removed {before - len(df)} duplicate rows")

# Fix negative quantities
neg_qty = (df["Quantity"] < 0).sum()

df["Quantity"] = df["Quantity"].abs()

print(f"Fixed {neg_qty} negative quantity values")

# Remove rows missing UnitPrice or Quantity
before = len(df)

df = df.dropna(
    subset=["UnitPrice", "Quantity"]
)

print(
    f"Dropped {before - len(df)} rows "
    "missing UnitPrice/Quantity"
)

# Missing discount = no discount
df["DiscountPct"] = df["DiscountPct"].fillna(0)

# Missing customer age = median age
median_age = df["CustomerAge"].median()

df["CustomerAge"] = df["CustomerAge"].fillna(
    median_age
)

print(f"Clean data: {df.shape[0]} rows remaining\n")

# ---------------------------------------------------------------
# 3. FEATURE ENGINEERING
# ---------------------------------------------------------------

# Revenue calculation
df["Revenue"] = (
    df["UnitPrice"]
    * df["Quantity"]
    * (1 - df["DiscountPct"] / 100)
)

# Date features
df["Year"] = df["OrderDate"].dt.year

df["Month"] = (
    df["OrderDate"]
    .dt.to_period("M")
    .astype(str)
)

df["MonthName"] = (
    df["OrderDate"]
    .dt.month_name()
)

# Save cleaned data
df.to_csv(
    "data/sales_data_cleaned.csv",
    index=False
)

print("Saved cleaned dataset -> data/sales_data_cleaned.csv")

# ---------------------------------------------------------------
# 4. EXPLORATORY DATA ANALYSIS
# ---------------------------------------------------------------

report_lines = []


def log(line=""):
    print(line)
    report_lines.append(line)


log("=" * 60)
log("SALES DATA ANALYSIS REPORT")
log("=" * 60)

# Overall KPIs
total_revenue = df["Revenue"].sum()

total_orders = df["OrderID"].nunique()

avg_order_value = (
    total_revenue / total_orders
)

log(f"\nTotal Revenue:      ${total_revenue:,.2f}")
log(f"Total Orders:       {total_orders:,}")
log(f"Average Order Value: ${avg_order_value:,.2f}")

# ---------------------------------------------------------------
# Revenue by Category
# ---------------------------------------------------------------

rev_by_category = (
    df.groupby("Category")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)

log("\nRevenue by Category:")

for cat, value in rev_by_category.items():
    log(f"  {cat:<15} ${value:,.2f}")

# ---------------------------------------------------------------
# Revenue by Region
# ---------------------------------------------------------------

rev_by_region = (
    df.groupby("Region")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)

log("\nRevenue by Region:")

for region, value in rev_by_region.items():
    log(f"  {region:<15} ${value:,.2f}")

# ---------------------------------------------------------------
# Top 5 Products
# ---------------------------------------------------------------

top_products = (
    df.groupby("Product")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

log("\nTop 5 Products by Revenue:")

for product, value in top_products.items():
    log(f"  {product:<15} ${value:,.2f}")

# ---------------------------------------------------------------
# Payment Method
# ---------------------------------------------------------------

payment_counts = (
    df["PaymentMethod"]
    .value_counts()
)

log("\nOrders by Payment Method:")

for method, count in payment_counts.items():
    log(f"  {method:<15} {count:,} orders")

# ---------------------------------------------------------------
# Monthly Revenue
# ---------------------------------------------------------------

monthly_rev = (
    df.groupby("Month")["Revenue"]
    .sum()
    .sort_index()
)

# Best and worst month
best_month = monthly_rev.idxmax()
worst_month = monthly_rev.idxmin()

log(
    f"\nBest month:  {best_month} "
    f"(${monthly_rev.max():,.2f})"
)

log(
    f"Worst month: {worst_month} "
    f"(${monthly_rev.min():,.2f})"
)

# ---------------------------------------------------------------
# 5. ADDITIONAL BUSINESS ANALYSIS
# ---------------------------------------------------------------

# Category revenue contribution
category_share = (
    rev_by_category / total_revenue * 100
).round(2)

log("\nCategory Revenue Contribution:")

for cat, share in category_share.items():
    log(f"  {cat:<15} {share:.2f}%")

# Region revenue contribution
region_share = (
    rev_by_region / total_revenue * 100
).round(2)

log("\nRegion Revenue Contribution:")

for region, share in region_share.items():
    log(f"  {region:<15} {share:.2f}%")

# Average revenue per transaction by category
avg_revenue_category = (
    df.groupby("Category")["Revenue"]
    .mean()
    .sort_values(ascending=False)
)

log("\nAverage Revenue per Transaction by Category:")

for cat, value in avg_revenue_category.items():
    log(f"  {cat:<15} ${value:,.2f}")

# Monthly revenue growth
monthly_growth = (
    monthly_rev.pct_change() * 100
)

log("\nMonthly Revenue Growth:")

for month, growth in monthly_growth.dropna().items():
    log(f"  {month}: {growth:+.2f}%")

# ---------------------------------------------------------------
# 6. BUSINESS RECOMMENDATIONS
# ---------------------------------------------------------------

best_category = rev_by_category.idxmax()

best_region = rev_by_region.idxmax()

best_product = top_products.idxmax()

log("\nBusiness Recommendations:")

log(
    f"1. Focus on the {best_category} category "
    "because it generates the highest revenue."
)

log(
    f"2. Strengthen sales strategies in the "
    f"{best_region} region."
)

log(
    f"3. Promote top-performing products such as "
    f"{best_product}."
)

log(
    "4. Monitor low-performing months and plan "
    "targeted promotions."
)

# ---------------------------------------------------------------
# SAVE TEXT REPORT
# ---------------------------------------------------------------

with open(
    "sales_report.txt",
    "w",
    encoding="utf-8"
) as file:

    file.write(
        "\n".join(report_lines)
    )

print("\nSaved text report -> sales_report.txt")

# ---------------------------------------------------------------
# 7. VISUALIZATIONS
# ---------------------------------------------------------------

# Chart 1: Monthly Revenue Trend
fig, ax = plt.subplots(figsize=(11, 5))

monthly_rev.plot(
    kind="line",
    marker="o",
    ax=ax
)

ax.set_title(
    "Monthly Revenue Trend",
    fontsize=14,
    fontweight="bold"
)

ax.set_xlabel("Month")
ax.set_ylabel("Revenue ($)")

ax.yaxis.set_major_formatter(
    mticker.FuncFormatter(
        lambda x, _: f"${x:,.0f}"
    )
)

plt.xticks(
    rotation=45,
    ha="right"
)

plt.tight_layout()

plt.savefig(
    "charts/monthly_revenue_trend.png",
    dpi=150
)

plt.close()

# ---------------------------------------------------------------
# Chart 2: Revenue by Category
# ---------------------------------------------------------------

fig, ax = plt.subplots(figsize=(8, 5))

rev_by_category.plot(
    kind="bar",
    ax=ax
)

ax.set_title(
    "Revenue by Category",
    fontsize=14,
    fontweight="bold"
)

ax.set_xlabel("Category")
ax.set_ylabel("Revenue ($)")

ax.yaxis.set_major_formatter(
    mticker.FuncFormatter(
        lambda x, _: f"${x:,.0f}"
    )
)

plt.xticks(
    rotation=30,
    ha="right"
)

plt.tight_layout()

plt.savefig(
    "charts/revenue_by_category.png",
    dpi=150
)

plt.close()

# ---------------------------------------------------------------
# Chart 3: Revenue by Region
# ---------------------------------------------------------------

fig, ax = plt.subplots(figsize=(7, 7))

rev_by_region.plot(
    kind="pie",
    ax=ax,
    autopct="%1.1f%%",
    ylabel=""
)

ax.set_title(
    "Revenue Share by Region",
    fontsize=14,
    fontweight="bold"
)

plt.tight_layout()

plt.savefig(
    "charts/revenue_by_region.png",
    dpi=150
)

plt.close()

# ---------------------------------------------------------------
# Chart 4: Top 5 Products
# ---------------------------------------------------------------

fig, ax = plt.subplots(figsize=(8, 5))

top_products.sort_values().plot(
    kind="barh",
    ax=ax
)

ax.set_title(
    "Top 5 Products by Revenue",
    fontsize=14,
    fontweight="bold"
)

ax.set_xlabel("Revenue ($)")

ax.xaxis.set_major_formatter(
    mticker.FuncFormatter(
        lambda x, _: f"${x:,.0f}"
    )
)

plt.tight_layout()

plt.savefig(
    "charts/top_5_products.png",
    dpi=150
)

plt.close()

# ---------------------------------------------------------------
# Chart 5: Payment Method Distribution
# ---------------------------------------------------------------

fig, ax = plt.subplots(figsize=(8, 5))

payment_counts.plot(
    kind="bar",
    ax=ax
)

ax.set_title(
    "Orders by Payment Method",
    fontsize=14,
    fontweight="bold"
)

ax.set_xlabel("Payment Method")
ax.set_ylabel("Number of Orders")

plt.xticks(
    rotation=20,
    ha="right"
)

plt.tight_layout()

plt.savefig(
    "charts/payment_method_distribution.png",
    dpi=150
)

plt.close()

# ---------------------------------------------------------------
# Chart 6: Monthly Revenue Growth
# ---------------------------------------------------------------

growth_data = monthly_growth.dropna()

fig, ax = plt.subplots(figsize=(11, 5))

growth_data.plot(
    kind="bar",
    ax=ax
)

ax.set_title(
    "Monthly Revenue Growth (%)",
    fontsize=14,
    fontweight="bold"
)

ax.set_xlabel("Month")
ax.set_ylabel("Revenue Growth (%)")

ax.axhline(
    y=0,
    linewidth=1
)

plt.xticks(
    rotation=45,
    ha="right"
)

plt.tight_layout()

plt.savefig(
    "charts/monthly_revenue_growth.png",
    dpi=150
)

plt.close()

# ---------------------------------------------------------------
# FINAL MESSAGE
# ---------------------------------------------------------------

print("\nSaved 6 charts -> /charts")

print("\nDone! Project complete.")
