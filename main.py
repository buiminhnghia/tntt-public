from flask import Flask, render_template_string
from supabase import create_client, Client

# ==========================
# Config Supabase
# ==========================
url = "https://upzxozuvjsbqtodrvmzm.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVwenhvenV2anNicXRvZHJ2bXptIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NjY1OTM0NywiZXhwIjoyMDcyMjM1MzQ3fQ.mfBZ00kmAoxoq1Ym46BavxtwUzuRg02AwXW2Bskg1mk"
supabase: Client = create_client(url, key)

# ==========================
# Flask App
# ==========================
app = Flask(__name__)

@app.route("/")
def index():
    # Lấy dữ liệu từ bảng aunhi2
    response = supabase.table("aunhi2").select("*").execute()
    rows = response.data
    
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

if __name__ == "__main__":
    app.run(debug=True)
