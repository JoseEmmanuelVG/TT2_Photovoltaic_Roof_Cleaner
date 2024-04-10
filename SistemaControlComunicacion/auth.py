from flask_login import UserMixin, LoginManager, login_user, logout_user
from flask_bcrypt import Bcrypt
from dash import Dash

# Suponiendo que este es tu usuario y contraseña encriptada
USERS = {
    "usuario": "hashed_pw_aquí"
}

app = Dash(__name__)
server = app.server  # Exponer el servidor Flask para Flask-Login
bcrypt = Bcrypt(server)  # Inicializar Bcrypt en el servidor Flask
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

# Función para verificar la contraseña
def check_password(username, password):
    if username in USERS and bcrypt.check_password_hash(USERS[username], password):
        return True
    return False

# Ejemplo de función para iniciar sesión
# Necesitarás implementar tu lógica para obtener los datos del formulario de inicio de sesión
def login(username, password):
    if check_password(username, password):
        user = User(username)
        login_user(user)
        return True
    return False
