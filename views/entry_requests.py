import sqlite3
import json
# Import from models
from models import Entry, Mood, EntryTag, Tag

def get_all_entries():
    """Get all entries from database"""
    # Open a connection to the database - must match the server name, change it for each project
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        # Added join SQL info
        # The name of tables below must match what is shown in SQL
        db_cursor.execute("""
        SELECT
            j.id,
            j.concept,
            j.entry,
            j.mood_id,
            j.date,
            m. id,
            m.label

        FROM Entry j
        JOIN Mood m
            ON m.id = j.mood_id

        """)
        #tag_id or entry_id????????

        # Initialize an empty list to hold all entries representations - plural - POSTMAN GET Requests
        entries = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an entry instance from the current row, in exact from above
            # The rows must match the parameters in entry.py, in exact order
            entry = Entry(row['id'], row['concept'], row['entry'], row['mood_id'], row['date'])

            # The rows must match the parameters in mood.py, in exact order
            # Create a Location instance from the current row
            mood = Mood(row['mood_id'], row['label'])

            # Add the dictionary representation of mood to the entry
            entry.mood = mood.__dict__
            
        # sql calls for tag id and label 
        # Indented to get all tags underneath entries
            db_cursor.execute("""
            SELECT
                e.tag_id,
                t.label

            FROM EntryTag e
            JOIN Tag t
                ON e.tag_id = t.id
            WHERE e.entry_id = ?
            """, (row['id'], ))
            # Initialize an empty list to hold all tags representations
            tags = []

            tagData = db_cursor.fetchall()

            # Iterate list of tagData returned from database
            # This part below had to be indented to avoid duplicates
            for row in tagData:

                # Create a tag instance from the current row, in exact from above
                # The rows must match the parameters, in exact order
                tag = Tag(row['tag_id'], row['label'])

                # Add the dictionary representation of tag to list
                tags.append(tag.__dict__)
                # Add tags to entry
                entry.tags = tags
                # Add the dictionary representation of the entries to the list
            entries.append(entry.__dict__)

    # Use `json` package to properly serialize list as JSON - POSTMAN GET Requests
    return json.dumps(entries)

# Single Entry Request Function
def get_single_entry(id):
    """Get single entry from list"""
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            j.id,
            j.concept,
            j.entry,
            j.mood_id,
            j.date,
            m.id,
            m. label
        FROM Entry j
        JOIN Mood m
            ON m.id = j.mood_id
        WHERE j.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        entry = Entry(data['id'], data['concept'], data['entry'], data['mood_id'], data['date'])
        
        # Create a mood instance from current row
        mood = Mood(data['id'], data['label'])
        
        # Add dictionary representation of mood to entry
        entry.mood = mood.__dict__

        return json.dumps(entry.__dict__)

# Update animal from list - you can also use update animal as parameter
def update_entry(id, replace_entry):
    """Update entry in list"""
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Entry
            SET
                concept = ?,
                entry = ?,
                mood_id = ?,
                date = ?
        WHERE id = ?
        """, (replace_entry['concept'], replace_entry['entry'],
              replace_entry['mood_id'], replace_entry['date'], id ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True

# Delete single entry
def delete_entry(id):
    """Delete entry from database list"""
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Entry
        WHERE id = ?
        """, (id, ))

# Allows users to search for entries
def get_entries_by_search(search_term):
    """Search for entries"""
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        select
            j.id,
            j.concept,
            j.entry,
            j.mood_id,
            j.date

        from Entry J
        WHERE j.entry LIKE ?       
        """, ( f'%{search_term[0]}%' , ))

        # Initialize an empty list to hold all entries representations - plural - POSTMAN GET Requests
        entries = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            # Create an entry instance from the current row, in exact from above
            # The rows must match the parameters in entry.py, in exact order
            entry = Entry(row['id'], row['concept'], row['entry'], row['mood_id'], row['date'])

            # Added mood into this search section below ***************
            # Create mood instance from current row
            #mood = Mood(row['id'], row['label'])

            # Add dictionary representation of mood
            #entry.mood = mood.__dict__
            # Add entry to list
            entries.append(entry.__dict__)

    return json.dumps(entries)

def create_entry(new_entry):
    """"Function that adds an new entry to the list
    Args:
        Entry(dict): The new entry to be added
    Returns:
        dict: The entry that was added with its new id
    """""
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Entry
            ( concept, entry, mood_id, date)
        VALUES
            ( ?, ?, ?, ?);
        """, (new_entry['concept'], new_entry['entry'],
              new_entry['mood_id'], new_entry['date']))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the entry dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_entry['id'] = id
        for tag in new_entry['tags']:
            
            db_cursor.execute("""
            INSERT INTO EntryTag
                ( entry_id, tag_id ) 
            VALUES
                ( ?, ?);
            """, (id, tag))

    return json.dumps(new_entry)
