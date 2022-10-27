from flask_app import create_app
from flask_mail import Mail
from flask_app.config import DevelopmentConfig

app = create_app(DevelopmentConfig)
mail = Mail(app)

if __name__ == '__main__':
    app.run(debug=True)