from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_cors import CORS 
import db
import logic

app = Flask(__name__)
app.secret_key = 'super_secreto_crecermas_v2'
CORS(app)

# ------------------------------------------------------
# 1. RUTAS PÚBLICAS Y ACCESO
# ------------------------------------------------------

@app.route('/')
def home():
    # Pasamos carreras para la sección de oferta académica en el landing
    return render_template('index.html', carreras=db.carreras)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']
        
        # Autenticación Simulada
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

# ------------------------------------------------------
# 2. PANELES PRINCIPALES (DASHBOARDS)
# ------------------------------------------------------

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'user' not in session or session['user'] != 'admin':
        flash('Acceso no autorizado.', 'warning')
        return redirect(url_for('login'))
        
    # Inyectamos proyectos para que los botones "Gestionar" aparezcan
    return render_template('dashboard_admin.html', 
                           carreras=db.carreras, 
                           kpis=db.kpis_admin, 
                           proyectos=db.proyectos_gestion)

@app.route('/campus')
def student_dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    return render_template('campus_virtual.html', cursos=db.campus_cursos)

# ------------------------------------------------------
# 3. MÓDULOS DE GESTIÓN (CRM, ALERTA, SIGAA)
# ------------------------------------------------------

# --- A. CRM ADMISIÓN ---
@app.route('/crm/dashboard')
def crm_dashboard():
    if 'user' not in session or session['user'] != 'admin':
        return redirect(url_for('login'))
    
    # Filtros para el Kanban
    nuevos = [l for l in db.crm_leads if l['estado'] == 'NUEVO']
    contactados = [l for l in db.crm_leads if l['estado'] in ['CONTACTADO', 'SEGUIMIENTO']]
    matriculados = [l for l in db.crm_leads if l['estado'] == 'MATRICULADO']
    
    return render_template('crm_dashboard.html', 
                           leads_nuevos=nuevos, 
                           leads_contactados=contactados, 
                           leads_matriculados=matriculados)

@app.route('/crm/crear', methods=['POST'])
def crm_crear():
    if session.get('user') == 'admin':
        nuevo_lead = {
            "id": len(db.crm_leads) + 101,
            "nombre": request.form['nombre'],
            "estado": "NUEVO",
            "canal": request.form['canal']
        }
        db.crm_leads.append(nuevo_lead)
        flash('Postulante registrado.', 'success')
    return redirect(url_for('crm_dashboard'))

@app.route('/crm/mover/<int:id>/<nuevo_estado>', methods=['POST'])
def crm_mover(id, nuevo_estado):
    if session.get('user') == 'admin':
        for lead in db.crm_leads:
            if lead['id'] == id:
                lead['estado'] = nuevo_estado
                break
    return redirect(url_for('crm_dashboard'))

# --- B. ALERTA TEMPRANA (CON IA/LOGIC.PY) ---
@app.route('/alerta/dashboard')
def alerta_dashboard():
    if 'user' not in session or session['user'] != 'admin':
        return redirect(url_for('login'))
    
    # 1. Traemos datos de alumnos (simulando conexión a BD)
    alumnos = db.sigaa_alumnos
    reporte = []
    contador_riesgo_alto = 0

    # 2. PROCESAMOS CON LOGIC.PY (IA)
    for a in alumnos:
        # Llamamos a la función del archivo logic.py
        riesgo_ia, score_ia = logic.simular_ia_riesgo(a['asistencia'], a['promedio'])
        
        if riesgo_ia == 'ALTO':
            contador_riesgo_alto += 1
            
        reporte.append({
            "nombre": a['nombre'],
            "asistencia": a['asistencia'],
            "promedio": a['promedio'],
            "riesgo": riesgo_ia, # Dato calculado
            "score": score_ia    # Dato calculado
        })
    
    # Ordenamos: los más riesgosos primero
    reporte.sort(key=lambda x: x['score'], reverse=True)

    return render_template('alerta_dashboard.html', 
                           reporte=reporte, 
                           alumnos_riesgo_alto=contador_riesgo_alto)

# --- C. SIGAA (GESTIÓN ACADÉMICA) ---
@app.route('/sigaa/dashboard')
def sigaa_dashboard():
    if 'user' not in session or session['user'] != 'admin':
        return redirect(url_for('login'))
        
    return render_template('sigaa_dashboard.html', alumnos=db.sigaa_alumnos)

# ------------------------------------------------------
# 4. FUNCIONES EXTRA (CRUD CARRERAS)
# ------------------------------------------------------

@app.route('/admin/crear_carrera', methods=['POST'])
def crear_carrera():
    if session.get('user') == 'admin':
        nueva = {
            "id": len(db.carreras) + 1,
            "nombre": request.form['nombre'],
            "duracion": request.form['duracion'],
            "jornada": request.form['jornada'],
            "alumnos": 0
        }
        db.carreras.append(nueva)
        flash('Carrera creada.', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/borrar/<int:id>')
def borrar_carrera(id):
    if session.get('user') == 'admin':
        db.carreras = [c for c in db.carreras if c['id'] != id]
        flash('Carrera eliminada.', 'warning')
    return redirect(url_for('admin_dashboard'))

# ------------------------------------------------------
# 5. API ENDPOINTS (Para JS asíncrono si se necesita)
# ------------------------------------------------------
@app.route('/api/crm/leads', methods=['GET'])
def get_leads(): return jsonify(db.crm_leads)

@app.route('/api/sigaa/alumnos', methods=['GET'])
def get_sigaa(): return jsonify(db.sigaa_alumnos)

@app.route('/api/campus/cursos', methods=['GET'])
def get_cursos(): return jsonify(db.campus_cursos)

if __name__ == '__main__':
    app.run(debug=True, port=5000)