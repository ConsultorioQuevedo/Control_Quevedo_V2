
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
import plotly.express as px

# 1. CONFIGURACIÓN E IDENTIDAD (Icono y Título)
# El ./ ayuda a que Windows encuentre la imagen en la misma carpeta
st.set_page_config(page_title="Control Quevedo PRO", page_icon="./icono_q.png", layout="wide")

# URL de su Excel (La llave maestra para evitar errores 400)
URL_EXCEL = "https://docs.google.com/spreadsheets/d/12DvNKDet5BRoYWlytg2qjWsm3IHPedkThHaopQKfwfY/edit?usp=sharing"

# Conexión con Google Sheets
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except:
    st.error("Error de conexión. Verifique su archivo secrets.toml.")

# Lógica de Navegación por Sesión
if 'pagina' not in st.session_state:
    st.session_state.pagina = "🏠 Inicio"

def navegar(nombre_pagina):
    st.session_state.pagina = nombre_pagina

# 2. BARRA LATERAL (MENÚ CON ICONO)
with st.sidebar:
    try:
        st.image("icono_q.png", width=120)
    except:
        st.warning("Archivo 'icono_q.png' no encontrado en la carpeta.")
    
    st.title("Menú Principal")
    if st.button("🏠 Inicio", use_container_width=True): navegar("🏠 Inicio")
    if st.button("🩸 CONTROL GLUCOSA", use_container_width=True, type="primary"): navegar("🩸 Glucosa")
    if st.button("💰 FINANZAS", use_container_width=True): navegar("💰 Finanzas")
    if st.button("🏥 SALUD GENERAL", use_container_width=True): navegar("🏥 Salud")
    st.divider()
    st.caption(f"Sr. Quevedo | {datetime.now().strftime('%d/%m/%Y')}")

# 3. LÓGICA DE PÁGINAS

# --- PÁGINA: INICIO ---
if st.session_state.pagina == "🏠 Inicio":
    st.title("🚀 Panel de Control Personal")
    st.write("Bienvenido al sistema. Seleccione una acción rápida:")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("### 🩸 Glucosa\nRegistro y gráficas.")
        if st.button("Abrir Glucosa", key="btn_g"): navegar("🩸 Glucosa"); st.rerun()
    with col2:
        st.success("### 💰 Finanzas\nIngresos y Gastos.")
        if st.button("Abrir Finanzas", key="btn_f"): navegar("💰 Finanzas"); st.rerun()
    with col3:
        st.warning("### 🏥 Salud\nCitas y Medicinas.")
        if st.button("Abrir Salud", key="btn_s"): navegar("🏥 Salud"); st.rerun()

# --- MÓDULO: GLUCOSA ---
elif st.session_state.pagina == "🩸 Glucosa":
    st.title("🩺 Control de Glucosa")
    
    with st.expander("➕ REGISTRAR MEDICIÓN", expanded=True):
        with st.form("form_g", clear_on_submit=True):
            c1, c2, c3 = st.columns(3)
            f = c1.date_input("Fecha", datetime.now())
            h = c1.time_input("Hora", datetime.now().time())
            n = c2.number_input("Nivel (mg/dL)", min_value=0, step=1)
            m = c2.selectbox("Momento", ["Ayunas", "Antes de comer", "Después de comer", "Noche"])
            nota = c3.text_input("Nota")
            if st.form_submit_button("GUARDAR EN GOOGLE SHEETS"):
                try:
                    df = conn.read(spreadsheet=URL_EXCEL, worksheet="GLUCOSA")
                    nueva = pd.DataFrame([{"Fecha": str(f), "Hora": str(h), "Nivel": n, "Momento": m, "Nota": nota}])
                    conn.update(spreadsheet=URL_EXCEL, worksheet="GLUCOSA", data=pd.concat([df, nueva], ignore_index=True))
                    st.success("✅ ¡Medición guardada!"); st.rerun()
                except Exception as e:
                    st.error(f"Error al conectar con Excel: {e}")

    st.subheader("📈 Tendencia Reciente")
    try:
        df_g = conn.read(spreadsheet=URL_EXCEL, worksheet="GLUCOSA")
        if not df_g.empty:
            fig = px.line(df_g.tail(15), x="Fecha", y="Nivel", markers=True, title="Historial de Glucosa")
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(df_g.tail(5), use_container_width=True)
    except:
        st.info("Pestaña GLUCOSA sin datos.")

# --- MÓDULO: FINANZAS ---
elif st.session_state.pagina == "💰 Finanzas":
    st.title("💰 Gestión de Finanzas")
    
    with st.expander("➕ NUEVO MOVIMIENTO", expanded=True):
        with st.form("form_f", clear_on_submit=True):
            c1, c2 = st.columns(2)
            f = c1.date_input("Fecha", datetime.now())
            t = c1.selectbox("Tipo", ["Gasto", "Ingreso"])
            cat = c2.selectbox("Categoría", ["Alimentación", "Salud", "Hogar", "Otros"])
            mon = c2.number_input("Monto ($)", min_value=0.0)
            det = st.text_input("Detalle")
            if st.form_submit_button("REGISTRAR"):
                try:
                    df = conn.read(spreadsheet=URL_EXCEL, worksheet="MOVIMIENTOS")
                    nueva = pd.DataFrame([{"Fecha": str(f), "Tipo": t, "Categoría": cat, "Monto": mon, "Detalle": det}])
                    conn.update(spreadsheet=URL_EXCEL, worksheet="MOVIMIENTOS", data=pd.concat([df, nueva], ignore_index=True))
                    st.balloons(); st.success("Registrado correctamente"); st.rerun()
                except Exception as e:
                    st.error(f"Error en finanzas: {e}")

    try:
        df_f = conn.read(spreadsheet=URL_EXCEL, worksheet="MOVIMIENTOS")
        if not df_f.empty:
            total_gasto = df_f[df_f['Tipo'] == 'Gasto']['Monto'].sum()
            st.metric("Total Gastado Acumulado", f"$ {total_gasto:,.2f}")
            st.dataframe(df_f.tail(10), use_container_width=True)
    except:
        st.info("No hay movimientos financieros.")

# --- MÓDULO: SALUD ---
elif st.session_state.pagina == "🏥 Salud":
    st.title("🏥 Salud General, Citas y Medicinas")
    
    with st.form("form_s", clear_on_submit=True):
        c1, c2 = st.columns(2)
        f = c1.date_input("Fecha", datetime.now())
        t = c1.selectbox("¿Qué registra?", ["Cita Médica", "Medicina", "Examen", "Nota de Salud"])
        esp = c2.text_input("Nombre / Especialidad")
        doc = c2.text_input("Doctor / Clínica / Dosis")
        if st.form_submit_button("💾 GUARDAR EN SALUD"):
            try:
                df = conn.read(spreadsheet=URL_EXCEL, worksheet="SALUD_REGISTRO")
                nueva = pd.DataFrame([{"Fecha": str(f), "Tipo": t, "Especialidad": esp, "Doctor": doc}])
                conn.update(spreadsheet=URL_EXCEL, worksheet="SALUD_REGISTRO", data=pd.concat([df, nueva], ignore_index=True))
                st.success("✅ Información de salud guardada"); st.rerun()
            except Exception as e:
                st.error(f"Error en SALUD_REGISTRO: {e}")
    
    st.subheader("📋 Historial de Salud")
    try:
        df_s = conn.read(spreadsheet=URL_EXCEL, worksheet="SALUD_REGISTRO")
        st.dataframe(df_s.tail(10), use_container_width=True)
    except:
        st.info("No hay registros médicos registrados.")
