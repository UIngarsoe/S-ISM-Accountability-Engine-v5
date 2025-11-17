#!/usr/bin/env python3
"""
SS'ISM Accountability Engine v5
Safe, evidence-based OSINT & accountability Streamlit prototype
Author: U Ingar Soe Myanmar/BURMA 2025
License: AGPL-3.0 (Justice Only — No Harm Amplification)

Purpose:
Document roles, events, allegations with sources; compute confidence; export JSON/MD; immutable proof hashes.
"""

import streamlit as st
import json
import hashlib
import datetime
from typing import List, Dict

st.set_page_config(page_title="SS'ISM Accountability Engine v5", layout="wide")

# -----------------------------
# Sample demonstration data (editable)
# -----------------------------

SAMPLE_PROFILES = {
    "khin_yi": {
        "id": "khin_yi",
        "name": "U Khin Yi",
        "summary": "Senior political actor with multiple government roles. This dataset contains allegations and public-source references, not criminal convictions.",
        "roles": [
            "USDP Chairman (2022–present)",
            "Myanmar Police Chief (2005–2011)",
            "Immigration Minister (2021–2022)"
        ],
        "events": [
            {
                "date": "2007-09-01",
                "title": "Saffron Crackdown (allegation)",
                "description": "Reported involvement in police responses to protests.",
                "sources": ["https://www.hrw.org/"],
                "confidence": 3
            },
        ],
        "allegations": [
            {
                "text": "Alleged direction of police crackdowns during the 2007 Saffron Revolution.",
                "sources": ["https://www.hrw.org/"],
                "confidence": 3
            }
        ],
        "legal_tags": ["human_rights", "public_official"],
        "notes": "All entries should be evidence-cited. This is a demo profile."
    }
}

# -----------------------------
# Utilities
# -----------------------------


def compute_confidence_score(items: List[Dict]) -> float:
    """Compute simple average confidence among provided items (1-5 scale)."""
    if not items:
        return 0.0
    total = sum(item.get("confidence", 1) for item in items)
    return round(total / len(items), 2)


def generate_proof_hash(profile: Dict) -> str:
    payload = json.dumps(profile, sort_keys=True, ensure_ascii=False).encode()
    return hashlib.sha256(payload).hexdigest()


from datetime import datetime, timezone   # add this import

# ... rest of your code ...

def profile_to_markdown(profile: Dict) -> str:
    md = [f"# Accountability Profile: {profile.get('name', 'Unknown')}", ""]
    md.append(f"Summary: {profile.get('summary', '')}")
    md.append("")
    md.append("## Roles")
    for r in profile.get('roles', []):
        md.append(f"- {r}")
    md.append("")
    md.append("## Events")
    for e in profile.get('events', []):
        md.append(f"- {e.get('date', '?')}: {e.get('title', '')} — {e.get('description', '')}")
        if e.get('sources'):
            md.append(f"  Sources: {', '.join(e.get('sources'))}")
        md.append(f"  Confidence: {e.get('confidence', 1)}")
        md.append("")
    md.append("## Allegations")
    for a in profile.get('allegations', []):
        md.append(f"- {a.get('text', '')}")
        if a.get('sources'):
            md.append(f"  Sources: {', '.join(a.get('sources'))}")
        md.append(f"  Confidence: {a.get('confidence', 1)}")
        md.append("")
    md.append("## Legal Tags")
    md.append(', '.join(profile.get('legal_tags', [])))
    md.append("")
    md.append("---")
    md.append(f"Proof Hash: {generate_proof_hash(profile)}")
    md.append(f"Generated: {datetime.now(timezone.utc).isoformat()}")
    return "\n".join(md)


st.rerun()

# -----------------------------
# App Layout
# -----------------------------

st.title("SS'ISM Accountability Engine — v5 (Safe OSINT)")
st.caption("Documenting public-source evidence, computing confidence, and exporting defensible profiles.")

col1, col2 = st.columns([2, 1])

with col2:
    st.header("Quick Actions")
    action = st.selectbox("Action", ["View profile", "Create new profile", "Import JSON", "Export all JSON"])
    st.markdown("---")

