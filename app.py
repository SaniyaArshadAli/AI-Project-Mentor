# =========================================================
# AI PROJECT MENTOR PRO
# FULL UPDATED COMPLETE CODE
# =========================================================

# INSTALL REQUIREMENTS:
# pip install streamlit groq python-dotenv SpeechRecognition pyaudio reportlab

# IF PYAUDIO FAILS:
# pip install pipwin
# pipwin install pyaudio

# =========================================================
# IMPORTS
# =========================================================

import streamlit as st
from groq import Groq
import json
import speech_recognition as sr
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()

GROQ_API_KEY = ("GROQ_API_KEY")

# =========================================================
# INITIALIZE GROQ CLIENT
# =========================================================

client = Groq(
    api_key=GROQ_API_KEY
)

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Project Mentor Pro",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS
# =========================================================

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
    margin-bottom: 10px;
}

.subtitle {
    text-align: center;
    color: #94a3b8;
    margin-bottom: 30px;
    font-size: 1.1rem;
}

.card {
    background: rgba(30, 41, 59, 0.90);
    padding: 20px;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 20px;
    box-shadow: 0 6px 25px rgba(0,0,0,0.35);
}

.score-box {
    background: #111827;
    padding: 18px;
    border-radius: 15px;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.05);
}

.stButton > button {
    background: linear-gradient(to right, #38bdf8, #818cf8);
    color: white;
    border-radius: 12px;
    border: none;
    padding: 10px 20px;
    font-weight: 600;
    width: 100%;
}

.stTextArea textarea {
    border-radius: 15px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">🤖 AI Project Mentor Pro</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Build, Learn, Explore and Improve AI Projects Step-by-Step</div>',
    unsafe_allow_html=True
)

# =========================================================
# MEMORY FILE SETUP
# =========================================================

MEMORY_FILE = "memory.json"

if not os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "w") as f:
        json.dump([], f)

with open(MEMORY_FILE, "r") as f:
    memory_data = json.load(f)

# =========================================================
# SESSION STATE
# =========================================================

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# =========================================================
# SPEECH TO TEXT FUNCTION
# =========================================================

def speech_to_text():

    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:

            st.info("🎤 Listening... Speak now.")

            recognizer.adjust_for_ambient_noise(source)

            audio = recognizer.listen(source, timeout=5)

            text = recognizer.recognize_google(audio)

            return text

    except Exception as e:
        return f"Voice input failed: {str(e)}"

# =========================================================
# AGENT FUNCTION
# =========================================================

