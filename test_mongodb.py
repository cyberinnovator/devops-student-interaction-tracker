#!/usr/bin/env python3
"""
test_mongodb.py

Test script to verify MongoDB integration is working correctly.
"""

import os
import logging
from db import (
    add_student, add_teacher, get_all_student_embeddings, 
    get_all_teacher_embeddings, get_student_by_roll_no,
    get_teacher_by_teacher_id, update_student_time,
    get_student_count, get_teacher_count
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_mongodb_connection():
    """Test basic MongoDB connection and operations."""
    try:
        logger.info("🧪 Testing MongoDB connection and operations...")
        
        # Test 1: Add a test student
        logger.info("📝 Adding test student...")
        add_student("TEST001", "test_embedding_001.npy")
        
        # Test 2: Add a test teacher
        logger.info("📝 Adding test teacher...")
        add_teacher("TEACHER001", "test_teacher_embedding_001.npy")
        
        # Test 3: Get student count
        student_count = get_student_count()
        logger.info(f"📊 Student count: {student_count}")
        
        # Test 4: Get teacher count
        teacher_count = get_teacher_count()
        logger.info(f"📊 Teacher count: {teacher_count}")
        
        # Test 5: Get all students
        students = get_all_student_embeddings()
        logger.info(f"📋 Students in database: {len(students)}")
        for student in students:
            logger.info(f"   - {student}")
        
        # Test 6: Get all teachers
        teachers = get_all_teacher_embeddings()
        logger.info(f"📋 Teachers in database: {len(teachers)}")
        for teacher in teachers:
            logger.info(f"   - {teacher}")
        
        # Test 7: Get specific student
        student = get_student_by_roll_no("TEST001")
        if student:
            logger.info(f"✅ Found student: {student}")
        else:
            logger.error("❌ Student not found")
        
        # Test 8: Get specific teacher
        teacher = get_teacher_by_teacher_id("TEACHER001")
        if teacher:
            logger.info(f"✅ Found teacher: {teacher}")
        else:
            logger.error("❌ Teacher not found")
        
        # Test 9: Update student time
        logger.info("📝 Updating student time...")
        update_student_time("TEST001", 30.5)
        
        # Test 10: Verify time update
        updated_student = get_student_by_roll_no("TEST001")
        if updated_student:
            logger.info(f"✅ Updated student time: {updated_student.get('time', 0)}")
        
        logger.info("🎉 All MongoDB tests passed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ MongoDB test failed: {e}")
        return False

def cleanup_test_data():
    """Clean up test data from database."""
    try:
        from db import delete_student, delete_teacher
        
        logger.info("🧹 Cleaning up test data...")
        delete_student("TEST001")
        delete_teacher("TEACHER001")
        logger.info("✅ Test data cleaned up")
        
    except Exception as e:
        logger.error(f"❌ Cleanup failed: {e}")

if __name__ == "__main__":
    # Check if MongoDB environment variables are set
    mongo_url = os.environ.get("MONGO_URL", "mongodb://localhost:27017/")
    db_name = os.environ.get("DB_NAME", "studentdb")
    
    logger.info(f"🔗 MongoDB URL: {mongo_url}")
    logger.info(f"📊 Database Name: {db_name}")
    
    # Run tests
    success = test_mongodb_connection()
    
    if success:
        # Ask if user wants to clean up test data
        response = input("\n🧹 Do you want to clean up test data? (y/n): ")
        if response.lower() in ['y', 'yes']:
            cleanup_test_data()
    else:
        logger.error("❌ Tests failed. Please check your MongoDB connection.") 