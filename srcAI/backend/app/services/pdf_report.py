from pathlib import Path
from fastapi import HTTPException
from fpdf import FPDF

from ..config import REPORTS_DIR


def generate_pdf_report(analysis) -> str:
    try:
        Path(REPORTS_DIR).mkdir(exist_ok=True)
        pdf_path = f"{REPORTS_DIR}/cybersentinel_report_{analysis.case_id}.pdf"

        severity_rgb = {
            "Low": (40, 167, 69),
            "Medium": (255, 193, 7),
            "High": (220, 53, 69),
        }
        sev = analysis.severity or "Unknown"
        sev_color = severity_rgb.get(sev, (108, 117, 125))

        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_left_margin(10)
        pdf.set_right_margin(10)

        # Title
        pdf.set_font("Helvetica", "B", 18)
        pdf.cell(0, 12, "CyberSentinel Threat Analysis Report", ln=1, align='C')
        pdf.ln(5)
        
        # Metadata
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(40, 6, "Case ID:", 0, 0)
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 6, str(analysis.case_id), 0, 1)
        
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(40, 6, "Timestamp:", 0, 0)
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 6, str(analysis.timestamp), 0, 1)
        
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(40, 6, "Threat Type:", 0, 0)
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 6, str(analysis.threat_type), 0, 1)
        
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(40, 6, "Severity:", 0, 0)
        pdf.set_text_color(*sev_color)
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(0, 6, str(sev), 0, 1)
        pdf.set_text_color(0, 0, 0)
        
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(40, 6, "Token Usage:", 0, 0)
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 6, str(analysis.token_usage), 0, 1)

        # Scenario Section
        pdf.ln(5)
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, "Scenario", 0, 1)
        pdf.set_font("Helvetica", "", 10)
        scenario_text = str(analysis.scenario) if analysis.scenario else "No scenario provided"
        pdf.multi_cell(0, 5, scenario_text)

        # Analysis Section
        pdf.ln(3)
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, "Analysis", 0, 1)
        pdf.set_font("Helvetica", "", 10)
        analysis_text = str(analysis.analysis) if analysis.analysis else "No analysis provided"
        pdf.multi_cell(0, 5, analysis_text)

        # Recommendations Section
        pdf.ln(3)
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, "Recommendations", 0, 1)
        pdf.set_font("Helvetica", "", 10)
        recs = analysis.recommendations or ["No recommendations provided."]
        for idx, rec in enumerate(recs, 1):
            rec_text = f"{idx}. {str(rec)}"
            pdf.multi_cell(0, 5, rec_text)
            pdf.ln(1)

        # Context Sources Section
        pdf.ln(2)
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, "Context Sources", 0, 1)
        pdf.set_font("Helvetica", "", 10)
        sources = analysis.context_sources or []
        sources_text = ", ".join(str(s) for s in sources) if sources else "No specific sources cited"
        pdf.multi_cell(0, 5, sources_text)

        pdf.output(pdf_path)
        return pdf_path
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {e}")
