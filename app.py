import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# 1. Cargar variables del archivo .env
load_dotenv()

app = Flask(__name__)

# 2. Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 3. Inicializar SQLAlchemy
db = SQLAlchemy(app)

# Definir un modelo simple para probar (El "M" de MVC)
class Producto(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)

@app.route('/')
def index():
    # Intentar leer un producto para verificar conexión
    primer_producto = Producto.query.first()
    if primer_producto:
        return f"Conexión exitosa. Primer producto en inventario: {primer_producto.nombre}"
    return "Conectado a Neon, pero la tabla está vacía."

if __name__ == '__main__':
    # El puerto 5000 es el estándar de Flask
    app.run(debug=True, port=5000)