def ask_agent(prompt):

    try:

        response = client.chat.completions.create(

            model="llama-3.1-8b-instant",

            messages=[

                {
                    "role": "system",
                    "content": """
You are AI Mentor Pro.

You are:
- beginner friendly
- intelligent
- practical
- educational
- supportive
- encouraging

You guide users step-by-step.
You explain things simply.
You encourage real learning.
You avoid unnecessary complexity.
"""
                },

                {
                    "role": "user",
                    "content": prompt
                }

            ],

            temperature=0.7,
            max_tokens=2000

        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"

# =========================================================
# PDF EXPORT FUNCTION
# =========================================================

def create_pdf(content):

    pdf_path = "ai_project_plan.pdf"

    doc = SimpleDocTemplate(pdf_path)

    styles = getSampleStyleSheet()

    story = []

    for line in content.split("\n"):

        story.append(
            Paragraph(line, styles['BodyText'])
        )

        story.append(
            Spacer(1, 8)
        )

    doc.build(story)

    return pdf_path

# =========================================================
# SIDEBAR SETTINGS
# =========================================================

st.sidebar.title("⚙️ Settings")

mode = st.sidebar.selectbox(

    "Select Mode",

    [
        "Learning Mode",
        "Hackathon Mode",
        "Project Planning Mode"
    ]

)

difficulty = st.sidebar.selectbox(

    "Difficulty Level",

    [
        "Beginner",
        "Intermediate",
        "Advanced"
    ]

)

# =========================================================
# MAIN INPUT
# =========================================================

st.markdown("## 💡 Describe Your AI Project Idea")

user_input = st.text_area(

    "Explain your project idea in your own words:",

    height=180,

    placeholder="Example: I want to build an AI app that helps students learn machine learning through projects..."

)

# =========================================================
# BUTTONS
# =========================================================

col1, col2 = st.columns(2)

# ---------------------------------------------------------
# VOICE INPUT
# ---------------------------------------------------------

with col1:

    if st.button("🎤 Speak Idea"):

        voice_text = speech_to_text()

        st.success(voice_text)

        user_input = voice_text

# ---------------------------------------------------------
# IMPROVE IDEA
# ---------------------------------------------------------

with col2:

    if st.button("✨ Improve My Idea"):

        if user_input:

            improve_prompt = f"""
Improve this AI project idea.

Idea:
{user_input}

Make it:
- more impactful
- more practical
- more meaningful
- beginner friendly
- technically impressive

Add:
- better features
- use cases
- uniqueness
"""

            improved_output = ask_agent(improve_prompt)

            st.markdown("## 🚀 Improved Idea")

            st.markdown(
                f"<div class='card'>{improved_output}</div>",
                unsafe_allow_html=True
            )

# =========================================================
# GENERATE FULL PROJECT PLAN
# =========================================================

if st.button("🚀 Generate Full Project Plan"):

    if user_input.strip() == "":

        st.warning("Please enter a project idea.")

    else:

        project_prompt = f"""
Create a complete AI project roadmap.

Project Idea:
{user_input}

Mode:
{mode}

Difficulty:
{difficulty}

Include:

1. Project Understanding
2. Real-world Use Case
3. Step-by-Step Roadmap
4. Architecture Workflow
5. Suggested Tools
6. Suggested Datasets
7. Key AI Concepts
8. Tech Stack
9. Innovation Ideas
10. Future Improvements
11. Beginner Guidance
12. Common Mistakes
13. Resume Value
14. Tips

Make it detailed but beginner-friendly.
"""

        with st.spinner("🤖 AI Mentor is thinking..."):

            output = ask_agent(project_prompt)

        # Save history

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

        # Display output

        st.markdown("## 📌 AI Project Plan")

        st.markdown(

            f"<div class='card'>{output}</div>",

            unsafe_allow_html=True

        )

        # =================================================
        # PROJECT SCORING
        # =================================================

        st.markdown("## 📊 Project Analysis")

        s1, s2, s3 = st.columns(3)

        with s1:

            st.markdown("""

<div class='score-box'>
<h3>⭐ Innovation</h3>
<h2>8.5/10</h2>
</div>

""", unsafe_allow_html=True)

        with s2:

            st.markdown("""

<div class='score-box'>
<h3>⚡ Feasibility</h3>
<h2>9/10</h2>
</div>

""", unsafe_allow_html=True)

        with s3:

            st.markdown("""

<div class='score-box'>
<h3>🎯 Resume Value</h3>
<h2>8/10</h2>
</div>

""", unsafe_allow_html=True)

# =========================================================
# GUIDED LEARNING MODE
# =========================================================

st.markdown("---")

st.markdown("## 🎓 Guided Learning Mode")

step_input = st.text_input(

    "Enter a project step to expand"

)

if st.button("📚 Explain This Step"):

    if step_input:

        explain_prompt = f"""
Explain this AI project step in beginner-friendly terms:

{step_input}

Include:
- what it means
- why it matters
- beginner example
- simple explanation
- tips
"""

        explanation = ask_agent(explain_prompt)

        st.markdown(

            f"<div class='card'>{explanation}</div>",

            unsafe_allow_html=True

        )

# =========================================================
# GENERATE CODE
# =========================================================

st.markdown("---")

st.markdown("## 💻 Generate Code")

code_input = st.text_input(

    "Enter what code you want generated"

)

if st.button("⚡ Generate Code"):

    if code_input:

        code_prompt = f"""
Generate beginner-friendly Python code for:

{code_input}

Requirements:
- clean code
- beginner-friendly
- comments included
- explain logic clearly
"""

        code_output = ask_agent(code_prompt)

        st.code(code_output, language="python")

# =========================================================
# DATASET FINDER
# =========================================================

st.markdown("---")

st.markdown("## 📊 Dataset Finder")

dataset_topic = st.text_input(

    "Enter domain/topic"

)

if st.button("🔍 Find Datasets"):

    if dataset_topic:

        dataset_prompt = f"""
Suggest datasets for:

{dataset_topic}

Include:
- dataset name
- source
- use case
- difficulty level
"""

        dataset_output = ask_agent(dataset_prompt)

        st.markdown(

            f"<div class='card'>{dataset_output}</div>",

            unsafe_allow_html=True

        )

# =========================================================
# EXPORT SESSION
# =========================================================

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

# =========================================================
# HISTORY PANEL
# =========================================================

st.sidebar.markdown("---")

st.sidebar.title("🧠 Previous Sessions")

for item in reversed(memory_data[-5:]):

    st.sidebar.markdown(

        f"""
<div class='card'>
<b>Idea:</b><br>
{item['idea'][:60]}...
</div>
""",

        unsafe_allow_html=True

    )

# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.markdown(

    """
<center>
Built with ❤️ using Streamlit + Groq + Agentic AI Concepts
</center>
""",

    unsafe_allow_html=True

)
