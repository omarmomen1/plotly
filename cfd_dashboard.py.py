import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# --- UI & APP CONFIGURATION ---
st.set_page_config(page_title="Plots", page_icon="🌪️", layout="wide")

# --- CUSTOM CSS INJECTION (THE POLISH) ---
st.markdown("""
<style>
    /* 1. Remove default Streamlit top padding */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
    }
    
    /* 2. Hide Streamlit watermarks for a professional look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 3. Custom Centered Title Styling */
    .custom-title {
        text-align: center;
        margin-top: -20px;
        margin-bottom: 30px;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .custom-title h1 {
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 0px;
        padding-bottom: 0px;
        /* Cool blue gradient text */
        background: -webkit-linear-gradient(45deg, #4facfe, #00f2fe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .custom-title p {
        font-size: 1.2rem;
        color: #888888;
        font-weight: 400;
        margin-top: 5px;
    }
</style>
""", unsafe_allow_html=True)

# --- THE NEW CENTERED TITLE ---
st.markdown("""
<div class="custom-title">
    <h1>🌪️ Professional CFD Dashboard</h1>
    <p>Advanced Post-Processing & Diagnostics Engine</p>
</div>
""", unsafe_allow_html=True)

# --- SIDEBAR: BOUNDARY CONDITIONS ---
st.sidebar.header("⚙️ System Parameters")
st.sidebar.markdown("Input physical properties to calculate exact performance metrics.")
fluid_density = st.sidebar.number_input("Fluid Density (kg/m³)", value=998.2, help="Default is water at room temp.")
pipe_diameter = st.sidebar.number_input("Inlet Diameter (m)", value=0.10)
cross_area = np.pi * (pipe_diameter / 2)**2

# --- UI TABS ---
tab1, tab2, tab3 = st.tabs(["📁 1. Visualization & Summary", "💡 2. Physics Insights", "⚖️ 3. Compare Designs"])

# ==========================================
# TAB 1: VISUALIZATION & DATA MAPPING
# ==========================================
with tab1:
    # Placed the uploader in a visually distinct container
    with st.container():
        uploaded_file = st.file_uploader("📂 Upload Fluent CSV Export", type=['csv', 'txt', 'out'], key="file_main")
    
    if uploaded_file is not None:
        try:
            # Read Data
            df = pd.read_csv(uploaded_file)
            
            # --- 1. SPATIAL MAPPING ---
            st.markdown("### 🗺️ Map Your Spatial Data")
            cols = st.columns(4)
            x_col = cols[0].selectbox("X Coordinate", options=df.columns, index=0)
            y_col = cols[1].selectbox("Y Coordinate", options=df.columns, index=1)
            z_col = cols[2].selectbox("Z Coordinate", options=df.columns, index=2)
            val_col = cols[3].selectbox("Primary Variable (Color)", options=df.columns, index=len(df.columns)-1)

            # --- 2. VELOCITY MAPPING ---
            st.markdown("### 💨 Map Velocity (For Vectors & Mass Flow)")
            v_cols = st.columns(3)
            u_col = v_cols[0].selectbox("X-Velocity", options=df.columns)
            v_col = v_cols[1].selectbox("Y-Velocity", options=df.columns)
            w_col = v_cols[2].selectbox("Z-Velocity", options=df.columns)
            
            # --- 3. PHYSICS CALCULATIONS ---
            max_val, min_val, avg_val = df[val_col].max(), df[val_col].min(), df[val_col].mean()
            
            # Delta P Estimation
            delta_p = 0
            press_cols = [c for c in df.columns if 'press' in c.lower()]
            if press_cols:
                p_col = press_cols[0]
                delta_p = df[p_col].max() - df[p_col].min()

            # Mass Flow & Velocity Estimation
            df['vel_mag'] = np.sqrt(df[u_col]**2 + df[v_col]**2 + df[w_col]**2)
            v_avg = df['vel_mag'].mean()
            mass_flow = fluid_density * v_avg * cross_area

            # --- 4. SUMMARY DASHBOARD ---
            st.markdown("---")
            st.markdown("### 📋 Case Performance Summary")
            mc1, mc2, mc3, mc4 = st.columns(4)
            mc1.metric("Mass Flow Rate (ṁ)", f"{mass_flow:.2f} kg/s")
            mc2.metric("Pressure Drop (ΔP)", f"{delta_p:.0f} Pa")
            mc3.metric("Avg Velocity", f"{v_avg:.2f} m/s")
            mc4.metric(f"Avg {val_col}", f"{avg_val:.2f}")

            # --- 5. RENDER ENGINE CONTROLS ---
            st.markdown("---")
            st.subheader("🖥️ Rendering Engine")
            
            gfx1, gfx2, gfx3 = st.columns(3)
            render_style = gfx1.radio("Plot Style", ["Point Cloud (High Speed)", "Velocity Vectors (Flow Direction)"])
            sample_rate = gfx2.slider("Data Sampling (%)", min_value=1, max_value=100, value=15, help="Lower to increase speed. Keep below 5% for Vectors.")
            arrow_size = gfx3.number_input("Arrow Size", min_value=0.001, max_value=5.0, value=0.05, step=0.01)
            
            # Sub-sample dataset for browser performance
            step = int(100 / sample_rate)
            df_render = df.iloc[::step]

            # --- 6. PLOTLY 3D BUILDER ---
            fig = go.Figure()

            if render_style == "Point Cloud (High Speed)":
                fig.add_trace(go.Scatter3d(
                    x=df_render[x_col], y=df_render[y_col], z=df_render[z_col],
                    mode='markers',
                    marker=dict(size=3, color=df_render[val_col], colorscale='Jet', opacity=0.9, colorbar=dict(title=val_col)),
                    name="Scalar Field"
                ))
            
            elif render_style == "Velocity Vectors (Flow Direction)":
                if sample_rate > 10:
                    st.warning("⚠️ Warning: High sampling rate with Vectors may cause browser lag. Recommend < 5%.")
                
                fig.add_trace(go.Cone(
                    x=df_render[x_col], y=df_render[y_col], z=df_render[z_col],
                    u=df_render[u_col], v=df_render[v_col], w=df_render[w_col],
                    colorscale='Jet',
                    sizemode="absolute",
                    sizeref=arrow_size,
                    name="Flow Vectors"
                ))

            # Maintain true physical aspect ratio
            fig.update_layout(
                height=700,
                scene=dict(xaxis_title='X (m)', yaxis_title='Y (m)', zaxis_title='Z (m)', aspectmode='auto'),
                margin=dict(l=0, r=0, b=0, t=0),
                paper_bgcolor="rgba(15, 15, 15, 1)",
                font=dict(color="#aaaaaa")
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.error(f"Render Error: Check column mappings. Details: {e}")

# =
