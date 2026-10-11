from flask import render_template, request, redirect, url_for, session, flash
from models.trabajador import Trabajador
from models.empresa import Empresa
from models.horario import Horario
from models.dia import Dia
from models.franja_horaria import FranjaHoraria
from models.incidencia import Incidencia
from models.rol import Rol
from models.registro import Registro
from extensions import db
from functools import wraps
from app import app
import datetime

# Decorador para requerir que el usuario esté logueado
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'access_token' not in session:  # Si no hay token en sesión
            return redirect(url_for('login'))  # Redirige al login
        return f(*args, **kwargs)  # Ejecuta la función original
    return decorated_function

# Ruta para la raíz que redirige al login
@app.route('/')
def index():
    return redirect(url_for('login'))  # Redirige a la función 'login'

# Ruta para la página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None  # Inicializa variable de error
    if request.method == 'POST':  # Si se envía el formulario
        user = request.form['user']  # Obtiene usuario y contraseña
        passwd = request.form['passwd']

        trabajador = Trabajador.query.filter_by(nif=user).first()  # Busca al trabajador por NIF o email
        if not trabajador:
            trabajador = Trabajador.query.filter_by(email=user).first()

        if not trabajador:  # Si no se encuentra
            error = 'Usuario no encontrado'
        elif not trabajador.check_password(passwd):  # Si la contraseña es incorrecta
            error = 'Contraseña incorrecta'
        elif trabajador.idRol != 1:  # Si no es administrador
            error = 'No tienes permisos de administrador'
        else:
            identity = str(trabajador.id_trabajador)  # Obtiene ID del trabajador
            session['access_token'] = identity  # Guarda el ID en la sesión
            return redirect(url_for('admin'))  # Redirige al panel de administración

    return render_template('login.html', error=error)  # Renderiza la plantilla de login

# Ruta para el panel de administración
@app.route('/admin')
@login_required  # Requiere login
def admin():
    return render_template('admin.html')  # Renderiza la plantilla de administración

# Ruta para cerrar sesión
@app.route('/logout')
@login_required  # Requiere login
def logout():
    session.pop('access_token', None)  # Elimina el token de la sesión
    return redirect(url_for('login'))  # Redirige al login

# Ruta para la gestión de la empresa
@app.route('/empresa', methods=['GET', 'POST'])
@login_required  # Requiere login
def gestion_empresa():
    empresa = Empresa.query.first()  # Obtiene la primera empresa

    if not empresa:  # Si no se encuentra la empresa
        flash('No se encontró la empresa. Debe crearla primero.', 'danger')
        return redirect(url_for('admin'))

    if request.method == 'POST':  # Si se envía el formulario
        empresa.nombre = request.form['nombre']  # Actualiza la información de la empresa
        try:
            empresa.lat = float(request.form['lat'])
            empresa.long = float(request.form['long'])
            empresa.radio = float(request.form['radio'])
        except ValueError:  # Si los valores no son números válidos
            flash('Latitud, longitud y radio deben ser números válidos.', 'danger')
            return render_template('gestion_empresa.html', empresa=empresa)

        db.session.commit()  # Guarda los cambios
        flash('Información de la empresa actualizada correctamente.', 'success')
        return redirect(url_for('gestion_empresa'))

    return render_template('gestion_empresa.html', empresa=empresa)  # Renderiza la plantilla

# Ruta para listar los horarios
@app.route('/horarios')
@login_required  # Requiere login
def listar_horarios():
    horarios = Horario.query.all()  # Obtiene todos los horarios
    return render_template('horarios/listar_horarios.html', horarios=horarios)  # Renderiza la plantilla

# Ruta para crear un nuevo horario
@app.route('/horarios/crear', methods=['GET', 'POST'])
@login_required  # Requiere login
def crear_horario():
    if request.method == 'POST':  # Si se envía el formulario
        nombre_horario = request.form['nombre_horario']  # Obtiene la información del formulario
        descripcion = request.form['descripcion']

        nuevo_horario = Horario(nombre_horario=nombre_horario, descripcion=descripcion)  # Crea el nuevo horario
        db.session.add(nuevo_horario)
        db.session.commit()

        flash('Horario creado correctamente.', 'success')
        return redirect(url_for('editar_horario', horario_id=nuevo_horario.id_horario))  # Redirige a editar

    return render_template('horarios/crear_horario.html')  # Renderiza la plantilla

