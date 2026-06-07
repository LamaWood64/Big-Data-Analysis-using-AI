# -*- coding: utf-8 -*-
"""
created by Ana Shad
30.05.2026
UCA and BSBI

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12
file_path = '/Users/anastasia/myWorkplace/datasets/Sample - Superstore.xls'

try:
    df = pd.read_excel(file_path)
    print("File found!")
    print(f" Num of rows: {df.shape[0]:,}")
    print(f" Num of cols: {df.shape[1]}")
except FileNotFoundError:
    print(f"❌ No file found: {file_path}")
    print("Pls check the path")
    raise

print("\n[3] Num of columns:")
print(df.columns.tolist())
print("\n[4] Data types:")
print(df.dtypes.value_counts())

print("\n[5] Checking for NoNs")
missing = df.isnull().sum()
print(missing[missing > 0] if any(missing > 0) else "✅ No NoNs")

print("\n[6] Numeric columns:")
numeric_cols = ['Sales', 'Profit', 'Discount', 'Quantity']
print(df[numeric_cols].describe().round(2))


sales_by_category = df.groupby('Category')['Sales'].sum().sort_values(ascending=False)
plt.figure(figsize=(10, 6))
colors = ['#2E86AB', '#A23B72', '#F18F01']
bars = plt.bar(sales_by_category.index, sales_by_category.values, color=colors, edgecolor='black')
plt.title('Sales by cathegory', fontsize=16, fontweight='bold')
plt.xlabel('Cathegory', fontsize=12)
plt.ylabel('Sum of sales ($)', fontsize=12)

for bar, value in zip(bars, sales_by_category.values):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10000,
             f'${value:,.0f}', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('01_sales_by_category.png', dpi=150, bbox_inches='tight')
plt.show()
print("Saved as '01_sales_by_category.png'")

df['Order Date'] = pd.to_datetime(df['Order Date'])
df['YearMonth'] = df['Order Date'].dt.to_period('M')
monthly_sales = df.groupby('YearMonth')['Sales'].sum()
monthly_sales.index = monthly_sales.index.astype(str)

plt.figure(figsize=(14, 6))
plt.plot(range(len(monthly_sales)), monthly_sales.values, 'o-', color='#2E86AB', linewidth=2, markersize=6)
plt.title('Sales dynamic by months', fontsize=16, fontweight='bold')
plt.xlabel('Month', fontsize=12)
plt.ylabel('Sum of sales ($)', fontsize=12)
plt.xticks(range(0, len(monthly_sales), 3), monthly_sales.index[::3], rotation=45)

z = np.polyfit(range(len(monthly_sales)), monthly_sales.values, 1)
p = np.poly1d(z)
plt.plot(range(len(monthly_sales)), p(range(len(monthly_sales))), '--', color='red', linewidth=2, label='Trend line')

plt.legend()
plt.tight_layout()
plt.savefig('02_monthly_sales_trend.png', dpi=150, bbox_inches='tight')
plt.show()
print("Saved as '02_monthly_sales_trend.png'")

sales_by_region = df.groupby('Region')['Sales'].sum().sort_values()

plt.figure(figsize=(10, 6))
colors = ['#F18F01', '#A23B72', '#2E86AB', '#06A77D']
bars = plt.barh(sales_by_region.index, sales_by_region.values, color=colors, edgecolor='black')
plt.title('Sales by region', fontsize=16, fontweight='bold')
plt.xlabel('Sum of sales($)', fontsize=12)
plt.ylabel('Region', fontsize=12)

for bar, value in zip(bars, sales_by_region.values):
    plt.text(bar.get_width() + 5000, bar.get_y() + bar.get_height()/2,
             f'${value:,.0f}', ha='left', va='center', fontweight='bold')

plt.tight_layout()
plt.savefig('03_sales_by_region.png', dpi=150, bbox_inches='tight')
plt.show()
print("Saved as '03_sales_by_region.png'")


sales_by_state = df.groupby('State/Province')['Sales'].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(12, 6))
bars = plt.bar(sales_by_state.index, sales_by_state.values, color='#2E86AB', edgecolor='black')
plt.title('Top 10 states by sales', fontsize=16, fontweight='bold')
plt.xlabel('State/Province', fontsize=12)
plt.ylabel('Sum of sales ($)', fontsize=12)
plt.xticks(rotation=45, ha='right')

for bar, value in zip(bars, sales_by_state.values):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5000,
             f'${value:,.0f}', ha='center', va='bottom', fontweight='bold', fontsize=10)

plt.tight_layout()
plt.savefig('04_top10_states_sales.png', dpi=150, bbox_inches='tight')
plt.show()
print("Saved as '04_top10_states_sales.png'")

ship_sales = df.groupby('Ship Mode')['Sales'].sum()
ship_profit = df.groupby('Ship Mode')['Profit'].sum()

fig, ax1 = plt.subplots(figsize=(12, 6))

x_pos = range(len(ship_sales))
width = 0.35
bars1 = ax1.bar([x - width/2 for x in x_pos], ship_sales.values, width, 
                color='#2E86AB', edgecolor='black', label='Sales')
ax1.set_xlabel('Delivery ways', fontsize=12)
ax1.set_ylabel('Sales ($)', fontsize=12, color='#2E86AB')
ax1.tick_params(axis='y', labelcolor='#2E86AB')
ax1.set_xticks(x_pos)
ax1.set_xticklabels(ship_sales.index, rotation=15)
ax2 = ax1.twinx()
bars2 = ax2.bar([x + width/2 for x in x_pos], ship_profit.values, width,
                color='#F18F01', edgecolor='black', label='Profit')
ax2.set_ylabel('Profit ($)', fontsize=12, color='#F18F01')
ax2.tick_params(axis='y', labelcolor='#F18F01')
plt.title('Comparing sales and profit by delivery ways', fontsize=16, fontweight='bold')

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

for bar, value in zip(bars1, ship_sales.values):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10000,
             f'${value:,.0f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

for bar, value in zip(bars2, ship_profit.values):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 500,
             f'${value:,.0f}', ha='center', va='bottom' if value >= 0 else 'top', 
             fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig('05_sales_profit_by_shipmode.png', dpi=150, bbox_inches='tight')
plt.show()
print("Saved as '05_sales_profit_by_shipmode.png'")


plt.figure(figsize=(12, 8))

categories = df['Category'].unique()
colors = ['#2E86AB', '#A23B72', '#F18F01']

for i, category in enumerate(categories):
    subset = df[df['Category'] == category]
    plt.scatter(subset['Sales'], subset['Profit'], 
                alpha=0.5, s=50, label=category, color=colors[i])

plt.axhline(y=0, color='red', linestyle='--', linewidth=1, alpha=0.7)
plt.axvline(x=0, color='red', linestyle='--', linewidth=1, alpha=0.7)
plt.xlabel('Sales ($)', fontsize=12)
plt.ylabel('Profit ($)', fontsize=12)
plt.title('Correlation for sales and profit', fontsize=16, fontweight='bold')
plt.legend()

correlation = df['Sales'].corr(df['Profit'])
plt.text(0.95, 0.95, f'Correlation: {correlation:.2f}', 
         transform=plt.gca().transAxes, ha='right', va='top',
         bbox=dict(boxstyle='round', facecolor='white', alpha=0.8),
         fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig('06_sales_profit_scatter.png', dpi=150, bbox_inches='tight')
plt.show()
print(" Saved as '06_sales_profit_scatter.png'")



correlation_matrix = df.groupby(['Segment', 'Category']).apply(
    lambda x: x['Sales'].corr(x['Profit'])).round(3)

correlation_df = correlation_matrix.unstack()
print("\nCorrelation Sales vs Profit by segments and cathegories:")
print(correlation_df)


customer_df = df.groupby('Customer ID').agg({
    'Customer Name': 'first',
    'Sales': 'sum',
    'Profit': 'sum',
    'Order ID': 'nunique',
    'Discount': 'mean',
    'Quantity': 'sum'}).rename(columns={
        'Order ID': 'OrderCount',
        'Sales': 'TotalSales',
        'Profit': 'TotalProfit',
        'Discount': 'AvgDiscount',
        'Quantity': 'TotalQuantity'})

customer_df['ProfitPerOrder'] = customer_df['TotalProfit'] / customer_df['OrderCount']
print(f"   - total unique clients: {len(customer_df):,}")
before_outliers = len(customer_df)
customer_df = customer_df[customer_df['TotalSales'] < customer_df['TotalSales'].quantile(0.99)]
after_outliers = len(customer_df)
print(f"   - Deliting outliers {before_outliers - after_outliers}")
features_for_clustering = ['TotalSales', 'OrderCount', 'AvgDiscount', 'ProfitPerOrder']
print(f"   - features_for_clustering: {features_for_clustering}")
scaler = StandardScaler()
scaled_features = scaler.fit_transform(customer_df[features_for_clustering])
inertias = []
k_range = range(2, 11)
for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(scaled_features)
    inertias.append(kmeans.inertia_)
    print(f"   - k={k}: inertia={kmeans.inertia_:.0f}")
plt.figure(figsize=(10, 6))
plt.plot(k_range, inertias, 'bo-', linewidth=2, markersize=8)
plt.xlabel('Numb of clusters', fontsize=12)
plt.ylabel('Inertia', fontsize=12)
plt.title('Elbow method', fontsize=16, fontweight='bold')
plt.xticks(k_range)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('07_elbow_method.png', dpi=150, bbox_inches='tight')
plt.show()
print("Saved as '07_elbow_method.png'")

k = 4
kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
customer_df['Cluster'] = kmeans.fit_predict(scaled_features)

cluster_names = {
    0: 'Cluster 0: Loyal clients',
    1: 'Cluster 1: New clients',
    2: 'Cluster 2: VIP clients',
    3: 'Cluster 3: Problematic clients'}

print("\n[17] Cluster analysis")

cluster_summary = customer_df.groupby('Cluster').agg({
    'TotalSales': ['mean', 'count'],
    'TotalProfit': 'mean',
    'OrderCount': 'mean',
    'AvgDiscount': 'mean',
    'ProfitPerOrder': 'mean'}).round(2)

cluster_summary.columns = ['AvgTotalSales', 'NumCustomers', 'AvgTotalProfit', 'AvgOrderCount', 'AvgDiscount', 'AvgProfitPerOrder']
print(cluster_summary)
print(f"Cluster 0: {cluster_summary.loc[0, 'AvgTotalSales']:.0f}$ sales, {cluster_summary.loc[0, 'AvgDiscount']:.2f} discount")
print(f"Cluster 1: {cluster_summary.loc[1, 'AvgTotalSales']:.0f}$ sales, {cluster_summary.loc[1, 'AvgDiscount']:.2f} discount")
print(f"Cluster 2: {cluster_summary.loc[2, 'AvgTotalSales']:.0f}$ sales, {cluster_summary.loc[2, 'AvgDiscount']:.2f} discount")
print(f"Cluster 3: {cluster_summary.loc[3, 'AvgTotalSales']:.0f}$ sales, {cluster_summary.loc[3, 'AvgDiscount']:.2f} discount")
plt.figure(figsize=(12, 8))
scatter = plt.scatter(customer_df['TotalSales'], customer_df['ProfitPerOrder'], 
                      c=customer_df['Cluster'], cmap='viridis', alpha=0.6, s=80, edgecolors='black')
plt.colorbar(scatter, label='Cluster', ticks=[0, 1, 2, 3])
plt.xlabel('Tot sales($)', fontsize=12)
plt.ylabel('Tot profit for order ($)', fontsize=12)
plt.title('Client clustering: sales vs profit for order', fontsize=16, fontweight='bold')

plt.text(0.95, 0.05, f'k = {k}\nВTotal clients: {len(customer_df)}', 
         transform=plt.gca().transAxes, ha='right', va='bottom',
         bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

plt.tight_layout()
plt.savefig('08_customer_clusters.png', dpi=150, bbox_inches='tight')
plt.show()
print("Saved as '08_customer_clusters.png'")


fig, axes = plt.subplots(1, 2, figsize=(14, 6))

avg_sales = cluster_summary['AvgTotalSales'].sort_values(ascending=False)
axes[0].bar(range(len(avg_sales)), avg_sales.values, color='#2E86AB', edgecolor='black')
axes[0].set_xticks(range(len(avg_sales)))
axes[0].set_xticklabels([f'Cluster {i}' for i in avg_sales.index])
axes[0].set_ylabel('Avg sales ($)', fontsize=12)
axes[0].set_title('Avg sales for client clusters', fontsize=14, fontweight='bold')
for i, (idx, value) in enumerate(avg_sales.items()):
    axes[0].text(i, value + 200, f'${value:,.0f}', ha='center', fontweight='bold')


avg_profit_per_order = cluster_summary['AvgProfitPerOrder'].sort_values(ascending=False)
colors_bar = ['#06A77D' if x > 0 else '#D62828' for x in avg_profit_per_order.values]
axes[1].bar(range(len(avg_profit_per_order)), avg_profit_per_order.values, color=colors_bar, edgecolor='black')
axes[1].set_xticks(range(len(avg_profit_per_order)))
axes[1].set_xticklabels([f'Cluster {i}' for i in avg_profit_per_order.index])
axes[1].set_ylabel('Avg profit ($)', fontsize=12)
axes[1].set_title('Avg profit for order by clusters', fontsize=14, fontweight='bold')
for i, (idx, value) in enumerate(avg_profit_per_order.items()):
    axes[1].text(i, value + 2 if value > 0 else value - 15, 
                 f'${value:.0f}', ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig('09_clusters_comparison.png', dpi=150, bbox_inches='tight')
plt.show()
print("   ✅ Saved as '09_clusters_comparison.png'")

print("\n[20] Dovnloading results")

customer_df.to_csv('customer_clusters_results.csv')
print("   ✅ Dovnloaded 'customer_clusters_results.csv'")

cluster_summary.to_csv('cluster_summary.csv')
print("   ✅ Dovnloaded 'cluster_summary.csv'")

correlation_df.to_csv('correlation_by_segment_category.csv')
print("   ✅ Dovnloaded 'correlation_by_segment_category.csv'")

print("\n[21] Additional stats")

total_sales = df['Sales'].sum()
total_profit = df['Profit'].sum()
avg_discount = df['Discount'].mean()
total_orders = df['Order ID'].nunique()

print("\n=== KPIs ===")
print(f"Total sales: ${total_sales:,.2f}")
print(f"Total profit: ${total_profit:,.2f}")
print(f"Avg discount: {avg_discount:.2%}")
print(f"Total orders: {total_orders:,}")

profitable_orders = (df['Profit'] > 0).sum()
loss_orders = (df['Profit'] < 0).sum()
print(f"\nProfitable orders: {profitable_orders} ({profitable_orders/len(df)*100:.1f}%)")
print(f"Non profitable orders: {loss_orders} ({loss_orders/len(df)*100:.1f}%)")

print("\n=== Delivery stats ===")
ship_stats = df.groupby('Ship Mode').agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Order ID': 'count'
}).rename(columns={'Order ID': 'OrderCount'})
print(ship_stats)
