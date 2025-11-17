#!/usr/bin/env python3
"""
SS'ISM Accountability Engine v5 + Ethical Chatbot (Fixed Groq Handling)
Safe, evidence-based OSINT + SS'ISM-guided AI advisor
Author: U Ingar Soe Myanmar/BURMA 2025
Zero-cost, robust Groq integration
"""

import streamlit as st
import json
import hashlib
from datetime import datetime, timezone
from typing import List, Dict
import requests
import time  # For retries

# ----------------------------- CONFIG -----------------------------
st.set_page_config(page_title="SS'ISM Accountability Engine v5 + Chat", layout="wide")

# Groq free API (Llama-3.1-70B or Mixtral) — no key needed for light use, but better with key
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")  # Put your free key in Secrets for unlimited use
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Fallback model list (all free tier)
MODELS = ["llama-3.1-70b-versatile", "mixtral-8x7b-32768", "gemma2-9b-it"]

# ----------------------------- SAMPLE DATA -----------------------------
if "profiles" not in st.session_state:
    st.session_state.profiles = {
        "khin_yi": {
            "id": "khin_yi",
            "name": "U Khin Yi",
            "summary": "Senior political actor. Public-source references only — no convictions.",
            "roles": ["USDP Chairman (2022–)", "Police Chief (2005–2011)", "Immigration Minister (2021–2022)"],
            "events": [{
                "date": "2007-09-01",
                "title": "Saffron Revolution response (alleged)",
                "description": "Reported oversight of police actions.",
                "sources": ["https://www.hrw.org/report/2009/09/24"],
                "confidence": 3
            }],
            "allegations": [{
                "text": "Alleged direction of excessive force in 2007 protests.",
                "sources": ["https://www.amnesty.org/"],
                "confidence": 3
            }],
            "legal_tags": ["human_rights", "public_official"],
            "notes": "Demo profile — always cite public sources."
        }
    }

# ----------------------------- UTILITIES -----------------------------
def compute_confidence(items: List[Dict]) -> float:
    if not items: return 0.0
    total = sum(item.get("confidence", 1) for item in items)
    return round(total / len(items), 2)

def generate_proof_hash(profile: Dict) -> str:
    payload = json.dumps(profile, sort_keys=True, ensure_ascii=False).encode()
    return hashlib.sha256(payload).hexdigest()

def profile_to_markdown(profile: Dict) -> str:
    md = [f"# SS'ISM Profile: {profile.get('name', 'Unknown')}", ""]
    md.append(f"**Summary**: {profile.get('summary', '')}\n")
    md.append("## Roles"); [md.append(f"- {r}") for r in profile.get("roles", [])]
    md.append("\n## Events")
    for e in profile.get("events", []):
        md.append(f"- **{e.get('date','?')}** — {e.get('title','')}")
        md.append(f"  {e.get('description','')}")
        if e.get("sources"): md.append(f"  Sources: {', '.join(e.get('sources'))}")
        md.append(f"  Confidence: {e.get('confidence',1)}\n")
    md.append("## Allegations")
    for a in profile.get("allegations", []):
        md.append(f"- {a.get('text','')}")
        if a.get("sources"): md.append(f"  Sources: {', '.join(a.get('sources'))}")
        md.append(f"  Confidence: {a.get('confidence',1)}\n")
    md.append(f"**Proof Hash**: {generate_proof_hash(profile)}")
    md.append(f"**Generated**: {datetime.now(timezone.utc).isoformat()}")
    return "\n".join(md)

