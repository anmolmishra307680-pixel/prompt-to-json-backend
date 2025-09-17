#!/usr/bin/env python3
"""Create database tables"""

from db.database import Database

# Create database instance to get engine
db = Database()
engine = db.engine

# Import models after engine is available
from db.models import Base

def create_tables():
    print("🔧 Creating database tables...")
    
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✅ All tables created successfully!")
        
        # List created tables
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        print(f"\n📊 Created tables: {', '.join(tables)}")
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")

if __name__ == "__main__":
    create_tables()