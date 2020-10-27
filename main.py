from app.server import app
import os

production = os.environ.get("PRODUCTION", False)

if __name__ == "__main__":
    if production:
        app.run(debug=True)
    else:
        app.run(debug=True,port="2020")
