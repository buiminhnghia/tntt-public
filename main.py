import os
from flask import Flask, jsonify, request
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
        # Lấy dữ liệu JSON từ request body
        new_data = request.get_json()

        if not new_data or "name" not in new_data:
            return jsonify({"error": "Thiếu field 'name'"}), 400

        response = supabase.table("aunhi2").insert(new_data).execute()
        return jsonify(response.data), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Chạy local
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
