"""
healthcare_db visualizer

Requirements:
    pip install pandas matplotlib seaborn sqlalchemy psycopg2-binary

Update the connection string below with your actual credentials before running.
"""

from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ------------------------------------------------------------------
# 1. CONNECT TO YOUR DATABASE
# ------------------------------------------------------------------
# Format: postgresql://username:password@host:port/database_name
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ.get("DB_NAME")


engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

sns.set_theme(style="whitegrid")

# ------------------------------------------------------------------
# 2. APPOINTMENT VOLUME OVER TIME
# ------------------------------------------------------------------
def plot_appointments_over_time():
    query = """
        SELECT DATE_TRUNC('month', appointment_date) AS month,
               COUNT(*) AS appointment_count
        FROM appointments
        GROUP BY month
        ORDER BY month;
    """
    df = pd.read_sql(query, engine)

    plt.figure(figsize=(10, 5))
    plt.plot(df["month"], df["appointment_count"], marker="o", linewidth=2)
    plt.title("Appointment Volume Over Time")
    plt.xlabel("Month")
    plt.ylabel("Number of Appointments")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


# ------------------------------------------------------------------
# 3. REVENUE BY DEPARTMENT
# ------------------------------------------------------------------
def plot_revenue_by_department():
    query = """
        SELECT dep.department_name, SUM(b.amount) AS total_revenue
        FROM billing b
        JOIN appointments a ON b.appointment_id = a.appointment_id
        JOIN doctors doc ON a.doctor_id = doc.doctor_id
        JOIN departments dep ON doc.department_id = dep.department_id
        GROUP BY dep.department_name
        ORDER BY total_revenue DESC;
    """
    df = pd.read_sql(query, engine)

    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x="total_revenue", y="department_name", palette="viridis")
    plt.title("Total Revenue by Department")
    plt.xlabel("Revenue ($)")
    plt.ylabel("Department")
    plt.tight_layout()
    plt.show()


# ------------------------------------------------------------------
# 4. NO-SHOW RATE BY DEPARTMENT
# ------------------------------------------------------------------
def plot_no_show_rate():
    query = """
        SELECT dep.department_name,
               ROUND(100.0 * SUM(CASE WHEN a.status = 'no-show' THEN 1 ELSE 0 END) / COUNT(*), 1) AS no_show_pct
        FROM appointments a
        JOIN doctors doc ON a.doctor_id = doc.doctor_id
        JOIN departments dep ON doc.department_id = dep.department_id
        GROUP BY dep.department_name
        ORDER BY no_show_pct DESC;
    """
    df = pd.read_sql(query, engine)

    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x="no_show_pct", y="department_name", palette="rocket")
    plt.title("No-Show Rate by Department")
    plt.xlabel("No-Show Rate (%)")
    plt.ylabel("Department")
    plt.tight_layout()
    plt.show()


# ------------------------------------------------------------------
# 5. TOP 10 MOST COMMON DIAGNOSES
# ------------------------------------------------------------------
def plot_top_diagnoses():
    query = """
        SELECT description, COUNT(*) AS occurrences
        FROM diagnoses
        GROUP BY description
        ORDER BY occurrences DESC
        LIMIT 10;
    """
    df = pd.read_sql(query, engine)

    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x="occurrences", y="description", palette="mako")
    plt.title("Top 10 Most Common Diagnoses")
    plt.xlabel("Number of Occurrences")
    plt.ylabel("Diagnosis")
    plt.tight_layout()
    plt.show()


# ------------------------------------------------------------------
# 6. PATIENT AGE DISTRIBUTION
# ------------------------------------------------------------------
def plot_age_distribution():
    query = """
        SELECT date_of_birth FROM patients;
    """
    df = pd.read_sql(query, engine)
    df["date_of_birth"] = pd.to_datetime(df["date_of_birth"])
    today = pd.Timestamp.today()
    df["age"] = (today - df["date_of_birth"]).dt.days // 365

    plt.figure(figsize=(10, 5))
    sns.histplot(df["age"], bins=20, kde=True, color="steelblue")
    plt.title("Patient Age Distribution")
    plt.xlabel("Age")
    plt.ylabel("Number of Patients")
    plt.tight_layout()
    plt.show()


# ------------------------------------------------------------------
# 7. APPOINTMENT STATUS BREAKDOWN
# ------------------------------------------------------------------
def plot_status_breakdown():
    query = """
        SELECT status, COUNT(*) AS count
        FROM appointments
        GROUP BY status;
    """
    df = pd.read_sql(query, engine)

    plt.figure(figsize=(7, 7))
    plt.pie(df["count"], labels=df["status"], autopct="%1.1f%%", startangle=90,
            colors=sns.color_palette("pastel"))
    plt.title("Appointment Status Breakdown")
    plt.tight_layout()
    plt.show()


# ------------------------------------------------------------------
# RUN ALL VISUALIZATIONS
# ------------------------------------------------------------------
if __name__ == "__main__":
    plot_appointments_over_time()
    plot_revenue_by_department()
    plot_no_show_rate()
    plot_top_diagnoses()
    plot_age_distribution()
    plot_status_breakdown()
