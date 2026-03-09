import streamlit as st
import math
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from calculations import calculate_all, CONDUCTORS

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Distance Protection Calculator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CUSTOM CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
}

.stApp {
    background: #0a0e1a;
    color: #e2e8f0;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0d1224 !important;
    border-right: 1px solid #1e2d4a;
}
section[data-testid="stSidebar"] * { color: #cbd5e1 !important; }
section[data-testid="stSidebar"] .stTextInput input,
section[data-testid="stSidebar"] .stNumberInput input,
section[data-testid="stSidebar"] .stSelectbox select {
    background: #131929 !important;
    border: 1px solid #1e3a5f !important;
    color: #e2e8f0 !important;
    border-radius: 4px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 13px;
}

/* Main titles */
.main-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 28px;
    font-weight: 600;
    color: #38bdf8;
    letter-spacing: -0.5px;
    margin-bottom: 4px;
}
.sub-title {
    font-size: 13px;
    color: #64748b;
    font-family: 'IBM Plex Mono', monospace;
    margin-bottom: 28px;
}

/* Section headers */
.sec-header {
    background: linear-gradient(90deg, #0f2744 0%, #0a1628 100%);
    border-left: 4px solid #38bdf8;
    padding: 10px 16px;
    margin: 20px 0 14px 0;
    border-radius: 0 6px 6px 0;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 14px;
    font-weight: 600;
    color: #38bdf8;
    letter-spacing: 0.5px;
}
.sec-header-def  { border-left-color: #fb923c; color: #fb923c;
    background: linear-gradient(90deg, #1a0f04 0%, #0a0e1a 100%); }
.sec-header-load { border-left-color: #a78bfa; color: #a78bfa;
    background: linear-gradient(90deg, #12082a 0%, #0a0e1a 100%); }
.sec-header-psb  { border-left-color: #34d399; color: #34d399;
    background: linear-gradient(90deg, #042014 0%, #0a0e1a 100%); }

/* Result cards */
.result-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 10px;
    margin: 10px 0;
}
.rcard {
    background: #111827;
    border: 1px solid #1e3a5f;
    border-radius: 8px;
    padding: 12px 14px;
    position: relative;
    overflow: hidden;
}
.rcard::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    background: #38bdf8;
}
.rcard.def::before   { background: #fb923c; }
.rcard.load::before  { background: #a78bfa; }
.rcard.psb::before   { background: #34d399; }
.rcard.warn::before  { background: #ef4444; }
.rcard-label {
    font-size: 11px;
    color: #64748b;
    font-family: 'IBM Plex Mono', monospace;
    margin-bottom: 4px;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}
.rcard-value {
    font-size: 22px;
    font-weight: 700;
    font-family: 'IBM Plex Mono', monospace;
    color: #f1f5f9;
}
.rcard-unit {
    font-size: 11px;
    color: #475569;
    font-family: 'IBM Plex Mono', monospace;
}
.rcard-sub {
    font-size: 11px;
    color: #38bdf8;
    margin-top: 2px;
    font-family: 'IBM Plex Mono', monospace;
}

/* Formula boxes */
.formula-box {
    background: #050d1a;
    border: 1px solid #1e3a5f;
    border-radius: 6px;
    padding: 14px 18px;
    margin: 8px 0;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 13px;
    color: #93c5fd;
}
.formula-box .step {
    color: #64748b;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 4px;
}
.formula-box .eq {
    color: #7dd3fc;
    font-size: 14px;
    margin: 3px 0;
}
.formula-box .result {
    color: #38bdf8;
    font-size: 16px;
    font-weight: 600;
    margin-top: 6px;
    padding-top: 6px;
    border-top: 1px solid #1e3a5f;
}
.formula-box .note {
    color: #475569;
    font-size: 11px;
    margin-top: 4px;
    font-style: italic;
}

/* Theory boxes */
.theory-box {
    background: #0a1628;
    border: 1px solid #1e3a5f;
    border-radius: 6px;
    padding: 16px 18px;
    margin: 8px 0;
    font-size: 13px;
    color: #94a3b8;
    line-height: 1.7;
}
.theory-box h4 {
    color: #38bdf8;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 10px;
    margin-top: 0;
}
.theory-box .q {
    color: #fbbf24;
    font-weight: 600;
    margin-top: 10px;
}
.theory-box .a {
    color: #94a3b8;
    margin-left: 12px;
    margin-top: 3px;
}

/* Zone summary table */
.zone-table {
    width: 100%;
    border-collapse: collapse;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 13px;
    margin: 10px 0;
}
.zone-table th {
    background: #0f2744;
    color: #38bdf8;
    padding: 8px 12px;
    text-align: center;
    font-size: 11px;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    border: 1px solid #1e3a5f;
}
.zone-table td {
    padding: 8px 12px;
    border: 1px solid #1a2744;
    text-align: center;
    color: #e2e8f0;
}
.zone-table tr:nth-child(even) td { background: #0d1628; }
.zone-table tr:hover td { background: #111f38; }
.badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 11px;
    font-family: 'IBM Plex Mono', monospace;
}
.badge-green  { background: #042014; color: #34d399; border: 1px solid #064f2a; }
.badge-blue   { background: #0f2744; color: #38bdf8; border: 1px solid #1e3a5f; }
.badge-orange { background: #1a0f04; color: #fb923c; border: 1px solid #3d1f05; }
.badge-red    { background: #1a0404; color: #f87171; border: 1px solid #3d0505; }
.badge-warn   { background: #1a1200; color: #fbbf24; border: 1px solid #3d2d00; }

/* Dividers */
.hdivider {
    border: none;
    border-top: 1px solid #1e2d4a;
    margin: 16px 0;
}

/* Streamlit overrides */
.stExpander {
    background: #0d1224 !important;
    border: 1px solid #1e2d4a !important;
    border-radius: 6px !important;
}
.stExpander summary {
    color: #64748b !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 12px !important;
}
div[data-testid="metric-container"] {
    background: #111827;
    border: 1px solid #1e3a5f;
    border-radius: 8px;
    padding: 10px;
}
</style>
""", unsafe_allow_html=True)

# ── HELPERS ───────────────────────────────────────────────────────────────────
def rcard(label, value, unit="", sub="", kind=""):
    cls = f"rcard {kind}"
    return f"""<div class="{cls}">
    <div class="rcard-label">{label}</div>
    <div class="rcard-value">{value}</div>
    <div class="rcard-unit">{unit}</div>
    {"<div class='rcard-sub'>" + sub + "</div>" if sub else ""}
</div>"""

def fbox(steps):
    inner = ""
    for s in steps:
        if s[0] == "step":
            inner += f'<div class="step">{s[1]}</div>'
        elif s[0] == "eq":
            inner += f'<div class="eq">{s[1]}</div>'
        elif s[0] == "res":
            inner += f'<div class="result">▶ {s[1]}</div>'
        elif s[0] == "note":
            inner += f'<div class="note">ℹ {s[1]}</div>'
    return f'<div class="formula-box">{inner}</div>'

def tbox(title, content):
    return f'<div class="theory-box"><h4>📖 {title}</h4>{content}</div>'

def badge(text, color):
    return f'<span class="badge badge-{color}">{text}</span>'

def sec(title, kind=""):
    cls = f"sec-header {('sec-header-' + kind) if kind else ''}"
    return f'<div class="{cls}">⚡ {title}</div>'

# ── SIDEBAR INPUTS ────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div style="font-family:IBM Plex Mono;font-size:16px;color:#38bdf8;font-weight:600;margin-bottom:4px;">⚡ DISTANCE PROTECTION</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-family:IBM Plex Mono;font-size:11px;color:#334155;margin-bottom:20px;">SETTING CALCULATOR v1.0</div>', unsafe_allow_html=True)

    st.markdown("**🏭 Identification**")
    sub_name  = st.text_input("Substation Name", "Biswanath Chairali")
    line_name = st.text_input("Line Name", "Itanagar Line-1")
    voltage   = st.selectbox("Voltage Level (kV)", [132, 220, 400, 765], index=0)

    st.markdown("---")
    st.markdown("**📐 Line Parameters**")
    line_len = st.number_input("Line Length (km)", 1.0, 2000.0, 100.0, 1.0)

    c1, c2 = st.columns(2)
    with c1:
        x1 = st.number_input("X1 (Ω/ph/km)", 0.001, 2.0, 0.307, 0.001, format="%.4f")
        x0 = st.number_input("X0 (Ω/ph/km)", 0.001, 5.0, 1.070, 0.001, format="%.4f")
    with c2:
        r1 = st.number_input("R1 (Ω/ph/km)", 0.001, 2.0, 0.0288, 0.001, format="%.4f")
        r0 = st.number_input("R0 (Ω/ph/km)", 0.001, 5.0, 0.269, 0.001, format="%.4f")

    st.markdown("---")
    st.markdown("**🔗 Adjacent Lines at Remote Bus**")
    lng_name = st.text_input("Longest Line Name", "Itanagar-RHEP")
    c1, c2 = st.columns(2)
    with c1: lng_len  = st.number_input("Length (km)", 1.0, 2000.0, 132.0, 1.0, key="lng_len")
    with c2: lng_z1km = st.number_input("Z1/km (Ω)", 0.01, 2.0, 0.3333, 0.001, format="%.4f", key="lng_z1")

    sh_name = st.text_input("Shortest Line Name", "Itanagar-Lekhi")
    c1, c2 = st.columns(2)
    with c1: sh_len  = st.number_input("Length (km)", 1.0, 2000.0, 161.0, 1.0, key="sh_len")
    with c2: sh_z1km = st.number_input("Z1/km (Ω)", 0.01, 2.0, 0.2513, 0.001, format="%.4f", key="sh_z1")

    st.markdown("---")
    st.markdown("**⚡ Fault Currents**")
    if3_local  = st.number_input("Max 3-ph Fault — Local Bus (A)", 100, 100000, 19406, 100)
    if1_remote = st.number_input("Min 1-ph Fault — Remote Bus (A)", 100, 100000, 1103, 10)

    st.markdown("---")
    st.markdown("**🔌 CT & PT**")
    c1, c2 = st.columns(2)
    with c1:
        ct_pri = st.number_input("CT Primary (A)", 100, 5000, 1000, 100)
        pt_pri = st.number_input("PT Primary (kV)", 1.0, 1000.0, 132.0, 1.0)
    with c2:
        ct_sec = st.number_input("CT Secondary (A)", 1, 5, 1, 1)
        pt_sec = st.number_input("PT Secondary (V)", 100, 200, 110, 5)

    st.markdown("---")
    st.markdown("**🔩 Conductor & Bay**")
    cond_name = st.selectbox("Conductor Type", list(CONDUCTORS.keys()), index=0)
    c1, c2 = st.columns(2)
    with c1: num_cond = st.number_input("No. of Conductors/Phase", 1, 4, 2)
    with c2: i_nom    = st.number_input("Bay Nominal Current (A)", 100, 5000, 1000, 100)

    st.markdown("---")
    st.markdown("**🌀 PSB**")
    f_swing = st.number_input("Swing Frequency (Hz)", 0.1, 5.0, 1.5, 0.1)

    st.markdown("---")
    calc_btn = st.button("⚡ CALCULATE", use_container_width=True, type="primary")

# ── MAIN AREA ─────────────────────────────────────────────────────────────────
st.markdown(f'<div class="main-title">⚡ Distance Protection Setting Calculator</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sub-title">Generic Distance | DEF | Load Encroachment | Power Swing Block</div>', unsafe_allow_html=True)

if not calc_btn:
    st.markdown("""
    <div style="background:#0d1224;border:1px solid #1e2d4a;border-radius:8px;padding:24px;margin-top:20px;text-align:center;">
        <div style="font-family:IBM Plex Mono;font-size:14px;color:#475569;margin-bottom:8px;">
            Fill in the parameters on the left panel
        </div>
        <div style="font-family:IBM Plex Mono;font-size:11px;color:#334155;">
            Outputs include: Zone Reaches · Earth Compensation · DEF Settings · Load Encroachment · Power Swing Block<br>
            Each section includes step-by-step formulae, justification and interview preparation notes
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── RUN CALCULATIONS ──────────────────────────────────────────────────────────
inp = dict(
    line_length=line_len, voltage_kv=voltage,
    x1=x1, r1=r1, x0=x0, r0=r0,
    longest_remote_length=lng_len, longest_remote_z1km=lng_z1km,
    shortest_remote_length=sh_len, shortest_remote_z1km=sh_z1km,
    fault_3ph_local=if3_local, fault_1ph_remote=if1_remote,
    ct_primary=ct_pri, ct_secondary=ct_sec,
    pt_primary_kv=pt_pri, pt_secondary_v=pt_sec,
    conductor_name=cond_name, num_conductors=num_cond,
    nominal_current=i_nom, swing_freq=f_swing
)
c = calculate_all(inp)

# ── HEADER INFO BAR ───────────────────────────────────────────────────────────
st.markdown(f"""
<div style="background:#0d1224;border:1px solid #1e2d4a;border-radius:8px;padding:14px 20px;
     display:flex;gap:30px;flex-wrap:wrap;margin-bottom:20px;">
  <div><span style="font-size:11px;color:#475569;font-family:IBM Plex Mono">SUBSTATION</span><br>
       <span style="font-size:15px;color:#f1f5f9;font-family:IBM Plex Mono;font-weight:600">{sub_name}</span></div>
  <div><span style="font-size:11px;color:#475569;font-family:IBM Plex Mono">LINE</span><br>
       <span style="font-size:15px;color:#f1f5f9;font-family:IBM Plex Mono;font-weight:600">{line_name}</span></div>
  <div><span style="font-size:11px;color:#475569;font-family:IBM Plex Mono">VOLTAGE</span><br>
       <span style="font-size:15px;color:#38bdf8;font-family:IBM Plex Mono;font-weight:600">{voltage} kV</span></div>
  <div><span style="font-size:11px;color:#475569;font-family:IBM Plex Mono">LENGTH</span><br>
       <span style="font-size:15px;color:#38bdf8;font-family:IBM Plex Mono;font-weight:600">{line_len} km</span></div>
  <div><span style="font-size:11px;color:#475569;font-family:IBM Plex Mono">CT / PT</span><br>
       <span style="font-size:15px;color:#f1f5f9;font-family:IBM Plex Mono;font-weight:600">{ct_pri}/{ct_sec}A · {pt_pri}kV/{pt_sec}V</span></div>
  <div><span style="font-size:11px;color:#475569;font-family:IBM Plex Mono">SHORT LINE</span><br>
       <span style="font-size:15px;font-family:IBM Plex Mono;font-weight:600">{badge("YES","warn") if c["short_line"] else badge("NO","green")}</span></div>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# SECTION 1 — LINE IMPEDANCES
# ════════════════════════════════════════════════════════════════════════════════
st.markdown(sec("SECTION 1 — LINE IMPEDANCES & EARTH COMPENSATION"), unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="result-grid">' +
        rcard("CTR / PTR", f"{c['kk']:.5f}", "conversion factor", f"CTR={int(c['CTR'])} | PTR={int(c['PTR'])}") +
        rcard("|Z1| Primary", f"{c['Z1_mag']:.4f}", "Ω (primary)", f"∠{c['Z1_ang']:.2f}°") +
        rcard("|Z1| Secondary", f"{c['Z1_sec']:.4f}", "Ω (secondary)", "= Z1 × CTR/PTR") +
        rcard("|Z0| Primary", f"{c['Z0_mag']:.4f}", "Ω (primary)", f"∠{c['Z0_ang']:.2f}°") +
    '</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="result-grid">' +
        rcard("Kn Magnitude", f"{c['Kn_mag']:.6f}", "earth comp.", "(Z0−Z1)/(3Z1)") +
        rcard("Kn Angle", f"{c['Kn_ang']:.3f}", "degrees", "arg(Kn complex)") +
        rcard("RE/RL", f"{c['RE_RL']:.4f}", "—", "(R0−R1)/(3R1) ABB fmt") +
        rcard("XE/XL", f"{c['XE_XL']:.4f}", "—", "(X0−X1)/(3X1) ABB fmt") +
    '</div>', unsafe_allow_html=True)

with st.expander("📐 Step-by-step Formulae — Impedances & Kn"):
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(fbox([
            ("step", "Total +ve Seq. Impedance"),
            ("eq",   f"R1_total = R1/km × L = {r1} × {line_len} = {c['R1t']:.4f} Ω"),
            ("eq",   f"X1_total = X1/km × L = {x1} × {line_len} = {c['X1t']:.4f} Ω"),
            ("eq",   f"|Z1| = √(R1² + X1²) = √({c['R1t']:.3f}² + {c['X1t']:.3f}²)"),
            ("res",  f"|Z1| = {c['Z1_mag']:.6f} Ω  ∠{c['Z1_ang']:.4f}°"),
            ("eq",   f"Z1_secondary = Z1 × CTR/PTR = {c['Z1_mag']:.4f} × {c['kk']:.5f}"),
            ("res",  f"Z1_sec = {c['Z1_sec']:.6f} Ω"),
        ]), unsafe_allow_html=True)
    with c2:
        st.markdown(fbox([
            ("step", "Earth Compensation Factor Kn (complex)"),
            ("eq",   f"Z1c = {c['R1t']:.3f} + j{c['X1t']:.3f}  Ω"),
            ("eq",   f"Z0c = {c['R0t']:.3f} + j{c['X0t']:.3f}  Ω"),
            ("eq",   "Kn = (Z0c − Z1c) / (3 × Z1c)"),
            ("res",  f"|Kn| = {c['Kn_mag']:.6f}   ∠Kn = {c['Kn_ang']:.4f}°"),
            ("note", "Kn entered in relay as kZ0 or kZN for earth fault distance measurement"),
        ]), unsafe_allow_html=True)

with st.expander("📖 Theory & Interview Prep — Why Earth Compensation?"):
    st.markdown(tbox("Earth Compensation Factor — Kn / kZ0", """
<div class='q'>Q: Why is earth compensation factor needed?</div>
<div class='a'>In a phase-earth fault, the current path includes zero sequence impedance (Z0), which is different from positive sequence (Z1). Without compensation, the relay would measure an incorrect fault impedance — it would see a HIGHER impedance than the true fault location, leading to under-reach. Kn corrects the measured impedance back to the positive sequence value.</div>

<div class='q'>Q: What is the formula and what does each term mean?</div>
<div class='a'>Kn = (Z0 − Z1) / (3 × Z1). The numerator (Z0−Z1) represents the zero sequence deviation from positive sequence. The denominator (3×Z1) normalises it. The factor 3 appears because residual current = 3×I0.</div>

<div class='q'>Q: What happens if Kn is set incorrectly?</div>
<div class='a'>If |Kn| is too low → relay under-reaches on earth faults (fails to trip for faults within zone). If |Kn| is too high → relay over-reaches (trips for faults beyond zone boundary).</div>

<div class='q'>Q: Why is Kn a complex number (has angle)?</div>
<div class='a'>Because Z0 and Z1 have different R/X ratios. The angle of Kn accounts for this phase difference. Most modern numerical relays accept both magnitude and angle of Kn for accurate compensation.</div>

<div class='q'>Q: Difference between Kn (Siemens/GE) and RE/RL, XE/XL (ABB/Hitachi)?</div>
<div class='a'>Both express the same earth compensation but in different formats. RE/RL = (R0−R1)/(3R1) and XE/XL = (X0−X1)/(3X1) are the real and imaginary components separately. Kn is the single complex ratio. Same physics, different relay parameter names.</div>
"""), unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# SECTION 2 — ZONE REACHES
# ════════════════════════════════════════════════════════════════════════════════
st.markdown(sec("SECTION 2 — ZONE REACH CALCULATIONS"), unsafe_allow_html=True)

# Summary table
z3_winner = "Opt 1 (110% Longest)" if c["Z3_opt1"] >= c["Z3_opt2"] else "Opt 2 (50% Shortest)"
st.markdown(f"""
<table class="zone-table">
<tr>
  <th>Zone</th><th>% Reach</th><th>Primary (Ω)</th><th>Secondary (Ω)</th>
  <th>Timer (s)</th><th>Criteria</th><th>Status</th>
</tr>
<tr>
  <td><b>Z1</b></td>
  <td>{badge("80%","blue")}</td>
  <td>{c['Z1r_pri']:.4f}</td><td><b>{c['Z1r_sec']:.4f}</b></td>
  <td>{c['tZ1']:.2f}</td>
  <td>80% principal (S/C)</td>
  <td>{badge("INSTANTANEOUS","green")}</td>
</tr>
<tr>
  <td><b>Z2</b></td>
  <td>{badge("120%","blue")}</td>
  <td>{c['Z2r_pri']:.4f}</td><td><b>{c['Z2r_sec']:.4f}</b></td>
  <td>{c['tZ2']:.2f}</td>
  <td>120% principal (S/C)</td>
  <td>{badge("tZ2 = " + str(c['tZ2']) + "s","orange")}</td>
</tr>
<tr>
  <td><b>Z3</b></td>
  <td>{badge(f"{c['Z3_pct']*100:.1f}%","blue")}</td>
  <td>{c['Z3r_pri']:.4f}</td><td><b>{c['Z3r_sec']:.4f}</b></td>
  <td>{c['tZ3']:.1f}</td>
  <td>Own + 110% Longest vs Own + 50% Shortest → MAX</td>
  <td>{badge(z3_winner,"warn")}</td>
</tr>
<tr>
  <td><b>Z4</b></td>
  <td>{badge(f"{c['Z4_line_pct']*100:.0f}% (Rev)","red")}</td>
  <td>{c['Z4r_pri']:.4f}</td><td><b>{c['Z4r_sec']:.4f}</b></td>
  <td>{c['tZ4']:.1f}</td>
  <td>Reverse: {int(c['Z4_line_pct']*100)}% principal (L{"≤" if line_len<=100 else ">"}100km)</td>
  <td>{badge("REVERSE","red")}</td>
</tr>
</table>
""", unsafe_allow_html=True)

with st.expander("📐 Step-by-step Formulae — Zone Reaches"):
    t1, t2, t3, t4 = st.tabs(["Zone 1", "Zone 2", "Zone 3", "Zone 4"])

    with t1:
        st.markdown(fbox([
            ("step", "Zone-1 Reach — 80% of Principal Line"),
            ("eq",   "Z1_reach = 80% × |Z1_line|"),
            ("eq",   f"= 0.80 × {c['Z1_mag']:.6f}"),
            ("res",  f"Z1_reach_primary = {c['Z1r_pri']:.6f} Ω"),
            ("eq",   f"Z1_reach_secondary = {c['Z1r_pri']:.6f} × {c['kk']:.5f}"),
            ("res",  f"Z1_reach_secondary = {c['Z1r_sec']:.6f} Ω"),
            ("note", "Timer tZ1 = 0.0s (Instantaneous). No FSC at remote bus."),
        ]), unsafe_allow_html=True)

    with t2:
        st.markdown(fbox([
            ("step", "Zone-2 Reach — 120% of Principal Line"),
            ("eq",   "Z2_reach = 120% × |Z1_line|"),
            ("eq",   f"= 1.20 × {c['Z1_mag']:.4f} = {c['Z2r_pri']:.6f} Ω (primary)"),
            ("res",  f"Z2_reach_secondary = {c['Z2r_sec']:.6f} Ω"),
            ("step", "Zone-2 Timer Check"),
            ("eq",   f"Z_line × (Z2% − 1.0) = {c['Z1_mag']:.4f} × 0.20 = {c['Z2_check']:.4f} Ω"),
            ("eq",   f"60% × Z_shortest_remote = 0.60 × {c['Z1_sh']:.4f} = {c['Z2_60pct_sh']:.4f} Ω"),
            ("eq",   f"{c['Z2_check']:.4f} {'<' if c['Z2_check'] < c['Z2_60pct_sh'] else '>'} {c['Z2_60pct_sh']:.4f}  →  tZ2 = {c['tZ2']}s"),
            ("res",  f"tZ2 = {c['tZ2']} s  ({'0.35s criterion met' if c['tZ2']==0.35 else '0.5s criterion applies'})"),
        ]), unsafe_allow_html=True)

    with t3:
        st.markdown(fbox([
            ("step", "Zone-3 Reach — Two Options, Take Maximum"),
            ("eq",   "Option 1: Z_principal + 110% × Z_longest_remote"),
            ("eq",   f"= {c['Z1_mag']:.4f} + 1.10 × {c['Z1_lng']:.4f}"),
            ("eq",   f"= {c['Z1_mag']:.4f} + {1.10*c['Z1_lng']:.4f} = {c['Z3_opt1']:.6f} Ω"),
            ("eq",   "Option 2: Z_principal + 50% × Z_shortest_remote"),
            ("eq",   f"= {c['Z1_mag']:.4f} + 0.50 × {c['Z1_sh']:.4f}"),
            ("eq",   f"= {c['Z1_mag']:.4f} + {0.5*c['Z1_sh']:.4f} = {c['Z3_opt2']:.6f} Ω"),
            ("res",  f"Z3_reach = max({c['Z3_opt1']:.4f}, {c['Z3_opt2']:.4f}) = {c['Z3r_pri']:.6f} Ω (primary)"),
            ("eq",   f"Z3_reach_secondary = {c['Z3r_pri']:.4f} × {c['kk']:.5f}"),
            ("res",  f"Z3_reach_secondary = {c['Z3r_sec']:.6f} Ω"),
            ("note", f"tZ3 = {c['tZ3']}s for {voltage}kV lines"),
        ]), unsafe_allow_html=True)

    with t4:
        st.markdown(fbox([
            ("step", "Zone-4 Reach — Reverse Zone"),
            ("eq",   f"Criteria: {int(c['Z4_line_pct']*100)}% of principal section (L {'≤' if line_len<=100 else '>'} 100km)"),
            ("eq",   f"Z4_reach = {c['Z4_line_pct']:.2f} × {c['Z1_mag']:.6f}"),
            ("res",  f"Z4_reach_primary = {c['Z4r_pri']:.6f} Ω"),
            ("res",  f"Z4_reach_secondary = {c['Z4r_sec']:.6f} Ω"),
            ("note", "If secondary value < 1Ω, set relay to 1Ω (as % reach). tZ4 = 0.5s."),
        ]), unsafe_allow_html=True)

with st.expander("📖 Theory & Interview Prep — Zone Reaches"):
    st.markdown(tbox("Distance Zone Philosophy", """
<div class='q'>Q: Why is Zone-1 set to 80% and not 100% of the line?</div>
<div class='a'>The 20% margin accounts for measurement errors — CT/PT inaccuracies, relay tolerances, and line parameter uncertainties. If set to 100%, a small overestimation could cause the relay to trip for faults just BEYOND the line end (overreach), which would be a false trip on the remote bus. 80% guarantees Zone-1 always stays within the protected line.</div>

<div class='q'>Q: Why does Zone-2 need to reach beyond the line end?</div>
<div class='a'>Zone-2 (120-150%) provides backup for the portion of the line NOT covered by Zone-1 (the last 20%). If Zone-1 at the remote end fails to trip, Zone-2 from the local end picks up with a 0.35-0.5s delay, allowing time for the remote relay to operate first.</div>

<div class='q'>Q: Explain the Zone-2 timer logic — why 0.35s vs 0.5s?</div>
<div class='a'>If Zone-2 overreach (Z_line × (Z2%-100%)) is LESS than 60% of the shortest adjacent line at remote bus, there is no risk of Zone-2 reaching into that adjacent line. So 0.35s is safe. If it CAN reach into adjacent lines, 0.5s is needed to allow the remote relay (Zone-1 of adjacent line) to clear first.</div>

<div class='q'>Q: Why two criteria for Zone-3?</div>
<div class='a'>Zone-3 must cover the longest possible fault path: (1) own line + infeed through remote bus transformers/longest line. Using 110% of longest remote line with 100% own line gives the forward reach. The 50% of shortest remote line check ensures Zone-3 doesn't overreach into adjacent feeders under infeed conditions. The MAXIMUM of both is taken to cover the worst case.</div>

<div class='q'>Q: What is the purpose of Zone-4 (Reverse Zone)?</div>
<div class='a'>Zone-4 looks backward (toward the local bus) and is used for: (1) Current reversal guard in teleprotection schemes, (2) Busbar backup protection, (3) Detecting faults on the busbar itself. Typical setting: 10-20% of the principal line in the reverse direction.</div>
"""), unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# SECTION 3 — DEF
# ════════════════════════════════════════════════════════════════════════════════
st.markdown(sec("SECTION 3 — DIRECTIONAL EARTH FAULT (DEF) SETTINGS", "def"), unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="result-grid">' +
        rcard("IN>1 Pickup (sec)", f"{c['Is_sec']:.3f}", "A secondary", f"= {int(c['Is_pri'])}A primary / CTR", "def") +
        rcard("Operating Time", f"{c['t_op']:.1f}", "seconds", f"tZ3 ({c['tZ3']}s) + 0.1s", "def") +
        rcard("If / Is Ratio", f"{c['ratio']:.4f}", "—", f"{int(c['If1R'])}A / {int(c['Is_pri'])}A", "def") +
        rcard("TMS", f"{c['TMS']:.6f}", "IEC S-Inverse", "Normal Inverse curve", "def") +
    '</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="result-grid">' +
        rcard("Char. Angle", "-45°", "degrees", "Standard DEF angle", "def") +
        rcard("Polarisation", "NEG. SEQ.", "I2 / V2", "Negative sequence", "def") +
        rcard("I2pol Threshold", "50 mA", "secondary", "Min I2 for direction", "def") +
        rcard("V2pol Threshold", f"{c['V2pol']:.3f}", "V secondary", "5% of Vph_sec", "def") +
    '</div>', unsafe_allow_html=True)

with st.expander("📐 Step-by-step Formulae — DEF TMS Calculation"):
    st.markdown(fbox([
        ("step", "Step 1: Determine Is Pickup"),
        ("eq",   f"Voltage = {voltage}kV  →  Is_primary = {'300A (765kV system)' if voltage>=765 else '200A (standard)'}"),
        ("eq",   f"Is_secondary = Is_primary / CTR = {int(c['Is_pri'])} / {int(c['CTR'])} = {c['Is_sec']:.4f} A"),
        ("step", "Step 2: Operating Time"),
        ("eq",   f"t_op = tZ3 + 0.1s = {c['tZ3']} + 0.1 = {c['t_op']:.1f} s"),
        ("note", "Coordination margin of 0.1s above Zone-3 to avoid false operation"),
        ("step", "Step 3: Fault Current Ratio"),
        ("eq",   f"If / Is = {int(c['If1R'])}A / {int(c['Is_pri'])}A = {c['ratio']:.6f}"),
        ("step", "Step 4: TMS — IEC Normal Inverse (Standard Inverse)"),
        ("eq",   "TMS = t × [(If/Is)^0.02 − 1] / 0.14"),
        ("eq",   f"TMS = {c['t_op']} × [{c['ratio']:.4f}^0.02 − 1] / 0.14"),
        ("eq",   f"TMS = {c['t_op']} × [{c['ratio']**0.02:.6f} − 1] / 0.14"),
        ("eq",   f"TMS = {c['t_op']} × {(c['ratio']**0.02 - 1):.6f} / 0.14"),
        ("res",  f"TMS = {c['TMS']:.6f}"),
        ("step", "Step 5: V2pol Threshold"),
        ("eq",   f"V2pol = 5% × (PT_sec/√3) = 0.05 × ({pt_sec}/1.732) = {c['V2pol']:.3f} V"),
    ]), unsafe_allow_html=True)

with st.expander("📖 Theory & Interview Prep — DEF"):
    st.markdown(tbox("Directional Earth Fault Protection", """
<div class='q'>Q: What is DEF and why is it needed alongside distance protection?</div>
<div class='a'>Distance protection can sometimes fail to detect high resistance earth faults (e.g. tree contact, dry soil) because the fault impedance lies outside the zone characteristic. DEF uses zero sequence / residual current (IN) with directionality to detect these faults that distance protection misses.</div>

<div class='q'>Q: Why directional? What happens without directionality?</div>
<div class='a'>Earth faults on the busbar or on adjacent feeders also produce residual current (IN) in the relay. Without direction, the relay would trip for faults BEHIND it (busbar faults), which should be handled by busbar protection. Directionality ensures the relay only trips for faults in the FORWARD direction (toward the protected line).</div>

<div class='q'>Q: Why negative sequence polarisation instead of zero sequence?</div>
<div class='a'>Negative sequence voltage (V2) is a more reliable polarising quantity because: (1) It is less affected by zero sequence mutual coupling on parallel lines, (2) It remains available even during close-up 3-phase faults where V0 may be zero, (3) It is not contaminated by load unbalance or healthy system zero sequence voltage. Zero sequence polarisation is used where negative sequence is unavailable (e.g. very solidly earthed systems with I0 >> I2).</div>

<div class='q'>Q: What is the significance of −45° characteristic angle for DEF?</div>
<div class='a'>The characteristic angle defines the direction of maximum torque / sensitivity. For earth faults on overhead lines, the typical earth fault current lags the residual voltage by around 45−60°. Setting −45° means the relay is most sensitive when IN lags VN by 45°, which matches typical earth fault conditions on 132-220kV systems.</div>

<div class='q'>Q: Why is the operating time tZ3 + 0.1s used for TMS?</div>
<div class='a'>The DEF element acts as BACKUP for faults that Zone-3 distance also covers. The additional 0.1s ensures that if Zone-3 trips correctly, DEF does not interfere. If Zone-3 fails (relay failure or carrier failure), DEF provides the backup trip after tZ3 + 0.1s.</div>

<div class='q'>Q: What is IEC Standard Inverse (Normal Inverse) curve?</div>
<div class='a'>Operating time = TMS × 0.14 / [(If/Is)^0.02 − 1]. This is IEC 60255 Standard Inverse curve. It has a moderate inverse characteristic — as fault current increases, operating time decreases but not as steeply as Very Inverse (VI) or Extremely Inverse (EI). Standard Inverse is preferred for backup earth fault on transmission lines as it gives better coordination with downstream relays.</div>
"""), unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# SECTION 4 — LOAD ENCROACHMENT
# ════════════════════════════════════════════════════════════════════════════════
st.markdown(sec("SECTION 4 — LOAD ENCROACHMENT / BLINDER SETTINGS", "load"), unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    thermal_total = CONDUCTORS.get(cond_name, 700) * num_cond
    st.markdown('<div class="result-grid">' +
        rcard("Conductor Thermal", f"{thermal_total}", "A total", f"{cond_name} × {num_cond}", "load") +
        rcard("I_max (1.5× limiting)", f"{c['I_max']:.0f}", "A", f"1.5 × min({thermal_total}, {i_nom})", "load") +
        rcard("Min Load R (Primary)", f"{c['Rload_pri']:.4f}", "Ω primary", "0.85 × Vph / I_max", "load") +
        rcard("Min Load R (Secondary)", f"{c['Rload_sec']:.4f}", "Ω secondary", "Rload_pri × CTR/PTR", "load") +
    '</div>', unsafe_allow_html=True)

with col2:
    encroach_badge = badge("⚠ RISK", "warn") if c["load_encroach_risk"] else badge("✓ SAFE", "green")
    st.markdown('<div class="result-grid">' +
        rcard("Z< Blinder (sec)", f"{c['Z_blinder_sec']:.4f}", "Ω secondary", "= Min Load R sec", "load") +
        rcard("Load Angle", "30°", "fixed", "Standard", "load") +
        rcard("Z3 / Blinder Ratio", f"{c['Z3_vs_load']:.3f}", "—", "Z3_sec / Rload_sec", "warn" if c["load_encroach_risk"] else "load") +
        rcard("Encroachment Risk", encroach_badge, "", f"Z3/Rload {'> 0.8 ⚠' if c['load_encroach_risk'] else '≤ 0.8 ✓'}", "warn" if c["load_encroach_risk"] else "load") +
    '</div>', unsafe_allow_html=True)

with st.expander("📐 Step-by-step Formulae — Load Encroachment"):
    st.markdown(fbox([
        ("step", "Step 1: Conductor Thermal Rating"),
        ("eq",   f"Conductor: {cond_name} → {CONDUCTORS.get(cond_name,700)}A per conductor (CEA 2023)"),
        ("eq",   f"Total thermal = {CONDUCTORS.get(cond_name,700)} × {num_cond} conductors = {thermal_total} A"),
        ("step", "Step 2: Maximum Current for Load Calculation"),
        ("eq",   f"I_max = 1.5 × min(thermal, bay_nominal) = 1.5 × min({thermal_total}, {i_nom})"),
        ("res",  f"I_max = 1.5 × {min(thermal_total, i_nom)} = {c['I_max']:.0f} A"),
        ("step", "Step 3: Minimum Load Resistance"),
        ("eq",   f"V_phase = 0.85 × (VkV × 1000 / √3) = 0.85 × ({voltage*1000}/1.732) = {0.85*voltage*1000/math.sqrt(3):.1f} V"),
        ("eq",   f"R_load_primary = V_phase / I_max = {0.85*voltage*1000/math.sqrt(3):.1f} / {c['I_max']:.0f}"),
        ("res",  f"R_load_primary = {c['Rload_pri']:.6f} Ω"),
        ("eq",   f"R_load_secondary = Rload × CTR/PTR = {c['Rload_pri']:.4f} × {c['kk']:.5f}"),
        ("res",  f"R_load_secondary = {c['Rload_sec']:.6f} Ω"),
        ("step", "Step 4: Load Encroachment Check"),
        ("eq",   f"Z3_reach_sec / R_load_sec = {c['Z3r_sec']:.4f} / {c['Rload_sec']:.4f} = {c['Z3_vs_load']:.4f}"),
        ("res",  f"{'⚠ WARNING: Z3 may encroach on load (ratio > 0.8). Enable load blinder!' if c['load_encroach_risk'] else '✓ SAFE: Z3 does not encroach on load impedance (ratio ≤ 0.8)'}"),
    ]), unsafe_allow_html=True)

with st.expander("📖 Theory & Interview Prep — Load Encroachment"):
    st.markdown(tbox("Load Encroachment in Distance Protection", """
<div class='q'>Q: How can load current cause a distance relay to mal-trip?</div>
<div class='a'>During heavy load conditions (high current, low power factor), the apparent impedance seen by the relay (V/I) can fall inside the Zone-3 or even Zone-2 characteristic. The relay cannot distinguish this from a high-impedance fault within its reach, so it may trip incorrectly — known as load encroachment.</div>

<div class='q'>Q: Why is 85% of system voltage used?</div>
<div class='a'>Under stressed system conditions (post-fault voltage depression, heavy load), voltage can drop to 85% of nominal while load current remains high. Using 85% Vph represents a realistic worst-case scenario for the apparent impedance calculation. Using 100% would be unconservative.</div>

<div class='q'>Q: What is a load blinder and how does it work?</div>
<div class='a'>A load blinder is a resistive boundary added to the zone characteristic. It cuts off the zone polygon at the load impedance region. If the measured impedance falls outside the blinder (in the load region), the relay is prevented from tripping even if the impedance is inside the zone reach. Most modern quadrilateral characteristic relays implement this as the "R-reach" or "load blinder resistance" setting.</div>

<div class='q'>Q: Why is load angle of 30° significant?</div>
<div class='a'>The load impedance vector is typically at the power factor angle (approximately 30° for transmission systems under heavy load). Setting the blinder at 30° from the resistive axis ensures the relay can still detect faults (which have angles close to the line impedance angle ~80°) while blocking the load region (30°).</div>

<div class='q'>Q: What is SIR and how does it relate to load encroachment?</div>
<div class='a'>SIR (Source Impedance Ratio) = Zs/Zline. For long lines or weak sources (high SIR), voltage at the relay reduces significantly during faults, and the apparent impedance may overlap with load. High SIR lines require more careful blinder settings and sometimes a reduced Zone-3 reach.</div>
"""), unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# SECTION 5 — POWER SWING BLOCK
# ════════════════════════════════════════════════════════════════════════════════
st.markdown(sec("SECTION 5 — POWER SWING BLOCK (PSB) SETTINGS", "psb"), unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="result-grid">' +
        rcard("Zs (Source Imp.)", f"{c['Zs_sec']:.4f}", "Ω secondary", f"= {c['Zs_pri']:.4f} Ω primary", "psb") +
        rcard("Inner Blinder (RLdInFw)", f"{c['RLdInFw']:.4f}", "Ω secondary", "R3Ph / 2", "psb") +
        rcard("Outer Blinder (RLdOutFw)", f"{c['RLdOutFw']:.4f}", "Ω secondary", "From δout calculation", "psb") +
        rcard("Delta R (Separation)", f"{c['Delta_R']:.4f}", "Ω secondary", "RLdOutFw − RLdInFw", "psb") +
    '</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="result-grid">' +
        rcard("δin (Entry angle)", f"{c['delta_in']:.3f}", "degrees", "2·arctan(Zs/2·RLdInFw)", "psb") +
        rcard("δout (Exit angle)", f"{c['delta_out']:.3f}", "degrees", "δin − tP1·fsw·360", "psb") +
        rcard("Swing Frequency", f"{f_swing}", "Hz", "User input", "psb") +
        rcard("PSB Timer", "50 ms", "milliseconds", "Fixed standard", "psb") +
    '</div>', unsafe_allow_html=True)

with st.expander("📐 Step-by-step Formulae — PSB Blinder Calculation"):
    st.markdown(fbox([
        ("step", "Step 1: Source Impedance from 3-ph Fault Current"),
        ("eq",   f"V_base = VkV × 1000 / √3 = {voltage*1000:.0f} / 1.732 = {voltage*1000/math.sqrt(3):.2f} V"),
        ("eq",   f"Zs_primary = V_base / If_3ph = {voltage*1000/math.sqrt(3):.2f} / {if3_local} = {c['Zs_pri']:.6f} Ω"),
        ("eq",   f"Zs_secondary = Zs_primary × CTR/PTR = {c['Zs_pri']:.4f} × {c['kk']:.5f}"),
        ("res",  f"Zs_secondary = {c['Zs_sec']:.6f} Ω"),
        ("step", "Step 2: Inner Blinder (RLdInFw)"),
        ("eq",   f"RLdInFw = R3Ph_resistive / 2 = Z_blinder_sec / 2 = {c['Z_blinder_sec']:.4f} / 2"),
        ("res",  f"RLdInFw = {c['RLdInFw']:.6f} Ω"),
        ("step", "Step 3: Entry Angle δin"),
        ("eq",   "δin = 2 × arctan(Zs / (2 × RLdInFw))"),
        ("eq",   f"δin = 2 × arctan({c['Zs_sec']:.4f} / (2 × {c['RLdInFw']:.4f}))"),
        ("res",  f"δin = {c['delta_in']:.4f}°"),
        ("step", "Step 4: Exit Angle δout"),
        ("eq",   f"δout = δin − tP1 × fsw × 360  (tP1 = 1 assumed)"),
        ("eq",   f"δout = {c['delta_in']:.4f} − 1 × {f_swing} × 360"),
        ("res",  f"δout = {c['delta_out']:.4f}°"),
        ("step", "Step 5: Outer Blinder (RLdOutFw)"),
        ("eq",   "RLdOutFw = Zs / (2 × tan(δout/2))"),
        ("res",  f"RLdOutFw = {c['RLdOutFw']:.6f} Ω"),
        ("step", "Step 6: Delta R (Blinder Separation)"),
        ("eq",   f"ΔR = RLdOutFw − RLdInFw = {c['RLdOutFw']:.4f} − {c['RLdInFw']:.4f}"),
        ("res",  f"ΔR = {c['Delta_R']:.6f} Ω"),
        ("note", "PSB timer = 50ms. If impedance trajectory crosses both blinders in < 50ms → SWING detected → Block."),
    ]), unsafe_allow_html=True)

with st.expander("📖 Theory & Interview Prep — Power Swing Block"):
    st.markdown(tbox("Power Swing Block Philosophy", """
<div class='q'>Q: What is a power swing and why can it cause distance relay mal-operation?</div>
<div class='a'>A power swing is an electromechanical oscillation between two parts of the power system following a disturbance (fault, sudden load change). During a swing, voltages and currents oscillate, causing the apparent impedance seen by the relay to move across the R-X diagram. If this trajectory passes through the Zone-2 or Zone-3 characteristic, the relay may trip — even though there is no actual fault. This is an unwanted trip that can worsen the disturbance.</div>

<div class='q'>Q: How does the PSB detect a power swing vs a real fault?</div>
<div class='a'>The key difference is SPEED. During a fault, impedance jumps instantly inside the zone (within a few milliseconds). During a power swing, impedance moves GRADUALLY across the zone boundary. The PSB uses two concentric blinders (inner and outer). If the impedance enters the outer blinder and then the inner blinder within a time > 50ms (swing timer), it is classified as a SWING and zones are blocked. If impedance jumps through both blinders faster than 50ms, it's treated as a FAULT and tripping is allowed.</div>

<div class='q'>Q: Why are Zone-1 and Zone-2 blocked but sometimes not Zone-1?</div>
<div class='a'>For NR (Northern Region) and most Indian utilities per RPC philosophy: All zones blocked for 132kV. The rationale is that Zone-1 (only 80% reach) rarely has swing impedance loci passing through it — swings typically affect Zone-2 and Zone-3 more. However, blocking all zones provides maximum security. For 400kV+ systems where stability is critical, all zones are blocked.</div>

<div class='q'>Q: What is SIR and how does it affect PSB blinder settings?</div>
<div class='a'>SIR = Zs/Zline. The source impedance Zs determines where the electrical centre of the system lies. If Zs is high (weak source), the swing locus passes deeper into the impedance plane. The inner blinder is set based on Zs to ensure the PSB detects swings before they reach Zone-1. Larger Zs requires a wider blinder separation (larger ΔR).</div>

<div class='q'>Q: What is Out-of-Step Tripping (OST) vs Power Swing Block (PSB)?</div>
<div class='a'>PSB BLOCKS tripping during recoverable swings (system will re-synchronise). OST ALLOWS tripping during unrecoverable loss-of-synchronism — when the two systems have passed through 180° electrical separation (pole-slip) and will not re-synchronise. OST uses the same blinder arrangement but monitors the number of pole-slips and trips at the optimal moment (when current is minimum) to minimise damage. PSB and OST work together: PSB prevents mal-trips during stable swings; OST ensures controlled separation during unstable swings.</div>

<div class='q'>Q: What is the significance of swing frequency (1.5 Hz default)?</div>
<div class='a'>Swing frequency (also called slip frequency) is how fast the impedance locus moves across the R-X diagram. Typical power system swings are 0.5−3 Hz. 1.5 Hz is used as the standard assumed worst-case for Indian grid. Higher swing frequency → impedance moves faster → PSB timer must be correctly set. At 1.5 Hz, one full swing cycle = 667ms. The PSB timer of 50ms must be much less than half this period to reliably detect the swing entry.</div>
"""), unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# FINAL SUMMARY
# ════════════════════════════════════════════════════════════════════════════════
st.markdown(sec("COMPLETE SETTINGS SUMMARY"), unsafe_allow_html=True)
st.markdown(f"""
<table class="zone-table">
<tr><th>Parameter</th><th>Primary (Ω)</th><th>Secondary (Ω)</th><th>Timer / Value</th><th>Notes</th></tr>
<tr><td>Line |Z1|</td><td>{c['Z1_mag']:.4f}</td><td>{c['Z1_sec']:.4f}</td><td>∠{c['Z1_ang']:.2f}°</td><td>Positive sequence total</td></tr>
<tr><td>Zone 1</td><td>{c['Z1r_pri']:.4f}</td><td>{c['Z1r_sec']:.4f}</td><td>{c['tZ1']}s</td><td>80% — Instantaneous</td></tr>
<tr><td>Zone 2</td><td>{c['Z2r_pri']:.4f}</td><td>{c['Z2r_sec']:.4f}</td><td>{c['tZ2']}s</td><td>120%</td></tr>
<tr><td>Zone 3</td><td>{c['Z3r_pri']:.4f}</td><td>{c['Z3r_sec']:.4f}</td><td>{c['tZ3']}s</td><td>Own + 110% Longest/50% Shortest</td></tr>
<tr><td>Zone 4 (Rev)</td><td>{c['Z4r_pri']:.4f}</td><td>{c['Z4r_sec']:.4f}</td><td>{c['tZ4']}s</td><td>{int(c['Z4_line_pct']*100)}% Reverse</td></tr>
<tr><td>Kn (kZN)</td><td colspan="2">{c['Kn_mag']:.6f} ∠ {c['Kn_ang']:.3f}°</td><td>—</td><td>Earth compensation</td></tr>
<tr><td>IN>1 Pickup</td><td>{int(c['Is_pri'])} A</td><td>{c['Is_sec']:.3f} A</td><td>—</td><td>DEF pickup</td></tr>
<tr><td>IN>1 TMS</td><td colspan="2">{c['TMS']:.6f}</td><td>IEC S-Inv</td><td>Normal Inverse</td></tr>
<tr><td>Load Blinder</td><td>{c['Rload_pri']:.4f}</td><td>{c['Z_blinder_sec']:.4f}</td><td>30°</td><td>{'⚠ Encroachment risk' if c['load_encroach_risk'] else '✓ Safe'}</td></tr>
<tr><td>PSB Inner (RLdInFw)</td><td>—</td><td>{c['RLdInFw']:.4f}</td><td>50ms</td><td>Inner blinder</td></tr>
<tr><td>PSB Outer (RLdOutFw)</td><td>—</td><td>{c['RLdOutFw']:.4f}</td><td>50ms</td><td>ΔR = {c['Delta_R']:.4f} Ω</td></tr>
</table>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style="margin-top:24px;padding:12px 16px;background:#0d1224;border:1px solid #1e2d4a;
     border-radius:6px;font-family:IBM Plex Mono;font-size:11px;color:#334155;line-height:1.8;">
⚡ Distance Protection Calculator | {sub_name} — {line_name} | {voltage}kV | {line_len}km<br>
All secondary values use CTR/PTR = {c['kk']:.5f} ({int(c['CTR'])}/{int(c['PTR'])}) |
Zone-4 secondary {f"= {c['Z4r_sec']:.4f}Ω — NOTE: if < 1Ω set relay to 1Ω" if c['Z4r_sec'] < 1 else f"= {c['Z4r_sec']:.4f}Ω ✓"} |
Generic S/C output — no FSC — load angle 30° fixed
</div>
""", unsafe_allow_html=True)

