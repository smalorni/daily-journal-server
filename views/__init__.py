# Views Module Imports

# Import from entry requests, split in two to prevent long line error
from .entry_requests import get_all_entries, get_single_entry
from .entry_requests import  create_entry, update_entry, get_entries_by_search, delete_entry
# Import from mood requests
from .mood_requests import delete_mood, get_all_moods, get_single_mood
# Import from tag requests
from .tag_requests import get_all_tags