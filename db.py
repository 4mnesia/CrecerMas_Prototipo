# db.py

# --- 1. SIGAA (Alumnos) ---
sigaa_alumnos = [
    {
        "id": 1, 
        "nombre": "Juan Pérez", 
        "carrera": "Téc. Conectividad", 
        "semestre": 3, 
        "promedio": 5.8, 
        "asistencia": 92
    },
    {
        "id": 2, 
        "nombre": "Ana Silva", 
        "carrera": "Ing. Informática", 
        "semestre": 5, 
        "promedio": 6.2, 
        "asistencia": 98
    }
]

# --- 2. CRM (Leads de Admisión) ---
crm_leads = [
    {"id": 101, "nombre": "Pedro Pascal", "estado": "NUEVO", "canal": "Instagram"},
    {"id": 102, "nombre": "Gabriela Mistral", "estado": "CONTACTADO", "canal": "Web"},
    {"id": 103, "nombre": "Pablo Neruda", "estado": "MATRICULADO", "canal": "Feria Vocacional"},
    {"id": 104, "nombre": "Isabel Allende", "estado": "SEGUIMIENTO", "canal": "Referido"},
]

# --- 3. ALERTA TEMPRANA (Riesgos Estudiantiles) ---
alerta_riesgos = [
    {"id": 501, "nombre": "Maria González", "riesgo": "ALTO", "score": 85, "asistencia": 45},
    {"id": 502, "nombre": "Carlos Ruiz", "riesgo": "MEDIO", "score": 50, "asistencia": 70},
    {"id": 503, "nombre": "Luis Tapia", "riesgo": "BAJO", "score": 15, "asistencia": 95},
]

# --- 4. CAMPUS VIRTUAL (Cursos del Alumno) ---
campus_cursos = [
    {
        "id": 1, 
        "nombre": "Gestión de Proyectos TI", 
        "progreso": 75, 
        "imagen": "https://images.unsplash.com/photo-1501504905252-473c47e087f8?auto=format&fit=crop&w=500&q=60", 
        "categoria": "Gestión",
        "proxima_tarea": "Entrega Final"
    },
    {
        "id": 2, 
        "nombre": "Programación Python Avanzada", 
        "progreso": 20, 
        "imagen": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=500&q=60", 
        "categoria": "Programación",
        "proxima_tarea": "Quiz Unidad 1"
    },
    {
        "id": 3, 
        "nombre": "Ciberseguridad Básica", 
        "progreso": 0, 
        "imagen": "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=500&q=60", 
        "categoria": "Seguridad",
        "proxima_tarea": "Lectura Cap 1"
    },
    {
        "id": 4, 
        "nombre": "Inglés Técnico II", 
        "progreso": 45, 
        "imagen": "https://images.unsplash.com/photo-1546410531-bb4caa6b424d?auto=format&fit=crop&w=500&q=60", 
        "categoria": "Idiomas",
        "proxima_tarea": "Speaking Test"
    },
]

# --- 5. GESTIÓN ADMIN (Carreras) ---
carreras = [
    {"id": 1, "nombre": "Ingeniería en Informática", "duracion": "8 Semestres", "jornada": "Diurno", "alumnos": 120},
    {"id": 2, "nombre": "Téc. en Ciberseguridad", "duracion": "5 Semestres", "jornada": "Vespertino", "alumnos": 85},
    {"id": 3, "nombre": "Analista Programador", "duracion": "4 Semestres", "jornada": "Online", "alumnos": 200},
]

# --- 6. KPIS ADMIN (Lo que faltaba) ---
kpis_admin = [
    {"titulo": "Matrícula 2026", "valor": "3,450", "delta": "+12%", "color": "success", "icono": "trending_up"},
    {"titulo": "Retención Anual", "valor": "88.5%", "delta": "+2%", "color": "primary", "icono": "people"},
    {"titulo": "Morosidad", "valor": "4.2%", "delta": "-1.5%", "color": "info", "icono": "paid"},
    {"titulo": "Satisfacción", "valor": "4.8/5", "delta": "=", "color": "warning", "icono": "star"}
]

# --- 7. PROYECTOS DE GESTIÓN (¡ESTO ES LO QUE DABA EL ERROR!) ---
# Estos datos vienen de los Excel que subiste (SIGAA, CRM, Alerta, Campus)
proyectos_gestion = [
    {
        "nombre": "SIGAA 2.0 (Gestión Académica)",
        "responsable": "Sebastián Bravo (TI)",
        "estado": "En Desarrollo",
        "avance": 65,
        "presupuesto": "$160 MM",
        "color": "primary" # Azul
    },
    {
        "nombre": "Campus Virtual+ (LMS)",
        "responsable": "Mariela Salazar",
        "estado": "Fase Piloto",
        "avance": 85,
        "presupuesto": "$52.5 MM",
        "color": "success" # Verde
    },
    {
        "nombre": "Sistema Alerta Temprana (IA)",
        "responsable": "Equipo Data Science",
        "estado": "Entrenamiento",
        "avance": 30,
        "presupuesto": "$110 MM",
        "color": "warning" # Amarillo
    },
    {
        "nombre": "CRM Admisión Automatizada",
        "responsable": "Paula Araya",
        "estado": "Go-Live",
        "avance": 95,
        "presupuesto": "$80 MM",
        "color": "danger" # Rojo
    }
]