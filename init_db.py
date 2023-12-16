from datetime import datetime, timedelta
from app import app, db, Categoria, Producto, Empleado
import random

def random_date(start, end):
    """
    Esta función generará una fecha aleatoria entre dos valores de fecha dados.
    """
    delta = end - start
    random_days = random.randrange(delta.days)
    return start + timedelta(days=random_days)

with app.app_context():
    # Crea las tablas, si aún no existen
    db.create_all()

    # Verificar si los empleados ya existen para evitar duplicados
    if Empleado.query.count() == 0:
        # Fechas de inicio y fin para la fecha de nacimiento
        start_date_nacimiento = datetime.now() - timedelta(days=60*365)  # 60 años atrás
        end_date_nacimiento = datetime.now() - timedelta(days=25*365)  # 25 años atrás

        # Fechas de inicio y fin para la fecha de contratación
        start_date_contratacion = datetime.now() - timedelta(days=10*365)  # 10 años atrás
        end_date_contratacion = datetime.now()  # hasta la fecha actual

        # Empleados de prueba
        empleado1 = Empleado(
            nombre='Juan',
            apellido='Pérez',
            rut='12345678-9',
            cargo='Vendedor',
            fecha_nacimiento=random_date(start_date_nacimiento, end_date_nacimiento),
            fecha_contratacion=random_date(start_date_contratacion, end_date_contratacion),
            jornada='Completa'
        )
        empleado2 = Empleado(
            nombre='Ana',
            apellido='García',
            rut='98765432-1',
            cargo='Gerente',
            fecha_nacimiento=random_date(start_date_nacimiento, end_date_nacimiento),
            fecha_contratacion=random_date(start_date_contratacion, end_date_contratacion),
            jornada='Completa'
        )
    # Verificar si las categorías ya existen
    if Categoria.query.count() == 0:
        # Categorías de prueba
        cat1 = Categoria(nombre='Categoria 1', descripcion='Descripción de la categoría 1')
        cat2 = Categoria(nombre='Categoria 2', descripcion='Descripción de la categoría 2')

        # Añadir las categorías a la sesión de la base de datos y guardar los cambios
        db.session.add(cat1)
        db.session.add(cat2)
        db.session.add(empleado1)
        db.session.add(empleado2)
        db.session.commit()

    # Asumiendo que cat1 y cat2 son las únicas categorías, las reutilizaremos para los productos
    cat1_id = Categoria.query.filter_by(nombre='Categoria 1').first().id
    cat2_id = Categoria.query.filter_by(nombre='Categoria 2').first().id

    # Verificar si los productos ya existen
    if Producto.query.count() == 0:
        # Crear productos y asignarles las categorías creadas anteriormente
        producto1 = Producto(nombre='Laptop Gamer', precio=1200.00, descripcion='Laptop de alta gama para juegos', categoria_id=cat1_id)
        producto2 = Producto(nombre='Smartphone Pro', precio=800.00, descripcion='Último modelo con cámara de alta calidad', categoria_id=cat2_id)

        # Añadir los productos a la base de datos
        db.session.add(producto1)
        db.session.add(producto2)
        db.session.commit()
