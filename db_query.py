#!/usr/bin/env python3
"""Simple database query tool"""

import sqlite3
import json
import sys

def query_database(db_path="prompt_to_json.db"):
    """Query and display database contents"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get specifications
        cursor.execute("SELECT COUNT(*) FROM specifications")
        spec_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM evaluations") 
        eval_count = cursor.fetchone()[0]
        
        print(f"Database Statistics:")
        print(f"- Specifications: {spec_count}")
        print(f"- Evaluations: {eval_count}")
        
        if spec_count > 0:
            print(f"\nRecent Specifications:")
            cursor.execute("""
                SELECT id, prompt, timestamp 
                FROM specifications 
                ORDER BY timestamp DESC 
                LIMIT 5
            """)
            
            for row in cursor.fetchall():
                print(f"  ID {row[0]}: '{row[1][:50]}...' ({row[2]})")
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except FileNotFoundError:
        print("Database file not found. Run with --use-db first.")

if __name__ == "__main__":
    query_database()