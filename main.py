"""
Student Performance Analytics System
Beginner-friendly project using Python, NumPy and Pandas.
Run: python main.py
"""
import numpy as np
import pandas as pd

DATA_FILE = "students.csv"
SUBJECTS = ["Python_Marks", "SQL_Marks", "Statistics_Marks", "Pandas_Marks"]
PASS_MARK = 40  # A student must score at least 40 in every subject to pass.


def assign_grade(average):
    """Return a grade based on the student's average marks."""
    if average >= 90:
        return "A+"
    elif average >= 80:
        return "A"
    elif average >= 70:
        return "B"
    elif average >= 60:
        return "C"
    elif average >= 50:
        return "D"
    else:
        return "F"


def calculate_student_results(data):
    """Add total, average, grade and pass/fail columns."""
    data = data.copy()
    data["Total_Marks"] = data[SUBJECTS].sum(axis=1)
    data["Average_Marks"] = data[SUBJECTS].mean(axis=1).round(2)
    data["Grade"] = data["Average_Marks"].apply(assign_grade)

    # A student passes only if their mark in every subject is at least PASS_MARK.
    data["Result"] = np.where((data[SUBJECTS] >= PASS_MARK).all(axis=1), "Pass", "Fail")
    return data


def show_subject_analysis(data):
    """Print average, highest and lowest marks for each subject."""
    print("\nSUBJECT-WISE ANALYSIS")
    print("-" * 65)
    for subject in SUBJECTS:  # Loop through each subject.
        print(
            f"{subject.replace('_Marks', ''):15} "
            f"Average: {data[subject].mean():6.2f} | "
            f"Highest: {data[subject].max():3} | "
            f"Lowest: {data[subject].min():3}"
        )


def main():
    try:
        data = pd.read_csv(DATA_FILE)
    except FileNotFoundError:
        print(f"Error: '{DATA_FILE}' was not found. Keep it in the same folder as main.py.")
        return

    print("=" * 65)
    print("       STUDENT PERFORMANCE ANALYTICS SYSTEM")
    print("=" * 65)
    print(f"\nNumber of students: {len(data)}")
    print(f"Columns in dataset: {len(data.columns)}")
    print("\nFirst five records:")
    print(data.head().to_string(index=False))

    results = calculate_student_results(data)

    print("\nSTUDENT RESULTS")
    print("-" * 90)
    display_columns = ["Student_ID", "Name", "Department", "Total_Marks",
                       "Average_Marks", "Grade", "Result", "Attendance_Percent"]
    print(results[display_columns].to_string(index=False))

    print("\nCLASS SUMMARY")
    print("-" * 65)
    print(f"Class average (all subject marks): {results[SUBJECTS].to_numpy().mean():.2f}")
    print(f"Highest student average: {results['Average_Marks'].max():.2f}")
    print(f"Lowest student average: {results['Average_Marks'].min():.2f}")
    print(f"Students passed: {(results['Result'] == 'Pass').sum()}")
    print(f"Students failed: {(results['Result'] == 'Fail').sum()}")
    print(f"Pass percentage: {(results['Result'].eq('Pass').mean() * 100):.2f}%")
    print(f"Average attendance: {results['Attendance_Percent'].mean():.2f}%")

    top_students = results.nlargest(3, "Average_Marks")
    print("\nTOP 3 PERFORMING STUDENTS")
    print("-" * 65)
    print(top_students[["Name", "Department", "Average_Marks", "Grade"]].to_string(index=False))

    best_student = results.loc[results["Average_Marks"].idxmax()]
    print(f"\nTop performer: {best_student['Name']} ({best_student['Average_Marks']:.2f} average)")

    show_subject_analysis(results)

    # Save the processed results so they can be reviewed or used in a report.
    results.to_csv("student_results.csv", index=False)
    print("\nProcessed results saved to 'student_results.csv'.")
    print("Project completed successfully.")


if __name__ == "__main__":
    main()
