import streamlit as st
import os

# Set Streamlit Page Config at top
st.set_page_config(
    page_title="Setup Copilot - AI Onboarding Agent",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

from src.utils import apply_custom_css, init_session_state
from src.copilot import render_setup_copilot_wizard
from src.rag_engine import RAGEngine
from src.workspace import render_agency_workspace, render_rag_chat_panel
from src.telemetry import render_telemetry_dashboard

def main():
    # 1. Apply Styles & State
    apply_custom_css()
    init_session_state()

    # 2. Load Grounded RAG Engine
    @st.cache_resource
    def load_rag():
        return RAGEngine()
    
    rag_engine = load_rag()

    # 3. Sidebar Navigation & Global Controls
    with st.sidebar:
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 20px;">
            <div style="background: linear-gradient(135deg, #6366F1, #4F46E5); padding: 10px; border-radius: 12px; font-size: 1.5rem; color: white;">⚡</div>
            <div>
                <h3 style="margin: 0; font-size: 1.2rem; font-weight: 700; color: white;">Setup Copilot</h3>
                <span style="font-size: 0.75rem; color: #94A3B8;">Locofast-style PM Tools</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # View Mode Selector
        view_options = ["🧙 Setup Copilot Wizard", "📁 Agency PM Workspace", "📊 Product Telemetry & A/B Test", "📝 Launch Copy & AI Appendix"]
        
        # Default view mode logic
        default_index = 0 if not st.session_state.onboarding_complete else 1
        
        current_view = st.radio(
            "Select View Mode:",
            view_options,
            index=default_index,
            key="navigation_view_mode"
        )

        st.markdown("---")

        # Sidebar Telemetry Widget
        st.markdown("### 🎯 North Star Metric")
        t = st.session_state.telemetry
        tr_rate = (t["treatment_activations"] / t["treatment_signups"]) * 100
        st.metric("7-Day Team Activation", f"{tr_rate:.1f}%", "+19.2% vs Baseline")

        st.markdown("---")

        # Demo Reset Controls
        if st.button("🔄 Reset Demo Onboarding State", use_container_width=True):
            st.session_state.onboarding_complete = False
            st.session_state.onboarding_step = 1
            st.session_state.tasks = []
            st.session_state.time_logs = []
            st.session_state.active_project = None
            st.rerun()

        st.markdown("<br><div style='text-align: center; color: #64748B; font-size: 0.8rem;'>Built with Streamlit & Python<br>PRD Spec: Rounak Raman</div>", unsafe_allow_html=True)

    # 4. View Routing Logic
    if "Setup Copilot" in current_view:
        if st.session_state.onboarding_complete:
            st.success("🎉 Setup Copilot Onboarding Complete! Your project is live in the workspace.")
            if st.button("Re-open Onboarding Wizard"):
                st.session_state.onboarding_complete = False
                st.rerun()
        render_setup_copilot_wizard()

    elif "Agency PM Workspace" in current_view:
        if not st.session_state.onboarding_complete:
            st.warning("⚠️ Setup Copilot Onboarding has not been completed yet. Using scaffolded default project.")
        render_agency_workspace(rag_engine)

    elif "Product Telemetry" in current_view:
        render_telemetry_dashboard()

    elif "Launch Copy" in current_view:
        render_launch_copy_view()


def render_launch_copy_view():
    """Render Task 3 (Launch Copy) and Task 4 (The Curveball) & AI Appendix from evaluation document."""
    st.subheader("📝 Product Launch Assets & AI Appendix")
    st.caption("Implementation of Task 3, Task 4, and AI Appendix from Rounak Raman's PM Evaluation Task document.")

    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📢 Task 3: Launch Copy")
        
        st.markdown("#### a) In-App Announcement (Login Modal)")
        st.info("""
        **Meet Setup Copilot.** Starting a new client project? Answer a few quick questions and we’ll build it with you, tasks scaffolded, your team invited, ready in minutes. No blank screen, no starting from scratch.
        
        ➔ **Try Setup Copilot**
        """)

        st.markdown("#### b) LinkedIn Post (Founder Voice)")
        st.code("""
I watched a designer open our app, stare at a blank workspace for ninety seconds, and close the tab for good.

That’s when I stopped blaming our marketing for early churn. We don’t lose agencies because they dislike the product, we lose them in the first ninety seconds, staring at a blank screen with nowhere to start.

So we built Setup Copilot. Tell it about one real client, and it builds the project with you, brings your team in, and carries over the work you’re already tracking elsewhere.

If your team has ever quietly closed a new tool’s tab in the first minute, this one’s for you.
        """, language="markdown")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### ⚡ Task 4: The Curveball")
        st.markdown("*Founder: 'Our biggest competitor just launched the exact same feature yesterday. Big press. What do we do?'*")
        st.warning("""
**Slack Reply to Founder:**

No, doesn’t change the plan. We built this because customers asked for it, not to race a competitor. Chasing them now just makes us reactive on our own roadmap.

Thing I’d do differently: spend this week reverse-engineering their launch, what they rushed, what’s missing. First-mover on a feature usually means shortest-path build. That gap is our next move, not a copycat feature.

Thing I’m holding firm on: user-centric prioritization. Every roadmap decision still comes from what our customers are actually stuck on, not from what they just shipped. That’s why this feature worked in the first place.

We’re good. Happy to dig into their launch details tomorrow if useful.
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 🤖 AI Appendix Summary")
    st.markdown("""
- **Tool Used**: Claude / Gemini 1.5 Pro & 3.6 Flash.
- **Approach**: AI for brainstorming, prompt self-correction, strict PRD synthesis, and end-to-end Python/Streamlit code architecture.
- **Key Iterations**: Re-ordered lead hypothesis from mid-funnel billing to empty-state overwhelm. Tied all user stories directly to the **7-Day Team Activation Rate** composite metric.
    """)
    st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
