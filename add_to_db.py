from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the database URL (for SQLite in this case)
DATABASE_URL = "sqlite:///./users.db"

engine = create_engine(DATABASE_URL, echo=True)

# Create a base class for models
Base = declarative_base()

# Define the Task model
class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    position = Column(String, index=True)
    room_id = Column(Integer, unique=True, index=True)

# Create the tables in the database
Base.metadata.create_all(bind=engine)

# Create a session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def add_task(position: str, room_id: int):
    # Create a new session
    db = SessionLocal()
    try:
        # Create a new Task instance
        new_task = Task(position=position, room_id=room_id)
        
        # Add the new Task to the session
        db.add(new_task)
        
        # Commit the transaction
        db.commit()
        
        print(f"Task added: Position='{position}', Room ID={room_id}")
    except Exception as e:
        print(f"Error adding task: {e}")
        db.rollback()
    finally:
        # Close the session
        db.close()

if __name__ == "__main__":
    # Example data to add
    positions = [
        {"position": "Aeronautical Engineer", "room_id": 101},
        {"position": "Software Engineer", "room_id": 102},
        {"position": "Mechanical Engineer", "room_id": 103}
    ]

    for pos in positions:
        add_task(pos["position"], pos["room_id"])




# import csv
# import sqlite3

# # Define the CSV file path
# csv_file_path = 'user.csv'

# # Connect to SQLite database
# conn = sqlite3.connect('users.db')

# # Create a cursor object
# cur = conn.cursor()

# skip = []

# # Function to add data from CSV to the database
# def add_data_to_db():
#     with open(csv_file_path, newline='') as csvfile:
#         reader = csv.DictReader(csvfile, fieldnames=['id', 'position', 'room_id'])
#         for row in reader:
#             try:
#             # Insert each row into the task table
#                 cur.execute('''
#                     INSERT INTO tasks (id, position, room_id)
#                     VALUES (?, ?, ?)
#                 ''', (int(row['id']), row['position'], int(row['room_id'])))
#             except Exception as e:
#                 print(e)
#                 skip.append(row)
    

#     # Commit the changes
#     conn.commit()

# # Run the function to insert data
# add_data_to_db()

# # Close the connection
# conn.close()
# print(skip)


# Create db

# import sqlite3

# # Connect to SQLite database (or create it if it doesn't exist)
# conn = sqlite3.connect('users.db')

# # Create a cursor object
# cur = conn.cursor()

# # Create the table
# cur.execute('''
#     CREATE TABLE IF NOT EXISTS tasks (
#         id INTEGER PRIMARY KEY,
#         position TEXT,
#         room_id INTEGER UNIQUE
#     )
# ''')

# # Commit the changes and close the connection
# conn.commit()
