#!/usr/bin/env python3
"""Database Module - SQLite connection and queries with schema validation"""

import sqlite3
import os
from typing import Optional, List, Tuple, Set
import pandas as pd


class Database:
    """SQLite database interface with schema validation"""
    
    REQUIRED_TABLES = ['deliveries', 'feedback']
    
    REQUIRED_COLUMNS = {
        'deliveries': ['delivery_id', 'branch', 'delivery_priority', 'vehicle_type',
                      'distance_km', 'num_stops_on_route', 'driver_experience_months'],
        'feedback': ['feedback_id', 'delivery_id', 'rating'],
    }
    
    def __init__(self, db_path: str):
        """Initialize database connection
        
        Args:
            db_path: Path to SQLite database file
            
        Raises:
            FileNotFoundError: If database file not found
            ValueError: If database schema is invalid
        """
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"Database file not found: {db_path}")
        
        self.db_path = db_path
        self.conn = None
    
    def connect(self) -> None:
        """Connect to database and validate schema
        
        Raises:
            ValueError: If schema validation fails
        """
        try:
            self.conn = sqlite3.connect(self.db_path)
        except sqlite3.Error as e:
            raise ValueError(f"Failed to connect to database: {e}")
        
        # Validate schema on connect
        self._validate_schema()
    
    def _validate_schema(self) -> None:
        """Validate database schema
        
        Raises:
            ValueError: If required tables/columns are missing
        """
        if not self.conn:
            raise ValueError("Database connection not established")
        
        cursor = self.conn.cursor()
        
        # Check tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        existing_tables = {row[0] for row in cursor.fetchall()}
        
        for table in self.REQUIRED_TABLES:
            if table not in existing_tables:
                raise ValueError(f"Required table '{table}' not found in database")
        
        # Check required columns exist
        for table, required_cols in self.REQUIRED_COLUMNS.items():
            cursor.execute(f"PRAGMA table_info({table})")
            existing_cols = {row[1] for row in cursor.fetchall()}
            
            missing_cols = [col for col in required_cols if col not in existing_cols]
            if missing_cols:
                raise ValueError(f"Table '{table}' missing required columns: {missing_cols}")
        
        cursor.close()
    
    def disconnect(self) -> None:
        """Close database connection"""
        if self.conn:
            self.conn.close()
            self.conn = None
    
    def query(self, sql: str) -> pd.DataFrame:
        """Execute query and return DataFrame
        
        Args:
            sql: SQL query string
            
        Returns:
            Query results as DataFrame
            
        Raises:
            ValueError: If connection not established
            sqlite3.DatabaseError: If query execution fails
        """
        if not self.conn:
            raise ValueError("Database connection not established. Call connect() first.")
        
        try:
            return pd.read_sql_query(sql, self.conn)
        except sqlite3.Error as e:
            raise sqlite3.DatabaseError(f"Query execution failed: {e}")
    
    def get_deliveries(self) -> pd.DataFrame:
        """Fetch deliveries table"""
        return self.query("SELECT * FROM deliveries")
    
    def get_feedback(self) -> pd.DataFrame:
        """Fetch feedback table"""
        return self.query("SELECT * FROM feedback")
    
    def get_deliveries_with_feedback(self) -> pd.DataFrame:
        """Fetch deliveries with feedback ratings"""
        sql = """
        SELECT d.*, f.rating
        FROM deliveries d
        LEFT JOIN feedback f ON d.delivery_id = f.delivery_id
        WHERE f.rating IS NOT NULL
        """
        return self.query(sql)
    
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