# Ruta para editar un horario existente
@app.route('/horarios/editar/<int:horario_id>', methods=['GET', 'POST'])
@login_required  # Requiere login
def editar_horario(horario_id):
    horario = Horario.query.get_or_404(horario_id)  # Obtiene el horario o devuelve 404
    dias = Dia.query.all()  # Obtiene todos los días

    if request.method == 'POST':  # Si se envía el formulario
        horario.nombre_horario = request.form['nombre_horario']  # Actualiza la información del horario
        horario.descripcion = request.form['descripcion']

        # Manejar las franjas horarias
        for dia in dias:  # Itera sobre los días
            hora_entrada_str = request.form.get(f'hora_entrada_{dia.id}')  # Obtiene la información de las franjas
            hora_salida_str = request.form.get(f'hora_salida_{dia.id}')

            if hora_entrada_str and hora_salida_str:  # Si ambas horas están presentes
                try:
                    hora_entrada = datetime.datetime.strptime(hora_entrada_str, '%H:%M').time()  # Convierte las horas a objetos time
                    hora_salida = datetime.datetime.strptime(hora_salida_str, '%H:%M').time()

                    if hora_entrada >= hora_salida:  # Valida que la hora de entrada sea anterior a la de salida
                        flash('La hora de entrada debe ser anterior a la hora de salida.', 'danger')
                        return render_template('horarios/editar_horario.html', horario=horario, dias=dias)

                    franja_existente = FranjaHoraria.query.filter_by(id_dia=dia.id, id_horario=horario.id_horario).first()  # Busca la franja existente
                    if franja_existente:  # Si existe, la actualiza
                        franja_existente.hora_entrada = hora_entrada
                        franja_existente.hora_salida = hora_salida
                    else:  # Si no existe, crea una nueva
                        nueva_franja = FranjaHoraria(id_dia=dia.id, id_horario=horario.id_horario, hora_entrada=hora_entrada, hora_salida=hora_salida)
                        db.session.add(nueva_franja)
                except ValueError:  # Si el formato de la hora es incorrecto
                    flash('Error en el formato de hora. Use HH:MM.', 'danger')
                    return render_template('horarios/editar_horario.html', horario=horario, dias=dias)
            elif hora_entrada_str or hora_salida_str:  # Si falta alguna hora
                flash('Debe proporcionar tanto la hora de entrada como la de salida para cada día.', 'danger')
                return render_template('horarios/editar_horario.html', horario=horario, dias=dias)
            else:
                 # Si no se proporcionan horas, eliminar la franja existente si existe
                franja_existente = FranjaHoraria.query.filter_by(id_dia=dia.id, id_horario=horario.id_horario).first()
                if franja_existente:
                    db.session.delete(franja_existente)

        db.session.commit()  # Guarda los cambios
        flash('Horario actualizado correctamente.', 'success')
        return redirect(url_for('listar_horarios'))  # Redirige a la lista de horarios

    return render_template('horarios/editar_horario.html', horario=horario, dias=dias)  # Renderiza la plantilla

# Ruta para eliminar un horario
@app.route('/horarios/eliminar/<int:horario_id>', methods=['POST'])
@login_required  # Requiere login
def eliminar_horario(horario_id):
    horario = Horario.query.get_or_404(horario_id)  # Obtiene el horario o devuelve 404

    # Verificar si existen trabajadores asociados al horario
    if Trabajador.query.filter_by(idHorario=horario.id_horario).count() > 0:
        flash('No se puede eliminar el horario porque existen trabajadores asociados a él.', 'danger')
        return redirect(url_for('listar_horarios'))

    # Si no hay trabajadores asociados, eliminar las franjas horarias y luego el horario
    FranjaHoraria.query.filter_by(id_horario=horario.id_horario).delete() #Elimina franjas horarias asociadas
    db.session.delete(horario)  # Elimina el horario
    db.session.commit()
    flash('Horario eliminado correctamente.', 'success')
    return redirect(url_for('listar_horarios'))  # Redirige a la lista de horarios

