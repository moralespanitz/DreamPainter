"""
Database configuration
"""
import sqlite3
import logging
from sqlite3 import Error
import os

logging.basicConfig()
logger = logging.getLogger()

def sqlite_connect(filepath):
    """
    Create a database or connect
    """
    conn =  None
    try:
        conn = sqlite3.connect(filepath)
        logger.info("Version: ", sqlite3.version)
    except Error as e:
        logger.error("Error: ", e)
    finally:
        if conn:
            conn.close()
if __name__ == "__main__":
    filepath = os.getenv("DATABAE_PATH")
    sqlite_connect(filepath)