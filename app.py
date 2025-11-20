from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_cors import CORS # Si no tienes esto instalado, pip install flask-cors
import db
import logic

app = Flask(__name__)
app.secret_key = 'super_secreto_crecermas_v2' # Clave para sesiones
CORS(app) # Permite peticiones cruzadas si fuera necesario

# ------------------------------------------------------
# 1. RUTAS DE VISTAS (Renderizan HTML)
# ------------------------------------------------------

@app.route('/')
def home():
    # Pasamos las carreras para mostrarlas en la sección "Oferta Académica"
    return render_template('index.html', carreras=db.carreras)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']
        
        # Autenticación Simulada (MOCK)
        if user == 'admin' and pwd == 'admin123':
            session['user'] = 'admin'
            session['nombre'] = 'Sebastián Bravo' # Director TI
            return redirect(url_for('admin_dashboard'))
            
        elif user == 'alumno' and pwd == 'alumno123':
            session['user'] = 'alumno'
            session['nombre'] = 'Juan Pérez' # Alumno Demo
            return redirect(url_for('student_dashboard'))
            
        else:
            flash('Credenciales incorrectas. Prueba: admin/admin123 o alumno/alumno123', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/admin/dashboard')
def admin_dashboard():
    # Protección de ruta
    if 'user' not in session or session['user'] != 'admin':
        flash('Acceso no autorizado. Inicia sesión como administrador.', 'warning')
        return redirect(url_for('login'))
        
    # Inyectamos TODOS los datos necesarios para dashboard_admin.html
    return render_template('dashboard_admin.html', 
                           carreras=db.carreras, 
                           kpis=db.kpis_admin, 
                           proyectos=db.proyectos_gestion) # ¡Aquí enviamos los proyectos!

@app.route('/campus')
def student_dashboard():
    # Protección de ruta
    if 'user' not in session:
        return redirect(url_for('login'))
    
    # Inyectamos los cursos para campus_virtual.html
    return render_template('campus_virtual.html', cursos=db.campus_cursos)

# ------------------------------------------------------
# 2. RUTAS DE FUNCIONALIDAD (Crear, Borrar - Simuladas)
# ------------------------------------------------------

@app.route('/admin/crear_carrera', methods=['POST'])
def crear_carrera():
    if session.get('user') == 'admin':
        # Lógica simple para agregar a la lista en memoria
        nueva_carrera = {
            "id": len(db.carreras) + 1,
            "nombre": request.form['nombre'],
            "duracion": request.form['duracion'],
            "jornada": request.form['jornada'],
            "alumnos": 0
        }
        db.carreras.append(nueva_carrera)
        flash('Carrera creada exitosamente.', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/borrar/<int:id>')
def borrar_carrera(id):
    if session.get('user') == 'admin':
        # Filtramos la lista para quitar el ID seleccionado
        db.carreras = [c for c in db.carreras if c['id'] != id]
        flash('Carrera eliminada.', 'warning')
    return redirect(url_for('admin_dashboard'))

# ------------------------------------------------------
# 3. API ENDPOINTS (Para el JavaScript asíncrono)
# ------------------------------------------------------

@app.route('/api/crm/leads', methods=['GET'])
def get_leads():
    return jsonify(db.crm_leads)

@app.route('/api/crm/nuevo', methods=['POST'])
def nuevo_lead():
    data = request.json
    nuevo = {
        "id": len(db.crm_leads) + 100,
        "nombre": data['nombre'],
        "estado": "NUEVO",
        "canal": data['canal']
    }
    db.crm_leads.append(nuevo)
    return jsonify({"mensaje": "Guardado", "lead": nuevo}), 201

@app.route('/api/sigaa/alumnos', methods=['GET'])
def get_sigaa():
    return jsonify(db.sigaa_alumnos)

@app.route('/api/campus/cursos', methods=['GET'])
def get_cursos():
    return jsonify(db.campus_cursos)

@app.route('/api/alerta/dashboard', methods=['GET'])
def get_alertas():
    # Aquí podríamos usar logic.py si quisiéramos recalcular en tiempo real
    # Por ahora devolvemos los datos fijos de db.py
    return jsonify(db.alerta_riesgos)

# ------------------------------------------------------
# INICIO DE LA APP
# ------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True, port=5000)