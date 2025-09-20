#!/usr/bin/env python3
"""Recreate the iteration_logs table in Supabase"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from src.db.iteration_models import IterationLog, Base

def recreate_iteration_table():
    """Recreate the iteration_logs table"""
    
    # Load environment variables
    config_path = Path(__file__).parent / "config" / ".env"
    load_dotenv(config_path)
    
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("ERROR: DATABASE_URL not found in environment variables")
        return False
    
    print("Recreating iteration_logs table in Supabase...")
    print(f"Database URL: {database_url[:50]}...")
    
    try:
        # Create engine
        engine = create_engine(database_url)
        
        # Drop the table if it exists (to recreate it fresh)
        print("Dropping existing iteration_logs table (if exists)...")
        with engine.connect() as conn:
            conn.execute(text("DROP TABLE IF EXISTS iteration_logs CASCADE;"))
            conn.commit()
        
        # Create the table
        print("Creating iteration_logs table...")
        IterationLog.__table__.create(engine, checkfirst=True)
        
        # Verify table creation
        print("Verifying table structure...")
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT column_name, data_type, is_nullable 
                FROM information_schema.columns 
                WHERE table_name = 'iteration_logs'
                ORDER BY ordinal_position;
            """))
            
            columns = result.fetchall()
            if columns:
                print("Table structure:")
                for col in columns:
                    print(f"   - {col[0]}: {col[1]} ({'NULL' if col[2] == 'YES' else 'NOT NULL'})")
                
                print(f"SUCCESS: iteration_logs table recreated with {len(columns)} columns")
                return True
            else:
                print("ERROR: Table not found after creation")
                return False
                
    except Exception as e:
        print(f"ERROR: Failed to recreate table: {e}")
        return False

def test_table_operations():
    """Test basic table operations"""
    print("\nTesting table operations...")
    
    try:
        from src.db.database import Database
        db = Database()
        
        # Test saving an iteration log
        session_id = "test_session_123"
        iteration_id = db.save_iteration_log(
            session_id=session_id,
            iteration_number=1,
            prompt="Test building design",
            spec_before={"building_type": "office"},
            spec_after={"building_type": "office", "stories": 2},
            evaluation_data={"score": 8.5},
            feedback_data={"feedback": "Good design"},
            score_before=7.0,
            score_after=8.5,
            reward=1.5
        )
        
        print(f"Test iteration saved with ID: {iteration_id}")
        
        # Test retrieving iteration logs
        logs = db.get_iteration_logs(session_id)
        if logs:
            print(f"Retrieved {len(logs)} iteration logs")
            print(f"   First log: iteration {logs[0]['iteration_number']}, score: {logs[0]['score_after']}")
        else:
            print("No logs retrieved (might be using file fallback)")
        
        return True
        
    except Exception as e:
        print(f"ERROR: Table operations test failed: {e}")
        return False

if __name__ == "__main__":
    print("Supabase Iteration Table Recovery")
    print("=" * 50)
    
    # Recreate table
    if recreate_iteration_table():
        # Test operations
        test_table_operations()
        print("\nIteration table successfully recreated and tested!")
    else:
        print("\nFailed to recreate iteration table")
        
    print("\nNext steps:")
    print("1. Check your Supabase dashboard to confirm the table exists")
    print("2. Run your RL training to test iteration logging")
    print("3. Use /iterate endpoint to verify everything works")