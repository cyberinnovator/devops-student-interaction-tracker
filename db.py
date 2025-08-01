"""
db.py

Handles database operations using MongoDB for student and teacher voice embeddings.
"""

from pymongo import MongoClient
import os
import logging

# Set up logging
logger = logging.getLogger(__name__)

# MongoDB connection
MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017/")
DB_NAME = os.environ.get("DB_NAME", "studentdb")

# Initialize MongoDB connection
client = MongoClient(MONGO_URL)
db = client[DB_NAME]

# Collections
students_collection = db.students
teachers_collection = db.teachers

def get_all_student_embeddings():
    """
    Get all student embeddings from MongoDB.
    Returns:
        list: List of student documents.
    """
    try:
        return list(students_collection.find({}, {"_id": 0}))
    except Exception as e:
        logger.error(f"Error getting all student embeddings: {e}")
        return []

def get_all_teacher_embeddings():
    """
    Get all teacher embeddings from MongoDB.
    Returns:
        list: List of teacher documents.
    """
    try:
        return list(teachers_collection.find({}, {"_id": 0}))
    except Exception as e:
        logger.error(f"Error getting all teacher embeddings: {e}")
        return []

def update_student_time(roll_no, delta_time):
    """
    Update student's total interaction time.
    Args:
        roll_no (str): Student roll number.
        delta_time (float): Time to add to current total.
    """
    try:
        students_collection.update_one(
            {"roll_no": roll_no},
            {"$inc": {"time": delta_time}},
            upsert=True
        )
    except Exception as e:
        logger.error(f"Error updating student time: {e}")

def add_student(roll_no, embedding_path):
    """
    Add or update a student record.
    Args:
        roll_no (str): Student roll number.
        embedding_path (str): Path to the embedding file.
    """
    try:
        students_collection.update_one(
            {"roll_no": roll_no},
            {"$set": {"embedding_path": embedding_path}},
            upsert=True
        )
    except Exception as e:
        logger.error(f"Error adding student: {e}")

def add_teacher(teacher_id, embedding_path):
    """
    Add or update a teacher record.
    Args:
        teacher_id (str): Teacher ID.
        embedding_path (str): Path to the embedding file.
    """
    try:
        teachers_collection.update_one(
            {"teacher_id": teacher_id},
            {"$set": {"embedding_path": embedding_path}},
            upsert=True
        )
    except Exception as e:
        logger.error(f"Error adding teacher: {e}")

def get_student_by_roll_no(roll_no):
    """
    Get student by roll number.
    Args:
        roll_no (str): Student roll number.
    Returns:
        dict: Student document or None if not found.
    """
    try:
        student = students_collection.find_one({"roll_no": roll_no}, {"_id": 0})
        return student
    except Exception as e:
        logger.error(f"Error getting student by roll number: {e}")
        return None

def get_teacher_by_teacher_id(teacher_id):
    """
    Get teacher by teacher ID.
    Args:
        teacher_id (str): Teacher ID.
    Returns:
        dict: Teacher document or None if not found.
    """
    try:
        teacher = teachers_collection.find_one({"teacher_id": teacher_id}, {"_id": 0})
        return teacher
    except Exception as e:
        logger.error(f"Error getting teacher by teacher ID: {e}")
        return None

def delete_student(roll_no):
    """
    Delete a student record.
    Args:
        roll_no (str): Student roll number.
    """
    try:
        students_collection.delete_one({"roll_no": roll_no})
    except Exception as e:
        logger.error(f"Error deleting student: {e}")

def delete_teacher(teacher_id):
    """
    Delete a teacher record.
    Args:
        teacher_id (str): Teacher ID.
    """
    try:
        teachers_collection.delete_one({"teacher_id": teacher_id})
    except Exception as e:
        logger.error(f"Error deleting teacher: {e}")

def get_student_count():
    """
    Get total number of students.
    Returns:
        int: Number of students.
    """
    try:
        return students_collection.count_documents({})
    except Exception as e:
        logger.error(f"Error getting student count: {e}")
        return 0

def get_teacher_count():
    """
    Get total number of teachers.
    Returns:
        int: Number of teachers.
    """
    try:
        return teachers_collection.count_documents({})
    except Exception as e:
        logger.error(f"Error getting teacher count: {e}")
        return 0

def get_students_by_time_range(min_time=0, max_time=None):
    """
    Get students within a time range.
    Args:
        min_time (float): Minimum time threshold.
        max_time (float): Maximum time threshold.
    Returns:
        list: List of students within the time range.
    """
    try:
        query = {"time": {"$gte": min_time}}
        if max_time is not None:
            query["time"]["$lte"] = max_time
        
        return list(students_collection.find(query, {"_id": 0}))
    except Exception as e:
        logger.error(f"Error getting students by time range: {e}")
        return []

# Initialize database indexes for better performance
def create_indexes():
    """
    Create indexes for better query performance.
    """
    try:
        # Create indexes on frequently queried fields
        students_collection.create_index("roll_no", unique=True)
        students_collection.create_index("time")
        teachers_collection.create_index("teacher_id", unique=True)
        logger.info("Database indexes created successfully")
    except Exception as e:
        logger.error(f"Error creating indexes: {e}")

# Create indexes when module is imported
create_indexes()
