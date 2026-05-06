import os
from dotenv import load_dotenv
from crewai import Crew, Process
from agents import ResearchAgents
from tasks import ResearchTasks

# Load API keys from .env
load_dotenv()

# Initialize our components
agents = ResearchAgents()
tasks = ResearchTasks()

# Setup Agents
librarian = agents.librarian_agent()
scout = agents.scout_agent()
editor = agents.editor_agent()

# Setup Tasks
task1 = tasks.analysis_task(librarian)
task2 = tasks.validation_task(scout)
task3 = tasks.report_task(editor, [task1, task2])

# Assemble the Crew
crew = Crew(
    agents=[librarian, scout, editor],
    tasks=[task1, task2, task3],
    process=Process.sequential, # One agent finishes, the next starts
    verbose=True
)

# START THE RESEARCH
print("## Starting Project Research Assistant...")
result = crew.kickoff(inputs={'topic': 'Convolutional Neural Networks (CNN)'})

print("\n\n########################")
print("## RESEARCH COMPLETE ##")
print("########################\n")
print(result)

