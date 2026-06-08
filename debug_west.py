import sqlite3
import pandas as pd

conn = sqlite3.connect('delivery.db')

query = """
SELECT 
    CASE 
        WHEN UPPER(branch) = 'CENTRAL' THEN 'CENTRAL'
        WHEN UPPER(branch) = 'CNETRAL' THEN 'CENTRAL'
        WHEN UPPER(branch) = 'NORTH' THEN 'NORTH'
        WHEN UPPER(branch) = 'NOTH' THEN 'NORTH'
        WHEN UPPER(branch) = 'EAST' THEN 'EAST'
        WHEN UPPER(branch) = 'WEST' THEN 'WEST'
        ELSE UPPER(branch)
    END AS Depot,
    COUNT(*) as Total_Deliveries
FROM deliveries
GROUP BY Depot
ORDER BY Total_Deliveries DESC
"""

df = pd.read_sql_query(query, conn)
print("Raw query result:")
print(df)

conn.close()
