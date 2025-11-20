// static/js/script.js

const API_URL = '/api';

// --- GESTIÓN DE MODO OSCURO Y UI ---
document.addEventListener('DOMContentLoaded', () => {
    const themeToggleBtn = document.getElementById('theme-toggle');
    
    // 1. Verificar preferencia guardada o preferencia del sistema
    const currentTheme = localStorage.getItem('theme');
    if (currentTheme) {
        document.documentElement.setAttribute('data-theme', currentTheme);
        updateIcon(currentTheme);
    } else {
        // Opcional: Detectar preferencia del sistema operativo si no hay guardado
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            document.documentElement.setAttribute('data-theme', 'dark');
            updateIcon('dark');
        }
    }

    // 2. Evento Click
    if(themeToggleBtn){
        themeToggleBtn.addEventListener('click', () => {
            let theme = document.documentElement.getAttribute('data-theme');
            
            // Lógica de switch simple
            theme = (theme === 'dark') ? 'light' : 'dark';
            
            document.documentElement.setAttribute('data-theme', theme);
            localStorage.setItem('theme', theme); // Persistencia
            updateIcon(theme);
        });
    }
    
    // Cargar vista inicial si es necesaria
    // navTo('home'); // Descomentar si quieres forzar home al inicio
});

function updateIcon(theme) {
    const icon = document.getElementById('theme-icon');
    if(icon) {
        icon.textContent = theme === 'dark' ? 'light_mode' : 'dark_mode';
    }
}

// --- NAVEGACIÓN (SPA Simulada) ---
function navTo(screen) {
    // 1. Ocultar todas las secciones
    // IMPORTANTE: Tus divs en el HTML deben tener la clase "section-content" y IDs tipo "home-section"
    document.querySelectorAll('.section-content').forEach(el => el.classList.add('d-none'));
    
    // 2. Mostrar la sección deseada
    const section = document.getElementById(screen + '-section');
    if(section) {
        section.classList.remove('d-none');
        // Pequeña animación de entrada
        section.classList.add('fade-in'); 
    }

    // 3. Actualizar Navbar activa
    document.querySelectorAll('.nav-link').forEach(el => el.classList.remove('active'));
    const navBtn = document.getElementById('nav-' + screen);
    if(navBtn) navBtn.classList.add('active');

    // 4. Cargas asíncronas de datos (Lazy Loading)
    if(screen === 'sigaa') loadSigaa();
    if(screen === 'campus') loadCampus();
    if(screen === 'alerta') loadAlerta();
    if(screen === 'crm') loadCrm();
}

// --- 1. SIGAA: Certificados y Horario ---
async function loadSigaa() {
    try {
        const res = await fetch(`${API_URL}/sigaa/alumnos`);
        const data = await res.json();
        const alumno = data[0]; // Simulamos el primer alumno

        let html = `
            <div class="card shadow-sm mb-3">
                <div class="card-body p-4">
                    <div class="d-flex align-items-center mb-3">
                        <div class="bg-primary text-white rounded-circle d-flex align-items-center justify-content-center me-3 shadow" style="width:60px;height:60px;font-size:24px;">${alumno.nombre[0]}</div>
                        <div><h5 class="mb-0 fw-bold">${alumno.nombre}</h5><small class="text-muted">${alumno.carrera}</small></div>
                    </div>
                    <div class="d-flex justify-content-between p-3 rounded-3 mb-3 border" style="background-color: var(--bg-body);">
                        <div class="text-center"><span class="d-block fw-bold text-primary fs-5">92%</span><small class="text-muted">Asistencia</small></div>
                        <div class="text-center border-start border-end px-3"><span class="d-block fw-bold text-success fs-5">${alumno.promedio}</span><small class="text-muted">Promedio</small></div>
                        <div class="text-center"><span class="d-block fw-bold fs-5">${alumno.semestre}º</span><small class="text-muted">Semestre</small></div>
                    </div>
                    
                    <div class="d-grid gap-2">
                        <button class="btn btn-outline-primary btn-sm d-flex align-items-center justify-content-center" onclick="descargarCertificado('Alumno Regular')">
                            <span class="material-icons fs-6 me-2">description</span> Certificado Alumno Regular
                        </button>
                        <button class="btn btn-outline-secondary btn-sm d-flex align-items-center justify-content-center" onclick="descargarCertificado('Concentración de Notas')">
                            <span class="material-icons fs-6 me-2">history_edu</span> Concentración de Notas
                        </button>
                    </div>
                </div>
            </div>

            <h6 class="fw-bold text-secondary mb-3 ps-2 border-start border-4 border-primary">HORARIO DE HOY</h6>
            <div class="card border-0 shadow-sm mb-3 p-3">
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <span class="badge bg-info text-dark">08:30 - 10:00</span>
                    <span class="fw-bold">Programación II</span>
                    <small class="text-muted">Lab 4</small>
                </div>
                <div class="d-flex justify-content-between align-items-center">
                    <span class="badge bg-secondary">10:15 - 11:45</span>
                    <span class="fw-bold text-muted">Inglés Técnico</span>
                    <small class="text-muted">Sala 202</small>
                </div>
            </div>

            <h6 class="fw-bold text-secondary mb-2 ps-2 border-start border-4 border-success">NOTAS RECIENTES</h6>`;

        const notas = [{m:"Programación II",n:6.5},{m:"Base de Datos",n:5.8},{m:"Inglés Técnico",n:3.9}];
        notas.forEach(n => {
            const color = n.n >= 4.0 ? 'text-primary' : 'text-danger';
            // Quitamos text-dark
            html += `<div class="card border-0 shadow-sm mb-2"><div class="card-body d-flex justify-content-between py-2 align-items-center"><span class="fw-semibold">${n.m}</span><span class="fw-bold ${color} fs-5">${n.n}</span></div></div>`;
        });
        document.getElementById('sigaa-content').innerHTML = html;
    } catch(e) {
        console.error("Error cargando SIGAA", e);
    }
}

