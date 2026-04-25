import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# ==========================================
# 1. APP CONFIGURATION & STARTUP DARK THEME
# ==========================================
st.set_page_config(page_title="AeroFlow AI | CFD Analytics", page_icon="🌪️", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    /* Midnight/Cyber Dark Background */
    .stApp {
        background-color: #030712; /* Deepest blue/black */
        color: #f8fafc;
        font-family: 'Inter', sans-serif;
    }
    
    /* High-Tech Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: 1px solid #1e293b !important;
    }
    
    /* Neon Inputs & Uploaders */
    div[data-baseweb="input"] > div, .stFileUploader > div > div {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        color: #00f3ff !important;
    }
    
    /* Force Input Text to be Bright Cyan */
    input[type="number"], input[type="text"] {
        color: #00f3ff !important;
        -webkit-text-fill-color: #00f3ff !important;
        font-weight: 700;
    }
    
    /* Glowing Startup Header */
    .startup-header {
        background: linear-gradient(90deg, rgba(15,23,42,1) 0%, rgba(3,7,18,1) 100%);
        padding: 20px;
        border-radius: 12px;
        border-left: 4px solid #00f3ff;
        margin-bottom: 25px;
        box-shadow: 0 4px 20px -2px rgba(0, 243, 255, 0.15);
    }
    .startup-header h1 {
        font-family: 'Space Grotesk', sans-serif;
        color: #ffffff;
        font-weight: 900;
        margin: 0;
        letter-spacing: -1px;
    }
    .startup-header span {
        color: #00f3ff; /* Neon Cyan */
        text-shadow: 0px 0px 15px rgba(0,243,255,0.4);
    }
    .startup-header p {
        color: #94a3b8;
        margin-top: 5px;
        margin-bottom: 0;
        font-size: 1.1rem;
        font-weight: 400;
    }

    /* Cyber Metric Cards */
    .cyber-metric {
        background-color: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        transition: all 0.3s ease;
    }
    .cyber-metric:hover {
        border-color: #00f3ff;
        box-shadow: 0px 0px 15px rgba(0,243,255,0.1);
    }
    .metric-value {
        font-family: 'Fira Code', monospace;
        font-size: 2.5rem;
        font-weight: 800;
        color: #00f3ff;
        text-shadow: 0px 0px 10px rgba(0, 243, 255, 0.4);
    }
    .metric-label {
        color: #94a3b8;
        text-transform: uppercase;
        font-size: 0.8rem;
        letter-spacing: 1.5px;
        font-weight: 600;
    }

    /* Styled Tabs (Overriding Streamlit defaults) */
    .stTabs [data-baseweb="tab-list"] {
        background-color: transparent;
        gap: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        color: #64748b;
        font-weight: 600;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        color: #f8fafc !important;
        border-bottom: 2px solid #00f3ff !important;
    }
    
    /* Hide Default Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. STARTUP HEADER
# ==========================================
st.markdown("""
<div class="startup-header">
    <h1>AeroFlow <span>AI</span></h1>
    <p>Next-Gen Computational Fluid Dynamics Diagnostics Engine</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 3. HIGH-TECH SIDEBAR (Control Deck)
# ==========================================
with st.sidebar:
    st.markdown("<h3 style='color: #ffffff; font-weight: 700;'>⚙️ Core Parameters</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748b; font-size: 0.9rem;'>Inject physical constraints to calibrate the post-processing engine.</p>", unsafe_allow_html=True)
    
    fluid_density = st.number_input("Fluid Density (kg/m³)", value=998.20, step=0.1)
    inlet_dia = st.number_input("Inlet Diameter (m)", value=0.10, step=0.01)
    kinematic_visc = st.number_input("Kinematic Viscosity (m²/s)", value=0.000001, format="%.6f")
    
    st.markdown("---")
    st.markdown("<h3 style='color: #ffffff; font-weight: 700;'>📂 Fluent Data Ingestion</h3>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload ANSYS/Fluent Export (.csv)", type=['csv'])

# ==========================================
# 4. MAIN DASHBOARD TABS
# ==========================================
tab1, tab2, tab3 = st.tabs(["🚀 Visualization & Summary", "🧠 Physics Insights", "⚖️ Compare Designs"])

# --- TAB 1: VISUALIZATION & SUMMARY ---
# --- TAB 1: VISUALIZATION & SUMMARY ---
with tab1:
    if uploaded_file is None:
        # Placeholder Startup-Vibe Graphic when no file is uploaded
        st.markdown("<h4 style='color: #94a3b8; text-align: center; margin-top: 50px;'>Awaiting Simulation Data...</h4>", unsafe_allow_html=True)
        
        x = np.linspace(-5, 5, 50)
        y = np.linspace(-5, 5, 50)
        xGrid, yGrid = np.meshgrid(x, y)
        z = np.sin(np.sqrt(xGrid**2 + yGrid**2))
        
        fig = go.Figure(data=[go.Surface(z=z, x=x, y=y, colorscale='Teal', opacity=0.8)])
        fig.update_layout(
            title="Simulated Velocity Profile Tensor (Demo Mode)",
            title_font=dict(color='#00f3ff'),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            scene=dict(
                xaxis=dict(gridcolor='#1e293b', backgroundcolor='rgba(0,0,0,0)'),
                yaxis=dict(gridcolor='#1e293b', backgroundcolor='rgba(0,0,0,0)'),
                zaxis=dict(gridcolor='#1e293b', backgroundcolor='rgba(0,0,0,0)')
            ),
            height=500, margin=dict(l=0, r=0, b=0, t=40)
        )
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        # 1. READ THE UPLOADED CSV DATA
        df = pd.pd.read_csv(uploaded_file)
        
        st.success(f"File '{uploaded_file.name}' ingested successfully. Running diagnostic tensors...")
        
        # 2. DYNAMIC CYBER METRICS
        colA, colB, colC = st.columns(3)
        with colA: st.markdown(f"<div class='cyber-metric'><div class='metric-label'>Data Rows Captured</div><div class='metric-value'>{len(df):,}</div></div>", unsafe_allow_html=True)
        with colB: st.markdown(f"<div class='cyber-metric'><div class='metric-label'>Variables Detected</div><div class='metric-value'>{len(df.columns)}</div></div>", unsafe_allow_html=True)
        with colC: st.markdown("<div class='cyber-metric'><div class='metric-label'>System Status</div><div class='metric-value'>OPTIMAL</div></div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # 3. DYNAMIC 3D DATA PROJECTOR
        st.markdown("<h3 style='color: #ffffff;'>🌌 3D Spatial Projection</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color: #94a3b8;'>Map your Fluent CSV columns to the visualization engine.</p>", unsafe_allow_html=True)

        # Create dropdowns so the user can select which columns to plot
        col_x, col_y, col_z, col_color = st.columns(4)
        cols = df.columns.tolist()
        
        # Safely assign default dropdown indices based on how many columns exist
        with col_x: x_val = st.selectbox("X-Axis", cols, index=0)
        with col_y: y_val = st.selectbox("Y-Axis", cols, index=min(1, len(cols)-1))
        with col_z: z_val = st.selectbox("Z-Axis", cols, index=min(2, len(cols)-1))
        with col_color: c_val = st.selectbox("Color Gradient (e.g. Velocity/Pressure)", cols, index=min(3, len(cols)-1))

        # Generate the live 3D Scatter Plot
        fig_real = go.Figure(data=[go.Scatter3d(
            x=df[x_val], y=df[y_val], z=df[z_val],
            mode='markers',
            marker=dict(
                size=3,
                color=df[c_val],
                colorscale='Electric', # Neon Cyber Theme
                opacity=0.8,
                colorbar=dict(title=dict(text=c_val, font=dict(color="#00f3ff")), tickfont=dict(color='#94a3b8'))
            )
        )])

        fig_real.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#94a3b8"),
            scene=dict(
                xaxis=dict(title=x_val, gridcolor='#1e293b', backgroundcolor='rgba(0,0,0,0)'),
                yaxis=dict(title=y_val, gridcolor='#1e293b', backgroundcolor='rgba(0,0,0,0)'),
                zaxis=dict(title=z_val, gridcolor='#1e293b', backgroundcolor='rgba(0,0,0,0)')
            ),
            height=600, margin=dict(l=0, r=0, b=0, t=0)
        )
        st.plotly_chart(fig_real, use_container_width=True)

        # 4. SHOW THE RAW DATA MATRIX
        st.markdown("<h3 style='color: #ffffff;'>📄 Raw Tensor Matrix</h3>", unsafe_allow_html=True)
        st.dataframe(df.head(100), use_container_width=True) # Display first 100 rows to keep app fast
# --- TAB 2: PHYSICS INSIGHTS ---
with tab2:
    st.markdown("### Deep Physics Analytics")
    st.markdown("Use this tab to plot contours, calculate forces, or display boundary layer separation data based on your CSV inputs.")
    
    # Another slick placeholder chart (Scatter/Residuals)
    x_res = np.arange(100)
    y_res = np.exp(-x_res/20) * np.cos(x_res/2)
    fig2 = go.Figure(go.Scatter(x=x_res, y=y_res, mode='lines', line=dict(color='#e11d48', width=3), fill='tozeroy', fillcolor='rgba(225, 29, 72, 0.2)'))
    fig2.update_layout(
        title="Convergence Residuals", title_font=dict(color='#f8fafc'),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=True, gridcolor='#1e293b'), yaxis=dict(showgrid=True, gridcolor='#1e293b'), height=400
    )
    st.plotly_chart(fig2, use_container_width=True)

# --- TAB 3: COMPARE DESIGNS ---
with tab3:
    st.markdown("### A/B Architecture Comparison")
    
    comp1, comp2 = st.columns(2)
    with comp1:
        st.markdown("#### Baseline Design (V1)")
        st.info("Upload V1 CSV to populate.")
    with comp2:
        st.markdown("#### Iteration (V2)")
        st.info("Upload V2 CSV to populate.")
