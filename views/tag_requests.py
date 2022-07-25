import sqlite3
import json
# Import from models
from models import Tag

def get_all_tags():
    """Get all tags from list"""
    # Open a connection to the database - change it for every project
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        # Parameters must match what is in mood.py, in exact order
        db_cursor.execute("""
        SELECT
            t.id,
            t.label
            
        FROM Tag t
        """)

        # Initialize an empty list to hold all customer representations - plural
        tags = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an customer instance from the current row.
            # Note that the database fields are specified in
            # Must match parameters shown above
            tag = Tag(row['id'], row['label'])

            tags.append(tag.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(tags)