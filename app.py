
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

st.set_page_config(
    page_title="Student Performance Analytics",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Student Performance Analytics System")
st.write("Analyze student marks, grades, and academic performance.")

file_path = Path(__file__).parent / "students.csv"

if not file_path.exists():
    st.error("students.csv was not found. Upload it to the repository.")
    st.stop()

df = pd.read_csv(file_path)

# Calculate totals and averages from subject marks
subject_cols = [
    col for col in df.columns
    if col.lower() in ["math", "mathematics", "science", "english",
                       "computer", "computer science"]
]

if not subject_cols:
    st.dataframe(df, use_container_width=True)
    st.info("Showing the available student dataset.")
    st.stop()

df["Total"] = df[subject_cols].sum(axis=1)
df["Average"] = df[subject_cols].mean(axis=1).round(2)

def get_grade(avg):
    if avg >= 90:
        return "A+"
    elif avg >= 80:
        return "A"
    elif avg >= 70:
        return "B"
    elif avg >= 60:
        return "C"
    elif avg >= 40:
        return "D"
    return "F"

df["Grade"] = df["Average"].apply(get_grade)
df["Result"] = np.where(df["Average"] >= 40, "Pass", "Fail")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Students", len(df))
c2.metric("Class Average", f"{df['Average'].mean():.2f}")
c3.metric("Passed", int((df["Result"] == "Pass").sum()))
c4.metric("Failed", int((df["Result"] == "Fail").sum()))

st.subheader("Student Results")
st.dataframe(
    df.sort_values("Average", ascending=False),
    use_container_width=True
)

st.subheader("Average Marks by Subject")
subject_avg = df[subject_cols].mean().sort_values(ascending=False)
st.bar_chart(subject_avg)

st.subheader("Top 5 Students")
st.dataframe(
    df.nlargest(min(5, len(df)), "Average"),
    use_container_width=True
)

st.download_button(
    "Download Results CSV",
    data=df.to_csv(index=False).encode("utf-8"),
    file_name="student_results.csv",
    mime="text/csv"
)
