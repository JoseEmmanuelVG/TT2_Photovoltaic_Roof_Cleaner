from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
hashed_pw = bcrypt.generate_password_hash('tu_contraseña').decode('utf-8')
print(hashed_pw)
