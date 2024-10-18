from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from dotenv import load_dotenv
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import os

app = Flask(__name__)
# Clave secreta para flash messages
app.secret_key = 'tu_clave_secreta'
# Carga de variables de entorno desde .env
load_dotenv()
print("Nombre de la base de datos:", os.getenv('MYSQL_DB'))


# Configuración BD
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')


mysql = MySQL(app)

# ----Seccion Login---
login_manager = LoginManager(app)
login_manager.login_message_category = 'Por favor inicia sesión para acceder a esta pagina'
login_manager.login_view = 'login'

# Modelo Usuario
class User(UserMixin):
    def __init__(self, id, nombre, email, password):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.password = password

@login_manager.user_loader
def load_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT id, nombre, email, contraseña FROM usuarios WHERE id = %s', (user_id,))
    user = cur.fetchone()
    cur.close()
    if user:
        return User(user[0], user[1], user[2], user[3])
    return None

#----RUTAS---------

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('index_usuarios'))
    return render_template('index.html')

@app.route('/index_usuarios')
def index_usuarios():
    if 'username' in session:
        return render_template('index_usuarios.html')
    return redirect(url_for('index'))

#lOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        contraseña = request.form.get('contraseña')
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()

        if user and user[3] == contraseña: 
            user_obj = User(user[0], user[1], user[2], user[3])
            login_user(user_obj)

            session['username'] = user[1]
            return redirect(url_for('index_usuarios'))
        else:
            flash('Correo electronico o contraseña incorrectos', 'danger')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

# Registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        contraseña = request.form.get('contraseña')

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO usuarios (nombre, email, contraseña) VALUES (%s, %s, %s)', (nombre, email, contraseña))
        mysql.connection.commit()
        cur.close()

        flash('¡Registro exitoso! Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
