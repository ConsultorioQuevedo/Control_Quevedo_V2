import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# 1. CONFIGURACIÓN DE PESTAÑA E ICONO (Favicon)
# Asegúrese de que 'icono_q.png' esté subido en GitHub junto a este archivo
st.set_page_config(
    page_title="Control Quevedo PRO", 
    page_icon="icono_q.png", 
    layout="wide"
)

# --- BASE DE DATOS LOCAL ---
def conectar_db():
    return sqlite3.connect('nexus_local.db', check_same_thread=False)

def crear_tablas():
    with conectar_db() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS glucosa 
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, fecha TEXT, nivel INTEGER, momento TEXT, nota TEXT)""")
        conn.execute("""CREATE TABLE IF NOT EXISTS salud 
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, fecha TEXT, tipo TEXT, especialidad TEXT, doctor TEXT)""")
        conn.execute("""CREATE TABLE IF NOT EXISTS finanzas 
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, fecha TEXT, tipo TEXT, monto REAL, detalle TEXT)""")

crear_tablas()

# --- DISEÑO VISUAL PERSONALIZADO ---
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #f4f7f9; }
    .header-quevedo {
        background: linear-gradient(90deg, #00adef 0%, #007bbd 100%);
        padding: 40px; border-radius: 0 0 35px 35px;
        color: white; margin-top: -75px; text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .card {
        background-color: white; padding: 20px;
        border-radius: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 20px; border: 1px solid #e1e4e8;
    }
    div.stButton > button { border-radius: 15px; font-weight: bold; }
    .btn-rojo button { background-color: #ff5e5e !important; color: white !important; height: 85px; font-size: 18px; }
    .btn-azul button { background-color: #4cd3e1 !important; color: white !important; height: 85px; font-size: 18px; }
    .btn-naranja button { background-color: #ffb37e !important; color: white !important; height: 85px; font-size: 18px; }
    </style>
    """, unsafe_allow_html=True)

# LÓGICA DE NAVEGACIÓN
if 'pagina' not in st.session_state: st.session_state.pagina = "🏠 Inicio"

def navegar(p):
    st.session_state.pagina = p
    st.rerun()

# --- BARRA LATERAL (SIDEBAR) CON LOGO ---
with st.sidebar:
    try:
        st.image("icono_q.png", width=150)
    except:
        st.title("QUEVEDO PRO")
    
    st.markdown("---")
    if st.button("🏠 Ir al Menú Principal", use_container_width=True): navegar("🏠 Inicio")
    st.caption(f"Actualizado: {datetime.now().strftime('%d/%m/%Y')}")

# --- PÁGINA INICIO ---
if st.session_state.pagina == "🏠 Inicio":
    st.markdown(f'<div class="header-quevedo"><h1>¡Buen día, Luis Rafael!</h1><p>{datetime.now().strftime("%A, %d de %B")}</p></div>', unsafe_allow_html=True)
    
    st.write("## 🚀 Acceso Directo")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown('<div class="btn-azul">', unsafe_allow_html=True)
        if st.button("🩸\nGLUCOSA", use_container_width=True): navegar("🩸 Glucosa")
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="btn-rojo">', unsafe_allow_html=True)
        if st.button("🏥\nSALUD / CITAS", use_container_width=True): navegar("🏥 Salud")
        st.markdown('</div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="btn-naranja">', unsafe_allow_html=True)
        if st.button("💰\nFINANZAS", use_container_width=True): navegar("💰 Finanzas")
        st.markdown('</div>', unsafe_allow_html=True)

