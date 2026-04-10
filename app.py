import streamlit as st
import pandas as pd
import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Yadav@123",
    database="learnlog"
)

st.title("📊 LearnLog Dashboard")

query = """
WITH WatchProgress AS (
    SELECT 
        ue.user_id,
        ue.lesson_id,
        MAX(ue.video_seconds_watched) AS max_watch,
        l.duration_seconds
    FROM User_Engagement ue
    JOIN Lessons l ON ue.lesson_id = l.lesson_id
    GROUP BY ue.user_id, ue.lesson_id
),

DropOff AS (
    SELECT 
        lesson_id,
        COUNT(*) AS total_users,
        SUM(CASE 
            WHEN max_watch < duration_seconds * 0.5 THEN 1 
            ELSE 0 
        END) AS drop_users
    FROM WatchProgress
    GROUP BY lesson_id
)

SELECT 
    lesson_id,
    total_users,
    drop_users,
    (drop_users / total_users) AS drop_rate
FROM DropOff
ORDER BY drop_rate DESC;
"""

df = pd.read_sql(query, conn)

st.subheader("🔥 Hardest Lessons")
st.dataframe(df)

st.bar_chart(df.set_index("lesson_id")["drop_rate"])

if st.button("💡 Explain Hardest Lesson"):

    top_lesson = df.iloc[0]

    drop_rate = top_lesson['drop_rate']

    if drop_rate > 0.7:
        level = "very high"
    elif drop_rate > 0.5:
        level = "high"
    else:
        level = "moderate"

    explanation = f"""
    🚨 Insight:
    This lesson has a {level} drop-off rate of {drop_rate:.2f}.

    📉 Why users are dropping:
    - The lesson may be too long or complex
    - Content might not be engaging enough
    - Users may not have required background knowledge

    ✅ How to improve:
    - Break lesson into shorter parts
    - Add real-world examples
    - Improve introduction to grab attention
    - Add visuals or interactive elements

    🎯 Business Impact:
    Fixing this can improve course completion rate and increase revenue.
    """

    st.write(explanation)