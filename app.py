from flask import Flask, jsonify, render_template
import sqlite3
import os
import pandas as pd

from concurrent.futures import ThreadPoolExecutor
from flask import send_file
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent



executor = ThreadPoolExecutor(max_workers=2)

EXPORT_FOLDER = "exports"

os.makedirs(EXPORT_FOLDER, exist_ok=True)

export_status = {
    "status": "idle",
    "filename": None
}

app = Flask(__name__)
DATABASE = BASE_DIR / "database" / "analytics.db"



# -----------------------------------
# Database Connection Helper
# -----------------------------------

def get_connection():

    conn = sqlite3.connect(DATABASE)

    conn.row_factory = sqlite3.Row

    return conn

def generate_export_csv():

    global export_status

    export_status["status"] = "processing"

    conn = get_connection()

    query = """
    SELECT *
    FROM analytics
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    filename = "analytics_export.csv"

    filepath = os.path.join(
        EXPORT_FOLDER,
        filename
    )

    df.to_csv(
        filepath,
        index=False
    )

    export_status["status"] = "completed"
    export_status["filename"] = filename
# -----------------------------------
# Dashboard Route
# -----------------------------------

@app.route("/")
def dashboard():

    return render_template("dashboard.html")


# -----------------------------------
# Pipeline Metrics API
# -----------------------------------

@app.route("/api/pipeline-metrics")
def pipeline_metrics():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT metric_name, metric_value
        FROM etl_metrics
    """)

    rows = cursor.fetchall()

    conn.close()

    response = {}

    for row in rows:
        response[row["metric_name"]] = row["metric_value"]

    return jsonify(response)


# -----------------------------------
# KPI API
# -----------------------------------

@app.route("/api/kpis")
def kpis():

    conn = get_connection()

    cursor = conn.cursor()

    # Total Users
    cursor.execute("""
        SELECT COUNT(DISTINCT user_id)
        FROM analytics
    """)

    total_users = cursor.fetchone()[0]
    cursor.execute("""
    SELECT COUNT(*)
    FROM analytics
    WHERE page_views <= 1
""")

    bounce_users = cursor.fetchone()[0]

    # Converted Users
    cursor.execute("""
        SELECT COUNT(*)
        FROM analytics
        WHERE conversion_flag = 1
    """)

    converted_users = cursor.fetchone()[0]

    # Average Dwell Time
    cursor.execute("""
        SELECT ROUND(AVG(dwell_time_secs),2)
        FROM analytics
    """)

    avg_dwell_time = cursor.fetchone()[0]

    # Average Page Views
    cursor.execute("""
        SELECT ROUND(AVG(page_views),2)
        FROM analytics
    """)

    avg_page_views = cursor.fetchone()[0]

    conversion_rate = 0

    if total_users > 0:
        conversion_rate = round(
            (converted_users / total_users) * 100,
            2
        )
        bounce_rate = round(
        (bounce_users / total_users) * 100,
        2
    )

    conn.close()

    return jsonify({
        "total_users": total_users,
        "converted_users": converted_users,
        "conversion_rate": conversion_rate,
        "bounce_rate": bounce_rate,
        "avg_dwell_time": avg_dwell_time,
        "avg_page_views": avg_page_views
    })


# -----------------------------------
# High Value Users API
# -----------------------------------

@app.route("/api/high-value-users")
def high_value_users():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            user_id,
            purchase_value,
            engagement_score,
            purchase_prediction
        FROM analytics
        ORDER BY purchase_value DESC
        LIMIT 50
    """)

    rows = cursor.fetchall()

    conn.close()

    data = []

    for row in rows:

        data.append({
            "user_id": row["user_id"],
            "purchase_value": row["purchase_value"],
            "engagement_score": row["engagement_score"],
            "purchase_prediction": row["purchase_prediction"]
        })

    return jsonify(data)


# -----------------------------------
# Device Distribution API
# -----------------------------------

@app.route("/api/device-distribution")
def device_distribution():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            device_category,
            COUNT(*) as total
        FROM analytics
        GROUP BY device_category
    """)

    rows = cursor.fetchall()

    conn.close()

    response = {}

    for row in rows:
        response[row["device_category"]] = row["total"]

    return jsonify(response)


@app.route("/api/conversion-overview")
def conversion_overview():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM analytics
        WHERE conversion_flag = 1
    """)

    converted = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM analytics
        WHERE conversion_flag = 0
    """)

    not_converted = cursor.fetchone()[0]

    conn.close()

    return jsonify({
        "Converted": converted,
        "Not Converted": not_converted
    })
@app.route("/api/export", methods=["POST"])
def export_data():

    executor.submit(
        generate_export_csv
    )

    return jsonify({
        "message": "Export started"
    })


@app.route("/api/export-status")
def export_status_api():

    return jsonify(export_status)


@app.route("/api/download/<filename>")
def download_file(filename):

    filepath = os.path.join(
        EXPORT_FOLDER,
        filename
    )

    return send_file(
        filepath,
        as_attachment=True
    )
# -----------------------------------
# Run App
# -----------------------------------

if __name__ == "__main__":

    app.run(
        debug=True
    )