# Ruta para listar los empleados
@app.route('/empleados')
@login_required  # Requiere login
def listar_empleados():
    empleados = Trabajador.query.all()  # Obtiene todos los empleados
    return render_template('empleados/listar_empleados.html', empleados=empleados)  # Renderiza la plantilla

# Ruta para crear un nuevo empleado
@app.route('/empleados/crear', methods=['GET', 'POST'])
@login_required  # Requiere login
def crear_empleado():
    horarios = Horario.query.all()  # Obtiene todos los horarios, roles y empresas
    roles = Rol.query.all()
    empresas = Empresa.query.all()

    if request.method == 'POST':  # Si se envía el formulario
        nif = request.form['nif']  # Obtiene la información del formulario
        nombre = request.form['nombre']
        email = request.form['email']
        telef = request.form['telef']
        passwd = request.form['passwd']
        idEmpresa = int(request.form['idEmpresa'])
        idHorario = int(request.form['idHorario'])
        idRol = int(request.form['idRol'])

        if not nif or not nombre or not passwd:  # Valida los campos obligatorios
            flash('NIF, Nombre y Contraseña son campos obligatorios.', 'danger')
            return render_template('empleados/crear_empleado.html', horarios=horarios, roles=roles, empresas=empresas)

        existing_employee_nif = Trabajador.query.filter_by(nif=nif).first()  # Valida que no exista el NIF
        if existing_employee_nif:
            flash('Ya existe un empleado con este NIF.', 'danger')
            return render_template('empleados/crear_empleado.html', horarios=horarios, roles=roles, empresas=empresas)

        if email: #valida que no exista el email
            existing_employee_email = Trabajador.query.filter_by(email=email).first()
            if existing_employee_email:
                flash('Ya existe un empleado con este email.', 'danger')
                return render_template('empleados/crear_empleado.html', horarios=horarios, roles=roles, empresas=empresas)

        nuevo_empleado = Trabajador(nif=nif, nombre=nombre, email=email, telef=telef, idEmpresa=idEmpresa, idHorario=idHorario, idRol=idRol)  # Crea el nuevo empleado
        nuevo_empleado.set_password(passwd)  # Hashea la contraseña
        db.session.add(nuevo_empleado)
        db.session.commit()

        flash('Empleado creado correctamente.', 'success')
        return redirect(url_for('listar_empleados'))  # Redirige a la lista de empleados

    return render_template('empleados/crear_empleado.html', horarios=horarios, roles=roles, empresas=empresas)  # Renderiza la plantilla

# Ruta para editar un empleado existente
@app.route('/empleados/editar/<int:empleado_id>', methods=['GET', 'POST'])
@login_required  # Requiere login
def editar_empleado(empleado_id):
    empleado = Trabajador.query.get_or_404(empleado_id)  # Obtiene el empleado o devuelve 404
    horarios = Horario.query.all()  # Obtiene todos los horarios, roles y empresas
    roles = Rol.query.all()
    empresas = Empresa.query.all()

    if request.method == 'POST':  # Si se envía el formulario
        nif = request.form['nif']  # Obtiene la información del formulario
        nombre = request.form['nombre']
        email = request.form['email']
        telef = request.form['telef']
        idEmpresa = int(request.form['idEmpresa'])
        idHorario = int(request.form['idHorario'])
        idRol = int(request.form['idRol'])

        if not nif or not nombre:  # Valida los campos obligatorios
            flash('NIF y Nombre son campos obligatorios.', 'danger')
            return render_template('empleados/editar_empleado.html', empleado=empleado, horarios=horarios, roles=roles, empresas=empresas)

        existing_employee_nif = Trabajador.query.filter(Trabajador.nif == nif, Trabajador.id_trabajador != empleado.id_trabajador).first()  # Valida que no exista el NIF (excepto el actual)
        if existing_employee_nif:
            flash('Ya existe un empleado con este NIF.', 'danger')
            return render_template('empleados/editar_empleado.html', empleado=empleado, horarios=horarios, roles=roles, empresas=empresas)

        if email: #valida que no exista el email
            existing_employee_email = Trabajador.query.filter(Trabajador.email == email, Trabajador.id_trabajador != empleado.id_trabajador).first()
            if existing_employee_email:
                flash('Ya existe un empleado con este email.', 'danger')
                return render_template('empleados/editar_empleado.html', empleado=empleado, horarios=horarios, roles=roles, empresas=empresas)

        empleado.nif = nif  # Actualiza la información del empleado
        empleado.nombre = nombre
        empleado.email = email
        empleado.telef = telef
        empleado.idEmpresa = idEmpresa
        empleado.idHorario = idHorario
        empleado.idRol = idRol

        new_password = request.form.get('new_password')  # Cambia la contraseña solo si se proporciona una nueva
        if new_password:
            empleado.set_password(new_password)

        db.session.commit()  # Guarda los cambios
        flash('Empleado actualizado correctamente.', 'success')
        return redirect(url_for('listar_empleados'))  # Redirige a la lista de empleados

    return render_template('empleados/editar_empleado.html', empleado=empleado, horarios=horarios, roles=roles, empresas=empresas)  # Renderiza la plantilla

