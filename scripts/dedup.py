import sqlite3

# Connect to your database
conn = sqlite3.connect("/Users/abhinavrai/PycharmProjects/MomentBot/data/data.db")
cursor = conn.cursor()

# Delete duplicates based on user_id, start_time, end_time
cursor.execute("""
    DELETE FROM swing_table
    WHERE rowid NOT IN (
        SELECT MIN(rowid)
        FROM swing_table
        GROUP BY user_id, start_time, end_time
    )
""")

# Commit changes and close connection
conn.commit()
conn.close()
