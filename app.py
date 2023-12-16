from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
# Configuración de la aplicación con la clave secreta y la base de datos SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///prototipo.db'
app.config['SECRET_KEY'] = 'esta_es_una_clave_secreta_para_el_prototipo'
db = SQLAlchemy(app)

# Modelo de Usuario para la base de datos
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(200), nullable=True)

    productos = db.relationship('Producto', backref='categoria', lazy=True)

# Modelo de Producto para la base de datos

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    descripcion = db.Column(db.String(200), nullable=True)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)


class Pedido(db.Model):
    __tablename__ = 'pedido'
    id = db.Column(db.Integer, primary_key=True)
    fecha_hora = db.Column(db.DateTime, default=datetime.utcnow)  # Fecha y hora actual UTC
    estado = db.Column(db.String(20), nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    descuento = db.Column(db.Float, nullable=True)
    total = db.Column(db.Float, nullable=False)
    # Asegúrate de que el modelo Empleado ya esté definido para poder usarlo aquí
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleado.id'), nullable=False)


class Empleado(db.Model):
    __tablename__ = 'empleado'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(20), nullable=False)
    apellido = db.Column(db.String(20), nullable=False)
    rut = db.Column(db.String(9), nullable=False)
    cargo = db.Column(db.String(30), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    fecha_contratacion = db.Column(db.Date, nullable=False)
    jornada = db.Column(db.String(10), nullable=False)


# Ruta para el inicio de sesión del usuario
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            return redirect(url_for('index'))
        else:
            return 'Invalid username or password'
    return render_template('login.html')

# Ruta para la página principal con el catálogo de productos
@app.route('/catalog', methods=['GET'])
def index():
    products = Producto.query.all()
    return render_template('index.html', products=products)

# Ruta para agregar un nuevo usuario (registro)
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/add-product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        descripcion = request.form['descripcion']
        categoria_id = request.form['categoria_id']

        new_product = Producto(nombre=nombre, precio=precio, descripcion=descripcion, categoria_id=categoria_id)
        db.session.add(new_product)
        db.session.commit()

        return redirect(url_for('index'))
    
    categorias = Categoria.query.all()
    return render_template('add-product.html', categorias=categorias)

@app.route('/add-order', methods=['GET', 'POST'])
def add_order():
    if request.method == 'POST':
        # Recoger los datos del formulario
        empleado_id = request.form.get('empleado_id')
        estado = request.form.get('estado')
        subtotal = request.form.get('subtotal')
        descuento = request.form.get('descuento') or 0  # Si no hay descuento, usar 0
        total = request.form.get('total')

        # Crear y guardar el nuevo pedido
        new_order = Pedido(
            empleado_id=empleado_id,
            estado=estado,
            subtotal=subtotal,
            descuento=descuento,
            total=total
        )
        db.session.add(new_order)
        db.session.commit()

        # Redirigir al usuario a la lista de pedidos
        return redirect(url_for('orders'))

    # Renderizar la plantilla si es una petición GET
    empleados = Empleado.query.all()  # Asegúrate de tener esta lista para el formulario
    return render_template('add_order.html', empleados=empleados)

@app.route('/orders')
def orders():
    all_orders = Pedido.query.all()  # Obtén todos los pedidos
    return render_template('orders.html', orders=all_orders)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crea las tablas de la base de datos si no existen
    app.run(debug=True)