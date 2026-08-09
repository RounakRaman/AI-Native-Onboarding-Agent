import streamlit as st
import pandas as pd
import datetime

def render_setup_copilot_wizard():
    """Render the 5-step Setup Copilot onboarding wizard panel."""
    
    # Progress Step Indicator
    current_step = st.session_state.onboarding_step
    
    st.markdown("""
    <div class="copilot-hero">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <span class="badge badge-primary" style="margin-bottom: 8px;">AI Onboarding Assistant</span>
                <h1 style="margin: 4px 0;">Setup Copilot</h1>
                <p>Build your first real client project & invite your team in under 3 minutes.</p>
            </div>
            <div style="text-align: right; background: rgba(255,255,255,0.1); padding: 12px 20px; border-radius: 12px;">
                <span style="font-size: 0.85rem; opacity: 0.8;">Setup Progress</span>
                <div style="font-size: 1.5rem; font-weight: 700;">Step {} of 5</div>
            </div>
        </div>
    </div>
    """.format(current_step), unsafe_allow_html=True)

    # Step Indicators
    cols = st.columns(5)
    steps_labels = ["1. Intake", "2. Import Work", "3. Scaffold Project", "4. Invite Team", "5. Billing Prep"]
    for idx, label in enumerate(steps_labels, 1):
        with cols[idx - 1]:
            if idx == current_step:
                st.markdown(f'<div class="step-pill step-pill-active">{label}</div>', unsafe_allow_html=True)
            elif idx < current_step:
                st.markdown(f'<div class="step-pill step-pill-done">✓ {label}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="step-pill">{label}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # STEP 1: Conversational Intake
    if current_step == 1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("📋 Step 1: Tell Copilot About Your Agency")
        st.caption("Copilot will use your answers to scaffold a real project with tasks, timelines, and rate cards.")

        col_a, col_b = st.columns(2)
        with col_a:
            agency_type = st.selectbox(
                "1. What type of agency do you run?",
                ["Design Agency", "Dev Agency", "Marketing Agency", "Other / Full Service"],
                index=0
            )
            
            client_name = st.text_input(
                "2. Enter one real current client name (Not a placeholder):",
                value=st.session_state.intake_data.get("client_name", "Acme Corp"),
                help="We'll name your first live workspace project after this client."
            )

        with col_b:
            project_shape = st.selectbox(
                "3. Typical project shape / billing model:",
                ["Fixed-scope", "Retainer", "Mixed / Hourly"],
                index=0
            )
            
            migration_source = st.selectbox(
                "4. Are you migrating work from an existing tool?",
                ["Trello", "Google Sheets", "Jira", "GitHub Issues", "None (Start Fresh)"],
                index=0
            )

        st.session_state.intake_data = {
            "agency_type": agency_type,
            "client_name": client_name if client_name.strip() else "Acme Client",
            "project_shape": project_shape,
            "migration_source": migration_source
        }

        st.markdown("<hr style='border-color: #334155;'>", unsafe_allow_html=True)
        
        btn_col1, btn_col2 = st.columns([4, 1])
        with btn_col2:
            if st.button("Continue to Import ➔", type="primary", use_container_width=True):
                st.session_state.onboarding_step = 2
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    # STEP 2: Conditional Import Step
    elif current_step == 2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        source = st.session_state.intake_data["migration_source"]
        st.subheader(f"📥 Step 2: Migration Import from {source}")
        
        if source in ["Trello", "Google Sheets"]:
            st.info("Upload your existing export file or use our pre-loaded sample dataset to preview task mapping.")
            
            use_sample = st.checkbox("Load Sample Agency Export CSV", value=True)
            
            if use_sample:
                csv_path = "sample_data/trello_export_sample.csv" if source == "Trello" else "sample_data/sheets_export_sample.csv"
                df = pd.read_csv(csv_path)
                st.markdown(f"**Loaded Sample CSV ({len(df)} Tasks):**")
                st.dataframe(df, use_container_width=True)
                
                st.success("✅ Copilot auto-mapped fields: `Task Name` ➔ Task Title | `Estimated Hours` ➔ Budget | `Status` ➔ Board Column")
                
                st.session_state.imported_tasks = df.to_dict("records")
            else:
                uploaded_file = st.file_uploader("Upload CSV Export", type=["csv"])
                if uploaded_file:
                    df = pd.read_csv(uploaded_file)
                    st.dataframe(df, use_container_width=True)
                    st.session_state.imported_tasks = df.to_dict("records")
                else:
                    st.session_state.imported_tasks = []

        elif source in ["Jira", "GitHub Issues"]:
            st.success(f"🔗 Simulated OAuth Connection to {source} Active!")
            st.markdown(f"**Discovered Remote Workspace:** `agency-{source.lower()}-org/acme-project`")
            st.markdown("**Mapped 5 Open Issues into Locofast Tasks:**")
            
            simulated_issues = [
                {"Task Name": "Database Schema Setup", "Status": "In Progress", "Estimated Hours": 16, "Assignee": "Karan Mehta"},
                {"Task Name": "API Authentication Middleware", "Status": "To Do", "Estimated Hours": 12, "Assignee": "Karan Mehta"},
                {"Task Name": "Frontend Integration & State Management", "Status": "To Do", "Estimated Hours": 20, "Assignee": "Aditi Rao"},
                {"Task Name": "QA Testing & Bug Fixes", "Status": "To Do", "Estimated Hours": 8, "Assignee": "Priya Nair"}
            ]
            st.dataframe(pd.DataFrame(simulated_issues), use_container_width=True)
            st.session_state.imported_tasks = simulated_issues

        else:
            st.info("No migration source selected. Copilot will scaffold standard high-value agency template tasks.")
            st.session_state.imported_tasks = []

        st.markdown("<hr style='border-color: #334155;'>", unsafe_allow_html=True)
        
        btn_col1, btn_col2, btn_col3 = st.columns([1, 3, 1])
        with btn_col1:
            if st.button("⬅ Back"):
                st.session_state.onboarding_step = 1
                st.rerun()
        with btn_col3:
            if st.button("Scaffold Project ➔", type="primary", use_container_width=True):
                st.session_state.onboarding_step = 3
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    # STEP 3: Project Scaffolding
    elif current_step == 3:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        client = st.session_state.intake_data["client_name"]
        agency = st.session_state.intake_data["agency_type"]
        shape = st.session_state.intake_data["project_shape"]

        st.subheader("🚀 Step 3: Project Scaffolding")
        st.caption(f"Copilot is creating real project structure for **{client}** ({agency} - {shape}).")

        # Generate Scaffolded Tasks if imported list is empty
        if not st.session_state.imported_tasks:
            if "Design" in agency:
                scaffolded = [
                    {"Task Name": f"{client} Brand Identity & Specs", "Status": "In Progress", "Estimated Hours": 18, "Assignee": "Aditi Rao", "Milestone": "Phase 1"},
                    {"Task Name": "Figma Component Library", "Status": "In Progress", "Estimated Hours": 24, "Assignee": "Karan Mehta", "Milestone": "Phase 2"},
                    {"Task Name": "Client Design Prototype Review", "Status": "To Do", "Estimated Hours": 10, "Assignee": "Priya Nair", "Milestone": "Phase 2"}
                ]
            elif "Dev" in agency:
                scaffolded = [
                    {"Task Name": f"{client} Architecture & Tech Stack Setup", "Status": "Done", "Estimated Hours": 12, "Assignee": "Karan Mehta", "Milestone": "Sprint 1"},
                    {"Task Name": "REST API & Database Schema", "Status": "In Progress", "Estimated Hours": 28, "Assignee": "Karan Mehta", "Milestone": "Sprint 1"},
                    {"Task Name": "Frontend Integration & UI Components", "Status": "To Do", "Estimated Hours": 32, "Assignee": "Aditi Rao", "Milestone": "Sprint 2"}
                ]
            else:
                scaffolded = [
                    {"Task Name": f"{client} Q3 Marketing Strategy Deck", "Status": "In Progress", "Estimated Hours": 15, "Assignee": "Priya Nair", "Milestone": "Retainer M1"},
                    {"Task Name": "Social Media Copywriting & Assets", "Status": "To Do", "Estimated Hours": 20, "Assignee": "Aditi Rao", "Milestone": "Retainer M1"},
                    {"Task Name": "Weekly Analytics & Performance Rollup", "Status": "To Do", "Estimated Hours": 8, "Assignee": "Priya Nair", "Milestone": "Retainer M1"}
                ]
            st.session_state.tasks = scaffolded
        else:
            # Map imported tasks to session tasks
            st.session_state.tasks = st.session_state.imported_tasks

        st.session_state.active_project = {
            "name": f"{client} Client Project",
            "client": client,
            "agency_type": agency,
            "shape": shape,
            "created_at": datetime.date.today().strftime("%Y-%m-%d"),
            "status": "Active"
        }
        st.session_state.telemetry["project_created"] = True

        st.success(f"✨ Project **'{st.session_state.active_project['name']}'** successfully scaffolded!")

        st.markdown("**Scaffolded Task List:**")
        st.dataframe(pd.DataFrame(st.session_state.tasks), use_container_width=True)

        st.markdown("<hr style='border-color: #334155;'>", unsafe_allow_html=True)
        
        btn_col1, btn_col2, btn_col3 = st.columns([1, 3, 1])
        with btn_col1:
            if st.button("⬅ Back"):
                st.session_state.onboarding_step = 2
                st.rerun()
        with btn_col3:
            if st.button("Invite Teammates ➔", type="primary", use_container_width=True):
                st.session_state.onboarding_step = 4
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    # STEP 4: In-Flow Team Invite
    elif current_step == 4:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("👥 Step 4: Invite Teammates directly to Project")
        st.caption("Solving Problem #2 (Partial Team Activation): Bring at least one teammate into this newly scaffolded project.")

        col1, col2 = st.columns(2)
        with col1:
            member_name = st.text_input("Teammate Name", value="Karan Mehta")
            member_email = st.text_input("Teammate Email", value="karan@agency.com")
        with col2:
            member_role = st.selectbox("Role in Project", ["Dev Lead", "Designer", "Marketing Ops", "Client Viewer"])
            proj_name = st.session_state.active_project["name"] if st.session_state.active_project else "Client Project"
            st.text_input("Land-Direct Invite Link", value=f"https://app.locofast.io/invite?project={proj_name.lower().replace(' ', '-')}&token=px901z", disabled=True)

        if st.button("➕ Send In-Flow Invite & Add Member", type="secondary"):
            new_member = {
                "name": member_name,
                "email": member_email,
                "role": member_role,
                "status": "Invited (Direct Project Link Sent)"
            }
            st.session_state.team_members.append(new_member)
            st.session_state.telemetry["teammate_invited"] = True
            st.success(f"🎉 Invite sent to **{member_name}** ({member_email}) with direct access to `{proj_name}`!")

        st.markdown("**Project Team Members:**")
        st.table(pd.DataFrame(st.session_state.team_members))

        st.markdown("<hr style='border-color: #334155;'>", unsafe_allow_html=True)
        
        btn_col1, btn_col2, btn_col3 = st.columns([1, 3, 1])
        with btn_col1:
            if st.button("⬅ Back"):
                st.session_state.onboarding_step = 3
                st.rerun()
        with btn_col3:
            if st.button("Billing Prep ➔", type="primary", use_container_width=True):
                st.session_state.onboarding_step = 5
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    # STEP 5: Billing Preparation
    elif current_step == 5:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("💳 Step 5: Draft Rate Card & Billing Preparation")
        st.caption("Pre-configures rates based on project shape without forcing immediate billing setup.")

        shape = st.session_state.intake_data["project_shape"]
        agency = st.session_state.intake_data["agency_type"]

        col1, col2 = st.columns(2)
        with col1:
            rate_type = st.selectbox("Rate Card Model", ["Hourly Rate", "Fixed Milestone", "Monthly Retainer"], index=0 if shape=="Mixed / Hourly" else (1 if shape=="Fixed-scope" else 2))
            hourly = st.number_input("Hourly Billing Rate ($/hr)", value=95.0 if "Dev" in agency else 85.0)
        with col2:
            milestone_fee = st.number_input("Fixed Milestone Fee ($)", value=4500.0)
            retainer = st.number_input("Monthly Retainer Fee ($/mo)", value=3500.0)

        st.session_state.rate_card = {
            "type": rate_type,
            "hourly_rate": hourly,
            "milestone_fee": milestone_fee,
            "retainer_monthly": retainer,
            "currency": "USD ($)",
            "status": "Draft Pre-Configured"
        }

        st.success(f"✅ Draft Rate Card generated ({rate_type}: ${hourly}/hr | Milestone: ${milestone_fee} | Retainer: ${retainer}/mo).")
        st.info("💡 Note: Billing setup is prepared for later. You can create invoices anytime after logging hours in your workspace!")

        st.markdown("<hr style='border-color: #334155;'>", unsafe_allow_html=True)
        
        btn_col1, btn_col2, btn_col3 = st.columns([1, 2, 2])
        with btn_col1:
            if st.button("⬅ Back"):
                st.session_state.onboarding_step = 4
                st.rerun()
        with btn_col3:
            if st.button("🎉 Finish Setup & Launch Workspace", type="primary", use_container_width=True):
                st.session_state.onboarding_complete = True
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)
