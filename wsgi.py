# from waitress import serve
from app import app

if __name__ == "__main__":
    app.run()
    # serve(app, host='0.0.0.0', port=8000)
