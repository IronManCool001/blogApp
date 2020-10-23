from app.server import app
from flask_sqlalchemy import SQLAlchemy
import os

production = os.environ.get("PRODUCTION", False)

if __name__ == "__main__":
    if production:
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///posts.db"
        app.run(debug=True)
    else:
        app.run(debug=True,port="2020")