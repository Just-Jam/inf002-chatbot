##I'm lazy to do extra installation for sqlite, this just drops the db table if I need to completely clear things##

import sqlite3

# Function to delete the chats table
def drop_chats_table():
    conn = sqlite3.connect('chat_history.db')  # Connect to the database
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS chats")  # Drop the chats table
    conn.commit()
    conn.close()

    print("Table 'chats' has been deleted.")

# Call the function to drop the table
drop_chats_table()
