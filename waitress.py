from waitress import serve
from app import app
if __name__ == "__main__":
    # 假設您的 Flask app 物件是 'app'
    serve(app, host='0.0.0.0', port=5000)