# Ruta para eliminar un empleado
@app.route('/empleados/eliminar/<int:empleado_id>', methods=['POST'])
@login_required  # Requiere login
def eliminar_empleado(empleado_id):
    empleado = Trabajador.query.get_or_404(empleado_id)  # Obtiene el empleado o devuelve 404

    if Registro.query.filter_by(id_trabajador=empleado.id_trabajador).count() > 0: #Verifica si existen registros asociados
        flash('No se puede eliminar el trabajador porque existen registros de presencia asociados a él.', 'danger')
        return redirect(url_for('listar_empleados'))

    if Incidencia.query.filter_by(id_trabajador=empleado.id_trabajador).count() > 0: #Verifica si existen incidencias asociadas
        flash('No se puede eliminar el trabajador porque existen incidencias asociadas a él.', 'danger')
        return redirect(url_for('listar_empleados'))

    db.session.delete(empleado)  # Elimina el empleado
    db.session.commit()
    flash('Empleado eliminado correctamente.', 'success')
    return redirect(url_for('listar_empleados'))  # Redirige a la lista de empleados

# Ruta para listar los registros de presencia
@app.route('/listar_registros', methods=['GET', 'POST'])
@login_required  # Requiere login
def listar_registros():
    fecha_str = request.args.get('fecha')  # Obtiene la fecha del request
    if fecha_str: #si hay fecha
        try:
            fecha = datetime.datetime.strptime(fecha_str, '%Y-%m-%d').date()  # Convierte la fecha a objeto date
        except ValueError: #si el formato no es correcto
            flash('Formato de fecha incorrecto. Use AAAA-MM-DD.', 'danger')
            fecha = datetime.date.today() #establece fecha actual
    else:
        fecha = datetime.date.today() #establece fecha actual

    registros = Registro.query.filter(db.func.date(Registro.fecha) == fecha).all()  # Obtiene los registros para la fecha

    registro_en_horario = {} #diccionario para ver si el registro esta en horario o no
    for registro in registros:  # Itera sobre los registros
        trabajador = registro.trabajador #obtiene trabajador, horario y dia de la semana
        horario = trabajador.horario
        dia_semana = fecha.weekday()  # 0: Lunes, 1: Martes, ..., 6: Domingo

        franja = FranjaHoraria.query.filter_by(id_horario=horario.id_horario, id_dia=dia_semana + 1).first() #busca franja horaria

        if franja: #si hay franja horaria
            hora_entrada_horario = franja.hora_entrada #obtiene hora de entrada y salida del horario
            hora_salida_horario = franja.hora_salida

            hora_entrada_registro = registro.hora_entrada.time() if registro.hora_entrada else None #obtiene hora de entrada y salida del registro
            hora_salida_registro = registro.hora_salida.time() if registro.hora_salida else None

            dentro_horario_entrada = hora_entrada_registro and hora_entrada_horario <= hora_entrada_registro <= hora_salida_horario #verifica si esta dentro de horario
            dentro_horario_salida = hora_salida_registro and hora_entrada_horario <= hora_salida_registro <= hora_salida_horario

            registro_en_horario[registro.id_registro] = dentro_horario_entrada and dentro_horario_salida #establece si esta en horario o no
        else:
            registro_en_horario[registro.id_registro] = False #si no hay franja horaria, no esta en horario

    return render_template('registros/listar_registros.html', registros=registros, fecha=fecha, registro_en_horario=registro_en_horario)  # Renderiza la plantilla








