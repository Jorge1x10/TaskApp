from flask import Request, render_template, url_for, flash, redirect, request, current_app
from flask_login import login_user, current_user, logout_user, login_required 
from threading import Thread
from sqlalchemy.sql.functions import user
from wtforms import form
from taskapp import app, db, bcrypt, mail
from flask_mail import Message
from taskapp.forms import RegistrationForm, LoginForm, TaskForm, ProjectForm, RequestResetForm, ResetPasswordForm
from taskapp.models import User, Task, Project



@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    task_form = TaskForm()
    project_form = ProjectForm()

    if task_form.validate_on_submit():
        # Aquí está la corrección: añadimos el proyecto seleccionado al crear la tarea.
        task = Task(title=task_form.title.data, 
                    description=task_form.description.data, 
                    deadline=task_form.deadline.data, 
                    project=task_form.project.data,  # <-- LÍNEA CLAVE
                    author=current_user)
        db.session.add(task)
        db.session.commit()
        flash('Task saved successfully!', 'success')
        return redirect(url_for('home'))

    
    # Tareas para la vista principal (sin filtrar por proyecto)
    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.date_created.desc()).all()    
    # Obtiene solo las 3 tareas más recientes para las tarjetas
    card_tasks = Task.query.filter_by(user_id=current_user.id, completed=False).order_by(Task.date_created.desc()).limit(3).all()
    # Obtiene los proyectos del Usuario
    projects = Project.query.filter_by(user_id=current_user.id).all()
    # Obtiene TODAS las tareas pendientes para la barra lateral "Recent"
    recent_tasks = Task.query.filter_by(user_id=current_user.id, completed=False).order_by(Task.date_created.desc()).all()
    recent_task_mobile = Task.query.filter_by(user_id=current_user.id, completed=False).order_by(Task.date_created.desc()).limit(2).all()
    #Proyetos NO completados por el usuario
    incomplete_projects = Project.query.filter_by(user_id=current_user.id, completed=False).all()

    return render_template('home.html', task_form=task_form, project_form=project_form, tasks=tasks, 
                            all_tasks=tasks, card_tasks=card_tasks, projects=projects, recent_tasks=recent_tasks, 
                            incomplete_projects=incomplete_projects, recent_task_mobile=recent_task_mobile)



@app.route('/')
@app.route('/index', )
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            user.firstTimeUser = False
            db.session.commit()
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw, firstTimeUser=True)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}, Try Login in.', 'success')
        return redirect(url_for('login'))
    else:
        flash(f"Theres has been an error, try again.", "danger")
    return render_template('register.html', title='Register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/task/<int:task_id>/complete', methods=['POST'])
@login_required
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        flash('You do not have permission to modify this task.', 'danger')
        return redirect(url_for('home'))
    
    task.completed = not task.completed
    db.session.commit()

    if task.project:
        if task.project.progress == 100:
            task.project.completed = True
        else:
            task.project.completed = False
        db.session.commit() # Guardamos el cambio en el proyecto

    if task.completed:
        flash('Task marked as complete!', 'success')
    else:
        flash('Task marked as incomplete!', 'success')
    
    return redirect(request.referrer)

