from flask import Flask, render_template, redirect, url_for, flash, request, jsonify,session, make_response
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, PasswordField
from wtforms.validators import InputRequired, Length, Email, DataRequired
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
import mysql.connector
import os
import pdfkit
import smtplib
from email.message import EmailMessage

UPLOAD_FOLDER = 'src/static/uploads'
app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'teacherplanner16@gmail.com'
app.config['MAIL_PASSWORD'] = 'dnze heig ycaa das s'

mail = Mail(app)

app.config['SECRET_KEY'] = 'B!1weNAt1T^%kvhUI*5^'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'teacher_planner'
app.config['UPLOAD_FOLDER'] = 'src/static/uploads'

db = mysql.connector.connect(
    host="localhost",
    user="root",
    database="teacher_planner"
)

mysql = MySQL(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

wkhtmltopdf_path = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'

pdf_output_folder = r'C:\Users\hola\Desktop\Proyecto Final\src\static\pdfs'

config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

mensage = ""


class User(UserMixin):
    def __init__(self, id, role=3):
        self.id = id
        self.role = role

# Función para cargar un usuario dado su id
@login_manager.user_loader
def load_user(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, COALESCE(role, 3) as role FROM users WHERE id = %s", (id,))
    user_data = cur.fetchone()
    cur.close()
    if user_data:
        return User(user_data[0], user_data[1])

    return None

# Definición del formulario de login
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=20)])
    submit = SubmitField('Login')

# Ruta para el login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, username, password, role FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()
        if user and username == user[1] and password == user[2]:

            session['id_user'] = user[0]
            session['user_id'] = user[0]
            session['user_username'] = user[1]
            
            login_user(User(user[0], role=user[3]))
            if user[3] == 1:
                return redirect(url_for('admin'))
            elif user[3] == 2:
                return redirect(url_for('gestion'))
            else:
                return redirect(url_for('index'))
        
        flash('Invalid username, email, or password', 'error')
    return render_template('login.html', form=form)

# Definición del formulario de registro
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=20)])
    submit = SubmitField('Register')

# Ruta para el registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM users WHERE username = %s", (username,))
        existing_user = cur.fetchone()
        if existing_user is not None:
            flash('Username already exists', 'error')
        else:
            cur.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (username, password, 3))  # Assuming role 3 is for docentes
            mysql.connection.commit()
            flash('User registered successfully', 'success')
            return redirect(url_for('login'))
        cur.close()
    return render_template('register.html', form=form)

# Rutas protegidas por login requerido y control de roles
@app.route('/admin')
@login_required
def admin():
    if current_user.role != 1:
        return redirect(url_for('index'))
    
    user_logged_in = session['user_username']

    return render_template('admin.html', user_logged_in=user_logged_in)

@app.route('/gestion')
@login_required
def gestion():
    if current_user.role != 2:
        return redirect(url_for('index'))
    
    user_logged_in = session['user_username']

    return render_template('gestion.html', user_logged_in=user_logged_in)

@app.route('/')
@login_required
def index():
    if current_user.role == 1:
        return redirect(url_for('admin'))
    elif current_user.role == 2:
        return redirect(url_for('gestion'))
    elif current_user.role != 3:
        # Manejar el caso en el que el rol no es ni 1, ni 2, ni 3
        return redirect(url_for('login'))

    user_logged_in = session['user_username']
    # Redirigir a la página de login
    return render_template('index.html', user_logged_in=user_logged_in)  # Mostrar el splash screen antes de redirigir al index

def get_username():
    user_id = session.get("id")
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE id=%s", (user_id,))
    username = cursor.fetchone()
    return username[0] if username else None