function descargarCertificado(tipo) {
    Swal.fire({
        title: 'Generando Documento',
        text: `Procesando solicitud de ${tipo}...`,
        icon: 'info',
        timer: 2000,
        timerProgressBar: true,
        didOpen: () => { Swal.showLoading() }
    }).then(() => {
        Swal.fire('¡Listo!', `El certificado de ${tipo} se ha descargado correctamente.`, 'success');
    });
}

// --- 2. CAMPUS: Streaming ---
async function loadCampus() {
    try {
        const res = await fetch(`${API_URL}/campus/cursos`);
        const data = await res.json();
        let html = '';
        
        // Array de imágenes de fallback o dinámicas
        const images = [
            'https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=600&q=80', 
            'https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=600&q=80',
            'https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=600&q=80',
            'https://images.unsplash.com/photo-1546410531-bb4caa6b424d?auto=format&fit=crop&w=600&q=80'
        ];

        data.forEach((c, i) => {
            const img = c.imagen ? c.imagen : images[i % images.length];
            html += `
                <div class="card border-0 shadow-sm mb-3 overflow-hidden hover-scale">
                    <div class="video-thumbnail" style="background-image: url('${img}'); height: 150px; background-size: cover; position: relative;">
                        <div class="d-flex align-items-center justify-content-center w-100 h-100" style="background: rgba(0,0,0,0.3);">
                             <span class="material-icons text-white fs-1">play_circle_outline</span>
                        </div>
                    </div>
                    <div class="card-body p-3">
                        <h6 class="fw-bold mb-1">${c.nombre}</h6>
                        <p class="text-muted small mb-2"><i class="material-icons fs-6 align-middle">schedule</i> ${c.proxima_tarea}</p>
                        <div class="progress" style="height: 6px;">
                            <div class="progress-bar bg-success" style="width: ${c.progreso}%"></div>
                        </div>
                        <div class="d-flex justify-content-between mt-2 align-items-center">
                            <small class="text-success fw-bold">${c.progreso}% Completado</small>
                            <button class="btn btn-link btn-sm p-0 text-muted" onclick="Swal.fire('Material Descargado', 'PDF de la unidad guardado.', 'success')"><i class="material-icons">download</i></button>
                        </div>
                    </div>
                </div>`;
        });
        document.getElementById('campus-content').innerHTML = html;
    } catch(e) { console.error("Error Campus", e); }
}

