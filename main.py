import os
from flask import Flask, render_template_string
from supabase import create_client, Client

# ==========================
# Config Supabase (dùng biến môi trường để bảo mật)
# ==========================
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

if not url or not key:
    raise ValueError("SUPABASE_URL và SUPABASE_KEY chưa được cấu hình trong biến môi trường")

supabase: Client = create_client(url, key)

# ==========================
# Flask App
# ==========================
app = Flask(__name__)

@app.route("/")
def index():
    try:
        response = supabase.table("aunhi2").select("*").execute()
        rows = response.data or []
    except Exception as e:
        return f"<h3>Lỗi khi lấy dữ liệu từ Supabase: {e}</h3>"

    if not rows:
        return "<h3>Không có dữ liệu trong bảng aunhi2</h3>"

    # HTML template đơn giản
    html = """
    <h2>Danh sách dữ liệu từ bảng aunhi2</h2>
    <table border="1" cellpadding="5">
        <tr>
            {% for col in rows[0].keys() %}
                <th>{{ col }}</th>
            {% endfor %}
        </tr>
        {% for row in rows %}
        <tr>
            {% for val in row.values() %}
                <td>{{ val }}</td>
            {% endfor %}
        </tr>
        {% endfor %}
    </table>
    """
    return render_template_string(html, rows=rows)


# Chạy local (Render sẽ bỏ qua đoạn này, dùng gunicorn)
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
