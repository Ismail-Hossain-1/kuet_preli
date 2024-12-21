import mysql.connector
from dotenv import load_dotenv
import uuid
import datetime
load_dotenv()
import os

def get_db_connection():
    connection = mysql.connector.connect(
        host=os.getenv('host'),           # MySQL server
        user=os.getenv('user'),          # MySQL user
        password=os.getenv('password', ''),  # MySQL password (empty string if not specified)
        database=os.getenv('database')   # Database name you created in phpMyAdmin
    )
    return connection


def make_meeting_schedule(user_Id:str, meetingName: str, startTime: str, endTime:str):
    print(user_Id)
    """
        make a new meeting schedule. make sure all the parameters are given if not ask user for them.
        
        parameters:
            user_Id: it the user id of the user
            meetingName: meetingName is the name of the meeting.
            startTime: startTime is the time when meeting starts. make sure it is in this format: "2024-12-09 12:09:49". if not convert the given time to this format
            
            endTime: endTime is the time when the meeting ends. make sure it is in this format: "2024-12-09 13:09:49".  if not convert the given time to this format

      Returns:
        str: Success or error message.
    """
    # Convert startTime and endTime to the correct format if necessary
   
    # Check if end time is after start time
    
    # Create the slot_id (for simplicity, let's use user_id + meeting_name)
    slot_id = str(uuid.uuid4())

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Insert the new slot into the database
    try:
        cursor.execute("""
            INSERT INTO slots (slot_id, slot_name, user_id, start_time, end_time, status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (slot_id, meetingName, user_Id, startTime, endTime, 'booked'))

        # Commit the transaction
        conn.commit()
        return f"Success: Meeting '{meetingName}' scheduled from {startTime} to {endTime}."

    except mysql.connector.Error as err:
        conn.rollback()  # Rollback if there is an error
        return f"Error: Unable to schedule the meeting. {err}"

    finally:
        cursor.close()
        conn.close()


