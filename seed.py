from app import app, db
from models import Category

def seed_categories():
    with app.app_context():
        # Entramos al "contexto de la aplicación"
        # Flask necesita esto para saber qué base de datos usar fuera de app.py
        print("sowing categories...")

# 1. Categories' list

        categories =[
            {"name": "Electronics", "description": "Devices, gadgets and components."},
            {"name": "Clothes", "description": "Clothing for all ages."},
            {"name": "Home", "description": "Furniture, decoration and kitchen utensils."},
            {"name": "Sports", "description": "equipment for physical activities."},
            ]

        for cat_data in categories:
            # Verificamos si la categoría ya existe para no duplicar y causar error
            existing = Category.query.filter_by(name=cat_data['name']).first()
            
            if not existing:
                new_category = Category(
                    name=cat_data['name'],
                    description=cat_data['description']
                )
                db.session.add(new_category)
                print(f"added: {cat_data['name']}")
            else:
                print(f"alredy exists: {cat_data['name']}")

    # 2. Guardar cambios permanentemente
        db.session.commit()
        print("Database successfully seeded!")

if __name__ == '__main__':
    seed_categories()