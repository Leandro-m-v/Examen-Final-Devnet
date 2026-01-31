from flask import Flask, request, redirect, url_for, render_template_string
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

# Inicializar Flask
app = Flask(__name__)

# Conexión a la base de datos SQLite
def get_db_connection():
    conn = sqlite3.connect('usuarios.db')
    conn.row_factory = sqlite3.Row
    return conn

# Crear tabla de usuarios
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Insertar usuarios iniciales
def insertar_usuarios():
    conn = get_db_connection()
    usuarios = [
        ("Leandro Miranda", generate_password_hash("clave123")),
        ("usuario2", generate_password_hash("password456"))
    ]
    for u in usuarios:
        try:
            conn.execute(
                "INSERT INTO usuarios (usuario, password) VALUES (?, ?)", u
            )
        except sqlite3.IntegrityError:
            pass
    conn.commit()
    conn.close()

# Página de login
@app.route('/', methods=['GET', 'POST'])
def login():
    mensaje = ""
    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM usuarios WHERE usuario = ?", (usuario,)
        ).fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            mensaje = "✅ Acceso concedido"
        else:
            mensaje = "❌ Usuario o contraseña incorrectos"

    return render_template_string('''
        <h2>Login</h2>
        <form method="post">
            Usuario: <input type="text" name="usuario"><br><br>
            Contraseña: <input type="password" name="password"><br><br>
            <input type="submit" value="Ingresar">
        </form>
        <p>{{mensaje}}</p>
    ''', mensaje=mensaje)

if __name__ == '__main__':
    init_db()
    insertar_usuarios()
    app.run(host='0.0.0.0', port=5800)
