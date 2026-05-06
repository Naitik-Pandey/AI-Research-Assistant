import os
from dotenv import load_dotenv
from crewai import Agent, LLM
from crewai.tools import tool
from crewai_tools import SerperDevTool, DirectoryReadTool
from PyPDF2 import PdfReader

load_dotenv()

# Final system-level safety flags
os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"
os.environ["OPENAI_API_KEY"] = "NA" 

# Local LLM with optimized temperature for 8GB RAM
local_llm = LLM(
    model="ollama/llama3.2:3b",
    base_url="http://localhost:11434",
    temperature=0.1 # Lower temperature = more stable JSON
)

# --- ROBUST PDF TOOL ---
@tool("robust_pdf_reader")
def robust_pdf_reader(file_path: str) -> str:
    """Reads text from a PDF. Always use this for documents."""
    try:
        clean_path = file_path.strip().replace('"', '').replace("'", "")
        reader = PdfReader(clean_path)
        text = " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
        return text[:10000] # Limit context for 8GB RAM safety
    except Exception as e:
        return f"Read Error: {str(e)}"

# --- SEARCH TOOL INITIALIZATION ---
# Initialize the tool explicitly so the agent sees it as a function call
search_tool = SerperDevTool()

class ResearchAgents:
    def librarian_agent(self):
        return Agent(
            role='Knowledge Librarian',
            goal='Extract technical methodology from {topic} PDF.',
            backstory='Expert in academic analysis.',
            tools=[robust_pdf_reader],
            llm=local_llm,
            verbose=True,
            allow_delegation=False,
            max_iter=3
        )

    def scout_agent(self):
        return Agent(
            role='Internet Scout',
            goal='Execute search for 2026 data on {topic} using Serper.',
            backstory='Digital trend hunter.',
            tools=[search_tool], # Ensure this is passed correctly
            llm=local_llm,
            verbose=True,
            allow_delegation=False,
            max_iter=3
        )

    def editor_agent(self):
        return Agent(
            role='Research Editor',
            goal='Synthesize report from findings.',
            backstory='Final synthesizer.',
            llm=local_llm,
            verbose=True,
            allow_delegation=False
        )