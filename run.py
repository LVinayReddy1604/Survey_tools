from app import app, db
from app.models import User, Survey, Question, Response

if __name__ == '__main__':
    app.run(debug=True)
