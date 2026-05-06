from crewai import Task

class ResearchTasks:
    def analysis_task(self, agent):
        path = "E:/Research Assistant/research_papers/current_research.pdf"
        return Task(
            description=f"Use robust_pdf_reader to read '{path}'. Summarize findings for {{topic}}.",
            expected_output="A methodology and results summary from the PDF.",
            agent=agent
        )

    def validation_task(self, agent):
        return Task(
            description="Search the web for the latest 2026 developments on {topic}.",
            expected_output="3-5 recent updates.",
            agent=agent
        )

    def report_task(self, agent, context):
        return Task(
        description=(
            "Synthesize a highly technical report. Include a 'Comparative Analysis' section "
            "listing specific accuracy figures from the PDF and 2026 hardware specs from the web."
        ),
        expected_output="A technical 5-section Markdown report with data tables and 2026 references.",
        agent=agent,
        context=context
    )