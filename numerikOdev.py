import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Pharmacokinetics ODE Model - Sevval Su",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- CUSTOM CSS WITH FIGMA PALETTE (GRADIENTS & STATIC BUBBLE UI) ---
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;900&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Nunito', sans-serif !important;
    }
    
    /* Static Gradient Background using Figma Palette */
    .stApp {
        background: linear-gradient(135deg, #F8DCC4 0%, #FFFFFF 100%) !important;
        color: #1D5381 !important;
    }
    
    /* Sidebar Bubble Card Styling */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 4px solid #ECA66B !important;
        box-shadow: 5px 0px 15px rgba(29, 83, 129, 0.05) !important;
    }
    
    /* Fix text colors inside sidebar */
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] span {
        color: #1D5381 !important;
        font-weight: 700 !important;
    }
    
    /* Custom Cartoon Bubble Cards */
    .bubble-card {
        background: #FFFFFF !important;
        border: 3px solid #1D5381 !important;
        border-radius: 24px !important;
        padding: 25px !important;
        margin-bottom: 25px !important;
        box-shadow: 0px 8px 0px #1D5381 !important;
    }
    
    /* Main Content Text Fixes */
    h1, h2, h3, p, span, label {
        color: #1D5381 !important;
    }
    
    h1 {
        font-weight: 900 !important;
    }
    
    /* Header Badge Style */
    .title-badge {
        background: linear-gradient(135deg, #1D5381, #ECA66B);
        color: #FFFFFF !important;
        padding: 12px 24px;
        border-radius: 20px;
        display: inline-block;
        font-weight: 900;
        margin-bottom: 15px;
        box-shadow: 0px 5px 0px #1D5381;
    }
    
    /* Dynamic Metric Display Custom Boxes */
    .metric-container {
        display: flex;
        gap: 20px;
        margin-bottom: 20px;
    }
    
    .custom-metric {
        background: #F8DCC4;
        border: 3px solid #1D5381;
        border-radius: 16px;
        padding: 15px;
        text-align: center;
        flex: 1;
        box-shadow: 0px 5px 0px #1D5381;
    }
    
    .custom-metric-title {
        font-size: 14px;
        font-weight: 700;
        color: #1D5381;
        margin-bottom: 5px;
    }
    
    .custom-metric-value {
        font-size: 24px;
        font-weight: 900;
        color: #1D5381;
    }

    /* Custom Alert Boxes */
    .alert-box {
        padding: 15px 20px;
        border-radius: 16px;
        border: 3px solid #1D5381;
        font-weight: 700;
        margin-top: 15px;
        box-shadow: 0px 5px 0px #1D5381;
    }
    .alert-success { background-color: #6ED49D !important; color: #FFFFFF !important; }
    .alert-warning { background-color: #ECA66B !important; color: #FFFFFF !important; }
    .alert-error { background-color: #59BE55 !important; color: #FFFFFF !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- HEADER SECTION ---
st.markdown(
    "<div class='title-badge'>✨ ODE NUMERICAL ANALYSIS PROJECT</div>",
    unsafe_allow_html=True,
)
st.markdown("<h1>Pharmacokinetics Model for Drug Absorption & Elimination</h1>", unsafe_allow_html=True)
st.markdown("<p style='font-size:16px; font-weight:700;'>Interactive dashboard simulating the physiological lifecycle of an analgesic compound using two coupled linear first-order Ordinary Differential Equations solved via the Euler Method.</p>", unsafe_allow_html=True)
st.write("---")

# --- SIDEBAR CONTROL CENTER ---
st.sidebar.markdown("## ⚙️ Control Center")
st.sidebar.markdown("Adjust parameters live to update the dynamic system state.")
st.sidebar.write("---")

st.sidebar.markdown("### 👤 Patient Profile")
dosage = st.sidebar.slider(
    "Administered Dosage (mg)",
    min_value=100,
    max_value=1000,
    value=500,
    step=50,
)
weight = st.sidebar.slider(
    "Patient Weight (kg)", min_value=45, max_value=120, value=75, step=5
)

st.sidebar.write("---")
st.sidebar.markdown("### 🧬 Kinetic Coefficients")
k_absorption = st.sidebar.slider(
    "Stomach Absorption Rate (k_abs)",
    min_value=0.1,
    max_value=2.0,
    value=0.6,
    step=0.1,
)
k_elimination = st.sidebar.slider(
    "Body Elimination Rate (k_elim)",
    min_value=0.05,
    max_value=0.8,
    value=0.15,
    step=0.05,
)


# --- MATHEMATICAL MODEL & ITERATIVE SOLUTION (EULER METHOD) ---
dt = 0.1  
total_time = 120  
time_steps = np.arange(0, total_time, dt)

M_stomach = [dosage]
K_blood = [0.0]

M_current = dosage
K_current = 0.0

for t in time_steps[:-1]:
    dM = -k_absorption * M_current * dt
    dK = (k_absorption * M_current - k_elimination * K_current) * dt

    M_current += dM
    K_current += dK

    M_stomach.append(M_current)
    K_blood.append(K_current)

concentration = np.array(K_blood) / weight

therapeutic_threshold = 1.5
toxic_threshold = 6.5


# --- PLOT DESIGN WITH FIGMA MATPLOTLIB STYLING ---
plt.rcParams["font.family"] = "sans-serif"
fig, ax = plt.subplots(figsize=(10, 5), facecolor="#FFFFFF")
ax.set_facecolor("#FFFFFF")

# Concentration Curve
ax.plot(
    time_steps,
    concentration,
    color="#1D5381",
    linewidth=4,
    zorder=3,
    label="Blood Concentration (mg/kg)"
)

# Threshold lines with Figma Colors
ax.axhline(
    y=therapeutic_threshold,
    color="#59BE55",
    linestyle="--",
    linewidth=2.5,
    label="Therapeutic Boundary (Pain Relief)",
    zorder=2,
)
ax.axhline(
    y=toxic_threshold,
    color="#ECA66B",
    linestyle="--",
    linewidth=2.5,
    label="Toxic Boundary (Danger Zone)",
    zorder=2,
)

# Chart Typography & Limits
ax.set_title("System State vs Time", fontsize=14, fontweight="bold", color="#1D5381", pad=15)
ax.set_xlabel("Time Elapsed (Minutes)", fontsize=11, fontweight="bold", color="#1D5381")
ax.set_ylabel("Concentration Scale (mg/kg)", fontsize=11, fontweight="bold", color="#1D5381")
ax.set_xlim(0, 120)
ax.set_ylim(0, 10)

# Grid and Spine Styling
ax.grid(True, linestyle="--", color="#F8DCC4", alpha=0.7, zorder=1)
for spine in ["top", "right"]:
    ax.spines[spine].set_visible(False)
for spine in ["left", "bottom"]:
    ax.spines[spine].set_color("#1D5381")
    ax.spines[spine].set_linewidth(2)

# Fix tick labels text visibility
ax.tick_params(colors='#1D5381', labelsize=10)

ax.legend(
    loc="upper right",
    frameon=True,
    facecolor="#FFFFFF",
    edgecolor="#1D5381",
)


# --- SITE LAYOUT CORNERSTONES ---
col1, col2 = st.columns([1.7, 1])

with col1:
    st.markdown("<div class='bubble-card'>", unsafe_allow_html=True)
    st.markdown("<h3>📊 Live Numerical Visualization</h3>", unsafe_allow_html=True)
    st.pyplot(fig)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='bubble-card'>", unsafe_allow_html=True)
    st.markdown("<h3>💡 Patient Metrics</h3>", unsafe_allow_html=True)

    max_effect = np.max(concentration)
    peak_time = time_steps[np.argmax(concentration)]

    # Clean custom metric blocks to prevent disappearing text
    st.markdown(f"""
    <div class='metric-container'>
        <div class='custom-metric'>
            <div class='custom-metric-title'>⚡ Max Concentration</div>
            <div class='custom-metric-value'>{max_effect:.2f} mg/kg</div>
        </div>
        <div class='custom-metric'>
            <div class='custom-metric-title'>⏱️ Time to Peak</div>
            <div class='custom-metric-value'>{peak_time:.1f} Mins</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Custom status notifications using Figma Palette colors
    if max_effect < therapeutic_threshold:
        st.markdown("<div class='alert-box alert-error'>❌ UNDERDOSE: Dosage is insufficient for this specific body mass. Minimal systemic impact.</div>", unsafe_allow_html=True)
    elif max_effect > toxic_threshold:
        st.markdown("<div class='alert-box alert-warning'>⚠️ TOXIC RISK: High concentrations reached! Adverse physiological risks detected.</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='alert-box alert-success'>✅ METRIC SUCCESS: Compound levels sustained within the safe therapeutic window.</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- LOWER DOCUMENTATION AREA ---
st.markdown("<div class='bubble-card'>", unsafe_allow_html=True)
st.markdown("<h3>📝 Mathematical Structure & Discussion</h3>", unsafe_allow_html=True)
st.markdown(f"""
The implementation models the dynamic compartmental tracks using **two coupled linear Ordinary Differential Equations (ODEs)**:
1. **Stomach Phase Decay:** $\\frac{{dM}}{{dt}} = -k_{{absorption}} \\cdot M$
2. **Bloodstream Intake and Clearance:** $\\frac{{dK}}{{dt}} = (k_{{absorption}} \\cdot M) - (k_{{elimination}} \\cdot K)$

**Parametric Study Evaluation:**
Currently, a patient weighing **{weight} kg** received a **{dosage} mg** active input. Peak systemic mass is achieved at **{peak_time:.1f} minutes** generating an exact maximum scale of **{max_effect:.2f} mg/kg**.

By shifting the input limits, we confirm that **increasing body weight drops the concentration peak downwards**, because the active chemical elements are distributed across a larger total body capacity. Conversely, **dropping the weight pushes the trajectory curve deep into the critical toxic space**. This serves as an elegant numerical demonstration of why weight-adjusted dosage computations are fundamental in clinical pharmacokinetics.
""")
st.markdown("</div>", unsafe_allow_html=True)