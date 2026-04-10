import mysql.connector
from faker import Faker

fake = Faker()

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Yadav@123",
    database="learnlog"
)

cursor = conn.cursor()

# Insert Users
for _ in range(20):
    name = fake.name()
    email = fake.unique.email()

    cursor.execute(
        "INSERT INTO Users (name, email) VALUES (%s, %s)",
        (name, email)
    )

conn.commit()

print("Users inserted successfully!")

# Insert Courses
categories = ['Tech', 'Business', 'Design']

for _ in range(10):
    title = fake.catch_phrase()
    category = fake.random_element(categories)

    cursor.execute(
        "INSERT INTO Courses (title, category) VALUES (%s, %s)",
        (title, category)
    )

conn.commit()

print("Courses inserted successfully!")

# Get all course IDs
cursor.execute("SELECT course_id FROM Courses")
course_ids = [row[0] for row in cursor.fetchall()]

# Insert Lessons
for course_id in course_ids:
    for _ in range(5):  # 5 lessons per course
        title = fake.sentence(nb_words=4)
        duration = fake.random_int(min=300, max=1800)  # 5–30 mins

        cursor.execute(
            "INSERT INTO Lessons (course_id, title, duration_seconds) VALUES (%s, %s, %s)",
            (course_id, title, duration)
        )

conn.commit()

print("Lessons inserted successfully!")

import random

# Get user IDs
cursor.execute("SELECT user_id FROM Users")
user_ids = [row[0] for row in cursor.fetchall()]

# Get lesson IDs + duration
cursor.execute("SELECT lesson_id, duration_seconds FROM Lessons")
lessons = cursor.fetchall()

# Insert Engagement Data
for _ in range(1000):
    user_id = random.choice(user_ids)
    lesson_id, duration = random.choice(lessons)

    watch_time = random.randint(0, duration)

    if watch_time >= duration:
        event = 'complete'
    elif watch_time > duration * 0.3:
        event = 'pause'
    else:
        event = 'play'

    cursor.execute(
        """INSERT INTO User_Engagement 
        (user_id, lesson_id, event_type, video_seconds_watched)
        VALUES (%s, %s, %s, %s)""",
        (user_id, lesson_id, event, watch_time)
    )

conn.commit()

print("User Engagement inserted successfully!")