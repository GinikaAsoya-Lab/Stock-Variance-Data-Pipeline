Hospitality Stock Variance & Shrinkage Analysis
The Problem: In multi-outlet hospitality, stock counted at closing rarely matches the expected stock calculated from opening counts, deliveries, sales, and waste. This project identifies which specific outlets are losing the most cash, on which products, and traces the operational causes behind the shrinkage.

The Data: Please note that all data in this repository is completely synthetic. It was generated via Python to safely mirror the exact operational shape, scale, and messiness of real-world racecourse hospitality data, completely avoiding the use of actual employer data.

The Approach:

An automated Python engine generated 60,000 rows of relational operational data.

A SQLite database was built to house the raw tables.

A robust SQL transformation pipeline utilizing Common Table Expressions (CTEs) and window functions was written to calculate expected stock and period-on-period financial variance.

A Star Schema was architected in Power BI, utilizing DAX iterator functions (SUMX, RELATED) to calculate the exact cash value of stock loss and dynamically cross-filter the bleeding by category.

The Findings:

Systematic Shrinkage: The Champagne Bar is the primary operational bleeder, systematically losing high-value inventory (specifically Spirits and Champagne).

Waste Discrepancies: Soft Drinks consistently register a 15% waste rate, drastically exceeding the 2% operational baseline seen across other product categories.

The "Phantom Stock" Anomaly: During massive, high-volume event days, extreme sales push system inventory to zero. Because physical stock counts cannot drop below zero, negative miscounts are truncated, while positive miscounts stack up. This creates a temporary, artificial illusion of positive cash variance on the worst operational days.

How to Run It: Execute data_generator.py followed by database_builder.py to recreate the local SQLite database. The SQL transformations can be viewed in variance_analysis.sql, and the final model is available in Chester_Stock_Variance.pbix.