import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# 1. CONFIGURACIÓN E IDENTIDAD
st.set_page_config(page_title="Control Quevedo LOCAL", page_icon="./icono_q.png", layout="wide")

# --- BASE DE DATOS LOCAL (SQLite) ---
def conectar_db():
    conn = sqlite3.connect('nexus_local.db')
    return conn

def crear_tablas():
    with conectar_db() as conn:
        # Tabla Glucosa
        conn.execute("""CREATE TABLE IF NOT EXISTS glucosa 
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, fecha TEXT, nivel INTEGER, momento TEXT, nota TEXT)""")
        # Tabla Salud/Citas
        conn.execute("""CREATE TABLE IF NOT EXISTS salud 
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, fecha TEXT, tipo TEXT, especialidad TEXT, doctor TEXT)""")
        # Tabla Finanzas
        conn.execute("""CREATE TABLE IF NOT EXISTS finanzas 
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, fecha TEXT, tipo TEXT, monto REAL, detalle TEXT)""")

crear_tablas()

# --- DISEÑO ESTILO "HUMANO SEGUROS" ---
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #f4f7f9; }
    .header-quevedo {
        background: linear-gradient(90deg, #00adef 0%, #007bbd 100%);
        padding: 35px; border-radius: 0 0 35px 35px;
        color: white; margin-top: -75px; text-align: center;
    }
    .card {
        background-color: white; padding: 20px;
        border-radius: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 20px; border: 1px solid #e1e4e8;
    }
    div.stButton > button { border-radius: 15px; font-weight: bold; transition: 0.3s; }
    .btn-rojo button { background-color: #ff5e5e !important; color: white !important; height: 90px; font-size: 20px; }
    .btn-azul button { background-color: #4cd3e1 !important; color: white !important; height: 90px; font-size: 20px; }
    .btn-naranja button { background-color: #ffb37e !important; color: white !important; height: 90px; font-size: 20px; }
    </style>
    """, unsafe_allow_html=True)

# LÓGICA DE NAVEGACIÓN
if 'pagina' not in st.session_state: st.session_state.pagina = "🏠 Inicio"

def navegar(p):
    st.session_state.pagina = p

# --- PÁGINA INICIO ---
if st.session_state.pagina == "🏠 Inicio":
    st.markdown('<div class="header-quevedo"><h1>¡Buen día, Luis Rafael!</h1><p>Sistema Local de Gestión Personal</p></div>', unsafe_allow_html=True)
    
    st.write("## 🚀 Acceso Directo")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown('<div class="btn-azul">', unsafe_allow_html=True)
        if st.button("🩸\nGLUCOSA", use_container_width=True): navegar("🩸 Glucosa"); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="btn-rojo">', unsafe_allow_html=True)
        if st.button("🏥\nSALUD / CITAS", use_container_width=True): navegar("🏥 Salud"); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="btn-naranja">', unsafe_allow_html=True)
        if st.button("💰\nFINANZAS", use_container_width=True): navegar("💰 Finanzas"); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- MÓDULO GLUCOSA ---
elif st.session_state.pagina == "🩸 Glucosa":
    if st.button("⬅️ REGRESAR AL MENÚ"): navegar("🏠 Inicio"); st.rerun()
    st.title("🩺 Control de Glucosa (Local)")
    
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        with st.form("f_g", clear_on_submit=True):
            col1, col2 = st.columns(2)
            f = col1.date_input("Fecha", datetime.now())
            n = col2.number_input("Nivel (mg/dL)", min_value=0)
            m = col1.selectbox("Momento", ["Ayunas", "Antes de Comer", "Después de Comer", "Noche"])
            nt = col2.text_input("Nota")
            if st.form_submit_button("💾 GUARDAR LOCALMENTE"):
                with conectar_db() as conn:
                    conn.execute("INSERT INTO glucosa (fecha, nivel, momento, nota) VALUES (?,?,?,?)", (str(f), n, m, nt))
                st.success("¡Guardado en su PC!"); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    df = pd.read_sql_query("SELECT * FROM glucosa ORDER BY id DESC LIMIT 10", conectar_db())
    if not df.empty:
        st.write("### Últimos Registros")
        st.table(df[['fecha', 'nivel', 'momento', 'nota']])
        if st.button("🗑️ BORRAR ÚLTIMA ENTRADA"):
            with conectar_db() as conn:
                conn.execute("DELETE FROM glucosa WHERE id = (SELECT MAX(id) FROM glucosa)")
            st.rerun()

# --- MÓDULO SALUD / CITAS ---
elif st.session_state.pagina == "🏥 Salud":
    if st.button("⬅️ REGRESAR AL MENÚ"): navegar("🏠 Inicio"); st.rerun()
    st.title("🏥 Salud y Citas")
    
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        with st.form("f_s", clear_on_submit=True):
            f = st.date_input("Fecha", datetime.now())
            t = st.selectbox("Categoría", ["Cita Médica", "Examen", "Medicina"])
            esp = st.text_input("Especialidad / Qué es?")
            doc = st.text_input("Doctor / Institución")
            if st.form_submit_button("💾 AGENDAR"):
                with conectar_db() as conn:
                    conn.execute("INSERT INTO salud (fecha, tipo, especialidad, doctor) VALUES (?,?,?,?)", (str(f), t, esp, doc))
                st.success("Cita agendada localmente"); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    df = pd.read_sql_query("SELECT * FROM salud ORDER BY id DESC LIMIT 10", conectar_db())
    if not df.empty:
        st.table(df[['fecha', 'tipo', 'especialidad', 'doctor']])
        if st.button("🗑️ BORRAR ÚLTIMA CITA"):
            with conectar_db() as conn:
                conn.execute("DELETE FROM salud WHERE id = (SELECT MAX(id) FROM salud)")
            st.rerun()

# --- MÓDULO FINANZAS ---
elif st.session_state.pagina == "💰 Finanzas":
    if st.button("⬅️ REGRESAR AL MENÚ"): navegar("🏠 Inicio"); st.rerun()
    st.title("💰 Mis Finanzas")
    
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        with st.form("f_f", clear_on_submit=True):
            f = st.date_input("Fecha", datetime.now())
            t = st.selectbox("Tipo", ["Gasto", "Ingreso"])
            mon = st.number_input("Monto ($)", min_value=0.0)
            det = st.text_input("Detalle del movimiento")
            if st.form_submit_button("💾 REGISTRAR"):
                with conectar_db() as conn:
                    conn.execute("INSERT INTO finanzas (fecha, tipo, monto, detalle) VALUES (?,?,?,?)", (str(f), t, mon, det))
                st.success("Movimiento guardado"); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    df = pd.read_sql_query("SELECT * FROM finanzas ORDER BY id DESC LIMIT 10", conectar_db())
    if not df.empty:
        st.table(df[['fecha', 'tipo', 'monto', 'detalle']])
        if st.button("🗑️ BORRAR ÚLTIMA FINANZA"):
            with conectar_db() as conn:
                conn.execute("DELETE FROM finanzas WHERE id = (SELECT MAX(id) FROM finanzas)")
            st.rerun()