# --- MÓDULO GLUCOSA ---
elif st.session_state.pagina == "🩸 Glucosa":
    st.title("🩺 Control de Glucosa")
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        with st.form("f_g", clear_on_submit=True):
            col1, col2 = st.columns(2)
            f = col1.date_input("Fecha", datetime.now())
            n = col2.number_input("Nivel (mg/dL)", min_value=0)
            m = col1.selectbox("Momento", ["Ayunas", "Antes de Comer", "Después de Comer", "Noche"])
            nt = col2.text_input("Nota")
            if st.form_submit_button("💾 GUARDAR REGISTRO"):
                with conectar_db() as conn:
                    conn.execute("INSERT INTO glucosa (fecha, nivel, momento, nota) VALUES (?,?,?,?)", (str(f), n, m, nt))
                st.success("Guardado localmente"); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    df = pd.read_sql_query("SELECT * FROM glucosa ORDER BY id DESC LIMIT 15", conectar_db())
    if not df.empty:
        st.write("### 📝 Historial Reciente")
        st.dataframe(df[['fecha', 'nivel', 'momento', 'nota']], use_container_width=True)
        if st.button("🗑️ Borrar último registro"):
            with conectar_db() as conn:
                conn.execute("DELETE FROM glucosa WHERE id = (SELECT MAX(id) FROM glucosa)")
            st.rerun()

# --- MÓDULO SALUD ---
elif st.session_state.pagina == "🏥 Salud":
    st.title("🏥 Salud y Citas")
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        with st.form("f_s", clear_on_submit=True):
            f = st.date_input("Fecha", datetime.now())
            t = st.selectbox("Tipo", ["Cita Médica", "Examen", "Medicina"])
            esp = st.text_input("Especialidad / Detalle")
            doc = st.text_input("Doctor / Clínica")
            if st.form_submit_button("💾 AGENDAR"):
                with conectar_db() as conn:
                    conn.execute("INSERT INTO salud (fecha, tipo, especialidad, doctor) VALUES (?,?,?,?)", (str(f), t, esp, doc))
                st.success("Cita guardada"); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    df = pd.read_sql_query("SELECT * FROM salud ORDER BY id DESC LIMIT 15", conectar_db())
    if not df.empty:
        st.dataframe(df[['fecha', 'tipo', 'especialidad', 'doctor']], use_container_width=True)
        if st.button("🗑️ Borrar última cita"):
            with conectar_db() as conn:
                conn.execute("DELETE FROM salud WHERE id = (SELECT MAX(id) FROM salud)")
            st.rerun()

# --- MÓDULO FINANZAS ---
elif st.session_state.pagina == "💰 Finanzas":
    st.title("💰 Mis Finanzas")
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        with st.form("f_f", clear_on_submit=True):
            f = st.date_input("Fecha", datetime.now())
            t = st.selectbox("Tipo", ["Gasto", "Ingreso"])
            mon = st.number_input("Monto ($)", min_value=0.0)
            det = st.text_input("Detalle")
            if st.form_submit_button("💾 REGISTRAR"):
                with conectar_db() as conn:
                    conn.execute("INSERT INTO finanzas (fecha, tipo, monto, detalle) VALUES (?,?,?,?)", (str(f), t, mon, det))
                st.success("Registro guardado"); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    df = pd.read_sql_query("SELECT * FROM finanzas ORDER BY id DESC LIMIT 15", conectar_db())
    if not df.empty:
        st.dataframe(df[['fecha', 'tipo', 'monto', 'detalle']], use_container_width=True)
        if st.button("🗑️ Borrar último movimiento"):
            with conectar_db() as conn:
                conn.execute("DELETE FROM finanzas WHERE id = (SELECT MAX(id) FROM finanzas)")
            st.rerun()

# --- 🖋️ PIE DE PÁGINA Y FIRMA ---
st.markdown("---")
f1, f2 = st.columns(2)
with f1:
    st.markdown(f"""
    **SISTEMA DE GESTIÓN PERSONAL**  
    *Arquitectura de Datos:* **Luis Rafael Quevedo** 🇩🇴  
    *Ubicación:* Almacenamiento Local (PC)
    """)
with f2:
    st.markdown("""
    **COLABORACIÓN TÉCNICA:**  
    *Diseño de Interfaz:* **Gemini AI**  
    *Versión:* 2.0 (Estilo Premium)
    """)
st.caption(f"© {datetime.now().year} Control Quevedo Pro - Todos los derechos reservados.")
