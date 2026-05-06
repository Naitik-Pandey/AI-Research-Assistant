import os
os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"

import streamlit as st
from crewai import Crew, Process
from agents import ResearchAgents
from tasks import ResearchTasks

st.set_page_config(page_title="AI Research Assistant", page_icon="🤖", layout="wide")

st.title("🤖 AI Research Assistant")
st.markdown("---")

with st.sidebar:
    st.header("Project Configuration")
    topic = st.text_input("Research Topic", placeholder="e.g., Medical Imaging CNNs")
    st.info("Compute: Local NVIDIA Graphic Card(Ollama)")
    
    uploaded_file = st.file_uploader("Upload Primary Research PDF", type=["pdf"])
    if uploaded_file:
        target_dir = r"E:\Research Assistant\research_papers"
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        
        # Consistent filename for easy agent access
        file_path = os.path.join(target_dir, "current_research.pdf")
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success("PDF uploaded and indexed!")

if st.button("Initialize AI Research Assistant "):
    if not topic:
        st.error("Please provide a research topic.")
    else:
        with st.status("Initiated...", expanded=True) as status:
            agents = ResearchAgents()
            tasks = ResearchTasks()
            
            # Setup Agents & Tasks
            librarian = agents.librarian_agent()
            scout = agents.scout_agent()
            editor = agents.editor_agent()
            
            t1 = tasks.analysis_task(librarian)
            t2 = tasks.validation_task(scout)
            t3 = tasks.report_task(editor, context=[t1, t2])
            
            # Crew setup optimized for 8GB RAM
            crew = Crew(
                agents=[librarian, scout, editor],
                tasks=[t1, t2, t3],
                process=Process.sequential,
                verbose=True,
                memory=False # Disabled to avoid OpenAI 401 errors
            )
            
            result = crew.kickoff(inputs={'topic': topic})
            status.update(label="✅ Research Complete!", state="complete")

        st.subheader("📝 Final Research Report")
        st.markdown(result)
        st.download_button("Download MD", data=str(result), file_name="report.md")