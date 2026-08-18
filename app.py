import streamlit as st
import plotly.graph_objects as go
from PIL import Image
from agent_executor import AutonomousAuditAgent

# --- Page Setup & Styling ---
st.set_page_config(
    page_title="AuditEngine-AI | Governance & Anomaly Control",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Enterprise Dark CSS
st.markdown("""
<style>
    /* Global background and typography tweaks */
    .main {
        background-color: #0B0F19;
    }
    
    /* Header branding */
    .brand-title {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(90deg, #38BDF8, #818CF8, #C084FC);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    .brand-sub {
        color: #94A3B8;
        font-size: 1.05rem;
        margin-bottom: 20px;
    }
    
    /* Glassmorphism Metric Cards */
    div[data-testid="stMetric"] {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 16px 20px;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
    }
    
    /* Audit card containers */
    .audit-card {
        background: #111827;
        border: 1px solid #1F2937;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 12px;
    }
    
    /* Action badges */
    .badge-high {
        color: #F87171;
        background: rgba(239, 68, 68, 0.15);
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .badge-normal {
        color: #34D399;
        background: rgba(16, 185, 129, 0.15);
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# --- Agent Caching ---
@st.cache_resource
def load_agent():
    return AutonomousAuditAgent()

agent = load_agent()

# --- Top Header ---
st.markdown('<div class="brand-title">🛡️ AuditEngine-AI Enterprise</div>', unsafe_allow_html=True)
st.markdown('<div class="brand-sub">Multi-Modal Infrastructure Telemetry Auditor & Autonomous Remediation Engine</div>', unsafe_allow_html=True)

# --- Sidebar Inputs ---
with st.sidebar:
    st.markdown("### ⚙️ System Controls")
    st.caption("Inject live runtime telemetry and infrastructure diagrams.")
    
    with st.expander("📊 Telemetry Configuration", expanded=True):
        login_failures = st.slider("Failed Auth / 5min", min_value=0, max_value=100, value=35)
        cpu_usage = st.slider("CPU Load (%)", min_value=0.0, max_value=100.0, value=91.5, step=0.5)
        request_rate = st.slider("Request Rate (req/sec)", min_value=10.0, max_value=3000.0, value=1850.0, step=50.0)

    with st.expander("🖼️ Architecture Blueprint", expanded=True):
        uploaded_file = st.file_uploader(
            "Upload System Diagram",
            type=["png", "jpg", "jpeg"]
        )

    st.markdown("---")
    trigger_btn = st.button("⚡ Run Intelligent Audit", type="primary", use_container_width=True)

# --- Main Dashboard Area ---
if trigger_btn:
    metrics = {
        "login_failures": login_failures,
        "cpu_usage": cpu_usage,
        "request_rate": request_rate
    }
    image_input = Image.open(uploaded_file) if uploaded_file else None

    with st.spinner("Processing Scikit-Learn heuristics, PyTorch vision tensors, and Vector RAG index..."):
        results = agent.run_full_audit(metrics, image_input=image_input)

    # 1. Top KPI Metric Row
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        st.metric(
            label="Calculated Risk Index",
            value=f"{results['log_analysis']['risk_score']}/100",
            delta="Anomaly Detected" if results["log_analysis"]["is_anomaly"] else "Nominal State",
            delta_color="inverse"
        )
    with kpi2:
        st.metric(
            label="Telemetry Evaluation",
            value="CRITICAL" if results["log_analysis"]["is_anomaly"] else "STABLE"
        )
    with kpi3:
        topol_name = results["vision_analysis"]["detected_topology"] if results["vision_analysis"] else "Standard VPC"
        st.metric(
            label="Identified Topology",
            value=topol_name.split()[0] + " " + topol_name.split()[1] if len(topol_name.split()) > 1 else topol_name
        )
    with kpi4:
        st.metric(
            label="RAG Matched Guidelines",
            value=f"{len(results['retrieved_guidelines'])} Active Rules"
        )

    st.markdown("---")

    # 2. Visual Analytics Section (Plotly Visualizations)
    st.subheader("📈 Real-Time Multi-Modal Telemetry Analytics")
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        # Gauge Chart for System Risk Score
        risk_val = results["log_analysis"]["risk_score"]
        gauge_fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=risk_val,
            title={'text': "Dynamic Threat Score (Isolation Forest)"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#EF4444" if risk_val > 50 else "#10B981"},
                'steps': [
                    {'range': [0, 40], 'color': "rgba(16, 185, 129, 0.15)"},
                    {'range': [40, 70], 'color': "rgba(245, 158, 11, 0.15)"},
                    {'range': [70, 100], 'color': "rgba(239, 68, 68, 0.15)"}
                ],
                'threshold': {
                    'line': {'color': "white", 'width': 3},
                    'thickness': 0.75,
                    'value': risk_val
                }
            }
        ))
        gauge_fig.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=280,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(gauge_fig, use_container_width=True)

    with col_chart2:
        # Horizontal Bar Chart for Vector RAG Similarity
        if results["retrieved_guidelines"]:
            rule_labels = [r["rule"][:25] + "..." for r in results["retrieved_guidelines"]]
            sim_scores = [r["similarity_pct"] for r in results["retrieved_guidelines"]]

            rag_fig = go.Figure(go.Bar(
                x=sim_scores,
                y=rule_labels,
                orientation='h',
                marker=dict(
                    color=sim_scores,
                    colorscale="Viridis",
                    showscale=False
                ),
                text=[f"{s}% Match" for s in sim_scores],
                textposition='auto'
            ))
            rag_fig.update_layout(
                title="ChromaDB Vector Semantic Relevance (%)",
                template="plotly_dark",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(range=[0, 100]),
                height=280,
                margin=dict(l=20, r=20, t=40, b=20)
            )
            st.plotly_chart(rag_fig, use_container_width=True)

    st.markdown("---")

    # 3. Execution Logs, RAG Details & Vision Inspector
    tab_overview, tab_rag, tab_vision = st.tabs(["⚡ Post-Mortem & Autonomous Actions", "📚 Vector RAG Knowledge", "🖼️ Multi-Modal Vision"])

    with tab_overview:
        c1, c2 = st.columns([1.2, 1])
        with c1:
            st.markdown("#### 📝 Executive Post-Mortem")
            st.markdown(results["llm_postmortem"])

            st.markdown("#### 🔍 Step-by-Step Reasoning Trace")
            for trace in results["audit_trail"]:
                st.code(trace, language="bash")

        with c2:
            st.markdown("#### 🛡️ Autonomous Remediation Queue")
            for action in results["actions_taken"]:
                st.success(action)

    with tab_rag:
        st.markdown("#### 🏛️ Retrieved Governance Standards (Hugging Face MiniLM + ChromaDB)")
        for idx, rule_data in enumerate(results["retrieved_guidelines"], 1):
            st.info(f"**Relevance: {rule_data['similarity_pct']}%** — {rule_data['rule']}")

    with tab_vision:
        if uploaded_file:
            v_col1, v_col2 = st.columns([1, 1.2])
            with v_col1:
                st.image(uploaded_file, caption="Topology Input Tensor (MobileNetV3)", use_container_width=True)
            with v_col2:
                st.markdown("#### 🧩 PyTorch Vision Diagnostics")
                if results["vision_analysis"]:
                    st.write(f"**Detected Topology:** `{results['vision_analysis']['detected_topology']}`")
                    st.write(f"**Classification Confidence:** `{results['vision_analysis']['confidence_pct']}%`")
                    st.write(f"**Topology Security Advisory:** {results['vision_analysis']['security_recommendation']}")
        else:
            st.info("No diagram uploaded. Telemetry-only audit executed.")

else:
    # Default State Landing View
    st.info("👈 Select telemetry parameters from the left sidebar and click **'Run Intelligent Audit'** to execute.")