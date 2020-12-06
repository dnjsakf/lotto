import dotenv
import os
from app import create_app

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

app_option = {
  "static_url_path": "/static/",
  "static_folder": os.path.join(ROOT_PATH, "src"),
  "template_folder": os.path.join(ROOT_PATH, "src"),
}

app = create_app(option=app_option)

if __name__ == '__main__':
  dotenv.load_dotenv(dotenv_path=".dev.env")

  app.run(host="0.0.0.0", port=3000, threaded=True)