import pandas as pd
import numpy as np
from datetime import timedelta
import os

# Set seed for reproducibility so your portfolio numbers remain consistent
np.random.seed(29)

# 1. Generate Event Days
start_date = pd.to_datetime('2026-05-01')
event_dates = [start_date + timedelta(days=i*7) for i in range(20)]

# 2. Generate Outlets
outlets = [
    "Champagne Bar", "The Monastery", "Club House", "Old Port Bistro", 
    "Final Furlong", "White Horse", "1539 Restaurant", "Paddock Bar",
    "County Stand Bar", "Tattersalls Bar", "Roodee Grill", "Owners & Trainers",
    "Jockeys Room", "Parade Ring Corner", "Festival Chalet"
]
df_outlets = pd.DataFrame({'Outlet_ID': range(1, 16), 'Outlet_Name': outlets})

# 3. Generate Products
categories = ["Bottled Beers & Ciders", "Spirits", "Wines", "Soft Drinks", "Champagne"]
products = []
for i in range(1, 201):
    cat = np.random.choice(categories, p=[0.3, 0.25, 0.2, 0.15, 0.1])
    cost = round(np.random.uniform(0.5, 15.0), 2)
    price = round(cost * np.random.uniform(2.5, 5.0), 2)
    products.append([i, f"Product_{i:03d}_{cat[:4].upper()}", cat, cost, price])

df_products = pd.DataFrame(products, columns=['Product_ID', 'Product_Name', 'Category', 'Cost_Price', 'Retail_Price'])

# 4. Generate Core Fact Data
fact_data = []

for date in event_dates:
    is_anomaly_day = (date == event_dates[9]) # Event 10 meltdown
    
    for _, outlet in df_outlets.iterrows():
        outlet_id = outlet['Outlet_ID']
        is_problem_outlet = (outlet['Outlet_Name'] == "Champagne Bar")
        
        for _, prod in df_products.iterrows():
            prod_id = prod['Product_ID']
            category = prod['Category']
            
            # Base metrics
            opening = np.random.randint(10, 100)
            delivery = np.random.randint(0, 50) if np.random.random() > 0.5 else 0
            
            # Anomaly day sales spike
            sales_multiplier = 3 if is_anomaly_day else 1
            sales = np.random.randint(5, opening + delivery + 1) * sales_multiplier
            sales = min(sales, opening + delivery) # Cap at available stock
            
            # Category waste problem
            waste_rate = 0.15 if category == "Soft Drinks" else 0.02
            waste = int(sales * np.random.uniform(0, waste_rate))
            
            expected = opening + delivery - sales - waste
            
            # The Variance Engine
            variance = 0
            if is_problem_outlet and category in ["Spirits", "Champagne"]:
                variance = -np.random.randint(2, 10) # Systematic shrinkage
            elif is_anomaly_day:
                variance = np.random.randint(-15, 15) # Total chaos miscounts
            elif np.random.random() > 0.8:
                variance = np.random.randint(-3, 3) # Standard human error
                
            closing = max(0, expected + variance)
            
            fact_data.append([date, outlet_id, prod_id, opening, delivery, sales, waste, closing])

df_facts = pd.DataFrame(fact_data, columns=['Date', 'Outlet_ID', 'Product_ID', 'Opening_Count', 'Delivery', 'Sales', 'Waste', 'Closing_Count'])

# Export to local CSVs
output_dir = "synthetic_data"
os.makedirs(output_dir, exist_ok=True)
df_outlets.to_csv(f"{output_dir}/dim_outlets.csv", index=False)
df_products.to_csv(f"{output_dir}/dim_products.csv", index=False)
df_facts.to_csv(f"{output_dir}/fact_stock_movements.csv", index=False)

print(f"Engine complete. Generated {len(df_facts)} rows of operational data.")