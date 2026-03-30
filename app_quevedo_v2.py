import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
import plotly.express as px

# 1. CONFIGURACIÓN E IDENTIDAD (Icono y Título)
st.set_page_config(page_title="Control Quevedo PRO", page_icon="./icono_q.png", layout="wide")

# --- DISEÑO PERSONALIZADO (EL "TRAJE" DE LA APP) ---
st.markdown("""
    <style>
    /* Fondo general y fuentes */
    [data-testid="stAppViewContainer"] {
        background-color: #f8f9fa;
    }
    
    /* Encabezado azul tipo Humano Seguros */
    .header-quevedo {
        background: linear-gradient(90deg, #00adef 0%, #007bbd 100%);
        padding: 40px 20px;
        border-radius: 0px 0px 30px 30px;
        color: white;
        margin-top: -60px;
        margin-bottom: 25px;
    }
    
    /* Tarjetas blancas redondeadas */
    .card-quevedo {
        background-color: white;
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        border: 1px solid #eee;
    }

    /* Botones de colores estilo la foto */
    div.stButton > button {
        border-radius: 15px;
        height: 100px;
        font-weight: bold;
        font-size: 18px;
        border: none;
        transition: 0.3s;
    }
    
    /* Colores específicos para botones */
    .btn-salud button { background-color: #ff5e5e !important; color: white !important; }
    .btn-glucosa button { background-color: #4cd3e1 !important; color: white !important; }
    .btn-finanzas button { background-color: #ffb37e !important; color: white !important; }
    
    </style>
    """, unsafe_allow_html=True)

# URL de su Excel
URL_EXCEL = "https://docs.google.com/spreadsheets/d/12DvNKDet5BRoYWlytg2qjWsm3IHPedkThHaopQKfwfY/edit?usp=sharing"

# Conexión con Google Sheets
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except:
    st.error("Error de conexión. Verifique su archivo secrets.toml.")

# Lógica de Navegación
if 'pagina' not in st.session_state:
    st.session_state.pagina = "🏠 Inicio"

def navegar(nombre_pagina):
    st.session_state.pagina = nombre_pagina

# --- BARRA LATERAL ---
with st.sidebar:
    try:
        st.image("icono_q.png", width=120)
    except:
        st.write("✨ **NEXUS QUEVEDO**")
    
    st.title("Navegación")
    if st.button("🏠 Inicio", use_container_width=True): navegar("🏠 Inicio")
    st.divider()
    st.caption(f"Sesión: Luis Rafael Quevedo\n{datetime.now().strftime('%d/%m/%Y')}")

# --- PÁGINA: INICIO (LA PORTADA) ---
if st.session_state.pagina == "🏠 Inicio":
    # Encabezado con saludo
    st.markdown(f"""
        <div class="header-quevedo">
            <h1 style='margin:0;'>¡Buenos días,</h1>
            <h1 style='margin:0; font-weight: 800;'>Luis Rafael!</h1>
        </div>
    """, unsafe_allow_html=True)

    # Tarjeta de Resumen (Como la de Seguros)
    st.markdown(f"""
        <div class="card-quevedo">
            <h3 style='color:#00adef; margin-top:0;'>🛡️ Resumen de Control</h3>
            <p style='margin:0; color:gray;'><b>IDENTIDAD:</b> LUIS RAFAEL QUEVEDO</p>
            <p style='margin:0; color:gray;'><b>ESTADO:</b> ACTIVO / OPERATIVO</p>
            <p style='margin:0; color:gray;'><b>FECHA:</b> {datetime.now().strftime('%d/%m/%Y')}</p>
        </div>
    """, unsafe_allow_html=True)

    st.subheader("Acciones Rápidas")
    
    # Fila de Botones Grandes y de Colores
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="btn-salud">', unsafe_allow_html=True)
        if st.button("🩸\nGLUCOSA", key="main_g", use_container_width=True): 
            navegar("🩸 Glucosa")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="btn-glucosa">', unsafe_allow_html=True)
        if st.button("🏥\nSALUD", key="main_s", use_container_width=True): 
            navegar("🏥 Salud")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="btn-finanzas">', unsafe_allow_html=True)
        if st.button("💰\nFINANZAS", key="main_f", use_container_width=True): 
            navegar("💰 Finanzas")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Simulación de "Últimas Transacciones" de la imagen
    st.markdown("### Últimos Registros")
    try:
        df_g = conn.read(spreadsheet=URL_EXCEL, worksheet="GLUCOSA").tail(2)
        for i, r in df_g.iterrows():
            st.markdown(f"""
                <div style="background-white; padding:15px; border-radius:15px; border-left: 5px solid #4cd3e1; margin-bottom:10px; background-color:white;">
                    <b>Glucosa:</b> {r['Nivel']} mg/dL <br>
                    <small style="color:gray;">{r['Fecha']} - {r['Momento']}</small>
                </div>
            """, unsafe_allow_html=True)
    except:
        st.write("No hay registros recientes.")

# --- MÓDULO: GLUCOSA (DISEÑO LIMPIO) ---
elif st.session_state.pagina == "🩸 Glucosa":
    st.markdown("<h2 style='color:#00adef;'>🩸 Control de Glucosa</h2>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="card-quevedo">', unsafe_allow_html=True)
        with st.form("form_g", clear_on_submit=True):
            c1, c2 = st.columns(2)
            f = c1.date_input("Fecha", datetime.now())
            h = c1.time_input("Hora", datetime.now().time())
            n = c2.number_input("Nivel (mg/dL)", min_value=0, step=1)
            m = c2.selectbox("Momento", ["Ayunas", "Antes de comer", "Después de comer", "Noche"])
            nota = st.text_input("Nota")
            if st.form_submit_button("GUARDAR EN GOOGLE SHEETS"):
                try:
                    df = conn.read(spreadsheet=URL_EXCEL, worksheet="GLUCOSA")
                    nueva = pd.DataFrame([{"Fecha": str(f), "Hora": str(h), "Nivel": n, "Momento": m, "Nota": nota}])
                    conn.update(spreadsheet=URL_EXCEL, worksheet="GLUCOSA", data=pd.concat([df, nueva], ignore_index=True))
                    st.success("✅ Guardado"); st.rerun()
                except Exception as e: st.error(e)
        st.markdown('</div>', unsafe_allow_html=True)

    # Gráfica estilizada
    try:
        df_g = conn.read(spreadsheet=URL_EXCEL, worksheet="GLUCOSA")
        if not df_g.empty:
            fig = px.line(df_g.tail(15), x="Fecha", y="Nivel", markers=True, color_discrete_sequence=['#00adef'])
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
    except: pass

# (Los otros módulos seguirían la misma estética de 'card-quevedo')
