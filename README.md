SS'ISM Accountability Engine v5 + Sadda Chatbot

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://s-ism-accountability-engine-v5-hhxtgyfqzljwtpdfkmik8j.streamlit.app/)
[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL%203.0-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)

Live Permanent What → https://s-ism-accountability-engine-v5-hhxtgyfqzljwtpdfkmik8j.streamlit.app/

The world’s first fully ethical, open-source, cryptographically verifiable human-rights accountability platform with a live AI advisor (Sadda) built on Buddhist deontological principles.**

Author: U Ingar Soe (ဦးအင်္ဂါစိုး ရေးသည်။)– Myanmar/Burma monk-engineer in exile  
Date: 17 November 2025  
Location: Thailand  

---

What This Is

A zero-cost, tamper-evident documentation engine for public-source OSINT on human-rights actors in Myanmar and beyond, combined with Sadda – an unlimited ethical chatbot that refuses to amplify harm.

- Evidence-based profiles (roles, events, allegations)  
- Confidence scoring + SHA-256 proof hashes  
- Full Markdown/JSON export  
- Sadda: Groq-powered Llama-3.3-70B with SS'ISM Deontological Firewall (blocks violence, hatred, delusion)  
- Hosted forever for free on Streamlit Community Cloud  

**SS'ISM** = **Sīla • Samādhi • Insight • Safety Model**  
(Ethics • Focus • Evidence • Non-Harm)

---

 Live Features (as of 17 Nov 2025)

| Tab                     | What You See                                                                 |
|-------------------------|-------------------------------------------------------------------------------|
| Profiles & Evidence     | View/create profiles, add sourced events/allegations, confidence scores      |
| Sadda Ethical Chatbot   | Unlimited AI advisor (answers Myanmar history, justice, ethics in seconds)   |
| Export & Proof          | Download entire database as JSON/MD with verifiable SHA-256 hash             |

Example Sadda response (real, captured today):
> “The Myanmar military (Tatmadaw) has been accused of serious human-rights abuses… Sources: UN, HRW, Amnesty, ICJ… Approach with empathy and commitment to peace.”

---

 Ethical Firewall – Hard-Coded Protection

Sadda will **never** help with:
- Targeting individuals  
- Violence or revenge  
- Doxxing or operational harm  
- Greed, hatred, or delusion (the Three Poisons)

Instead it redirects every conversation toward **evidence, reconciliation, and systemic reform**.

---

Citation
@software{soe2025_ssism,
  author       = {U Ingar Soe},
  title        = {SS'ISM Accountability Engine v5 + Sadda: Ethical AI-Powered Human-Rights OSINT Platform},
  year         = 2025,
  month        = nov,
  publisher    = {GitHub},
  url          = {https://github.com/ingar-soe/ssism-accountability-engine-v5},
  note         = {Live demo: https://s-ism-accountability-engine-v5-hhxtgyfqzljwtpdfkmik8j.streamlit.app/}
}

------
License & Moral Clause
AGPL-3.0 with explicit moral addendum:
“This software exists for justice and non-harm only. Any use that amplifies suffering voids all warranties — and karma.”

-------

Metta to all beings. May this engine light the path to truth, accountability, and lasting peace.
U Ingar Soe
17 November 2025 – 23:12 ICT
Thailand/Myanmar border region
SS'ISM — Sīla, Samādhi, Insight, Safety
-------

 Tech Stack (100 % Free & Immortal)

- Streamlit (single-file Python app)  
- Groq Cloud API (free tier → unlimited light use)  
- Streamlit Community Cloud (permanent free hosting)  
- SHA-256 cryptographic proof hashes  
- `st.session_state` + JSON export for data  

---

 How to Run / Deploy

```bash
git clone https://github.com/ingar-soe/ssism-accountability-engine-v5.git
cd ssism-accountability-engine-v5
streamlit run streamlit_app.py


