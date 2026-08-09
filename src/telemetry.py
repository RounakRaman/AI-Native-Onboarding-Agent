import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def render_telemetry_dashboard():
    """Render PM & Founder Telemetry & A/B Testing Analytics Dashboard."""
    
    st.subheader("📊 Setup Copilot Telemetry & North Star Analytics")
    st.caption("Tracking activation metrics, per-hypothesis friction, guardrails, and A/B test results (Section 6 & 7 of PRD).")

    t_data = st.session_state.telemetry

    # Current Session Activation Milestone Tracker
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 🎯 Current Account 7-Day Team Activation Criteria")
    c1, c2, c3, c4 = st.columns(4)
    
    p_done = t_data["project_created"]
    i_done = t_data["teammate_invited"]
    t_done = t_data["first_task_completed"]
    activated = p_done and i_done and t_done

    c1.markdown(f"**1. Real Project Created**<br>{'✅ Yes' if p_done else '❌ Pending'}", unsafe_allow_html=True)
    c2.markdown(f"**2. Teammate Invited**<br>{'✅ Yes' if i_done else '❌ Pending'}", unsafe_allow_html=True)
    c3.markdown(f"**3. First Task Completed**<br>{'✅ Yes' if t_done else '❌ Pending'}", unsafe_allow_html=True)
    c4.markdown(f"**Composite Status**<br>{'🎉 ACTIVATED' if activated else '⏳ In Progress'}", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Key KPI Overview
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    
    control_rate = (t_data["control_activations"] / t_data["control_signups"]) * 100
    treatment_rate = (t_data["treatment_activations"] / t_data["treatment_signups"]) * 100
    lift = treatment_rate - control_rate

    kpi1.metric("North Star: 7-Day Activation Rate", f"{treatment_rate:.1f}%", f"+{lift:.1f}% vs Control", delta_color="normal")
    kpi2.metric("Baseline Target", "45.0%", "Target in 60 days")
    kpi3.metric("Copilot Completion Rate", "92.5%", "+14% vs self-setup")
    kpi4.metric("Support Ticket Volume / Acc", "0.4 tkt", "-35% reduction")

    st.markdown("<br>", unsafe_allow_html=True)

    # A/B Test Results Comparison Chart
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🧪 A/B Test: 7-Day Team Activation Lift")
        
        df_ab = pd.DataFrame({
            "Cohort": ["Control (Unguided Onboarding)", "Treatment (Setup Copilot v1.0)"],
            "Activation Rate (%)": [control_rate, treatment_rate],
            "Signups": [t_data["control_signups"], t_data["treatment_signups"]],
            "Activated Accounts": [t_data["control_activations"], t_data["treatment_activations"]]
        })
        
        fig = px.bar(
            df_ab, 
            x="Cohort", 
            y="Activation Rate (%)", 
            color="Cohort",
            color_discrete_sequence=["#EF4444", "#10B981"],
            text_auto=".1f",
            height=320
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#F8FAFC"),
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_chart2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📌 Per-Hypothesis Breakdown")
        
        df_hypo = pd.DataFrame({
            "Hypothesis": ["H1: Empty-State Overwhelm", "H2: Partial Team Activation", "H3: Switching Cost (Imports)"],
            "Before Copilot (%)": [52.0, 22.0, 18.0],
            "After Copilot (%)": [12.0, 68.0, 64.0]
        })
        
        fig_hyp = go.Figure(data=[
            go.Bar(name='Before Copilot (Control)', x=df_hypo['Hypothesis'], y=df_hypo['Before Copilot (%)'], marker_color='#F59E0B'),
            go.Bar(name='After Copilot (Treatment)', x=df_hypo['Hypothesis'], y=df_hypo['After Copilot (%)'], marker_color='#6366F1')
        ])
        fig_hyp.update_layout(
            barmode='group',
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#F8FAFC"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            height=320
        )
        st.plotly_chart(fig_hyp, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Guardrail Metrics Table
    st.markdown("### 🛡️ Guardrail Metrics Monitoring")
    guardrails = [
        {"Guardrail": "Support ticket volume per new account (1st 7 days)", "Target": "< 0.5 tickets", "Current Value": "0.4 tickets", "Status": "✅ PASS"},
        {"Guardrail": "Setup Copilot completion rate without mid-flow drop", "Target": "> 85%", "Current Value": "92.5%", "Status": "✅ PASS"},
        {"Guardrail": "Time-to-first real project created", "Target": "< 10 mins", "Current Value": "2.8 mins", "Status": "✅ PASS"},
        {"Guardrail": "30-day paid retention rate", "Target": "+12% lift", "Current Value": "+14.2% lift", "Status": "✅ PASS"}
    ]
    st.table(pd.DataFrame(guardrails))
