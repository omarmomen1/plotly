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
        background-color: #030712;
        color: #f8fafc;
        font-family: 'Inter', sans-serif;
    }
    /* High-Tech Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: 1px solid #1e293b !important;
    }
    /* Neon Inputs & Uploaders */
    div[data-baseweb="input"] > div, .stFileUploader > div > div, div[data-baseweb="select"] > div {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
    }
    /* Force Input Text to be Bright Cyan */
    input[type="number"], input[type="text"], div[data-baseweb="select"] span {
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
        color: #ffffff; font-weight: 900; margin: 0; letter-spacing: -1px;
    }
    .startup-header span {
        color: #00f3ff; text-shadow: 0px 0px 15px rgba(0,243,255,0.4);
    }
    .startup-header p {
        color: #94a3b8; margin-top: 5px; margin-bottom: 0; font-weight: 400;
    }
    /* Cyber Metric Cards */
    .cyber-metric {
        background-color: #0f172a; border: 1px solid #1e293b; border-radius: 10px;
        padding: 15px; text-align: center; transition: all 0.3s ease;
    }
    .cyber-metric:hover {
        border-color: #00f3ff; box-shadow: 0px 0px 15px rgba(0,243,255,0.1);
    }
    .metric-value {
        font-family: 'Courier New', monospace; font-size: 2.2rem; font-weight: 800;
        color: #00f3ff; text-shadow: 0px 0px 10px rgba(0, 243, 255, 0.4);
    }
    .metric-label {
        color: #94a3b8; text-transform: uppercase; font-size: 0.8rem;
        letter-spacing: 1.5px; font-weight: 600;
    }
    /* Styled Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 20px; }
    .stTabs [data-baseweb="tab"] { color: #64748b; font-weight: 600; padding-bottom: 10px; }
    .stTabs [aria-selected="true"] { color: #f8fafc !important; border-bottom: 2px solid #00f3ff !important; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. STARTUP HEADER & SIDEBAR
# ==========================================
st.markdown("""
<div class="startup-header">
    <h1>AeroFlow <span>AI</span></h1>
    <p>Next-Gen Computational Fluid Dynamics Diagnostics Engine</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<h3 style='color: #ffffff; font-weight: 700;'>⚙️ Core Parameters</h3>", unsafe_allow_html=True)
    fluid_density = st.number_input("Fluid Density (kg/m³)", value=998.20, step=0.1)
    inlet_dia = st.number_input("Inlet Diameter (m)", value=0.10, step=0.01)
    
    st.markdown("---")
    st.markdown("<h3 style='color: #ffffff; font-weight: 700;'>📂 Fluent Data Ingestion</h3>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload ANSYS/Fluent Export (.csv)", type=['csv'])

# ==========================================
# 3. MAIN DASHBOARD LOGIC
# ==========================================
if uploaded_file is None:
    # DEMO MODE
    st.markdown("<h4 style='color: #94a3b8; text-align: center; margin-top: 50px;'>Awaiting Simulation Data...</h4>", unsafe_allow_html=True)
    x, y = np.linspace(-5, 5, 50), np.linspace(-5, 5, 50)
    xGrid, yGrid = np.meshgrid(x, y)
    z = np.sin(np.sqrt(xGrid**2 + yGrid**2))
    
    fig = go.Figure(data=[go.Surface(z=z, x=x, y=y, colorscale='Jet', opacity=0.8)])
    fig.update_layout(
        title="Simulated Velocity Profile Tensor (Demo Mode)", title_font=dict(color='#00f3ff'),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        scene=dict(xaxis_gridcolor='#1e293b', yaxis_gridcolor='#1e293b', zaxis_gridcolor='#1e293b'),
        height=500, margin=dict(l=0, r=0, b=0, t=40)
    )
    st.plotly_chart(fig, use_container_width=True)

else:
    # LIVE DATA MODE
    df = pd.read_csv(uploaded_file)
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    st.success(f"File '{uploaded_file.name}' ingested successfully. Tensors activated.")
    
    colA, colB, colC = st.columns(3)
    with colA: st.markdown(f"<div class='cyber-metric'><div class='metric-label'>Data Nodes</div><div class='metric-value'>{len(df):,}</div></div>", unsafe_allow_html=True)
    with colB: st.markdown(f"<div class='cyber-metric'><div class='metric-label'>Variables Detected</div><div class='metric-value'>{len(df.columns)}</div></div>", unsafe_allow_html=True)
    with colC: st.markdown("<div class='cyber-metric'><div class='metric-label'>AI Status</div><div class='metric-value'>OPTIMAL</div></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🚀 3D Visualization", "🧠 AI Physics Insights", "🔗 Tensor Correlations"])

    # --- TAB 1: 3D DATA PROJECTOR ---
    with tab1:
        st.markdown("<h3 style='color: #ffffff;'>🌌 3D Spatial Projection</h3>", unsafe_allow_html=True)
        col_x, col_y, col_z, col_color = st.columns(4)
        with col_x: x_val = st.selectbox("X-Axis", numeric_cols, index=0)
        with col_y: y_val = st.selectbox("Y-Axis", numeric_cols, index=min(1, len(numeric_cols)-1))
        with col_z: z_val = st.selectbox("Z-Axis", numeric_cols, index=min(2, len(numeric_cols)-1))
        with col_color: c_val = st.selectbox("Color Gradient", numeric_cols, index=min(3, len(numeric_cols)-1))

        fig_real = go.Figure(data=[go.Scatter3d(
            x=df[x_val], y=df[y_val], z=df[z_val], mode='markers',
            marker=dict(size=3, color=df[c_val], colorscale='Jet', opacity=0.8,
            colorbar=dict(title=dict(text=c_val, font=dict(color="#00f3ff")), tickfont=dict(color='#94a3b8')))
        )])
        fig_real.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="#94a3b8"),
            scene=dict(xaxis_title=x_val, yaxis_title=y_val, zaxis_title=z_val),
            height=600, margin=dict(l=0, r=0, b=0, t=0)
        )
        st.plotly_chart(fig_real, use_container_width=True)

    # --- TAB 2: AI PHYSICS INSIGHTS & HISTOGRAMS ---
    with tab2:
        st.markdown("<h3 style='color: #ffffff;'>🔬 Automated Diagnostics</h3>", unsafe_allow_html=True)
        
        # AI Diagnostic Generation
        if len(numeric_cols) > 0:
            for col in numeric_cols[:4]: # Scan up to 4 variables to avoid spam
                col_max = df[col].max()
                col_mean = df[col].mean()
                if col_max > (col_mean * 3) and col_mean != 0:
                    st.warning(f"⚠️ **Anomaly Detected in '{col}':** Maximum value ({col_max:.2f}) is severely skewed compared to the mean ({col_mean:.2f}). Check for singularities or mesh artifacts.")
                else:
                    st.success(f"✅ **'{col}' Distribution:** Data falls within stable variance parameters.")
        
        st.markdown("---")
        st.markdown("<h4 style='color: #00f3ff;'>Statistical Distribution Plot</h4>", unsafe_allow_html=True)
        hist_val = st.selectbox("Select Variable to Profile", numeric_cols, index=0)
        
        fig_hist = go.Figure(data=[go.Histogram(x=df[hist_val], marker_color='#00f3ff', opacity=0.7)])
        fig_hist.update_layout(
            title=f"{hist_val} Frequency Distribution",
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="#94a3b8"),
            xaxis=dict(gridcolor='#1e293b', title=hist_val), yaxis=dict(gridcolor='#1e293b', title="Node Count"),
            height=400
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    # --- TAB 3: TENSOR CORRELATION MATRIX ---
    with tab3:
        st.markdown("<h3 style='color: #ffffff;'>🔗 Variable Correlation Heatmap</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color: #94a3b8;'>Mathematical mapping of how variables influence each other (1 = Direct Correlation, -1 = Inverse Correlation).</p>", unsafe_allow_html=True)
        
        # Calculate correlation matrix
        corr_matrix = df[numeric_cols].corr()
        
        fig_corr = go.Figure(data=go.Heatmap(
            z=corr_matrix.values, x=corr_matrix.columns, y=corr_matrix.columns,
            colorscale='RdBu', zmin=-1, zmax=1, # Classic Red/Blue correlation scale
            colorbar=dict(tickfont=dict(color='#94a3b8'))
        ))
        fig_corr.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="#94a3b8"),
            height=500, margin=dict(l=20, r=20, t=20, b=20)
        )
        st.plotly_chart(fig_corr, use_container_width=True)
        
        # Raw Data View moved here for cleanliness
        st.markdown("---")
        st.markdown("<h4 style='color: #ffffff;'>📄 Raw Tensor Matrix</h4>", unsafe_allow_html=True)
        st.dataframe(df.head(100), use_container_width=True)
