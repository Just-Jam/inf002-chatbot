import sqlite3

from database import init_db

DB = 'test.db'

def create_tables():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute(
        '''CREATE TABLE IF NOT EXISTS Conversations (
        conversation_id INTEGER PRIMARY KEY AUTOINCREMENT,
        conversation_title VARCHAR(255),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        '''
    )
    conn.commit()

    c.execute(
        '''
        CREATE TABLE Messages (
        message_id INTEGER PRIMARY KEY AUTOINCREMENT,
        conversation_id INTEGER NOT NULL,
        sender VARCHAR(100),
        message_text TEXT,
        sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (conversation_id) REFERENCES Conversations(conversation_id) ON DELETE CASCADE
        )
        '''
    )
    return conn

def create_conversation(conversation_title: str) -> int:
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''
    INSERT INTO Conversations (conversation_title) VALUES (?)
    ''', (conversation_title,))
    conn.commit()

    conversation_id = c.lastrowid
    conn.close()
    return conversation_id

def save_message(sender: str, message: str, conversation_id: int = 0, conversation_title = None) -> int:
    # if conversation_id == 0:
    #     #Auto create new conversation if no pass conversation_id
    #     conversation_id = create_conversation(conversation_title)

    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('PRAGMA foreign_keys = ON;')
    c.execute('''
    INSERT INTO Messages (conversation_id, sender, message_text)
    VALUES (?, ?, ?)
    ''', (conversation_id, sender, message))
    conn.commit()

    # c.execute('''SELECT * FROM Conversations''')
    # print(c.fetchall())
    # c.execute('''SELECT * FROM Messages''')
    # print(c.fetchall())
    message_id = c.lastrowid
    conn.close()
    return message_id


def load_messages_from_conversation(conversation_id: int):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''
    SELECT sender, message_text FROM Messages WHERE conversation_id = ? ORDER BY sent_at ASC
    ''', (conversation_id,))
    messages = c.fetchall()
    conn.close()
    return messages

# Get all session_ids to display in sidebar
def get_all_conversations() -> list[str]:
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT * FROM Conversations")
    conversations = c.fetchall()
    conn.close()
    return conversations


def delete_conversation(conversation_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("DELETE FROM Conversations WHERE conversation_id = ?", (conversation_id,))
    conn.commit()
    conn.close()

# save_message("hihi3","user", 3)
# msg = load_messages_from_conversation(3)
# print(msg)
# delete_conversation(3)
# convs = get_all_conversations()
# print(convs)

create_tables()