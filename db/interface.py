"""Database interface for BHIV Bucket"""

from .database import Database

# Export main database interface
__all__ = ['Database']

# Global database instance
db = Database()