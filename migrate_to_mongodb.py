#!/usr/bin/env python3
"""
migrate_to_mongodb.py

Migration script to transfer data from SQLite to MongoDB.
Run this script if you have existing data in SQLite that you want to transfer.
"""

import sqlite3
import os
import logging
from pymongo import MongoClient

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MongoDB connection
MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017/")
DB_NAME = os.environ.get("DB_NAME", "studentdb")

def migrate_sqlite_to_mongodb():
    """
    Migrate data from SQLite to MongoDB.
    """
    try:
        # Connect to SQLite
        sqlite_path = 'student_voice_track.db'
        if not os.path.exists(sqlite_path):
            logger.warning(f"SQLite database {sqlite_path} not found. Nothing to migrate.")
            return
        
        logger.info(f"Connecting to SQLite database: {sqlite_path}")
        sqlite_conn = sqlite3.connect(sqlite_path)
        sqlite_cursor = sqlite_conn.cursor()
        
        # Connect to MongoDB
        logger.info(f"Connecting to MongoDB: {MONGO_URL}")
        mongo_client = MongoClient(MONGO_URL)
        mongo_db = mongo_client[DB_NAME]
        
        # Migrate students
        logger.info("Migrating students...")
        sqlite_cursor.execute('SELECT roll_no, embedding_path, time FROM students')
        students = sqlite_cursor.fetchall()
        
        for roll_no, embedding_path, time in students:
            # Check if embedding file exists
            if os.path.exists(embedding_path):
                mongo_db.students.update_one(
                    {"roll_no": roll_no},
                    {"$set": {
                        "roll_no": roll_no,
                        "embedding_path": embedding_path,
                        "time": time
                    }},
                    upsert=True
                )
                logger.info(f"Migrated student: {roll_no}")
            else:
                logger.warning(f"Embedding file not found for student {roll_no}: {embedding_path}")
        
        # Migrate teachers
        logger.info("Migrating teachers...")
        sqlite_cursor.execute('SELECT teacher_id, embedding_path FROM teachers')
        teachers = sqlite_cursor.fetchall()
        
        for teacher_id, embedding_path in teachers:
            # Check if embedding file exists
            if os.path.exists(embedding_path):
                mongo_db.teachers.update_one(
                    {"teacher_id": teacher_id},
                    {"$set": {
                        "teacher_id": teacher_id,
                        "embedding_path": embedding_path
                    }},
                    upsert=True
                )
                logger.info(f"Migrated teacher: {teacher_id}")
            else:
                logger.warning(f"Embedding file not found for teacher {teacher_id}: {embedding_path}")
        
        # Close connections
        sqlite_conn.close()
        mongo_client.close()
        
        logger.info("Migration completed successfully!")
        
        # Print summary
        student_count = mongo_db.students.count_documents({})
        teacher_count = mongo_db.teachers.count_documents({})
        logger.info(f"Final counts - Students: {student_count}, Teachers: {teacher_count}")
        
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        raise

if __name__ == "__main__":
    migrate_sqlite_to_mongodb() 