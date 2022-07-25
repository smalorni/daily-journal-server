import sqlite3
import json
# Import from models
from models import Mood

def get_all_moods():
    """Get all moods from list"""
    # Open a connection to the database - change it for every project
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        # Parameters must match what is in mood.py, in exact order
        db_cursor.execute("""
        SELECT
            m.id,
            m.label
            
        FROM Mood m
        """)

        # Initialize an empty list to hold all customer representations - plural
        moods = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an customer instance from the current row.
            # Note that the database fields are specified in
            # Must match parameters shown above
            mood = Mood(row['id'], row['label'])

            moods.append(mood.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(moods)

# Single Mood Request Function - realized this wasn't necessary, but left section alone ***********
def get_single_mood(id):
    """Get single mood from list"""
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            m.id
            m.label

        FROM Mood m
        WHERE m.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()
        
        # Create a mood instance from current row, must match row above
        mood = Mood(data['id'], data['label'])

        return json.dumps(mood.__dict__)

 # Delete single mood
def delete_mood(id):
    """Delete mood from database list"""
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Mood
        WHERE id = ?
        """, (id, ))