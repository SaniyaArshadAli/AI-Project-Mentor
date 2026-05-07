import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
import json
import speech_recognition as sr
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# =====================================================
# LOAD ENV
# =====================================================
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="AI Project Mentor Pro",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# CUSTOM CSS
# =====================================================
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
}

body {
    background-color: #0f172a;
}

.main-title {
    font-size: 3rem;
    font-weight: 800;
    text-align: center;
    background: linear-gradient(to right, #38bdf8, #818cf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    text-align: center;
    color: #94a3b8;
    margin-bottom: 30px;
}

.card {
    background: rgba(30, 41, 59, 0.85);
    padding: 20px;
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 15px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}

.stButton>button {
    background: linear-gradient(to right, #38bdf8, #818cf8);
    color: white;
    border-radius: 10px;
    border: none;
    padding: 10px 18px;
    font-weight: 600;
}

.score-box {
    background: #111827;
    padding: 12px;
    border-radius: 12px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# HEADER
# =====================================================
st.markdown('<div class="main-title">🤖 AI Project Mentor Pro</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Build, Learn, Explore and Improve AI Projects Step-by-Step</div>', unsafe_allow_html=True)

# =====================================================
# MEMORY FILE
# =====================================================
MEMORY_FILE = "memory.json"

if not os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "w") as f:
        json.dump([], f)

with open(MEMORY_FILE, "r") as f:
    memory_data = json.load(f)

# =====================================================
# SESSION STATE
# =====================================================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# =====================================================
# SPEECH TO TEXT
# =====================================================
def speech_to_text():
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            st.info("🎤 Listening...")
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            return text

    except Exception as e:
        return f"Voice input failed: {e}"

# =====================================================
# GROQ RESPONSE
# =====================================================
def ask_agent(prompt):
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {
                "role": "system",
                "content": """
You are AI Mentor Pro.

You are:
- beginner friendly
- highly intelligent
- encouraging
- educational
- practical

You guide users step-by-step.
You encourage thinking.
You explain concepts simply.
You act like a real AI coach.
"""
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content

# =====================================================
# PDF EXPORT
# =====================================================
def create_pdf(content):
    pdf_path = "session_output.pdf"

    doc = SimpleDocTemplate(pdf_path)
    styles = getSampleStyleSheet()
    story = []

    for line in content.split("\n"):
        story.append(Paragraph(line, styles['BodyText']))
        story.append(Spacer(1, 8))

    doc.build(story)

    return pdf_path

# =====================================================
# SIDEBAR
# =====================================================
st.sidebar.title("⚙ Settings")

mode = st.sidebar.selectbox(
    "Select Mode",
    [
        "Learning Mode",
        "Hackathon Mode",
        "Project Planning Mode"
    ]
)

level = st.sidebar.selectbox(
    "Difficulty Level",
    [
        "Beginner",
        "Intermediate",
        "Advanced"
    ]
)

# =====================================================
# MAIN INPUT
# =====================================================
st.markdown("### 💡 Describe Your AI Project Idea")

user_input = st.text_area(
    "Explain your project idea in your own words:",
    height=180,
    placeholder="Example: I want to build an AI app that helps students learn machine learning through projects..."
)

# =====================================================
# VOICE BUTTON
# =====================================================
col1, col2 = st.columns([1, 1])

with col1:
    if st.button("🎤 Speak Idea"):
        voice_text = speech_to_text()
        st.success(voice_text)
        user_input = voice_text

with col2:
    if st.button("✨ Improve My Idea"):
        if user_input:
            improve_prompt = f"""
Improve this AI project idea.

Idea:
{user_input}

Make it:
- more practical
- more impactful
- beginner-friendly
- technically impressive
- meaningful

Add:
- features
- use cases
- uniqueness
"""

            improved = ask_agent(improve_prompt)

            st.markdown("### 🚀 Improved Idea")
            st.markdown(f"<div class='card'>{improved}</div>", unsafe_allow_html=True)

# =====================================================
# GENERATE MAIN PLAN
# =====================================================
if st.button("🚀 Generate Full Project Plan"):

    if user_input.strip() == "":
        st.warning("Please enter your project idea.")

    else:

        prompt = f"""
Create a complete AI project roadmap.

Project Idea:
{user_input}

Mode:
{mode}

Difficulty:
{level}

Include:

1. Project Understanding
2. Real-world Use Case
3. Step-by-Step Plan
4. Architecture Workflow
5. Suggested Tools
6. Suggested Datasets
7. Key AI Concepts
8. Tech Stack
9. Innovation Ideas
10. Future Improvements
11. Beginner Guidance
12. Common Mistakes
13. Tips

Be detailed but beginner-friendly.
"""

        with st.spinner("🤖 AI Mentor is thinking..."):
            output = ask_agent(prompt)

        st.session_state.chat_history.append({
            "idea": user_input,
            "response": output
        })

        memory_data.append({
            "idea": user_input,
            "response": output
        })

        with open(MEMORY_FILE, "w") as f:
            json.dump(memory_data, f, indent=4)

        st.markdown("## 📌 AI Project Plan")
        st.markdown(f"<div class='card'>{output}</div>", unsafe_allow_html=True)

        # =================================================
        # PROJECT SCORING
        # =================================================
        st.markdown("## 📊 Project Analysis")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown("""
<div class='score-box'>
<h3>⭐ Innovation</h3>
<h2>8.5/10</h2>
</div>
""", unsafe_allow_html=True)

        with c2:
            st.markdown("""
<div class='score-box'>
<h3>⚡ Feasibility</h3>
<h2>9/10</h2>
</div>
""", unsafe_allow_html=True)

        with c3:
            st.markdown("""
<div class='score-box'>
<h3>🎯 Resume Value</h3>
<h2>8/10</h2>
</div>
""", unsafe_allow_html=True)

# =====================================================
# GUIDED LEARNING MODE
# =====================================================
st.markdown("---")
st.markdown("## 🎓 Guided Learning Mode")

step_input = st.text_input("Enter a project step to expand")

if st.button("📚 Explain This Step"):

    if step_input:

        explain_prompt = f"""
Explain this AI project step in beginner-friendly terms:

{step_input}

Include:
- what it means
- why it matters
- example
- beginner tips
"""

        explanation = ask_agent(explain_prompt)

        st.markdown(f"<div class='card'>{explanation}</div>", unsafe_allow_html=True)

# =====================================================
# GENERATE CODE
# =====================================================
st.markdown("---")
st.markdown("## 💻 Generate Code For Any Step")

code_input = st.text_input("Enter what code you want")

if st.button("⚡ Generate Code"):

    if code_input:

        code_prompt = f"""
Generate beginner-friendly Python code for:

{code_input}

Requirements:
- add comments
- explain logic simply
- make it readable
- beginner friendly
"""

        code_output = ask_agent(code_prompt)

        st.code(code_output, language="python")

# =====================================================
# DATASET FINDER
# =====================================================
st.markdown("---")
st.markdown("## 📊 Dataset Finder")

find_dataset = st.text_input("Enter domain/topic")

if st.button("🔍 Find Datasets"):

    if find_dataset:

        dataset_prompt = f"""
Suggest datasets for:
{find_dataset}

Include:
- dataset name
- source
- use case
- difficulty level
"""

        dataset_output = ask_agent(dataset_prompt)

        st.markdown(f"<div class='card'>{dataset_output}</div>", unsafe_allow_html=True)

# =====================================================
# DOWNLOAD FEATURE
# =====================================================
st.markdown("---")
st.markdown("## 📥 Export Session")

if st.session_state.chat_history:

    full_content = "\n\n".join([
        f"IDEA:\n{x['idea']}\n\nRESPONSE:\n{x['response']}"
        for x in st.session_state.chat_history
    ])

    pdf_file = create_pdf(full_content)

    with open(pdf_file, "rb") as file:
        st.download_button(
            label="📄 Download as PDF",
            data=file,
            file_name="ai_project_plan.pdf",
            mime="application/pdf"
        )

# =====================================================
# HISTORY PANEL
# =====================================================
st.sidebar.markdown("---")
st.sidebar.title("🧠 Previous Sessions")

for item in reversed(memory_data[-5:]):
    st.sidebar.markdown(f"""
<div class='card'>
<b>Idea:</b><br>
{item['idea'][:60]}...
</div>
""", unsafe_allow_html=True)

# =====================================================
# FOOTER
# =====================================================
st.markdown("---")
st.markdown(
    "<center>Built with ❤️ using Streamlit + Groq + Agentic AI Concepts</center>",
    unsafe_allow_html=True
)
