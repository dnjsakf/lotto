import dotenv
import os
from app import create_app

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

app = create_app(ROOT_PATH=ROOT_PATH)

if __name__ == '__main__':
  dotenv.load_dotenv(dotenv_path=".dev.env")

  app.run(host="0.0.0.0", port=3000, threaded=True)