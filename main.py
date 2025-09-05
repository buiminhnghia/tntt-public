import os
import io
import qrcode
import base64
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from supabase import create_client, Client

# ==========================
# Config Supabase
# ==========================
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

if not url or not key:
    raise ValueError("SUPABASE_URL và SUPABASE_KEY chưa được cấu hình")

supabase: Client = create_client(url, key)

# ==========================
# Flask App
# ==========================
app = Flask(__name__)
CORS(app)  # Cho phép tất cả domain truy cập
# Nếu muốn giới hạn chỉ frontend Cloudflare, dùng:
# CORS(app, resources={r"/*": {"origins": "https://your-frontend.pages.dev"}})

@app.route("/", methods=["GET"])
def index():
    try:
        response = supabase.table("aunhi2").select("*").execute()
        rows = response.data or []
        return jsonify(rows)  # trả về JSON cho frontend React
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["POST"])
def insert_data():
    try:
        new_data = request.get_json()
        if not new_data or "name" not in new_data:
            return jsonify({"error": "Thiếu field 'name'"}), 400

        record_name = new_data["name"]
        date = new_data["date"]
        telephone = new_data["telephone"]
        manager_name = new_data.get("manager_name", "")
        # Tạo QR content
        qr_content = f"name:{record_name};date:{date};telephone:{telephone};manager_name:{manager_name}"
        qr = qrcode.make(qr_content)
        buf = io.BytesIO()
        qr.save(buf, format="PNG")
        buf.seek(0)

        qr_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
        qr_data_url = f"data:image/png;base64,{qr_base64}"

        # Insert trực tiếp name + qr_code_img
        response = supabase.table("aunhi2").insert({
            "name": record_name,
            "date":date,
            "telephone":telephone,
            "manager_name": manager_name,
            "qr_code_img": qr_data_url
        }).execute()

        row = response.data[0]
        return jsonify(row), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


    
    
# Chạy local
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
