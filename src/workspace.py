import streamlit as st
import pandas as pd
import datetime

def render_agency_workspace(rag_engine):
    """Render the full interactive Agency PM Workspace."""
    
    project = st.session_state.active_project or {
        "name": "Acme Client Project",
        "client": "Acme Corp",
        "agency_type": "Design Agency",
        "shape": "Fixed-scope"
    }

    # Workspace Header Banner
    st.markdown(f"""
    <div style="background: #1E293B; border-bottom: 1px solid #334155; padding: 20px 24px; border-radius: 14px; margin-bottom: 24px;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <span class="badge badge-success">Live Workspace Project</span>
                <h2 style="margin: 6px 0 0 0; color: white;">📁 {project['name']}</h2>
                <p style="margin: 0; opacity: 0.8; font-size: 0.9rem;">Client: <b>{project['client']}</b> | Type: {project['agency_type']} | Billing: {project['shape']}</p>
            </div>
            <div>
                <span class="badge badge-primary">Rate Card: {st.session_state.rate_card['type']} (${st.session_state.rate_card['hourly_rate']}/hr)</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Workspace Navigation Tabs
    tab_projects, tab_time_billing, tab_team, tab_rag_copilot = st.tabs([
        "📋 Tasks & Kanban Board", 
        "⏱️ Time Logging & Invoicing", 
        "👥 Team & Access", 
        "🤖 Setup Copilot RAG Assistant"
    ])

    # TAB 1: Tasks & Board View
    with tab_projects:
        col_title, col_add = st.columns([3, 1])
        with col_title:
            st.subheader("Task Management Board")
        with col_add:
            with st.popover("➕ Add New Task"):
                new_title = st.text_input("Task Title")
                new_est = st.number_input("Estimated Hours", value=8)
                new_assignee = st.selectbox("Assignee", [m["name"] for m in st.session_state.team_members])
                new_status = st.selectbox("Status", ["To Do", "In Progress", "Done"])
                if st.button("Save Task"):
                    if new_title:
                        st.session_state.tasks.append({
                            "Task Name": new_title,
                            "Status": new_status,
                            "Estimated Hours": new_est,
                            "Assignee": new_assignee
                        })
                        st.success("Task added!")
                        st.rerun()

        # Task Metrics Summary
        tot_tasks = len(st.session_state.tasks)
        done_tasks = sum(1 for t in st.session_state.tasks if t.get("Status") == "Done")
        in_prog = sum(1 for t in st.session_state.tasks if t.get("Status") == "In Progress")
        to_do = sum(1 for t in st.session_state.tasks if t.get("Status") == "To Do")

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Tasks", tot_tasks)
        m2.metric("To Do", to_do)
        m3.metric("In Progress", in_prog)
        m4.metric("Completed (Done)", done_tasks)

        st.markdown("<br>", unsafe_allow_html=True)

        # Interactive Task List / Status Changer
        st.markdown("**Interactive Task Table:** (Change status to test activation flow)")
        
        for idx, task in enumerate(st.session_state.tasks):
            with st.container():
                st.markdown('<div class="task-card">', unsafe_allow_html=True)
                c1, c2, c3, c4, c5 = st.columns([3, 2, 2, 2, 2])
                with c1:
                    st.markdown(f"**{task['Task Name']}**")
                with c2:
                    st.caption(f"👤 {task.get('Assignee', 'Unassigned')}")
                with c3:
                    st.caption(f"⏱️ {task.get('Estimated Hours', 0)} hrs est.")
                with c4:
                    status_colors = {"To Do": "#F59E0B", "In Progress": "#3B82F6", "Done": "#10B981"}
                    st.markdown(f"<span style='color: {status_colors.get(task.get('Status'), '#FFF')}; font-weight:600;'>{task.get('Status')}</span>", unsafe_allow_html=True)
                with c5:
                    new_st = st.selectbox("Update", ["To Do", "In Progress", "Done"], index=["To Do", "In Progress", "Done"].index(task.get("Status", "To Do")), key=f"task_status_{idx}")
                    if new_st != task.get("Status"):
                        st.session_state.tasks[idx]["Status"] = new_st
                        if new_st == "Done":
                            st.session_state.telemetry["first_task_completed"] = True
                        st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

    # TAB 2: Time Logging & Invoicing
    with tab_time_billing:
        st.subheader("⏱️ Log Billable Time & Generate Client Invoices")
        
        col_log, col_card = st.columns([3, 2])
        
        with col_log:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("### Log Work Hours")
            
            task_choice = st.selectbox("Select Task", [t["Task Name"] for t in st.session_state.tasks])
            hours_logged = st.number_input("Hours Spent", min_value=0.5, max_value=24.0, value=2.5, step=0.5)
            work_notes = st.text_area("Work Summary / Notes", value="Completed milestone review and initial code refactoring.")
            
            if st.button("💾 Save Time Entry", type="primary"):
                st.session_state.time_logs.append({
                    "task": task_choice,
                    "hours": hours_logged,
                    "date": datetime.date.today().strftime("%Y-%m-%d"),
                    "notes": work_notes,
                    "logged_by": st.session_state.team_members[0]["name"]
                })
                st.success(f"Logged {hours_logged} hrs against '{task_choice}'!")
                st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)

        with col_card:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            rc = st.session_state.rate_card
            st.markdown("### Pre-Configured Rate Card")
            st.markdown(f"**Model:** {rc['type']}")
            st.markdown(f"**Hourly Rate:** ${rc['hourly_rate']}/hr")
            st.markdown(f"**Fixed Milestone:** ${rc['milestone_fee']}")
            st.markdown(f"**Monthly Retainer:** ${rc['retainer_monthly']}/mo")
            st.markdown(f"**Status:** `{rc['status']}`")
            st.markdown('</div>', unsafe_allow_html=True)

        # Logged Time History & Invoice Generator
        st.markdown("### Logged Time & Unbilled Revenue")
        if st.session_state.time_logs:
            df_logs = pd.DataFrame(st.session_state.time_logs)
            st.dataframe(df_logs, use_container_width=True)

            total_hrs = df_logs["hours"].sum()
            billable_amount = total_hrs * st.session_state.rate_card["hourly_rate"]

            st.markdown(f"**Total Logged Hours:** `{total_hrs} hrs` | **Unbilled Total:** `${billable_amount:,.2f}`")

            if st.button("🧾 Generate Draft Client Invoice", type="primary"):
                st.balloons()
                st.success(f"🎉 Draft Invoice #INV-2026-001 generated for **{project['client']}** in the amount of **${billable_amount:,.2f}**!")
        else:
            st.info("No time logged yet. Use the form above to log hours against scaffolded tasks.")

    # TAB 3: Team Management
    with tab_team:
        st.subheader("👥 Project Team & Permissions")
        st.caption("Addressing Problem #2 (Partial Team Activation)")

        col_t1, col_t2 = st.columns([2, 1])
        with col_t1:
            st.markdown("### Active & Invited Team Members")
            st.dataframe(pd.DataFrame(st.session_state.team_members), use_container_width=True)

        with col_t2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("### Quick Invite Link")
            st.text_input("Project Direct Link", value="https://app.locofast.io/invite?project=acme-corp&token=px901z", disabled=True)
            st.button("📋 Copy Project Invite Link")
            st.markdown('</div>', unsafe_allow_html=True)

    # TAB 4: RAG Copilot Contextual Help Panel
    with tab_rag_copilot:
        render_rag_chat_panel(rag_engine)


def render_rag_chat_panel(rag_engine):
    """Render the embedded Grounded RAG Chat Assistant panel."""
    st.subheader("🤖 Setup Copilot Grounded RAG Help Assistant")
    st.caption("Ask questions about billing, rate cards, invites, time tracking, or project settings. Grounded strictly in company documentation & PII-scrubbed support tickets.")

    # Render Chat History
    for idx, msg in enumerate(st.session_state.rag_messages):
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            if msg.get("sources"):
                st.caption(f"📚 Verified Sources: {', '.join(msg['sources'])}")
            if msg.get("confidence") is not None:
                st.caption(f"🎯 Retrieval Confidence Score: `{msg['confidence']:.2f}`")
            
            # Feedback Control
            if msg["role"] == "assistant" and idx > 0:
                f_col1, f_col2, f_col3 = st.columns([1, 1, 8])
                with f_col1:
                    if st.button("👍", key=f"thumbs_up_{idx}"):
                        st.session_state.telemetry["rag_positive_feedback"] += 1
                        st.toast("Thanks for your feedback!")
                with f_col2:
                    if st.button("👎", key=f"thumbs_down_{idx}"):
                        st.toast("Feedback recorded for weekly audit!")

    # Chat Input
    user_q = st.chat_input("Ask a question (e.g. 'Where do I set hourly vs fixed rate?')")
    if user_q:
        st.session_state.rag_messages.append({"role": "user", "content": user_q})
        st.session_state.telemetry["rag_questions_asked"] += 1

        # RAG Engine Query Execution
        result = rag_engine.query(user_q)
        
        st.session_state.rag_messages.append({
            "role": "assistant",
            "content": result["answer"],
            "confidence": result["confidence"],
            "sources": result.get("sources", []),
            "low_confidence": result.get("low_confidence", False)
        })
        st.rerun()