@app.route('/task/<int:task_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        flash('You do not have permission to edit this task.', 'danger')
        return redirect(url_for('home'))
    
    # Usamos instance=task para que el formulario se cargue con los datos de la tarea
    form = TaskForm(obj=task)

    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.deadline = form.deadline.data
        task.project = form.project.data # Asegurarse de actualizar el proyecto también
        db.session.commit()
        flash('Task updated successfully!', 'success')
        # Después de editar, siempre redirigimos a la página principal.
        return redirect(url_for('home'))
    # El método GET no es necesario para esta ruta, ya que el formulario se llena con JS.
    # Pero si se accediera directamente, redirigimos para evitar errores.
    return redirect(url_for('home'))


@app.route('/task/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        flash('You do not have permission to delete this task.', 'danger')
        return redirect(url_for('home'))
    
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('home'))

@app.route('/project/new', methods=['GET', 'POST'])
@login_required
def new_project():
    form = ProjectForm() # Aquí 'form' está bien porque es la única variable de formulario en esta ruta.
    # El formulario de creación de proyectos se envía a esta ruta.
    if form.validate_on_submit():
        project = Project(name=form.name.data, deadline=form.deadline.data, user_id=current_user.id)
        db.session.add(project)
        db.session.commit()
        flash('Project created successfully!', 'success')
    # Después de procesar, redirigimos a home para evitar reenvíos del formulario.
    return redirect(url_for('home'))

def send_async_email(app, msg):
    """Función para enviar correo en un hilo separado."""
    with app.app_context():
        mail.send(msg)

def send_reset_email(user):
    """Función auxiliar para enviar el correo."""
    token = user.get_reset_token()
    msg = Message('Solicitud de Reseteo de Contraseña',
                  sender=app.config.get('MAIL_DEFAULT_SENDER') or 'noreply@demo.com',  # ✅ Usar config
                  recipients=[user.email])
    msg.body = f'''Para restablecer tu contraseña, visita el siguiente enlace (el enlace expira en 30 minutos):
{url_for('reset_password', token=token, _external=True)}

Si no solicitaste este cambio, simplemente ignora este correo y no se realizará ningún cambio.
'''
    # Inicia un hilo para enviar el correo en segundo plano
    # Pasamos 'current_app._get_current_object()' para evitar problemas de contexto de la aplicación en el hilo
    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()

@app.route('/resetRequest', methods=['GET', 'POST'])
def reset_Request():
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_email(user)
            flash('Se ha enviado el correo de recuperacion.', 'info')
        return redirect(url_for('login'))

    return render_template('resetRequest.html', form=form)

@app.route('/resetPassword/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.verify_reset_token(token)
    if user is None:
        flash('Invalid token', 'danger')
        return redirect(url_for('reset_Request'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated succesfully', 'success')
        return redirect(url_for('login'))

    return render_template('resetPassword.html', form=form)

@app.route('/project/<int:project_id>', methods=['GET', 'POST'])  # ✅ Agregar methods=['GET', 'POST'] al decorador
@login_required
def view_project(project_id):  # ✅ Remover methods de los parámetros de la función
    task_form = TaskForm()
    project_form = ProjectForm()
    project_list = Project.query.filter_by(user_id=current_user.id, completed=False).all()
    project = Project.query.get_or_404(project_id)
    if project.user_id != current_user.id:
        flash('You do not have permission to view this project.', 'danger')
        return redirect(url_for('home'))

    # ✅ Agregar lógica para manejar el envío del formulario de tareas
    if task_form.validate_on_submit():
        task = Task(title=task_form.title.data, 
                    description=task_form.description.data, 
                    deadline=task_form.deadline.data, 
                    project=task_form.project.data or project,  # Si no se selecciona proyecto, usar el actual
                    author=current_user)
        db.session.add(task)
        db.session.commit()
        flash('Task saved successfully!', 'success')
        return redirect(url_for('view_project', project_id=project_id))

    tasks_in_project = Task.query.filter_by(project_id=project_id).order_by(Task.date_created.desc()).all()
    all_tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.date_created.desc()).all()
    recent_tasks = Task.query.filter_by(user_id=current_user.id, completed=False).order_by(Task.date_created.desc()).all()

    return render_template('home.html', all_tasks=all_tasks, project=project, project_list=project_list, tasks=tasks_in_project, task_form=task_form,  # ✅ Usar task_form en lugar de TaskForm()
                            project_form=project_form, projects=Project.query.filter_by(user_id=current_user.id).all(), recent_tasks=recent_tasks)


@app.route('/project/<int:project_id>/complete', methods=['POST'])
@login_required
def complete_project_route(project_id):
    project = Project.query.get_or_404(project_id)
    if project.user_id != current_user.id:
        flash('You do not have permission to modify this project.', 'danger')
        return redirect(url_for('home')) 

    project.completed = not project.completed
    db.session.commit()
    if project.completed:
        flash('Project marked as complete!', 'success')
    else:
        flash('Project marked as incomplete!', 'success')
    return redirect(url_for('view_project', project_id=project.id))


@app.route('/project/<int:project_id>/delete', methods=['POST'])
@login_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    if project.user_id != current_user.id:
        flash('You do not have permission to delete this project.', 'danger')
        return redirect(url_for('home'))
    
    for task in project.tasks:
        db.session.delete(task)
        
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('home'))