with col1:
    if action == "View profile":
        st.subheader("Profiles")
        profile_keys = list(SAMPLE_PROFILES.keys())
        selected = st.selectbox("Select profile", profile_keys)
        profile = SAMPLE_PROFILES[selected]

        st.markdown("### Summary")
        st.write(profile.get('summary'))

        st.markdown("### Roles")
        for r in profile.get('roles', []):
            st.write(f"- {r}")

        st.markdown("### Events")
        for e in profile.get('events', []):
            st.write(f"- **{e.get('date', '?')}** {e.get('title', '')}")
            st.write(e.get('description', ''))
            if e.get('sources'):
                st.markdown(f"Sources: {', '.join(e.get('sources'))}")
            st.write(f"Confidence: {e.get('confidence', 1)}")

        st.markdown("### Allegations")
        for a in profile.get('allegations', []):
            st.write(f"- {a.get('text', '')}")
            if a.get('sources'):
                st.write(f"Sources: {', '.join(a.get('sources'))}")
            st.write(f"Confidence: {a.get('confidence', 1)}")

        st.markdown("---")
        conf_score = compute_confidence_score(profile.get('events', []) + profile.get('allegations', []))
        st.metric("Confidence Score (1-5)", conf_score)

        proof = generate_proof_hash(profile)
        st.code(f"Proof SHA256: {proof}")

        md = profile_to_markdown(profile)
        st.download_button("Download profile (Markdown)", md, file_name=f"{profile.get('id')}_profile.md")
        st.download_button("Download profile (JSON)", json.dumps(profile, ensure_ascii=False, indent=2), file_name=f"{profile.get('id')}_profile.json")

    elif action == "Create new profile":
        st.subheader("Create a new accountability profile")
        with st.form("create_profile"):
            pid = st.text_input("Profile ID (short, no spaces)")
            name = st.text_input("Full name")
            summary = st.text_area("Summary / description")
            roles_input = st.text_area("Roles (one per line)")
            notes = st.text_area("Notes / editorial guidance")
            legal_tags = st.multiselect(
                "Legal tags",
                ["human_rights", "war_crimes", "public_official", "sanctions_candidate", "other"]
            )

            submitted = st.form_submit_button("Create profile")
            if submitted:
                roles = [r.strip() for r in roles_input.splitlines() if r.strip()]
                new_profile = {
                    "id": pid,
                    "name": name,
                    "summary": summary,
                    "roles": roles,
                    "events": [],
                    "allegations": [],
                    "legal_tags": legal_tags,
                    "notes": notes
                }
                SAMPLE_PROFILES[pid] = new_profile
                st.success(f"Profile {pid} created. Use 'View profile' to edit and add events.")

    elif action == "Import JSON":
        st.subheader("Import JSON file (profile or profiles)")
        uploaded = st.file_uploader("Upload JSON", type=["json"])
        if uploaded is not None:
            try:
                data = json.load(uploaded)
                if isinstance(data, dict):
                    # assume single profile or dict of profiles
                    if data.get('id'):
                        SAMPLE_PROFILES[data['id']] = data
                        st.success(f"Imported profile {data['id']}")
                    else:
                        # assume multiple
                        for k, v in data.items():
                            SAMPLE_PROFILES[k] = v
                        st.success(f"Imported {len(data)} profiles")
                else:
                    st.error("JSON must contain a profile dict or a dict of profiles.")
            except Exception as e:
                st.error(f"Invalid JSON: {e}")

    elif action == "Export all JSON":
        st.subheader("Export all profiles as JSON")
        all_json = json.dumps(SAMPLE_PROFILES, ensure_ascii=False, indent=2)
        st.download_button("Download all profiles (JSON)", all_json, file_name="ssism_profiles_export.json")

# -----------------------------
# Sidebar: edit selected profile (simple editor)
# -----------------------------

st.sidebar.header("Profile Editor")
selected_profile = st.sidebar.selectbox("Select profile to edit", list(SAMPLE_PROFILES.keys()))
profile = SAMPLE_PROFILES[selected_profile]

st.sidebar.markdown("Add event")
with st.sidebar.form("add_event_form"):
    e_date = st.date_input("Event date", value=None)
    e_title = st.text_input("Event title")
    e_desc = st.text_area("Description")
    e_sources = st.text_area("Sources (one per line)")
    e_conf = st.slider("Confidence", 1, 5, 3)
    add_event = st.form_submit_button("Add event")
    if add_event:
        event = {
            "date": e_date.isoformat() if e_date else "",
            "title": e_title,
            "description": e_desc,
            "sources": [s.strip() for s in e_sources.splitlines() if s.strip()],
            "confidence": e_conf
        }
        profile.setdefault('events', []).append(event)
        SAMPLE_PROFILES[selected_profile] = profile
        st.experimental_rerun()

st.sidebar.markdown("Add allegation")
with st.sidebar.form("add_allegation_form"):
    a_text = st.text_area("Allegation text")
    a_sources = st.text_area("Sources (one per line)")
    a_conf = st.slider("Confidence", 1, 5, 3, key='al_conf')
    add_alleg = st.form_submit_button("Add allegation")
    if add_alleg:
        allegation = {
            "text": a_text,
            "sources": [s.strip() for s in a_sources.splitlines() if s.strip()],
            "confidence": a_conf
        }
        profile.setdefault('allegations', []).append(allegation)
        SAMPLE_PROFILES[selected_profile] = profile
        st.experimental_rerun()

st.sidebar.markdown("---")
if st.sidebar.button("Compute proof hash for selected profile"):
    proof = generate_proof_hash(profile)
    st.sidebar.code(proof)

st.sidebar.markdown("---")

# -----------------------------
# Footer / Guidance
# -----------------------------

st.markdown("---")
st.caption("Guidance: All entries should be supported by public-source evidence. This tool is for documentation and accountability. Avoid operational or targeted content that may endanger civilians.")
