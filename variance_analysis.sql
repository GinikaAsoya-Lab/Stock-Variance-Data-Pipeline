-- CTE 1: Calculate the expected stock and raw variance per transaction
WITH StockMovements AS (
    SELECT 
        f.Date,
        o.Outlet_Name,
        p.Product_Name,
        p.Category,
        p.Cost_Price,
        f.Opening_Count,
        f.Delivery,
        f.Sales,
        f.Waste,
        f.Closing_Count,
        -- Expected Stock = Opening + Delivery - Sales - Waste
        (f.Opening_Count + f.Delivery - f.Sales - f.Waste) AS Expected_Stock,
        -- Variance Qty = Actual Closing Count - Expected Stock
        (f.Closing_Count - (f.Opening_Count + f.Delivery - f.Sales - f.Waste)) AS Variance_Qty,
        -- Variance Value = Variance Qty * Cost Price (Financial impact of shrinkage)
        (f.Closing_Count - (f.Opening_Count + f.Delivery - f.Sales - f.Waste)) * p.Cost_Price AS Variance_Value
    FROM fact_stock_movements f
    JOIN dim_outlets o ON f.Outlet_ID = o.Outlet_ID
    JOIN dim_products p ON f.Product_ID = p.Product_ID
),

-- CTE 2: Aggregate variance by Outlet and Date to find the biggest bleeders
OutletPerformance AS (
    SELECT 
        Date,
        Outlet_Name,
        SUM(Variance_Qty) AS Total_Variance_Qty,
        ROUND(SUM(Variance_Value), 2) AS Total_Variance_Value,
        SUM(Waste) AS Total_Waste_Qty
    FROM StockMovements
    GROUP BY 
        Date, 
        Outlet_Name
)

-- Final Output: Add a Window Function to compare against the previous week
SELECT 
    Date,
    Outlet_Name,
    Total_Variance_Value,
    -- Window Function: Get the variance value from the previous week for this specific outlet
    LAG(Total_Variance_Value) OVER (PARTITION BY Outlet_Name ORDER BY Date) AS Previous_Week_Variance,
    Total_Waste_Qty
FROM OutletPerformance
ORDER BY 
    Date DESC, 
    Total_Variance_Value ASC;