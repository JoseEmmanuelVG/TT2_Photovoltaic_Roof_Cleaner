from flask_login import UserMixin, LoginManager, login_user, logout_user
from flask_bcrypt import Bcrypt
from dash import Dash

# Usuario y contraseña encrytados con bcrypt
USERS = {
    "TTM_JEVG": "$2b$12$fifc8eb4cjSY/tYwewISa.7V8q2m051yemDQcsUVVAG3r9T4W/0DC"
}

app = Dash(__name__)
server = app.server  # Exponer el servidor Flask para Flask-Login
bcrypt = Bcrypt(server)
login_manager = LoginManager()
login_manager.init_app(server)

class User(UserMixin):
    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def load_user(user_id):
    if user_id in USERS:
        return User(user_id)
    return None

def check_password(username, password):
    if username in USERS:
        return bcrypt.check_password_hash(USERS[username], password)
    return False

def login(username, password):
    if check_password(username, password):
        user = User(username)
        login_user(user)
        return True
    return False



