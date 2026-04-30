import unittest
from app import app, db
from models import Category

class TestCategoryModel(unittest.TestCase):

    def setUp(self):
        # Configuramos la app para usar una base de datos temporal en memoria
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        # Limpiamos todo al terminar cada prueba
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_new_category(self):
        """Prueba que una categoría se cree correctamente con nombre y descripción"""
        cat = Category(name="Prueba", description="Esta es una descripción de test")
        db.session.add(cat)
        db.session.commit()
        
        # Verificaciones (Asserts)
        self.assertIsNotNone(cat.id)
        self.assertEqual(cat.name, "Prueba")
        self.assertIsNotNone(cat.created_at)

if __name__ == '__main__':
    unittest.main()