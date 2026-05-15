
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_migrate import Migrate
from datetime import datetime
from flask import jsonify
from flask import request

    
# 1. Cargar variables del archivo .env
load_dotenv()

app = Flask(__name__)
# 2. Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from models import db, Category # Línea de importación
db.init_app(app)               # Línea de inicialización (¡En una línea nueva!)
migrate = Migrate(app, db)

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





class Category(db.Model):
    __tablename__ = 'categories' #Nombre de la tabla en Neon
    __table_args__ = {'extend_existing': True} 

    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(100), nullable=False) #nullable=False hace que sea un campo obligatorio
    description = db.Column(db.String(300))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    update_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        # Esta función nos ayudará a convertir el objeto a JSON fácilmente
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "update_at": self.update_at.isoformat()
        }
    

    


# 2. Convertir cada objeto de la base de datos a un diccionario (usando nuestro to_dict)
    # 3. jsonify se encarga de convertir esa lista en una respuesta JSON oficial

def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'update_at': self.update_at.isoformat() if self.update_at else None
            }

@app.route('/api/categories', methods=['GET', 'POST'])
def handle_categories():
    from models import Category
    
    # 1. Si es POST, creamos la categoría
    if request.method == 'POST':
        data = request.get_json()
        if not data or 'name' not in data:
            return jsonify({"error": "Falta el nombre"}), 400
        
        new_cat = Category(name=data['name'], description=data.get('description'))
        db.session.add(new_cat)
        db.session.commit()
        return jsonify({"message": "Categoría creada", "name": new_cat.name}), 201

    # 2. Si es GET, consultamos y definimos la variable SIEMPRE
    all_cats = Category.query.all() # Esto crea la variable que faltaba en image_dc47b9.png
    return jsonify([cat.to_dict() for cat in all_cats]), 200
    
@app.route('/api/categories/<int:id>', methods=['DELETE'])
def delete_category(id):
    from models import Category
    category = Category.query.get_or_404(id)
    
    db.session.delete(category)
    db.session.commit()
    
    return jsonify({"message": "Categoría eliminada con éxito"}), 200



if __name__ == '__main__':
    app.run(debug=True)






