from __future__ import annotations

import json

import requests

try:
    import streamlit as st
except ModuleNotFoundError:  # pragma: no cover - local fallback for environments without Streamlit
    class _MissingStreamlit:
        def __getattr__(self, name):
            raise RuntimeError(
                "Streamlit is not installed in this Python environment. "
                "Install the project requirements to run the UI."
            )

    st = _MissingStreamlit()

API_URL = "http://127.0.0.1:8000/summarize-meeting"

SAMPLE_TRANSCRIPTS = {
    "Project update": (
        "James Miller: The team will finalize the roadmap by Friday. "
        "Alice will send the design notes by Thursday. "
        "We decided to ship the first milestone next week."
    ),
    "Decision review": (
        "The team agreed to use the transformer model. "
        "Priya will share the infrastructure requirements by Monday. "
        "Robert approved the rollout plan."
    ),
}


def _inject_styles() -> None:
    st.markdown(
        """
        <style>
        .stApp {
            background:
                radial-gradient(circle at top left, rgba(15, 118, 110, 0.18), transparent 30%),
                radial-gradient(circle at top right, rgba(2, 132, 199, 0.16), transparent 28%),
                linear-gradient(180deg, #f8fafc 0%, #eef2ff 100%);
        }
        .hero {
            padding: 2rem 2rem 1.6rem 2rem;
            border-radius: 24px;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 55%, #0f766e 100%);
            color: white;
            box-shadow: 0 20px 60px rgba(15, 23, 42, 0.25);
            border: 1px solid rgba(255, 255, 255, 0.08);
        }
        .hero h1 {
            margin: 0;
            font-size: 2.4rem;
            line-height: 1.1;
        }
        .hero p {
            margin-top: 0.75rem;
            margin-bottom: 0;
            max-width: 760px;
            color: rgba(255, 255, 255, 0.85);
            font-size: 1.02rem;
        }
        .card {
            background: rgba(255, 255, 255, 0.88);
            border: 1px solid rgba(148, 163, 184, 0.25);
            border-radius: 20px;
            padding: 1.1rem 1.2rem;
            box-shadow: 0 14px 40px rgba(15, 23, 42, 0.08);
        }
        .metric-label {
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: #64748b;
            margin-bottom: 0.2rem;
        }
        .metric-value {
            font-size: 1.3rem;
            font-weight: 700;
            color: #0f172a;
        }
        .section-title {
            font-size: 1.02rem;
            font-weight: 700;
            color: #0f172a;
            margin: 0 0 0.75rem 0;
        }
        .subtle {
            color: #475569;
            font-size: 0.95rem;
        }
        .result-box {
            background: rgba(255, 255, 255, 0.92);
            border-radius: 18px;
            padding: 1rem 1.1rem;
            border: 1px solid rgba(148, 163, 184, 0.2);
            box-shadow: 0 12px 30px rgba(15, 23, 42, 0.06);
        }
        .tag {
            display: inline-block;
            padding: 0.28rem 0.65rem;
            border-radius: 999px;
            background: #e2e8f0;
            color: #0f172a;
            font-size: 0.78rem;
            margin-right: 0.35rem;
            margin-bottom: 0.35rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _render_hero() -> None:
    st.markdown(
        """
        <div class="hero">
            <h1>Meeting Intelligence Assistant</h1>
            <p>
                Turn long meeting transcripts into concise summaries, action items,
                and key decisions with a cleaner, more visual workflow.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_metric(label: str, value: str) -> None:
    st.markdown(
        f"""
        <div class="card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_tags(items: list[str]) -> None:
    if not items:
        st.write("No items found.")
        return

    tags = "".join(f'<span class="tag">{item}</span>' for item in items)
    st.markdown(tags, unsafe_allow_html=True)


def _load_sample(name: str) -> str:
    return SAMPLE_TRANSCRIPTS.get(name, "")


def main() -> None:
    st.set_page_config(
        page_title="Meeting Intelligence Assistant",
        page_icon="AI",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    _inject_styles()
    _render_hero()

    st.markdown("<div style='height: 1rem'></div>", unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("### Controls")
        sample_name = st.selectbox("Load a sample transcript", ["Custom"] + list(SAMPLE_TRANSCRIPTS.keys()))
        st.caption("Use a sample to preview the analysis experience quickly.")

        if sample_name != "Custom":
            if st.button("Load sample transcript", use_container_width=True):
                st.session_state["transcript"] = _load_sample(sample_name)

        st.divider()
        st.markdown("### Input tips")
        st.write("• Paste the full transcript, even if it is long.")
        st.write("• Use speakers and dates for better extraction.")
        st.write("• The backend now handles chunking with overlap.")

    col1, col2, col3 = st.columns(3)
    with col1:
        _render_metric("Mode", "Meeting analysis")
    with col2:
        _render_metric("Output", "Summary + actions")
    with col3:
        _render_metric("Backend", "FastAPI")

    st.markdown("<div style='height: 0.75rem'></div>", unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Transcript</div>', unsafe_allow_html=True)
    transcript = st.text_area(
        "Paste Meeting Transcript",
        value=st.session_state.get("transcript", ""),
        height=320,
        placeholder="Paste your meeting notes here. You can include multiple speakers, decisions, and deadlines.",
        label_visibility="collapsed",
    )

    uploaded_file = st.file_uploader(
        "Optional: upload a .txt file",
        type=["txt"],
        accept_multiple_files=False,
        label_visibility="collapsed",
    )
    if uploaded_file is not None:
        file_text = uploaded_file.read().decode("utf-8", errors="replace")
        if file_text:
            transcript = file_text
            st.session_state["transcript"] = file_text
            st.info("Loaded transcript from file upload.")

    action_col, clear_col = st.columns([1, 1])
    with action_col:
        analyze_clicked = st.button("Analyze Meeting", type="primary", use_container_width=True)
    with clear_col:
        if st.button("Clear Transcript", use_container_width=True):
            st.session_state["transcript"] = ""
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    if analyze_clicked:
        if not transcript.strip():
            st.error("Please enter a meeting transcript.")
            return

        payload = {"transcript": transcript}

        with st.spinner("Analyzing meeting..."):
            try:
                response = requests.post(API_URL, json=payload, timeout=120)
                response.raise_for_status()
            except requests.RequestException as exc:
                st.error(f"Could not reach the API: {exc}")
                return

        result = response.json()
        data = result.get("data", {})

        summary = data.get("meeting_summary", "")
        action_items = data.get("action_items", [])
        decisions = data.get("key_decisions", [])
        processing_time = data.get("processing_time_seconds", 0)

        st.markdown("<div style='height: 1rem'></div>", unsafe_allow_html=True)
        left, right = st.columns([1.3, 1])

        with left:
            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.markdown("### Meeting Summary")
            st.write(summary or "No summary returned.")
            st.markdown("</div>", unsafe_allow_html=True)

        with right:
            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.markdown("### Overview")
            st.metric("Action items", len(action_items))
            st.metric("Decisions", len(decisions))
            st.metric("Processing time", f"{processing_time} s")
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div style='height: 1rem'></div>", unsafe_allow_html=True)
        items_col, decisions_col = st.columns(2)

        with items_col:
            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.markdown("### Action Items")
            if action_items:
                for item in action_items:
                    st.markdown(
                        f"""
                        <div style="margin-bottom: 0.8rem; padding: 0.85rem; border-radius: 14px; background: #f8fafc; border: 1px solid #e2e8f0;">
                            <strong>{item.get('owner', '') or 'Unassigned'}</strong><br/>
                            <span class="subtle">{item.get('task', '')}</span><br/>
                            <small>Deadline: {item.get('deadline', '') or 'Not specified'}</small>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
            else:
                st.write("No action items detected.")
            st.markdown("</div>", unsafe_allow_html=True)

        with decisions_col:
            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.markdown("### Key Decisions")
            if decisions:
                for decision in decisions:
                    st.markdown(f"- {decision}")
            else:
                st.write("No decisions detected.")
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div style='height: 1rem'></div>", unsafe_allow_html=True)
        with st.expander("Raw response"):
            st.json(result)

    st.markdown("<div style='height: 1rem'></div>", unsafe_allow_html=True)
    st.markdown("### Example outputs")
    preview_cols = st.columns(2)
    with preview_cols[0]:
        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        st.markdown("#### Sample transcript themes")
        _render_tags(["Release planning", "Deadlines", "Owners", "Decisions"])
        st.markdown("</div>", unsafe_allow_html=True)

    with preview_cols[1]:
        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        st.markdown("#### Supported inputs")
        st.write("• Plain meeting text")
        st.write("• Long transcripts with multiple speakers")
        st.write("• Pasted multiline notes")
        st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