@app.route('/perfil', methods=['GET', 'POST'])
@login_required
def perfil():
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre_apellido = request.form['nombre_apellido']
        edad = request.form['edad']
        pais = request.form['pais']
        telefono = request.form['telefono']
        materia = request.form['materia']

        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET nombre_apellido = %s, edad = %s, pais = %s, telefono = %s, materia = %s WHERE id = %s", (nombre_apellido, edad, pais, telefono, materia, session['user_id']))
        mysql.connection.commit()
        cur.close()

        flash('Perfil actualizado correctamente', 'success')
        return redirect(url_for('perfil'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT nombre_apellido, edad, pais, telefono, materia FROM users WHERE id = %s", (session['user_id'],))
    user_data = cur.fetchone()
    cur.close()

    user_logged_in = session['user_username']

    return render_template('perfil.html', user_logged_in=user_logged_in, user_data=user_data)

@app.route('/editar-perfil')
@login_required
def editar_perfil():
    cur = mysql.connection.cursor()
    cur.execute("SELECT nombre_apellido, edad, pais, telefono, materia FROM users WHERE id = %s", (session['user_id'],))
    user_data = cur.fetchone()
    cur.close()

    return render_template('editar_perfil.html', user_data=user_data)

@app.route('/eliminar-perfil', methods=['POST'])
@login_required
def eliminar_perfil():
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", (session['user_id'],))
    mysql.connection.commit()
    cur.close()

    flash('Perfil eliminado correctamente', 'success')
    session.clear()
    return redirect(url_for('login'))

@app.route('/help')
@login_required
def help():
    return render_template('help.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))



@app.route('/calendar_admin')
@login_required
def calendar_admin():
    return render_template('calendar_admin.html')

@app.route('/calendar')
@login_required
def calendar():
    return render_template('calendar.html')

@app.route('/get_events')
@login_required
def get_events():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, title, start_date AS start, end_date AS end FROM events WHERE user_id = %s", (current_user.id,))
    events = cur.fetchall()
    cur.close()
    
    return jsonify({'events': events})


@app.route('/add_event', methods=['POST'])
@login_required
def add_event():
    data = request.json
    title = data.get('title')
    start_date = data.get('start_date')
    end_date = data.get('end_date')

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO events (title, start_date, end_date, user_id) VALUES (%s, %s, %s, %s)", (title, start_date, end_date, current_user.id))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'Event added successfully'})

@app.route('/delete_event', methods=['POST'])
@login_required
def delete_event():
    data = request.json
    event_id = data.get('id')

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM events WHERE id = %s AND user_id = %s", (event_id, current_user.id))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'Event deleted successfully'})



@app.route('/materiales', methods=['GET', 'POST'])
@login_required
def materiales():
    if request.method == 'POST':
        area_taller = request.form['area_taller']
        docente = request.form['docente']
        materiales_cantidad = request.form.getlist('material_cantidad[]')
        materiales_descripcion = request.form.getlist('material_descripcion[]')
        materiales_existencia = request.form.getlist('material_existencia[]')
        materiales_comprar = request.form.getlist('material_comprar[]')

        cur = mysql.connection.cursor()

        for i in range(len(materiales_cantidad)):
            cantidad = materiales_cantidad[i]
            descripcion = materiales_descripcion[i]
            existencia = materiales_existencia[i]
            comprar = materiales_comprar[i]
            cur.execute("INSERT INTO materiales (area_taller, docente, cantidad, descripcion, en_existencia, comprar, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s)", (area_taller, docente, cantidad, descripcion, existencia, comprar, session['user_id']))

        mysql.connection.commit()
        cur.close()

        flash('Materiales agregados correctamente', 'success')

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM materiales WHERE user_id = %s", (session['user_id'],))
    materiales = cur.fetchall()
    cur.close()
    user_logged_in = session['user_username']

    return render_template('materiales.html', materiales=materiales, user_logged_in=user_logged_in)

@app.route('/ver_materiales_enviados/<id>', methods=['GET'])
@login_required
def ver_materiales_enviados(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM materiales WHERE id = %s", (id,))
    materiales = cur.fetchall()
    cur.close()

    return render_template('materiales_enviados.html', materiales=materiales)

@app.route('/ver_materiales_enviados2/<id>', methods=['GET'])
def ver_materiales_enviados2(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM materiales WHERE id = %s", (id,))
    materiales = cur.fetchall()
    cur.close()

    return render_template('materiales_enviados2.html', materiales=materiales)


@app.route('/descargar_materiales', methods=["GET"])
@login_required
def descargar_materiales():
    # URL del contenido a convertir en PDF
    url = 'http://127.0.0.1:5000/ver_materiales_enviados2/18'  # Se debe especificar un ID válido

    # Genera el PDF desde la URL
    pdf = pdfkit.from_url(url, False, configuration=config)

    # Crea una respuesta para descargar el PDF
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=materiales N. 001.pdf'

    return response

def enviar(id):
    pdf_output_path = os.path.join(pdf_output_folder, 'materiales.pdf')
    if os.path.exists(pdf_output_path):
        os.remove(pdf_output_path)

    id_materiales = str(id)
    session['id_materiales_enviada'] = int(id_materiales)

    # Renderiza el contenido HTML
    url = f'http://127.0.0.1:5000/ver_materiales_enviados2/{id_materiales}'

    # Genera el PDF desde el HTML
    pdf = pdfkit.from_url(url, False, configuration=config)

    # Guarda el PDF como archivo en la carpeta especificada
    with open(pdf_output_path, 'wb') as f:
        f.write(pdf)

    # Devuelve una respuesta con la ubicación del archivo PDF generado
    return f'PDF generado y guardado en: {pdf_output_path}'


@app.route('/enviar_Email', methods=['GET'])
@login_required
def enviar_e():
    # Genera y guarda el archivo PDF
    enviar(18)

    pdf_output_path = os.path.join(pdf_output_folder, 'materiales.pdf')
    pdf_path = pdf_output_path

    # Configuración del correo electrónico
    correo_remitente = "teacherplanner16@gmail.com"
    contrasena_remitente = "dnze heig ycaa das s"
    correo_destinatario = "daurisyjoniken@gmail.com"
    servidor_smtp = "smtp.gmail.com"
    puerto_smtp = 587

    # Crear mensaje de correo electrónico
    email = EmailMessage()
    email["From"] = correo_remitente
    email["To"] = correo_destinatario
    email["Subject"] = "Materiales adjunta"
    email.set_content("Adjunto encontrarás los Materiales")

    # Adjuntar el archivo PDF
    with open(pdf_path, "rb") as attachment:
        contenido_pdf = attachment.read()
    email.add_attachment(contenido_pdf, maintype="application", subtype="octet-stream", filename=os.path.basename(pdf_path))

    # Enviar correo electrónico
    with smtplib.SMTP(servidor_smtp, puerto_smtp) as smtp:
        smtp.starttls()
        smtp.login(correo_remitente, contrasena_remitente)
        smtp.send_message(email)

    # Redirigir después de enviar el correo
    return redirect(url_for('index'))



@app.route('/editar_material/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_material(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM materiales WHERE id = %s", (id,))
    material = cur.fetchone()
    cur.close()

    if request.method == 'POST':
        area_taller = request.form['area_taller']
        docente = request.form['docente']
        cantidad = request.form['materiales_cantidad']
        descripcion = request.form['materiales_descripcion']
        existencia = request.form['materiales_existencia']
        comprar = request.form['materiales_comprar']

        cur = mysql.connection.cursor()
        cur.execute("UPDATE materiales SET area_taller = %s, docente = %s, cantidad = %s, descripcion = %s, en_existencia = %s, comprar = %s WHERE id = %s", (area_taller, docente, cantidad, descripcion, existencia, comprar, id))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('materiales'))

    return render_template('editar_material.html', material=material)

@app.route('/eliminar_material/<string:id>', methods=['POST'])
@login_required
def eliminar_material(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM materiales WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('materiales'))

@app.route('/materiales_gestion', methods=['GET', 'POST'])
@login_required
def materiales_gestion():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM materiales")
    materiales = cur.fetchall()
    cur.close()
    user_logged_in = session['user_username']

    return render_template('materiales_gestion.html', materiales=materiales, user_logged_in=user_logged_in)

@app.route('/editar_material_gestion/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_material_gestion(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM materiales WHERE id = %s", (id,))
    material = cur.fetchone()
    cur.close()

    if request.method == 'POST':
        area_taller = request.form['area_taller']
        docente = request.form['docente']
        cantidad = request.form['cantidad']
        descripcion = request.form['descripcion']
        existencia = request.form['existencia']
        comprar = request.form['comprar']

        cur = mysql.connection.cursor()
        cur.execute("UPDATE materiales SET area_taller = %s, docente = %s, cantidad = %s, descripcion = %s, en_existencia = %s, comprar = %s WHERE id = %s", (area_taller, docente, cantidad, descripcion, existencia, comprar, id))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('materiales_gestion'))

    return render_template('editar_material_gestion.html', material=material)

@app.route('/eliminar_material_gestion/<int:id>', methods=['POST'])
@login_required
def eliminar_material_gestion(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM materiales WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('materiales_gestion'))

class PlanificacionForm(FlaskForm):
    institucion = StringField('Institucion', validators=[DataRequired()])
    area_taller = StringField('Area/Taller', validators=[DataRequired()])
    ra = StringField('Resultado de Aprendizaje', validators=[DataRequired()])
    elementos_capacidad = StringField('Elementos de Capacidad', validators=[DataRequired()])
    nivel = StringField('Nivel', validators=[DataRequired()])
    fecha = StringField('Fecha', validators=[DataRequired()])
    estrategias = StringField('Estrategias de Enseñanza-Aprendizaje', validators=[DataRequired()])
    actividades_evaluacion = StringField('Actividades de Evaluación e instrumentos de Evaluación', validators=[DataRequired()])
    contenidos_trabajados = StringField('Contenidos Trabajados', validators=[DataRequired()])
    docente = StringField('docente', validators=[DataRequired()])
    codigo = StringField('codigo', validators=[DataRequired()])
    UC = StringField('codigo', validators=[DataRequired()])
    fecha_inicio = DateField('Fecha de Inicio', format='%Y-%m-%d', validators=[DataRequired()])
    fecha_termino = DateField('Fecha de Termino', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Enviar')

@app.route('/planificacion', methods=['GET', 'POST'])
@login_required
def planificacion():
    form = PlanificacionForm()
    if form.validate_on_submit():
        institucion = form.institucion.data
        taller = form.area_taller.data
        ra = form.ra.data
        elementos_capacidad = form.elementos_capacidad.data
        nivel = form.nivel.data
        fecha = form.fecha.data
        estrategias = form.estrategias.data
        actividades_evaluacion = form.actividades_evaluacion.data
        contenidos_trabajados = form.contenidos_trabajados.data
        docente = form.docente.data
        codigo = form.codigo.data
        UC = form.UC.data
        fecha_inicio = form.fecha_inicio.data
        fecha_termino = form.fecha_termino.data

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO planificaciones (institucion, taller, ra, elementos_capacidad, nivel, fecha, estrategias, actividades_evaluacion, contenidos_trabajados, docente, codigo, UC, inicio, termino, id_user) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (institucion, taller, ra, elementos_capacidad, nivel, fecha, estrategias, actividades_evaluacion, contenidos_trabajados, docente, codigo, UC, fecha_inicio, fecha_termino, session['id_user']))
        mysql.connection.commit()
        cur.close()

        flash('Planificación agregada correctamente', 'success')
        return redirect(url_for('planificacion'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM planificaciones WHERE id_user = %s",(session['id_user'],))
    planificacion = cur.fetchall()
    cur.close()
    user_logged_in = session['user_username']

    return render_template('planificacion2.html', form=form, planificacion=planificacion, user_logged_in=user_logged_in)

@app.route('/agregarplanificacion')
@login_required
def agregarplanificacion():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM planificaciones')
    data = cur.fetchall()
    cur.close()  # Cerrar el cursor después de usarlo
    return render_template('agregarplanificacion.html', planificacion=data)

@app.route('/add_contact3', methods=["POST"])
@login_required
def add_contact_planificacion():
    if request.method == 'POST':
        institucion = request.form['institucion']
        taller = request.form['taller']
        ra = request.form['ra']
        elementos_capacidad = request.form['elementos_capacidad']
        nivel = request.form['nivel']
        fecha = request.form['fecha']
        estrategias = request.form['estrategias']
        actividades_evaluacion = request.form['actividades_evaluacion']
        contenidos_trabajados = request.form['contenidos_trabajados']
        docente = request.form['docente']
        codigo = request.form['codigo']
        UC = request.form['UC']
        fecha_inicio = request.form['fecha_inicio']
        fecha_termino = request.form['fecha_termino']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO planificaciones (institucion, taller, ra, elementos_capacidad, nivel, fecha, estrategias, actividades_evaluacion, contenidos_trabajados, docente, codigo, UC, inicio, termino) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    (institucion, taller, ra, elementos_capacidad, nivel, fecha, estrategias, actividades_evaluacion, contenidos_trabajados, docente, codigo, UC, fecha_inicio, fecha_termino))

        mysql.connection.commit()
        cur.close()  # Cerrar el cursor después de usarlo
        flash('Contact Added Successfully')
        return redirect(url_for('planificacion'))

@app.route('/edit3/<id>', methods=['GET', 'POST'])
@login_required
def edit_planificacion(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM planificaciones WHERE id = %s', (id,))
    planificacion = cur.fetchone()
    cur.close()

    form = PlanificacionForm(obj=planificacion)

    if form.validate_on_submit():
        # Aquí tu código para actualizar una planificación existente
        flash('Planificación actualizada correctamente', 'success')
        return redirect(url_for('planificacion'))

    return render_template('edit-planificacion.html', form=form)

@app.route('/update3/<id>', methods=['POST'])
@login_required
def update_contact_planificaciones(id):
    if request.method == 'POST':
        institucion = request.form['institucion']
        taller = request.form['taller']
        ra = request.form['ra']
        elementos_capacidad = request.form['elementos_capacidad']
        nivel = request.form['nivel']
        fecha = request.form['fecha']
        estrategias = request.form['estrategias']
        actividades_evaluacion = request.form['actividades_evaluacion']
        contenidos_trabajados = request.form['contenidos_trabajados']
        docente = request.form['docente']
        codigo = request.form['codigo']
        UC = request.form['UC']
        fecha_inicio = request.form['fecha_inicio']
        fecha_termino = request.form['fecha_termino']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE planificaciones SET institucion=%s, taller=%s, ra=%s, elementos_capacidad=%s, nivel=%s, fecha=%s, estrategias=%s, actividades_evaluacion=%s, contenidos_trabajados=%s, docente=%s,codigo=%s,UC=%s, inicio=%s, termino=%s, WHERE id=%s",
                     (institucion, taller, ra, elementos_capacidad, nivel, fecha, estrategias, actividades_evaluacion, contenidos_trabajados, docente, codigo,UC, fecha_inicio, fecha_termino, id))

        flash(f'Contact  has been updated!', 'success')
        return redirect(url_for('planificacion'))

@app.route('/delete3/<string:id>')
@login_required
def delete_contact_planificaciones(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM planificaciones WHERE id = %s", (id,))
    mysql.connection.commit()
    flash('Contact Deleted Successfully')
    return redirect(url_for('planificacion'))

@app.route('/ver_planificacion/<id>', methods=["GET"])
@login_required
def ver_planificacion(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM planificaciones WHERE id = %s", (id,))
    data = cur.fetchone()
    cur.close()

    return render_template('ver_planificacion.html', data=data)

@app.route('/ver_planificacion_2/<id>', methods=["GET"])
def ver_planificacion_2(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM planificaciones WHERE id = %s", (id,))
    data = cur.fetchone()
    cur.close()

    return render_template('ver_planificacion_2.html', data=data)

config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
options = {
    'page-size': 'Legal',
    'orientation': 'Landscape'
}

@app.route('/descargar_planificacion/<id>', methods=["GET"])
@login_required
def descargar_planificacion(id):
    id_planificacion = id
    # URL del contenido a convertir en PDF
    url = 'http://127.0.0.1:5000//ver_planificacion_2/' + id_planificacion
    # Genera el PDF desde la URL con las opciones de configuración
    pdf = pdfkit.from_url(url, False, configuration=config, options=options)

    # Genera el nombre del archivo PDF
    id_factura_int = int(id_planificacion)
    if id_factura_int >= 10:
        filename = 'planificacion N. 000' + id_planificacion + '.pdf'
    elif id_factura_int > 99:
        filename = 'planificacion N. 00' + id_planificacion + '.pdf'
    else:
        filename = 'Planificacion N. 0000' + id_planificacion + '.pdf'

    # Crea una respuesta para descargar el PDF
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=' + filename

    return response

@app.route('/agregardocentes')
@login_required
def agregardocentes():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM users')
    data = cur.fetchall()
    cur.close()  # Cerrar el cursor después de usarlo
    return render_template('agregardocentes.html', contacts=data)

@app.route('/add_contact', methods=["POST"])
@login_required
def add_contact():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO users (username,  password, role) VALUES (%s,  %s, %s)',
                    (username,  password, role))
        mysql.connection.commit()
        cur.close()  # Cerrar el cursor después de usarlo
        flash('Contact Added Successfully')
        return redirect(url_for('agregardocentes'))

@app.route('/edit/<id>')
@login_required
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM users WHERE id = %s', (id,))
    data = cur.fetchall()
    return render_template('edit-contact.html', contact=data[0])

@app.route('/update/<id>', methods=['POST'])
@login_required
def update_contact(id):
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET username=%s, password=%s, role=%s WHERE id=%s",
                    (username,  password, role, id))
        mysql.connection.commit()
        flash(f'Contact {username} has been updated!', 'success')
        return redirect(url_for('agregardocentes'))

@app.route('/delete/<string:id>')
@login_required
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", (id,))
    mysql.connection.commit()
    flash('Contact Deleted Successfully')
    return redirect(url_for('agregardocentes'))

@app.route('/agregargestion')
@login_required
def agregargestion():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM users')
    data = cur.fetchall()
    cur.close()  # Cerrar el cursor después de usarlo
    return render_template('agregargestion.html', contacts=data)

@app.route('/add_contact1', methods=["POST"])
@login_required
def add_contact1():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO users (username, password, role) VALUES (%s, %s, %s)',
                    (username, password, role))
        mysql.connection.commit()
        cur.close()  # Cerrar el cursor después de usarlo
        flash('Contact Added Successfully')
        return redirect(url_for('agregargestion'))

@app.route('/edit1/<id>')
@login_required
def get_contact1(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM users WHERE id = %s', (id,))
    data = cur.fetchall()
    return render_template('edit-contact1.html', contact=data[0])

@app.route('/update1/<id>', methods=['POST'])
@login_required
def update_contact1(id):
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET username=%s, password=%s, role=%s WHERE id=%s",
                    (username, password, role, id))
        mysql.connection.commit()
        flash(f'Contact {username} has been updated!', 'success')
        return redirect(url_for('agregargestion'))

@app.route('/delete1/<string:id>')
@login_required
def delete_contact1(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", (id,))
    mysql.connection.commit()
    flash('Contact Deleted Successfully')
    return redirect(url_for('agregargestion'))

@app.route('/agregarusuario')
@login_required
def agregar_usuario():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM users')
    data = cur.fetchall()
    cur.close()  # Cerrar el cursor después de usarlo
    return render_template('agregar_usuario.html', contacts=data)

@app.route('/agregar_usuario', methods=["POST"])
@login_required
def agregar_usuario_post():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO users (username, password, role) VALUES (%s, %s, %s)',
                    (username, password, role))
        mysql.connection.commit()
        cur.close()  # Cerrar el cursor después de usarlo
        flash('Usuario agregado exitosamente')
        return redirect(url_for('agregar_usuario'))

@app.route('/editar_usuario/<id>')
@login_required
def editar_usuario(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM users WHERE id = %s', (id,))
    data = cur.fetchall()
    return render_template('editar_usuario.html', contact=data[0])

@app.route('/editar_usuario/<id>', methods=['POST'])
@login_required
def editar_usuario_post(id):
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET username=%s, password=%s, role=%s WHERE id=%s",
                    (username, password, role, id))
        mysql.connection.commit()
        flash(f'Usuario {username} ha sido actualizado!', 'success')
        return redirect(url_for('agregar_usuario'))

@app.route('/eliminar_usuario/<string:id>')
@login_required
def eliminar_usuario(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", (id,))
    mysql.connection.commit()
    flash('Usuario eliminado exitosamente')
    return redirect(url_for('agregar_usuario'))

class Planificacion2Form(FlaskForm):
    instituto = StringField('instituto', validators=[DataRequired()])
    asignatura = StringField('asignatura', validators=[DataRequired()])
    grado = StringField('grado', validators=[DataRequired()])
    docente = StringField('docente', validators=[DataRequired()])
    tiempo_asignado = StringField('tiempo_asignado', validators=[DataRequired()])
    tema = StringField('tema', validators=[DataRequired()])
    competencias_fundamentales = StringField('competencias_fundamentales', validators=[DataRequired()])
    nivel_de_dominio = StringField('nivel_de_dominio', validators=[DataRequired()])
    competencias_especificas = StringField('competencias_especificas', validators=[DataRequired()])
    situacion_de_aprendizaje = StringField('situacion_de_aprendizaje', validators=[DataRequired()])
    secuencias_didacticas = StringField('secuencias_didacticas', validators=[DataRequired()])
    momento = StringField('momento', validators=[DataRequired()])
    tiempo = StringField('tiempo', validators=[DataRequired()])
    actividades_de_aprendizaje = StringField('actividades_de_aprendizaje', validators=[DataRequired()])
    indicadores_de_logro = StringField('indicadores_de_logro', validators=[DataRequired()])
    metacognicion = StringField('metacognicion', validators=[DataRequired()])
    evidencias = StringField('evidencias', validators=[DataRequired()])
    tecnicas_e_instrumentos = StringField('tecnicas_e_instrumentos', validators=[DataRequired()])
    recursos = StringField('recursos', validators=[DataRequired()])
    submit = SubmitField('Enviar')

@app.route('/planificacion_academica', methods=['GET', 'POST'])
@login_required
def planificacion_academica():
    form = Planificacion2Form()
    if form.validate_on_submit():
        instituto = form.instituto.data
        asignatura = form.asignatura.data
        grado = form.grado.data
        docente = form.docente.data
        tiempo_asignado = form.tiempo_asignado.data
        tema = form.tema.data
        competencias_fundamentales = form.competencias_fundamentales.data
        nivel_de_dominio = form.nivel_de_dominio.data
        competencias_especificas = form.competencias_especificas.data
        situacion_de_aprendizaje = form.situacion_de_aprendizaje.data
        secuencias_didacticas = form.secuencias_didacticas.data
        momento = form.momento.data
        tiempo = form.tiempo.data
        actividades_de_aprendizaje = form.actividades_de_aprendizaje.data
        indicadores_de_logro = form.indicadores_de_logro.data
        metacognicion = form.metacognicion.data
        evidencias = form.evidencias.data
        tecnicas_e_instrumentos = form.tecnicas_e_instrumentos.data
        recursos = form.recursos.data

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO planificacion_academica (instituto, asignatura, grado, docente, tiempo_asignado, tema, competencias_fundamentales, nivel_de_dominio, competencias_especificas, situacion_de_aprendizaje, secuencias_didacticas, momento, tiempo, actividades_de_aprendizaje, indicadores_de_logro, metacognicion, evidencias, tecnicas_e_instrumentos, recursos, id_user) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                    (instituto, asignatura, grado, docente, tiempo_asignado, tema, competencias_fundamentales, nivel_de_dominio, competencias_especificas, situacion_de_aprendizaje, secuencias_didacticas, momento, tiempo, actividades_de_aprendizaje, indicadores_de_logro, metacognicion, evidencias, tecnicas_e_instrumentos, recursos, session['id_user']))
        mysql.connection.commit()
        cur.close()

        flash('Planificación agregada correctamente', 'success')
        return redirect(url_for('planificacion_academica'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM planificacion_academica WHERE id_user = %s",(session['id_user'],))
    planificacion_academica = cur.fetchall()
    cur.close()
    user_logged_in = session['user_username']

    return render_template('planificacion_academica.html', form=form, planificacion_academica=planificacion_academica, user_logged_in=user_logged_in)

@app.route('/agregarplanificacion_academica')
@login_required
def agregarplanificacion_academica():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM planificacion_academica')
    data_academica = cur.fetchall()
    cur.close()  # Cerrar el cursor después de usarlo
    return render_template('agregarplanificacion_academica.html', planificacion_academica=data_academica)

@app.route('/add_contact3_academica', methods=["POST"])
@login_required
def add_contact_planificacion_academica():
    if request.method == 'POST':
        instituto = request.form['instituto']
        asignatura = request.form['asignatura']
        grado = request.form['grado']
        docente = request.form['docente']
        tiempo_asignado = request.form['tiempo_asignado']
        tema = request.form['tema']
        competencias_fundamentales = request.form['competencias_fundamentales']
        nivel_de_dominio = request.form['nivel_de_dominio']
        competencias_especificas = request.form['competencias_especificas']
        situacion_de_aprendizaje = request.form['situacion_de_aprendizaje']
        secuencias_didacticas = request.form['secuencias_didacticas']
        momento = request.form['momento']
        tiempo = request.form['tiempo']
        actividades_de_aprendizaje = request.form['actividades_de_aprendizaje']
        indicadores_de_logro = request.form['indicadores_de_logro']
        metacognicion = request.form['metacognicion']
        evidencias = request.form['evidencias']
        tecnicas_e_instrumentos = request.form['tecnicas_e_instrumentos']
        recursos = request.form['recursos']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO planificacion_academica (instituto, asignatura, grado, docente, tiempo_asignado, tema, competencias_fundamentales, nivel_de_dominio, competencias_especificas, situacion_de_aprendizaje, secuencias_didacticas, momento, tiempo, actividades_de_aprendizaje, indicadores_de_logro, metacognicion, evidencias, tecnicas_e_instrumentos, recursos, id_user) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                    (instituto, asignatura, grado, docente, tiempo_asignado, tema, competencias_fundamentales, nivel_de_dominio, competencias_especificas, situacion_de_aprendizaje, secuencias_didacticas, momento, tiempo, actividades_de_aprendizaje, indicadores_de_logro, metacognicion, evidencias, tecnicas_e_instrumentos, recursos, session['id_user']))

        mysql.connection.commit()
        cur.close()  # Cerrar el cursor después de usarlo
        flash('Contact Added Successfully')
        return redirect(url_for('planificacion_academica'))

@app.route('/edit3_academica/<id>', methods=['GET', 'POST'])
@login_required
def edit_planificacion_academica(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM planificacion_academica WHERE id = %s', (id,))
    planificacion = cur.fetchone()
    cur.close()

    form = Planificacion2Form(obj=planificacion)

    if form.validate_on_submit():
        # Aquí tu código para actualizar una planificación existente
        flash('Planificación actualizada correctamente', 'success')
        return redirect(url_for('planificacion_academica'))

    return render_template('edit-planificacion_academica.html', form=form)

@app.route('/update3_academica/<id>', methods=['POST'])
@login_required
def update_contact_planificaciones_academica(id):
    if request.method == 'POST':
        instituto = request.form['instituto']
        asignatura = request.form['asignatura']
        grado = request.form['grado']
        docente = request.form['docente']
        tiempo_asignado = request.form['tiempo_asignado']
        tema = request.form['tema']
        competencias_fundamentales = request.form['competencias_fundamentales']
        nivel_de_dominio = request.form['nivel_de_dominio']
        competencias_especificas = request.form['competencias_especificas']
        situacion_de_aprendizaje = request.form['situacion_de_aprendizaje']
        secuencias_didacticas = request.form['secuencias_didacticas']
        momento = request.form['momento']
        tiempo = request.form['tiempo']
        actividades_de_aprendizaje = request.form['actividades_de_aprendizaje']
        indicadores_de_logro = request.form['indicadores_de_logro']
        metacognicion = request.form['metacognicion']
        evidencias = request.form['evidencias']
        tecnicas_e_instrumentos = request.form['tecnicas_e_instrumentos']
        recursos = request.form['recursos']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO planificacion_academica (instituto, asignatura, grado, docente, tiempo_asignado, tema, competencias_fundamentales, nivel_de_dominio, competencias_especificas, situacion_de_aprendizaje, secuencias_didacticas, momento, tiempo, actividades_de_aprendizaje, indicadores_de_logro, metacognicion, evidencias, tecnicas_e_instrumentos, recursos, id_user) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                    (instituto, asignatura, grado, docente, tiempo_asignado, tema, competencias_fundamentales, nivel_de_dominio, competencias_especificas, situacion_de_aprendizaje, secuencias_didacticas, momento, tiempo, actividades_de_aprendizaje, indicadores_de_logro, metacognicion, evidencias, tecnicas_e_instrumentos, recursos, session['id_user']))

        flash(f'Contact  has been updated!', 'success')
        return redirect(url_for('planificacion_academica'))

@app.route('/delete3_academica/<string:id>')
@login_required
def delete_contact_planificaciones_academica(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM planificacion_academica WHERE id = %s", (id,))
    mysql.connection.commit()
    flash('Contact Deleted Successfully')
    return redirect(url_for('planificacion_academica'))

@app.route('/ver_planificacion_academica/<id>', methods=["GET"])
@login_required
def ver_planificacion_academica(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM planificacion_academica WHERE id = %s", (id,))
    data_academica = cur.fetchone()
    cur.close()

    return render_template('ver_planificacion_academica.html', data_academica=data_academica)

@app.route('/ver_planificacion_2_academica/<id>', methods=["GET"])
def ver_planificacion_2_academica(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM planificacion_academica WHERE id = %s", (id,))
    data_academica = cur.fetchone()
    cur.close()

    return render_template('ver_planificacion_2_academica.html', data_academica=data_academica)

config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
options = {
    'page-size': 'Legal',
    'orientation': 'Landscape'
}

@app.route('/descargar_planificacion_academica/<id>', methods=["GET"])
@login_required
def descargar_planificacion_academica(id):
    id_planificacion_academica = id
    # URL del contenido a convertir en PDF
    url = 'http://127.0.0.1:5000//ver_planificacion_2_academica/' + id_planificacion_academica
    # Genera el PDF desde la URL con las opciones de configuración
    pdf = pdfkit.from_url(url, False, configuration=config, options=options)

    # Genera el nombre del archivo PDF
    id_factura_int = int(id_planificacion_academica)
    if id_factura_int >= 10:
        filename = 'planificacion N. 000' + id_planificacion_academica + '.pdf'
    elif id_factura_int > 99:
        filename = 'planificacion N. 00' + id_planificacion_academica + '.pdf'
    else:
        filename = 'Planificacion N. 0000' + id_planificacion_academica + '.pdf'

    # Crea una respuesta para descargar el PDF
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=' + filename

    return response

class Planificacion_adminForm(FlaskForm):
    institucion = StringField('Institucion', validators=[DataRequired()])
    area_taller = StringField('Area/Taller', validators=[DataRequired()])
    ra = StringField('Resultado de Aprendizaje', validators=[DataRequired()])
    elementos_capacidad = StringField('Elementos de Capacidad', validators=[DataRequired()])
    nivel = StringField('Nivel', validators=[DataRequired()])
    fecha = StringField('Fecha', validators=[DataRequired()])
    estrategias = StringField('Estrategias de Enseñanza-Aprendizaje', validators=[DataRequired()])
    actividades_evaluacion = StringField('Actividades de Evaluación e instrumentos de Evaluación', validators=[DataRequired()])
    contenidos_trabajados = StringField('Contenidos Trabajados', validators=[DataRequired()])
    docente = StringField('docente', validators=[DataRequired()])
    codigo = StringField('codigo', validators=[DataRequired()])
    UC = StringField('codigo', validators=[DataRequired()])
    fecha_inicio = DateField('Fecha de Inicio', format='%Y-%m-%d', validators=[DataRequired()])
    fecha_termino = DateField('Fecha de Termino', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Enviar')

@app.route('/planificacion_admin', methods=['GET', 'POST'])
@login_required
def planificacion_admin():
    form = Planificacion_adminForm()
    if form.validate_on_submit():
        institucion = form.institucion.data
        taller = form.area_taller.data
        ra = form.ra.data
        elementos_capacidad = form.elementos_capacidad.data
        nivel = form.nivel.data
        fecha = form.fecha.data
        estrategias = form.estrategias.data
        actividades_evaluacion = form.actividades_evaluacion.data
        contenidos_trabajados = form.contenidos_trabajados.data
        docente = form.docente.data
        codigo = form.codigo.data
        UC = form.UC.data
        fecha_inicio = form.fecha_inicio.data
        fecha_termino = form.fecha_termino.data

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO planificaciones (institucion, taller, ra, elementos_capacidad, nivel, fecha, estrategias, actividades_evaluacion, contenidos_trabajados, docente, codigo, UC, inicio, termino, id_user) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (institucion, taller, ra, elementos_capacidad, nivel, fecha, estrategias, actividades_evaluacion, contenidos_trabajados, docente, codigo, UC, fecha_inicio, fecha_termino, session['id_user']))
        mysql.connection.commit()
        cur.close()

        flash('Planificación agregada correctamente', 'success')
        return redirect(url_for('planificacion_admin'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM planificaciones WHERE id_user = %s",(session['id_user'],))
    planificacion = cur.fetchall()
    cur.close()
    user_logged_in = session['user_username']

    return render_template('planificacion_admin.html', form=form, planificacion=planificacion, user_logged_in=user_logged_in)

class Planificacion_academica_adminForm(FlaskForm):
    instituto = StringField('instituto', validators=[DataRequired()])
    asignatura = StringField('asignatura', validators=[DataRequired()])
    grado = StringField('grado', validators=[DataRequired()])
    docente = StringField('docente', validators=[DataRequired()])
    tiempo_asignado = StringField('tiempo_asignado', validators=[DataRequired()])
    tema = StringField('tema', validators=[DataRequired()])
    competencias_fundamentales = StringField('competencias_fundamentales', validators=[DataRequired()])
    nivel_de_dominio = StringField('nivel_de_dominio', validators=[DataRequired()])
    competencias_especificas = StringField('competencias_especificas', validators=[DataRequired()])
    situacion_de_aprendizaje = StringField('situacion_de_aprendizaje', validators=[DataRequired()])
    secuencias_didacticas = StringField('secuencias_didacticas', validators=[DataRequired()])
    momento = StringField('momento', validators=[DataRequired()])
    tiempo = StringField('tiempo', validators=[DataRequired()])
    actividades_de_aprendizaje = StringField('actividades_de_aprendizaje', validators=[DataRequired()])
    indicadores_de_logro = StringField('indicadores_de_logro', validators=[DataRequired()])
    metacognicion = StringField('metacognicion', validators=[DataRequired()])
    evidencias = StringField('evidencias', validators=[DataRequired()])
    tecnicas_e_instrumentos = StringField('tecnicas_e_instrumentos', validators=[DataRequired()])
    recursos = StringField('recursos', validators=[DataRequired()])
    submit = SubmitField('Enviar')

@app.route('/planificacion_academica_admin', methods=['GET', 'POST'])
@login_required
def planificacion_academica_admin():
    form = Planificacion_academica_adminForm()
    if form.validate_on_submit():
        instituto = form.instituto.data
        asignatura = form.asignatura.data
        grado = form.grado.data
        docente = form.docente.data
        tiempo_asignado = form.tiempo_asignado.data
        tema = form.tema.data
        competencias_fundamentales = form.competencias_fundamentales.data
        nivel_de_dominio = form.nivel_de_dominio.data
        competencias_especificas = form.competencias_especificas.data
        situacion_de_aprendizaje = form.situacion_de_aprendizaje.data
        secuencias_didacticas = form.secuencias_didacticas.data
        momento = form.momento.data
        tiempo = form.tiempo.data
        actividades_de_aprendizaje = form.actividades_de_aprendizaje.data
        indicadores_de_logro = form.indicadores_de_logro.data
        metacognicion = form.metacognicion.data
        evidencias = form.evidencias.data
        tecnicas_e_instrumentos = form.tecnicas_e_instrumentos.data
        recursos = form.recursos.data

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO planificacion_academica (instituto, asignatura, grado, docente, tiempo_asignado, tema, competencias_fundamentales, nivel_de_dominio, competencias_especificas, situacion_de_aprendizaje, secuencias_didacticas, momento, tiempo, actividades_de_aprendizaje, indicadores_de_logro, metacognicion, evidencias, tecnicas_e_instrumentos, recursos, id_user) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                    (instituto, asignatura, grado, docente, tiempo_asignado, tema, competencias_fundamentales, nivel_de_dominio, competencias_especificas, situacion_de_aprendizaje, secuencias_didacticas, momento, tiempo, actividades_de_aprendizaje, indicadores_de_logro, metacognicion, evidencias, tecnicas_e_instrumentos, recursos, session['id_user']))
        mysql.connection.commit()
        cur.close()

        flash('Planificación agregada correctamente', 'success')
        return redirect(url_for('planificacion_academica_admin'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM planificacion_academica WHERE id_user = %s",(session['id_user'],))
    planificacion_academica = cur.fetchall()
    cur.close()
    user_logged_in = session['user_username']

    return render_template('planificacion_academica_admin.html', form=form, planificacion_academica=planificacion_academica, user_logged_in=user_logged_in)

@app.route('/materiales_admin', methods=['GET', 'POST'])
@login_required
def materiales_admin():
    if request.method == 'POST':
        area_taller = request.form['area_taller']
        docente = request.form['docente']
        materiales_cantidad = request.form.getlist('material_cantidad[]')
        materiales_descripcion = request.form.getlist('material_descripcion[]')
        materiales_existencia = request.form.getlist('material_existencia[]')
        materiales_comprar = request.form.getlist('material_comprar[]')

        cur = mysql.connection.cursor()

        for i in range(len(materiales_cantidad)):
            cantidad = materiales_cantidad[i]
            descripcion = materiales_descripcion[i]
            existencia = materiales_existencia[i]
            comprar = materiales_comprar[i]
            cur.execute("INSERT INTO materiales (area_taller, docente, cantidad, descripcion, en_existencia, comprar, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s)", (area_taller, docente, cantidad, descripcion, existencia, comprar, session['user_id']))

        mysql.connection.commit()
        cur.close()

        flash('Materiales agregados correctamente', 'success')

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM materiales WHERE user_id = %s", (session['user_id'],))
    materiales = cur.fetchall()
    cur.close()
    user_logged_in = session['user_username']

    return render_template('materiales_admin.html', materiales=materiales, user_logged_in=user_logged_in)


@app.route('/solicitud_requerimientos', methods=['GET', 'POST'])
@login_required
def solicitud_requerimientos():
    if request.method == 'POST':
        tipo_requerimiento = request.form['tipo_requerimiento']
        cur = mysql.connection.cursor()

        # Obtener los datos del formulario
        area_taller = request.form.get('area_taller')
        cantidad = request.form.get('Cantidad')
        descripcion = request.form.get('Descripcion')
        observacion = request.form.get('Observacion')
        fecha = request.form.get('Fecha')
        nombre = request.form.get('nombre')
        solicitado_por = request.form.get('solicitado_por')

        # Insertar los datos en la tabla correspondiente según el tipo de requerimiento
        if tipo_requerimiento == 'equipos':
            cur.execute("INSERT INTO equipos_o_maquinarias (area_taller, Cantidad, Descripcion, Observacion, Fecha, Nombre, Solicitado_por, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (area_taller, cantidad, descripcion, observacion, fecha, nombre, solicitado_por, session['user_id']))
        elif tipo_requerimiento == 'practicas':
            cur.execute("INSERT INTO Practicas_Pedagogicas (area_taller, Cantidad, Descripcion, Observacion, Fecha, Nombre, Solicitado_por, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (area_taller, cantidad, descripcion, observacion, fecha, nombre, solicitado_por, session['user_id']))
        elif tipo_requerimiento == 'oficina':
            cur.execute("INSERT INTO practicas_oficina (area_taller, Cantidad, Descripcion, Observacion, Fecha, Nombre, Solicitado_por, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (area_taller, cantidad, descripcion, observacion, fecha, nombre, solicitado_por, session['user_id']))
        elif tipo_requerimiento == 'murales':
            cur.execute("INSERT INTO practicas_murales (area_taller, Cantidad, Descripcion, Observacion, Fecha, Nombre, Solicitado_por, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (area_taller, cantidad, descripcion, observacion, fecha, nombre, solicitado_por, session['user_id']))
        elif tipo_requerimiento == 'limpieza':
            cur.execute("INSERT INTO practicas_limpieza (area_taller, Cantidad, Descripcion, Observacion, Fecha, Nombre, Solicitado_por, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (area_taller, cantidad, descripcion, observacion, fecha, nombre, solicitado_por, session['user_id']))
        elif tipo_requerimiento == 'reparaciones':
            cur.execute("INSERT INTO practicas_reparaciones (area_taller, Cantidad, Descripcion, Observacion, Fecha, Nombre, Solicitado_por, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (area_taller, cantidad, descripcion, observacion, fecha, nombre, solicitado_por, session['user_id']))
        # Agregar más casos según sea necesario

        mysql.connection.commit()
        cur.close()
        flash('Requerimientos agregados correctamente', 'success')

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM equipos_o_maquinarias WHERE user_id = %s", (session['user_id'],))
    equipos = cur.fetchall()
    cur.execute("SELECT * FROM Practicas_Pedagogicas WHERE user_id = %s", (session['user_id'],))
    practicas = cur.fetchall()
    cur.execute("SELECT * FROM practicas_oficina WHERE user_id = %s", (session['user_id'],))
    oficinas = cur.fetchall()
    cur.execute("SELECT * FROM practicas_murales WHERE user_id = %s", (session['user_id'],))
    murales = cur.fetchall()
    cur.execute("SELECT * FROM practicas_limpieza WHERE user_id = %s", (session['user_id'],))
    limpiezas = cur.fetchall()
    cur.execute("SELECT * FROM practicas_reparaciones WHERE user_id = %s", (session['user_id'],))
    reparaciones = cur.fetchall()
    # Agregar más consultas según sea necesario
    cur.close()

    user_logged_in = session['user_username']
    return render_template('Solicitud_requerimientos.html', equipos=equipos, practicas=practicas,  oficinas=oficinas, murales=murales, limpiezas=limpiezas, reparaciones=reparaciones, user_logged_in=user_logged_in)

@app.route('/ver_solicitud_enviados/<id>', methods=['GET'])
@login_required
def ver_solicitud_enviados(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM equipos_o_maquinarias WHERE user_id = %s", (session['user_id'],))
    equipos = cur.fetchall()
    cur.execute("SELECT * FROM Practicas_Pedagogicas WHERE user_id = %s", (session['user_id'],))
    practicas = cur.fetchall()
    cur.execute("SELECT * FROM practicas_oficina WHERE user_id = %s", (session['user_id'],))
    oficinas = cur.fetchall()
    cur.execute("SELECT * FROM practicas_murales WHERE user_id = %s", (session['user_id'],))
    murales = cur.fetchall()
    cur.execute("SELECT * FROM practicas_limpieza WHERE user_id = %s", (session['user_id'],))
    limpiezas = cur.fetchall()
    cur.execute("SELECT * FROM practicas_reparaciones WHERE user_id = %s", (session['user_id'],))
    reparaciones = cur.fetchall()
    cur.close()

    return render_template('solicitud_enviados.html', equipos=equipos, practicas=practicas,  oficinas=oficinas, murales=murales, limpiezas=limpiezas, reparaciones=reparaciones)

@app.route('/ver_solicitud_enviados2/<id>', methods=['GET'])
def ver_solicitud_enviados2(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM equipos_o_maquinarias WHERE user_id = %s", (session['user_id'],))
    equipos = cur.fetchall()
    cur.execute("SELECT * FROM Practicas_Pedagogicas WHERE user_id = %s", (session['user_id'],))
    practicas = cur.fetchall()
    cur.execute("SELECT * FROM practicas_oficina WHERE user_id = %s", (session['user_id'],))
    oficinas = cur.fetchall()
    cur.execute("SELECT * FROM practicas_murales WHERE user_id = %s", (session['user_id'],))
    murales = cur.fetchall()
    cur.execute("SELECT * FROM practicas_limpieza WHERE user_id = %s", (session['user_id'],))
    limpiezas = cur.fetchall()
    cur.execute("SELECT * FROM practicas_reparaciones WHERE user_id = %s", (session['user_id'],))
    reparaciones = cur.fetchall()
    cur.close()

    return render_template('solicitud_enviados2.html', equipos=equipos, practicas=practicas,  oficinas=oficinas, murales=murales, limpiezas=limpiezas, reparaciones=reparaciones)

@app.route('/descargar_solicitud', methods=["GET"])
@login_required
def descargar_solicitud():
    # URL del contenido a convertir en PDF
    url = 'http://127.0.0.1:5000/ver_solicitud_enviados2/18'  # Se debe especificar un ID válido

    # Genera el PDF desde la URL
    pdf = pdfkit.from_url(url, False, configuration=config)

    # Crea una respuesta para descargar el PDF
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=solicitud N. 001.pdf'

    return response

def enviar2(id):
    pdf_output_path = os.path.join(pdf_output_folder, 'solicitud.pdf')
    if os.path.exists(pdf_output_path):
        os.remove(pdf_output_path)

    id_solicitud = str(id)
    session['id_solicitud_enviada'] = int(id_solicitud)

    # Renderiza el contenido HTML
    url = f'http://127.0.0.1:5000/ver_solicitud_enviados2/{id_solicitud}'

    # Genera el PDF desde el HTML
    pdf = pdfkit.from_url(url, False, configuration=config)

    # Guarda el PDF como archivo en la carpeta especificada
    with open(pdf_output_path, 'wb') as f:
        f.write(pdf)

    # Devuelve una respuesta con la ubicación del archivo PDF generado
    return f'PDF generado y guardado en: {pdf_output_path}'

@app.route('/enviar_Email2', methods=['GET'])
@login_required
def enviar_e2():
    # Genera y guarda el archivo PDF
    enviar2(18)

    pdf_output_path = os.path.join(pdf_output_folder, 'solicitud.pdf')
    pdf_path = pdf_output_path

    # Configuración del correo electrónico
    correo_remitente = "teacherplanner16@gmail.com"
    contrasena_remitente = "dnze heig ycaa das s"
    correo_destinatario = "daurisyjoniken@gmail.com"
    servidor_smtp = "smtp.gmail.com"
    puerto_smtp = 587

    # Crear mensaje de correo electrónico
    email = EmailMessage()
    email["From"] = correo_remitente
    email["To"] = correo_destinatario
    email["Subject"] = "solicitud adjunta"
    email.set_content("Adjunto encontrarás los solicitud")

    # Adjuntar el archivo PDF
    with open(pdf_path, "rb") as attachment:
        contenido_pdf = attachment.read()
    email.add_attachment(contenido_pdf, maintype="application", subtype="octet-stream", filename=os.path.basename(pdf_path))

    # Enviar correo electrónico
    with smtplib.SMTP(servidor_smtp, puerto_smtp) as smtp:
        smtp.starttls()
        smtp.login(correo_remitente, contrasena_remitente)
        smtp.send_message(email)

    # Redirigir después de enviar el correo
    return redirect(url_for('index'))

@app.route('/ver_equipos/<id>', methods=['GET'])
def ver_equipos(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM equipos_o_maquinarias WHERE user_id = %s", (session['user_id'],))
    equipos = cur.fetchall()

    return render_template('ver_equipos.html', equipos=equipos)

@app.route('/ver_equipos2/<id>', methods=['GET'])
def ver_equipos2(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM equipos_o_maquinarias WHERE user_id = %s", (session['user_id'],))
    equipos = cur.fetchall()

    return render_template('ver_equipos2.html', equipos=equipos)

@app.route('/descargar_equipos', methods=["GET"])
@login_required
def descargar_equipos():
    # URL del contenido a convertir en PDF
    url = 'http://127.0.0.1:5000/ver_equipos2/18'  # Se debe especificar un ID válido

    # Genera el PDF desde la URL
    pdf = pdfkit.from_url(url, False, configuration=config)

    # Crea una respuesta para descargar el PDF
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=equipos N. 001.pdf'

    return response

def enviar3(id):
    pdf_output_path = os.path.join(pdf_output_folder, 'equipos.pdf')
    if os.path.exists(pdf_output_path):
        os.remove(pdf_output_path)

    id_equipos = str(id)
    session['id_equipos_enviada'] = int(id_equipos)

    # Renderiza el contenido HTML
    url = f'http://127.0.0.1:5000/ver_equipos2/{id_equipos}'

    # Genera el PDF desde el HTML
    pdf = pdfkit.from_url(url, False, configuration=config)

    # Guarda el PDF como archivo en la carpeta especificada
    with open(pdf_output_path, 'wb') as f:
        f.write(pdf)

    # Devuelve una respuesta con la ubicación del archivo PDF generado
    return f'PDF generado y guardado en: {pdf_output_path}'

@app.route('/enviar_Email3', methods=['GET'])
@login_required
def enviar_e3():
    # Genera y guarda el archivo PDF
    enviar3(18)

    pdf_output_path = os.path.join(pdf_output_folder, 'equipos.pdf')
    pdf_path = pdf_output_path

    # Configuración del correo electrónico
    correo_remitente = "teacherplanner16@gmail.com"
    contrasena_remitente = "dnze heig ycaa das s"
    correo_destinatario = "daurisyjoniken@gmail.com"
    servidor_smtp = "smtp.gmail.com"
    puerto_smtp = 587

    # Crear mensaje de correo electrónico
    email = EmailMessage()
    email["From"] = correo_remitente
    email["To"] = correo_destinatario
    email["Subject"] = "equipos adjunta"
    email.set_content("Adjunto encontrarás los equipos")

    # Adjuntar el archivo PDF
    with open(pdf_path, "rb") as attachment:
        contenido_pdf = attachment.read()
    email.add_attachment(contenido_pdf, maintype="application", subtype="octet-stream", filename=os.path.basename(pdf_path))

    # Enviar correo electrónico
    with smtplib.SMTP(servidor_smtp, puerto_smtp) as smtp:
        smtp.starttls()
        smtp.login(correo_remitente, contrasena_remitente)
        smtp.send_message(email)

    # Redirigir después de enviar el correo
    return redirect(url_for('index'))

@app.route('/ver_practicas/<id>', methods=['GET'])
def ver_practicas(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Practicas_Pedagogicas WHERE user_id = %s", (session['user_id'],))
    practicas = cur.fetchall()

    return render_template('ver_practicas.html', practicas=practicas)

@app.route('/ver_practicas2/<id>', methods=['GET'])
def ver_practicas2(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Practicas_Pedagogicas WHERE user_id = %s", (session['user_id'],))
    practicas = cur.fetchall()

    return render_template('ver_practicas2.html', practicas=practicas)

@app.route('/descargar_practicas', methods=["GET"])
@login_required
def descargar_practicas():
    # URL del contenido a convertir en PDF
    url = 'http://127.0.0.1:5000/ver_practicas2/18'  # Se debe especificar un ID válido

    # Genera el PDF desde la URL
    pdf = pdfkit.from_url(url, False, configuration=config)

    # Crea una respuesta para descargar el PDF
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=practicas N. 001.pdf'

    return response

def enviar4(id):
    pdf_output_path = os.path.join(pdf_output_folder, 'practicas.pdf')
    if os.path.exists(pdf_output_path):
        os.remove(pdf_output_path)

    id_practicas = str(id)
    session['id_practicas_enviada'] = int(id_practicas)

    # Renderiza el contenido HTML
    url = f'http://127.0.0.1:5000/ver_practicas2/{id_practicas}'

    # Genera el PDF desde el HTML
    pdf = pdfkit.from_url(url, False, configuration=config)

    # Guarda el PDF como archivo en la carpeta especificada
    with open(pdf_output_path, 'wb') as f:
        f.write(pdf)

    # Devuelve una respuesta con la ubicación del archivo PDF generado
    return f'PDF generado y guardado en: {pdf_output_path}'

@app.route('/enviar_Email4', methods=['GET'])
@login_required
def enviar_e4():
    # Genera y guarda el archivo PDF
    enviar4(18)

    pdf_output_path = os.path.join(pdf_output_folder, 'practicas.pdf')
    pdf_path = pdf_output_path

    # Configuración del correo electrónico
    correo_remitente = "teacherplanner16@gmail.com"
    contrasena_remitente = "dnze heig ycaa das s"
    correo_destinatario = "daurisyjoniken@gmail.com"
    servidor_smtp = "smtp.gmail.com"
    puerto_smtp = 587

    # Crear mensaje de correo electrónico
    email = EmailMessage()
    email["From"] = correo_remitente
    email["To"] = correo_destinatario
    email["Subject"] = "practicas adjunta"
    email.set_content("Adjunto encontrarás los practicas")

    # Adjuntar el archivo PDF
    with open(pdf_path, "rb") as attachment:
        contenido_pdf = attachment.read()
    email.add_attachment(contenido_pdf, maintype="application", subtype="octet-stream", filename=os.path.basename(pdf_path))

    # Enviar correo electrónico
    with smtplib.SMTP(servidor_smtp, puerto_smtp) as smtp:
        smtp.starttls()
        smtp.login(correo_remitente, contrasena_remitente)
        smtp.send_message(email)

    # Redirigir después de enviar el correo
    return redirect(url_for('index'))

@app.route('/ver_oficinas/<id>', methods=['GET'])
def ver_oficinas(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM practicas_oficina WHERE user_id = %s", (session['user_id'],))
    oficinas = cur.fetchall()

    return render_template('ver_oficinas.html', oficinas=oficinas)

@app.route('/ver_oficinas2/<id>', methods=['GET'])
def ver_oficinas2(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM practicas_oficina WHERE user_id = %s", (session['user_id'],))
    oficinas = cur.fetchall()

    return render_template('ver_oficinas2.html', oficinas=oficinas)

@app.route('/descargar_oficinas', methods=["GET"])
@login_required
def descargar_oficinas():
    # URL del contenido a convertir en PDF
    url = 'http://127.0.0.1:5000/ver_oficinas2/18'  # Se debe especificar un ID válido

    # Genera el PDF desde la URL
    pdf = pdfkit.from_url(url, False, configuration=config)

    # Crea una respuesta para descargar el PDF
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=oficinas N. 001.pdf'

    return response

def enviar5(id):
    pdf_output_path = os.path.join(pdf_output_folder, 'oficinas.pdf')
    if os.path.exists(pdf_output_path):
        os.remove(pdf_output_path)

    id_oficinas = str(id)
    session['id_oficinas_enviada'] = int(id_oficinas)

    # Renderiza el contenido HTML
    url = f'http://127.0.0.1:5000/ver_oficinas2/{id_oficinas}'

    # Genera el PDF desde el HTML
    pdf = pdfkit.from_url(url, False, configuration=config)

    # Guarda el PDF como archivo en la carpeta especificada
    with open(pdf_output_path, 'wb') as f:
        f.write(pdf)

    # Devuelve una respuesta con la ubicación del archivo PDF generado
    return f'PDF generado y guardado en: {pdf_output_path}'

@app.route('/enviar_Email5', methods=['GET'])
@login_required
def enviar_e5():
    # Genera y guarda el archivo PDF
    enviar5(18)

    pdf_output_path = os.path.join(pdf_output_folder, 'oficinas.pdf')
    pdf_path = pdf_output_path

    # Configuración del correo electrónico
    correo_remitente = "teacherplanner16@gmail.com"
    contrasena_remitente = "dnze heig ycaa das s"
    correo_destinatario = "daurisyjoniken@gmail.com"
    servidor_smtp = "smtp.gmail.com"
    puerto_smtp = 587

    # Crear mensaje de correo electrónico
    email = EmailMessage()
    email["From"] = correo_remitente
    email["To"] = correo_destinatario
    email["Subject"] = "oficinas adjunta"
    email.set_content("Adjunto encontrarás los oficinas")

    # Adjuntar el archivo PDF
    with open(pdf_path, "rb") as attachment:
        contenido_pdf = attachment.read()
    email.add_attachment(contenido_pdf, maintype="application", subtype="octet-stream", filename=os.path.basename(pdf_path))

    # Enviar correo electrónico
    with smtplib.SMTP(servidor_smtp, puerto_smtp) as smtp:
        smtp.starttls()
        smtp.login(correo_remitente, contrasena_remitente)
        smtp.send_message(email)

    # Redirigir después de enviar el correo
    return redirect(url_for('index'))

@app.route('/ver_murales/<id>', methods=['GET'])
def ver_murales(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM practicas_murales WHERE user_id = %s", (session['user_id'],))
    murales = cur.fetchall()

    return render_template('ver_murales.html', murales=murales)

@app.route('/ver_murales2/<id>', methods=['GET'])
def ver_murales2(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM practicas_murales WHERE user_id = %s", (session['user_id'],))
    murales = cur.fetchall()

    return render_template('ver_murales2.html', murales=murales)

@app.route('/descargar_murales', methods=["GET"])
@login_required
def descargar_murales():
    # URL del contenido a convertir en PDF
    url = 'http://127.0.0.1:5000/ver_murales2/18'  # Se debe especificar un ID válido

    # Genera el PDF desde la URL
    pdf = pdfkit.from_url(url, False, configuration=config)

    # Crea una respuesta para descargar el PDF
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=murales N. 001.pdf'

    return response

def enviar6(id):
    pdf_output_path = os.path.join(pdf_output_folder, 'murales.pdf')
    if os.path.exists(pdf_output_path):
        os.remove(pdf_output_path)

    id_murales = str(id)
    session['id_murales_enviada'] = int(id_murales)

    # Renderiza el contenido HTML
    url = f'http://127.0.0.1:5000/ver_murales2/{id_murales}'

    # Genera el PDF desde el HTML
    pdf = pdfkit.from_url(url, False, configuration=config)

    # Guarda el PDF como archivo en la carpeta especificada
    with open(pdf_output_path, 'wb') as f:
        f.write(pdf)

    # Devuelve una respuesta con la ubicación del archivo PDF generado
    return f'PDF generado y guardado en: {pdf_output_path}'

@app.route('/enviar_Email6', methods=['GET'])
@login_required
def enviar_e6():
    # Genera y guarda el archivo PDF
    enviar6(18)

    pdf_output_path = os.path.join(pdf_output_folder, 'murales.pdf')
    pdf_path = pdf_output_path

    # Configuración del correo electrónico
    correo_remitente = "teacherplanner16@gmail.com"
    contrasena_remitente = "dnze heig ycaa das s"
    correo_destinatario = "daurisyjoniken@gmail.com"
    servidor_smtp = "smtp.gmail.com"
    puerto_smtp = 587

    # Crear mensaje de correo electrónico
    email = EmailMessage()
    email["From"] = correo_remitente
    email["To"] = correo_destinatario
    email["Subject"] = "murales adjunta"
    email.set_content("Adjunto encontrarás los murales")

    # Adjuntar el archivo PDF
    with open(pdf_path, "rb") as attachment:
        contenido_pdf = attachment.read()
    email.add_attachment(contenido_pdf, maintype="application", subtype="octet-stream", filename=os.path.basename(pdf_path))

    # Enviar correo electrónico
    with smtplib.SMTP(servidor_smtp, puerto_smtp) as smtp:
        smtp.starttls()
        smtp.login(correo_remitente, contrasena_remitente)
        smtp.send_message(email)

    # Redirigir después de enviar el correo
    return redirect(url_for('index'))

@app.route('/ver_limpiezas/<id>', methods=['GET'])
def ver_limpiezas(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM practicas_limpieza WHERE user_id = %s", (session['user_id'],))
    limpiezas = cur.fetchall()

    return render_template('ver_limpiezas.html', limpiezas=limpiezas)

@app.route('/ver_limpiezas2/<id>', methods=['GET'])
def ver_limpiezas2(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM practicas_limpieza WHERE user_id = %s", (session['user_id'],))
    limpiezas = cur.fetchall()

    return render_template('ver_limpiezas2.html', limpiezas=limpiezas)

@app.route('/descargar_limpiezas', methods=["GET"])
@login_required
def descargar_limpiezas():
    # URL del contenido a convertir en PDF
    url = 'http://127.0.0.1:5000/ver_limpiezas2/18'  # Se debe especificar un ID válido

    # Genera el PDF desde la URL
    pdf = pdfkit.from_url(url, False, configuration=config)

    # Crea una respuesta para descargar el PDF
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=limpiezas N. 001.pdf'

    return response

def enviar7(id):
    pdf_output_path = os.path.join(pdf_output_folder, 'limpiezas.pdf')
    if os.path.exists(pdf_output_path):
        os.remove(pdf_output_path)

    id_limpiezas = str(id)
    session['id_limpiezas_enviada'] = int(id_limpiezas)

    # Renderiza el contenido HTML
    url = f'http://127.0.0.1:5000/ver_limpiezas2/{id_limpiezas}'

    # Genera el PDF desde el HTML
    pdf = pdfkit.from_url(url, False, configuration=config)

    # Guarda el PDF como archivo en la carpeta especificada
    with open(pdf_output_path, 'wb') as f:
        f.write(pdf)

    # Devuelve una respuesta con la ubicación del archivo PDF generado
    return f'PDF generado y guardado en: {pdf_output_path}'

@app.route('/enviar_Email7', methods=['GET'])
@login_required
def enviar_e7():
    # Genera y guarda el archivo PDF
    enviar7(18)

    pdf_output_path = os.path.join(pdf_output_folder, 'limpiezas.pdf')
    pdf_path = pdf_output_path

    # Configuración del correo electrónico
    correo_remitente = "teacherplanner16@gmail.com"
    contrasena_remitente = "dnze heig ycaa das s"
    correo_destinatario = "daurisyjoniken@gmail.com"
    servidor_smtp = "smtp.gmail.com"
    puerto_smtp = 587

    # Crear mensaje de correo electrónico
    email = EmailMessage()
    email["From"] = correo_remitente
    email["To"] = correo_destinatario
    email["Subject"] = "limpiezas adjunta"
    email.set_content("Adjunto encontrarás los limpiezas")

    # Adjuntar el archivo PDF
    with open(pdf_path, "rb") as attachment:
        contenido_pdf = attachment.read()
    email.add_attachment(contenido_pdf, maintype="application", subtype="octet-stream", filename=os.path.basename(pdf_path))

    # Enviar correo electrónico
    with smtplib.SMTP(servidor_smtp, puerto_smtp) as smtp:
        smtp.starttls()
        smtp.login(correo_remitente, contrasena_remitente)
        smtp.send_message(email)

    # Redirigir después de enviar el correo
    return redirect(url_for('index'))

@app.route('/ver_reparaciones/<id>', methods=['GET'])
def ver_reparaciones(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM practicas_reparaciones WHERE user_id = %s", (session['user_id'],))
    reparaciones = cur.fetchall()

    return render_template('ver_reparaciones.html', reparaciones=reparaciones)

@app.route('/ver_reparaciones2/<id>', methods=['GET'])
def ver_reparaciones2(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM practicas_reparaciones WHERE user_id = %s", (session['user_id'],))
    reparaciones = cur.fetchall()

    return render_template('ver_reparaciones2.html', reparaciones=reparaciones)

@app.route('/descargar_reparaciones', methods=["GET"])
@login_required
def descargar_reparaciones():
    # URL del contenido a convertir en PDF
    url = 'http://127.0.0.1:5000/ver_reparaciones2/18'  # Se debe especificar un ID válido

    # Genera el PDF desde la URL
    pdf = pdfkit.from_url(url, False, configuration=config)

    # Crea una respuesta para descargar el PDF
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=reparaciones N. 001.pdf'

    return response

def enviar8(id):
    pdf_output_path = os.path.join(pdf_output_folder, 'reparaciones.pdf')
    if os.path.exists(pdf_output_path):
        os.remove(pdf_output_path)

    id_reparaciones = str(id)
    session['id_reparaciones_enviada'] = int(id_reparaciones)

    # Renderiza el contenido HTML
    url = f'http://127.0.0.1:5000/ver_reparaciones2/{id_reparaciones}'

    # Genera el PDF desde el HTML
    pdf = pdfkit.from_url(url, False, configuration=config)

    # Guarda el PDF como archivo en la carpeta especificada
    with open(pdf_output_path, 'wb') as f:
        f.write(pdf)

    # Devuelve una respuesta con la ubicación del archivo PDF generado
    return f'PDF generado y guardado en: {pdf_output_path}'

@app.route('/enviar_Email8', methods=['GET'])
@login_required
def enviar_e8():
    # Genera y guarda el archivo PDF
    enviar8(18)

    pdf_output_path = os.path.join(pdf_output_folder, 'reparaciones.pdf')
    pdf_path = pdf_output_path

    # Configuración del correo electrónico
    correo_remitente = "teacherplanner16@gmail.com"
    contrasena_remitente = "dnze heig ycaa das s"
    correo_destinatario = "daurisyjoniken@gmail.com"
    servidor_smtp = "smtp.gmail.com"
    puerto_smtp = 587

    # Crear mensaje de correo electrónico
    email = EmailMessage()
    email["From"] = correo_remitente
    email["To"] = correo_destinatario
    email["Subject"] = "reparaciones adjunta"
    email.set_content("Adjunto encontrarás los reparaciones")

    # Adjuntar el archivo PDF
    with open(pdf_path, "rb") as attachment:
        contenido_pdf = attachment.read()
    email.add_attachment(contenido_pdf, maintype="application", subtype="octet-stream", filename=os.path.basename(pdf_path))

    # Enviar correo electrónico
    with smtplib.SMTP(servidor_smtp, puerto_smtp) as smtp:
        smtp.starttls()
        smtp.login(correo_remitente, contrasena_remitente)
        smtp.send_message(email)

    # Redirigir después de enviar el correo
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)