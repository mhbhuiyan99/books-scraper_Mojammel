import sqlite3

conn = sqlite3.connect("books.db")
cursor = conn.cursor()

# Count records
cursor.execute("SELECT COUNT(*) FROM books")
print(f"Total books: {cursor.fetchone()[0]}")

# Show all records
cursor.execute("SELECT * FROM books")
for row in cursor.fetchall():
    print(row)

conn.close()