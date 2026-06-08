#!/usr/bin/env python3
"""Inspect SQLite database schema"""

import sqlite3
import os

db_path = os.path.join('.', 'data', 'delivery.db')

if not os.path.exists(db_path):
    print(f"❌ Database not found at {db_path}")
else:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print(f"✅ Database found: {db_path}")
    print(f"\n📊 TABLES ({len(tables)}):")
    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        row_count = cursor.fetchone()[0]
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        print(f"\n  {table_name} ({row_count} rows, {len(columns)} columns)")
        for col in columns:
            col_id, col_name, col_type, not_null, default, pk = col
            pk_mark = " [PK]" if pk else ""
            print(f"    - {col_name}: {col_type}{pk_mark}")
    
    conn.close()
    print("\n✅ Database structure ready for pipeline")