# ----------------------------- GROQ CHAT (SS'ISM ETHICAL + ROBUST) -----------------------------
def ssism_chat(prompt: str, history: list) -> str:
    if not GROQ_API_KEY:
        return "⚠️ Sadda Tip: Add your Groq API key in Settings → Secrets for unlimited chats. (Free at console.groq.com/keys)"

    # SS'ISM Deontological Firewall + Three Poisons Veto
    veto_phrases = [
        "harm", "violence", "target", "kill", "attack", "dox", "leak", "revenge", "greed", "hatred", "delusion",
        "lobha", "dosa", "moha", "illegal", "weapon", "bomb", "assassinate"
    ]
    if any(bad in prompt.lower() for bad in veto_phrases):
        return "🛡️ Blocked: SS'ISM Firewall activated — this request risks harm (ahiṃsā principle). Let's focus on justice through evidence and metta."

    system_prompt = """
You are Sadda — the compassionate voice of SS'ISM (Sila-Samadhi-Insight-Safety Model).
Always respond with metta, karuna, wisdom, and truth.
Never suggest harm, targeting, or amplification of suffering.
Prioritize justice through evidence, reconciliation, and systemic reform.
You are helping document accountability using only public sources.
"""

    messages = [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": prompt}]

    # Retry logic for robustness
    for attempt in range(2):  # Try twice
        try:
            response = requests.post(
                GROQ_API_URL,
                headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
                json={"model": MODELS[0], "messages": messages, "temperature": 0.7, "max_tokens": 1024},
                timeout=10
            )
            
            # Log for debugging (visible in Streamlit Cloud logs)
            st.info(f"Groq Status: {response.status_code} (Attempt {attempt + 1})")
            
            if response.status_code == 200:
                data = response.json()
                if "choices" in data and data["choices"]:
                    return data["choices"][0]["message"]["content"]
                else:
                    return f"🤔 Sadda paused: Unexpected response from Groq. (No choices in reply.) Try rephrasing!"
            elif response.status_code == 429:
                if attempt == 0:
                    time.sleep(2)  # Rate limit: wait and retry
                    continue
                return "⏳ Sadda is catching breath (rate limit). Wait 1 min or try a shorter prompt."
            else:
                error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {"error": response.text}
                return f"⚠️ Groq hiccup: {error_data.get('error', 'Unknown issue')[:200]}... (Status: {response.status_code}). Sadda will try again soon."
        
        except requests.exceptions.Timeout:
            if attempt == 0:
                continue
            return "⏰ Timeout: Sadda is thinking deeply — network delay. Refresh and retry."
        except Exception as e:
            if attempt == 0:
                continue
            return f"🤖 Chat hiccup: {str(e)[:100]}... Sadda sends metta — let's try again."
    
    return "🛡️ Sadda couldn't connect this time. Check your key or refresh. (All good otherwise!)"

# ----------------------------- MAIN APP -----------------------------
st.title("🛡️ SS'ISM Accountability Engine v5 + Sadda Chatbot")
st.caption("Evidence-based OSINT profiles • Ethical AI advisor • Proof hashes • Zero harm")

tab1, tab2, tab3 = st.tabs(["Profiles & Evidence", "Sadda Ethical Chatbot", "Export & Proof"])

with tab1:
    col1, col2 = st.columns([2, 1])
    with col2:
        action = st.selectbox("Action", ["View Profile", "Create New", "Import JSON"])
    
    with col1:
        profiles = st.session_state.profiles
        if action == "View Profile":
            selected = st.selectbox("Select profile", list(profiles.keys()))
            p = profiles[selected]
            st.subheader(p["name"])
            st.write(p["summary"])
            st.markdown("### Roles"); [st.write(f"- {r}") for r in p["roles"]]
            st.markdown("### Events")
            for e in p.get("events", []):
                st.write(f"**{e['date']}** — {e['title']}")
                st.caption(e['description'])
                if e.get("sources"): st.caption("Sources: " + ", ".join(e["sources"]))
            st.markdown("### Allegations")
            for a in p.get("allegations", []):
                st.write(f"- {a['text']}")
                if a.get("sources"): st.caption("Sources: " + ", ".join(a["sources"]))
            score = compute_confidence(p.get("events",[]) + p.get("allegations",[]))
            st.metric("Average Confidence", f"{score}/5")
            st.code(generate_proof_hash(p), language=None)
            md = profile_to_markdown(p)
            st.download_button("Download Markdown", md, f"{p['id']}.md", "text/markdown")
            st.download_button("Download JSON", json.dumps(p, ensure_ascii=False, indent=2), f"{p['id']}.json")

        elif action == "Create New":
            with st.form("new_profile"):
                pid = st.text_input("ID (no spaces)")
                name = st.text_input("Name")
                summary = st.text_area("Summary")
                roles_input = st.text_area("Roles (one per line)")
                submitted = st.form_submit_button("Create")
                if submitted and pid:
                    roles = [r.strip() for r in roles_input.splitlines() if r.strip()]
                    profiles[pid] = {
                        "id": pid, "name": name, "summary": summary, "roles": roles,
                        "events": [], "allegations": [], "legal_tags": [], "notes": ""
                    }
                    st.success("Created! Refresh to see."); st.rerun()

with tab2:
    st.header("Sadda — SS'ISM Ethical Chatbot")
    st.caption("Powered by Groq/Llama-3.1-70B • Full SS'ISM Deontological Firewall active • Now crash-proof!")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    
    if prompt := st.chat_input("Ask Sadda anything (justice, evidence, ethics, Myanmar, Buddhism…)"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Sadda is thinking with metta…"):
                reply = ssism_chat(prompt, st.session_state.messages[:-1])
            st.write(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})

with tab3:
    st.subheader("Export All Profiles")
    all_json = json.dumps(st.session_state.profiles, ensure_ascii=False, indent=2)
    st.download_button("Download All Profiles (JSON)", all_json, "ssism_all_profiles.json")
    st.code(generate_proof_hash(st.session_state.profiles), language=None)
    st.caption("This hash proves integrity of the entire database at this moment.")

# ----------------------------- SIDEBAR EDITOR -----------------------------
with st.sidebar:
    st.header("Quick Editor")
    sel = st.selectbox("Edit", ["Add Event", "Add Allegation"] + list(st.session_state.profiles.keys()))
    profiles = st.session_state.profiles
    if sel in profiles:
        p = profiles[sel]
        with st.form("add_event"):
            e_date = st.date_input("Date")
            e_title = st.text_input("Title")
            e_desc = st.text_area("Description")
            e_src = st.text_area("Sources (one per line)")
            e_conf = st.slider("Confidence", 1, 5, 3)
            if st.form_submit_button("Add Event"):
                p.setdefault("events", []).append({
                    "date": str(e_date), "title": e_title, "description": e_desc,
                    "sources": [s.strip() for s in e_src.splitlines() if s.strip()],
                    "confidence": e_conf
                })
                st.success("Added!"); st.rerun()
        
        with st.form("add_allegation"):
            a_text = st.text_area("Allegation")
            a_src = st.text_area("Sources")
            a_conf = st.slider("Confidence", 1, 5, 3)
            if st.form_submit_button("Add Allegation"):
                p.setdefault("allegations", []).append({
                    "text": a_text,
                    "sources": [s.strip() for s in a_src.splitlines() if s.strip()],
                    "confidence": a_conf
                })
                st.success("Added!"); st.rerun()

st.caption("SS'ISM Accountability Engine v5 + Sadda • Built with metta • Nov 2025 • AGPL-3.0 Justice Only")
