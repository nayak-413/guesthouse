from flask import Flask, render_template
import pymysql
import os
import traceback

app = Flask(__name__, template_folder="templates", static_folder="static")

# Try MySQL connection (optional — only if environment variables are set)
try:
    conn = pymysql.connect(
        host=os.environ.get("MYSQL_ADDON_HOST"),
        user=os.environ.get("MYSQL_ADDON_USER"),
        password=os.environ.get("MYSQL_ADDON_PASSWORD"),
        database=os.environ.get("MYSQL_ADDON_DB"),
        port=int(os.environ.get("MYSQL_ADDON_PORT", 3306)),
    )
except Exception as e:
    conn = None
    print("❌ MySQL connection failed:", str(e))


@app.route("/")
def home():
    try:
        return render_template("index.html")
    except Exception as e:
        print("❌ Error in home route:", traceback.format_exc())
        return f"500 - Template error: {str(e)}", 500


@app.route("/test-db")
def test_db():
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT NOW()")
            now = cursor.fetchone()
        return f"MySQL connected. Time: {now[0]}"
    except Exception as e:
        return f"❌ MySQL error: {str(e)}"


@app.errorhandler(500)
def error_500(e):
    return f"500 - Internal Server Error: {str(e)}", 500


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # PORT is provided by Render
    app.run(host='0.0.0.0', port=port)
