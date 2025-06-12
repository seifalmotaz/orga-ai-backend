import dotenv
from src.server import app

dotenv.load_dotenv()


if __name__ == "__main__":
    app.start(host="0.0.0.0", port=8080)
