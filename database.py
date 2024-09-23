import sqlite3
import uuid
# Initialize the database with session support
#myUUID = uuid.uuid4()

def init_db():
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS chats (
                 id TEXT PRIMARY KEY, 
                 session_id TEXT, 
                 sender TEXT, 
                 msg TEXT, 
                 timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    return conn
init_db()
# Save msg with session_id
def save_msg(myUUID, session_id, sender, msg):
    if not session_id:  # Ensure session_id is not empty
        session_id = "default_session"  # Provide a default session ID
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    c.execute("INSERT INTO chats (id, session_id, sender, msg) VALUES (?, ?, ?, ?)", 
              (myUUID, session_id, sender, msg))
    conn.commit()
    conn.close()

# Load chat history based on session_id
def load_chat_history(session_id):
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    c.execute("SELECT sender, msg FROM chats WHERE session_id = ? ORDER BY timestamp ASC", (session_id,))
    chat_history = c.fetchall()
    conn.close()
    return chat_history

# Get all session_ids to display in sidebar
def get_sessions():
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    c.execute("SELECT DISTINCT session_id FROM chats")
    sessions = c.fetchall()
    conn.close()
    return [s[0] for s in sessions]  # Convert from list of tuples to list


def clear_chat_history(session_id):
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    print("see here>>>>",session_id)
    c.execute("DELETE FROM chats WHERE session_id = ?", (session_id,))
    conn.commit()
    conn.close()



