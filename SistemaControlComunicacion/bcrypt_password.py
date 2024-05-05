from dash import Dash
from flask_bcrypt import Bcrypt

app = Dash(__name__)
bcrypt = Bcrypt(app.server)

password = "-"
hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
print(hashed_password)
