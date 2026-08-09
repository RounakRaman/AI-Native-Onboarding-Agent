import streamlit as st

def apply_custom_css():
    st.markdown("""
    <style>
    /* Google Fonts Import */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Gradient Header & Modern Glassmorphism */
    .stApp {
        background-color: #0F172A;
        color: #F8FAFC;
    }

    /* Glass Cards */
    .glass-card {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.36);
        transition: all 0.3s ease;
    }

    .glass-card:hover {
        border-color: rgba(99, 102, 241, 0.4);
        box-shadow: 0 12px 40px 0 rgba(99, 102, 241, 0.15);
    }

    /* Hero Banner */
    .copilot-hero {
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 50%, #2563EB 100%);
        border-radius: 18px;
        padding: 28px 32px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 10px 30px rgba(79, 70, 229, 0.3);
    }

    .copilot-hero h1 {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 8px;
        letter-spacing: -0.02em;
    }

    .copilot-hero p {
        font-size: 1.05rem;
        opacity: 0.92;
        margin: 0;
    }

    /* Badge & Pills */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .badge-primary {
        background-color: rgba(99, 102, 241, 0.2);
        color: #818CF8;
        border: 1px solid rgba(99, 102, 241, 0.4);
    }

    .badge-success {
        background-color: rgba(16, 185, 129, 0.2);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.4);
    }

    .badge-warning {
        background-color: rgba(245, 158, 11, 0.2);
        color: #FBBF24;
        border: 1px solid rgba(245, 158, 11, 0.4);
    }

    /* Step Indicator Progress Bar */
    .step-pill {
        padding: 10px 16px;
        border-radius: 10px;
        background: #1E293B;
        border: 1px solid #334155;
        color: #94A3B8;
        font-weight: 600;
        font-size: 0.85rem;
        text-align: center;
    }

    .step-pill-active {
        background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%);
        color: white;
        border-color: #818CF8;
        box-shadow: 0 4px 14px rgba(99, 102, 241, 0.35);
    }

    .step-pill-done {
        background: #065F46;
        color: #A7F3D0;
        border-color: #059669;
    }

    /* Task Card */
    .task-card {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }

    .task-card:hover {
        border-color: #6366F1;
        transform: translateY(-2px);
    }

    /* Sidebar RAG Chat Box */
    .rag-chat-container {
        background: #0F172A;
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 16px;
    }

    /* Hide standard Streamlit header & footer for clean app feel */
    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }
    footer {
        visibility: hidden;
    }
    </style>
    """, unsafe_allow_html=True)


def init_session_state():
    """Initialize application session state variables."""
    if "onboarding_complete" not in st.session_state:
        st.session_state.onboarding_complete = False

    if "onboarding_step" not in st.session_state:
        st.session_state.onboarding_step = 1

    # Intake answers
    if "intake_data" not in st.session_state:
        st.session_state.intake_data = {
            "agency_type": "Design Agency",
            "client_name": "Acme Corp",
            "project_shape": "Fixed-scope",
            "migration_source": "None"
        }

    # Imported Tasks Buffer
    if "imported_tasks" not in st.session_state:
        st.session_state.imported_tasks = []

    # Active Project
    if "active_project" not in st.session_state:
        st.session_state.active_project = None

    # Tasks List
    if "tasks" not in st.session_state:
        st.session_state.tasks = []

    # Team Members
    if "team_members" not in st.session_state:
        st.session_state.team_members = [
            {"name": "You (Account Owner)", "email": "owner@agency.com", "role": "Owner", "status": "Active"}
        ]

    # Rate Card / Billing State
    if "rate_card" not in st.session_state:
        st.session_state.rate_card = {
            "type": "Fixed Milestone",
            "hourly_rate": 85.0,
            "milestone_fee": 5000.0,
            "retainer_monthly": 3500.0,
            "currency": "USD ($)",
            "status": "Draft Pre-Configured"
        }

    # Time Logs
    if "time_logs" not in st.session_state:
        st.session_state.time_logs = []

    # RAG Chat Messages
    if "rag_messages" not in st.session_state:
        st.session_state.rag_messages = [
            {
                "role": "assistant",
                "content": "Hi! I'm Setup Copilot's grounded RAG assistant. Ask me anything about rate cards, project settings, inviting teammates, or time tracking!",
                "helpful": None
            }
        ]

    # Telemetry Data
    if "telemetry" not in st.session_state:
        st.session_state.telemetry = {
            "total_signups": 120,
            "control_signups": 60,
            "treatment_signups": 60,
            "control_activations": 15, # ~25% baseline
            "treatment_activations": 27, # ~45% target
            "first_actions_taken": True,
            "project_created": False,
            "teammate_invited": False,
            "first_task_completed": False,
            "support_tickets_raised": 2,
            "rag_questions_asked": 0,
            "rag_positive_feedback": 0
        }