// --- 3. ALERTA: Intervención ---
async function loadAlerta() {
    try {
        const res = await fetch(`${API_URL}/alerta/dashboard`);
        const data = await res.json();
        let html = '';
        data.forEach(a => {
            let color = a.riesgo==='ALTO'?'danger':(a.riesgo==='MEDIO'?'warning':'success');
            let factor = a.riesgo==='ALTO' ? 'Baja Asistencia Crítica' : (a.riesgo==='MEDIO' ? 'Notas bajo el promedio' : 'Sin riesgo aparente');
            
            html += `
                <div class="card border-0 shadow-sm mb-3 border-start border-4 border-${color}">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-start">
                            <div>
                                <h6 class="fw-bold mb-0">${a.nombre}</h6>
                                <span class="badge bg-${color} bg-opacity-10 text-${color} border border-${color} mt-1 mb-2">Factor: ${factor}</span>
                                <small class="d-block text-muted">Asistencia: <b>${a.asistencia}%</b> | IA Score: <b>${a.score}</b></small>
                            </div>
                            <div class="text-center">
                                 <span class="material-icons text-${color} fs-2">warning</span>
                                 <small class="d-block fw-bold text-${color}">${a.riesgo}</small>
                            </div>
                        </div>
                        ${a.riesgo !== 'BAJO' ? 
                        `<hr class="my-2 opacity-25">
                        <div class="d-grid">
                            <button class="btn btn-${color} btn-sm text-white fw-bold" onclick="intervenirAlumno('${a.nombre}')">
                                <i class="material-icons align-middle fs-6 me-1">send</i> Intervenir Ahora
                            </button>
                        </div>` : ''}
                    </div>
                </div>`;
        });
        document.getElementById('alerta-content').innerHTML = html;
    } catch(e) { console.error("Error Alerta", e); }
}

function intervenirAlumno(nombre) {
    Swal.fire({
        title: `Intervenir a ${nombre}`,
        text: "¿Qué canal deseas utilizar?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: '📧 Email',
        cancelButtonText: '📱 WhatsApp',
        confirmButtonColor: '#1565C0',
        cancelButtonColor: '#2E7D32'
    }).then((result) => {
        if (result.isConfirmed) Swal.fire('Enviado', `Correo de alerta enviado a ${nombre}`, 'success');
        else if (result.dismiss === Swal.DismissReason.cancel) Swal.fire('Enviado', `Mensaje de WhatsApp enviado a ${nombre}`, 'success');
    });
}

// --- 4. CRM: Pipeline ---
async function loadCrm() {
    try {
        const res = await fetch(`${API_URL}/crm/leads`);
        const data = await res.json();
        let html = '';
        
        if(data.length === 0) html = '<div class="text-center mt-5 text-muted"><i class="material-icons fs-1">inbox</i><p>No hay leads activos</p></div>';
        
        data.forEach(l => {
            let statusColor = l.estado === 'NUEVO' ? 'primary' : (l.estado === 'MATRICULADO' ? 'success' : 'warning');
            let icon = l.canal === 'Instagram' ? 'camera_alt' : 'public';
            
            html += `
                <div class="card border-0 shadow-sm mb-2 hover-card">
                    <div class="card-body d-flex align-items-center p-3">
                        <div class="rounded-3 p-2 me-3 text-center" style="min-width: 50px; background-color: var(--bg-body);">
                            <i class="material-icons text-secondary fs-5">${icon}</i>
                            <small class="d-block text-muted mt-1" style="font-size:9px">${l.canal}</small>
                        </div>
                        <div class="flex-grow-1">
                            <h6 class="fw-bold mb-1">${l.nombre}</h6>
                            <span class="badge bg-${statusColor} bg-opacity-10 text-${statusColor} border border-${statusColor} rounded-pill">${l.estado}</span>
                        </div>
                        <button class="btn btn-custom btn-sm rounded-circle" onclick="Swal.fire('Detalle', 'Viendo ficha de ${l.nombre}', 'info')"><i class="material-icons">chevron_right</i></button>
                    </div>
                </div>`;
        });
        document.getElementById('crm-content').innerHTML = html;
    } catch(e) { console.error("Error CRM", e); }
}

async function guardarLead() {
    const n=document.getElementById('leadName').value; 
    const c=document.getElementById('leadCanal').value;
    
    if(!n) return Swal.fire('Error', 'El nombre es obligatorio', 'error');

    try {
        // Nota: Como no tenemos endpoint real de escritura, simulamos el éxito
        // await fetch(`${API_URL}/crm/nuevo`, ...); 
        
        // Simulamos cierre y recarga
        const modalEl = document.getElementById('leadModal');
        const modal = bootstrap.Modal.getInstance(modalEl);
        modal.hide();
        
        document.getElementById('leadName').value='';
        Swal.fire('Guardado', 'Lead ingresado al Pipeline (Simulación)', 'success');
        loadCrm(); // Recarga para ver cambios (si hubiera backend real)
        
    } catch(e) {
        Swal.fire('Error', 'No se pudo conectar al servidor', 'error');
    }
}

function abrirModalLead() { 
    const modal = new bootstrap.Modal(document.getElementById('leadModal'));
    modal.show(); 
}