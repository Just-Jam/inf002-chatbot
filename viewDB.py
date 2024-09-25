import sqlite3

# Connect to the database
conn = sqlite3.connect('chat_history.db')
c = conn.cursor()

# Execute a query to select all data from the chats table
c.execute("SELECT * FROM chats")

# Fetch all rows
rows = c.fetchall()
print("here")
# Display the rows
for row in rows:
    print(row)
    print(type(row))

# Close the connection
conn.close()
