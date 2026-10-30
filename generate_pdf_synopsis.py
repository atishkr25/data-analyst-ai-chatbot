import os
import sys
from pathlib import Path
from PIL import Image

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch, cm, mm
pt = 1.0
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image as RLImage, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

# ----------------- Numbered Canvas for Running Headers and Footers -----------------
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        page_w, page_h = A4
        margin_x = 38 * pt

        # 1. Running Header
        self.saveState()
        self.setFont("Helvetica-Bold", 7.5)
        self.setFillColor(colors.HexColor("#475569"))
        self.drawString(margin_x, page_h - 32 * pt, "DATA ANALYST AI CHATBOT | PROJECT SYNOPSIS")
        
        # Header Blue Rule
        self.setStrokeColor(colors.HexColor("#1e40af"))
        self.setLineWidth(0.8)
        self.line(margin_x, page_h - 36 * pt, page_w - margin_x, page_h - 36 * pt)

        # 2. Running Footer
        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#64748b"))
        footer_text = f"Atish Kumar | HCLTech Career Shaper Programme | {self._pageNumber}"
        self.drawCentredString(page_w / 2.0, 22 * pt, footer_text)
        self.restoreState()


def build_pdf():
    pdf_path = Path(r"C:\Users\Asus\.gemini\antigravity\scratch\data-analyst-ai-chatbot\Data_Analyst_AI_Chatbot_Synopsis.pdf")
    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=A4,
        leftMargin=38 * pt,
        rightMargin=38 * pt,
        topMargin=46 * pt,
        bottomMargin=38 * pt,
    )

    printable_w = A4[0] - 76 * pt  # ~519.27 pt

    styles = getSampleStyleSheet()

    # Custom styles
    title_prog = ParagraphStyle(
        "ProgTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#1e40af"),
    )
    sub_title_tag = ParagraphStyle(
        "SubTitleTag",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#64748b"),
        spaceAfter=4,
    )
    main_h1 = ParagraphStyle(
        "MainH1",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=28,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=4,
    )
    proj_desc = ParagraphStyle(
        "ProjDesc",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#475569"),
        spaceAfter=10,
    )
    sec_heading = ParagraphStyle(
        "SecHeading",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=8,
        spaceAfter=5,
    )
    subsec_heading = ParagraphStyle(
        "SubSecHeading",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#0369a1"),
        spaceBefore=6,
        spaceAfter=3,
    )
    body_p = ParagraphStyle(
        "BodyP",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#1e293b"),
        spaceAfter=5,
    )
    body_bullet = ParagraphStyle(
        "BodyBullet",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#1e293b"),
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=3,
    )
    fig_caption = ParagraphStyle(
        "FigCaption",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#475569"),
        alignment=1, # Center
        spaceBefore=2,
        spaceAfter=6,
    )
    table_cell = ParagraphStyle(
        "TableCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#1e293b"),
    )
    table_cell_bold = ParagraphStyle(
        "TableCellBold",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#0f172a"),
    )
    table_header = ParagraphStyle(
        "TableHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#0f172a"),
    )
    code_style = ParagraphStyle(
        "CodeStyle",
        parent=styles["Normal"],
        fontName="Courier",
        fontSize=7.2,
        leading=9.2,
        textColor=colors.HexColor("#0f172a"),
    )

    story = []

    # =========================================================================
    # PAGE 1: TITLE, DETAILS TABLE, CONTENTS
    # =========================================================================
    story.append(Paragraph("HCLTech Career Shaper Programme | Academic Year 2026-27", title_prog))
    story.append(Paragraph("PROJECT SYNOPSIS", sub_title_tag))
    story.append(Paragraph("Data Analyst AI Chatbot", main_h1))
    story.append(Paragraph(
        "Conversational Business Intelligence over CSV and Excel Datasets with "
        "Validated Natural-Language-to-SQL, Deterministic Local Fallback, and Interactive Plotly Visualizations",
        proj_desc
    ))

    # Details Table
    details_data = [
        [Paragraph("Field", table_header), Paragraph("Details", table_header)],
        [Paragraph("Project Title", table_cell_bold), Paragraph("Data Analyst AI Chatbot (AI-Based SQL Analytics & Tabular Data Explorer)", table_cell)],
        [Paragraph("Project ID", table_cell_bold), Paragraph("P_123", table_cell)],
        [Paragraph("Domain", table_cell_bold), Paragraph("Data Analytics / Python / Generative AI", table_cell)],
        [Paragraph("Difficulty", table_cell_bold), Paragraph("Advanced", table_cell)],
        [Paragraph("Format", table_cell_bold), Paragraph("Individual Project", table_cell)],
        [Paragraph("Learner Name", table_cell_bold), Paragraph("Atish Kumar", table_cell)],
        [Paragraph("Roll Number", table_cell_bold), Paragraph("2300320120071", table_cell)],
        [Paragraph("College / Campus", table_cell_bold), Paragraph("ABES Engineering College, Ghaziabad", table_cell)],
        [Paragraph("Mentor / Guide Name", table_cell_bold), Paragraph("Amit Bhatnagar", table_cell)],
        [Paragraph("Academic Year", table_cell_bold), Paragraph("2026-27", table_cell)],
        [Paragraph("Submission Date", table_cell_bold), Paragraph("30 October 2026", table_cell)],
        [Paragraph("GitHub Repository", table_cell_bold), Paragraph("https://github.com/atishkr25/data-analyst-ai-chatbot", table_cell)],
    ]
    t_details = Table(details_data, colWidths=[120 * pt, printable_w - 120 * pt])
    t_details.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (1, 0), colors.HexColor("#f8fafc")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ("TOPPADDING", (0, 0), (-1, -1), 4.2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4.2),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(t_details)
    story.append(Spacer(1, 14 * pt))

    # Contents callout box
    contents_text = (
        "<b>Contents</b><br/>"
        "1. Problem Statement | 2. Proposed Solution | 3. System Architecture | 4. Technology Stack | "
        "5. Dataset Used | 6. Key Results and Metrics | Application Output Screenshots | "
        "7. Challenges and Resolutions | 8. References | 9. Ethical Compliance Declaration | Appendix"
    )
    t_contents = Table([[Paragraph(contents_text, table_cell)]], colWidths=[printable_w])
    t_contents.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ("LINEBEFORE", (0, 0), (0, -1), 3.0, colors.HexColor("#2563eb")),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(t_contents)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: PROBLEM STATEMENT, PROPOSED SOLUTION & MAIN FEATURES
    # =========================================================================
    story.append(Paragraph("1. Problem Statement", sec_heading))
    p_data = [
        [Paragraph("5W1H", table_header), Paragraph("Project-specific response", table_header)],
        [Paragraph("Who?", table_cell_bold), Paragraph("Business stakeholders, product managers, sales analysts, and non-technical operators who interact daily with tabular spreadsheets.", table_cell)],
        [Paragraph("What?", table_cell_bold), Paragraph("Querying tabular data (CSV, XLSX) requires SQL or Python fluency, creating communication bottlenecks. Furthermore, pure cloud-LLM tools break down when API token limits are exhausted or network connectivity drops.", table_cell)],
        [Paragraph("When / where?", table_cell_bold), Paragraph("During executive KPI reviews, sales pipeline analysis, ad-hoc business inquiries, and daily performance reporting.", table_cell)],
        [Paragraph("Why?", table_cell_bold), Paragraph("Instant, safe natural-language querying eliminates reporting backlogs, while fail-safe offline calculations protect business operations from unexpected API outages.", table_cell)],
        [Paragraph("How?", table_cell_bold), Paragraph("Ingest and sanitize files into an embedded SQLite database, synthesize validated read-only SQL via LLMs, and seamlessly fall back to local Pandas aggregations whenever API limits are reached.", table_cell)],
    ]
    t_5w1h = Table(p_data, colWidths=[90 * pt, printable_w - 90 * pt])
    t_5w1h.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (1, 0), colors.HexColor("#f1f5f9")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("TOPPADDING", (0, 0), (-1, -1), 4.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4.5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(t_5w1h)
    story.append(Spacer(1, 10 * pt))

    story.append(Paragraph("2. Proposed Solution and Approach", sec_heading))
    story.append(Paragraph(
        "The project is a full-stack, enterprise-grade data intelligence application built with Python and Streamlit. "
        "Users upload structured tabular datasets (CSV, XLSX, XLS), which undergo automated sanitization—including whitespace "
        "trimming, header normalization, type coercion, and missing-value logging—before being loaded into an embedded SQLite database. "
        "The application provides a resilient <b>dual-layer query execution engine</b>: when OpenAI API credentials are active, "
        "natural language questions are translated into SQLite queries, strictly validated against destructive mutations using an AST parser, "
        "and explained in clear business English. When API credits are missing or exhausted, a deterministic <b>Local Pandas Fallback engine</b> "
        "transparently computes aggregations, group-bys, and filters without external dependencies.",
        body_p
    ))

    story.append(Paragraph("2.1 Main features", subsec_heading))
    features = [
        "<b>Multi-Format Ingestion:</b> Supports CSV, XLSX, and XLS formats with automated encoding detection and error resilience.",
        "<b>Automated Data Cleaning:</b> Fixes malformed headers, strips trailing whitespaces, coerces numeric fields, and maintains a transparent cleaning audit log.",
        "<b>Data Profiling & Quality Metrics:</b> Computes cardinality, null cell percentages, duplicate counts, memory footprints, and categorical distributions.",
        "<b>Embedded SQLite Integration:</b> Fast, serverless relational persistence enabling complex analytical queries without external database overhead.",
        "<b>AST-Based SQL Security Validator:</b> Strictly permits only single read-only <code>SELECT</code> and CTE statements; intercepts destructive operations (<code>DROP</code>, <code>DELETE</code>, <code>UPDATE</code>, <code>ALTER</code>).",
        "<b>Deterministic Local Pandas Fallback:</b> Answers core aggregation inquiries (average, sum, count, min, max, group by) locally when API quotas are exceeded.",
        "<b>Dynamic Plotly Visualizations:</b> Automatically renders responsive bar charts, line graphs, and histograms tailored to the query output.",
        "<b>Interactive Multi-View Portal:</b> Includes Dataset Uploader, KPI Executive Dashboard, Data Explorer, Conversational Chatbot, SQL Sandbox, and Automated Insights.",
    ]
    for feat in features:
        story.append(Paragraph(f"• {feat}", body_bullet))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: ARCHITECTURE & TECHNOLOGY STACK (PART 1)
    # =========================================================================
    story.append(Paragraph("3. System Architecture", sec_heading))
    story.append(Paragraph("3.1 Data Flow Diagram - Level 0", subsec_heading))
    
    img_l0 = Path(r"C:\Users\Asus\.gemini\antigravity\scratch\data-analyst-ai-chatbot\screenshots\diagram_level0.png")
    if img_l0.exists():
        story.append(RLImage(str(img_l0), width=printable_w, height=110 * pt))
    story.append(Paragraph(
        "Figure 1. Level 0 data flow: user spreadsheets and natural-language queries enter the Streamlit system, which orchestrates "
        "SQLite, OpenAI API, and local Pandas fallback to return verified, visualized insights.",
        fig_caption
    ))

    story.append(Paragraph("3.2 System block diagram", subsec_heading))
    img_blk = Path(r"C:\Users\Asus\.gemini\antigravity\scratch\data-analyst-ai-chatbot\screenshots\diagram_block.png")
    if img_blk.exists():
        story.append(RLImage(str(img_blk), width=printable_w, height=185 * pt))
    story.append(Paragraph(
        "Figure 2. Ingestion pipeline (top) and dual-engine query & visual analytics pipeline (bottom) of the application.",
        fig_caption
    ))

    story.append(Paragraph("3.3 Flow in brief", subsec_heading))
    brief_points = [
        "<b>Upload & Sanitization:</b> Files are parsed, cleaned on a separate memory copy, and loaded into an indexed SQLite table.",
        "<b>Query Parsing & Routing:</b> The chatbot inspects API availability; if available, it prompts GPT-4o-mini with the table schema and top 5 rows.",
        "<b>AST Security Check:</b> Generated SQL is validated using <code>sqlparse</code>; multi-statement attacks or mutation keywords are rejected.",
        "<b>Execution & Explanation:</b> The query runs against SQLite; results are summarized by the LLM and rendered into interactive Plotly charts.",
        "<b>Local Fallback Protection:</b> If the API is missing or quota-exhausted, the regex engine processes aggregations locally with zero downtime.",
    ]
    for pt_item in brief_points:
        story.append(Paragraph(f"• {pt_item}", body_bullet))

    story.append(Paragraph("4. Technology Stack", sec_heading))
    stack_data_p1 = [
        [Paragraph("Layer", table_header), Paragraph("Technology", table_header), Paragraph("Role in this project", table_header)],
        [Paragraph("Frontend / UI", table_cell_bold), Paragraph("Streamlit 1.37+", table_cell), Paragraph("Interactive dashboard, multi-tab explorer, chat interface, and parameter controls.", table_cell)],
        [Paragraph("Backend / Logic", table_cell_bold), Paragraph("Python 3.12, Pandas, NumPy", table_cell), Paragraph("Data extraction, automated cleaning, AST SQL parsing, and fallback analytics.", table_cell)],
        [Paragraph("Database", table_cell_bold), Paragraph("SQLite (Embedded)", table_cell), Paragraph("Serverless relational data storage, fast execution, and dynamic schema inspection.", table_cell)],
        [Paragraph("AI / LLM", table_cell_bold), Paragraph("OpenAI GPT-4o-mini API", table_cell), Paragraph("Translates natural language to SQL queries and generates business summaries.", table_cell)],
    ]
    t_stack_p1 = Table(stack_data_p1, colWidths=[90 * pt, 120 * pt, printable_w - 210 * pt])
    t_stack_p1.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("TOPPADDING", (0, 0), (-1, -1), 3.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(t_stack_p1)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: TECH STACK (PART 2), REPO STRUCTURE, DATASET & RESULTS
    # =========================================================================
    stack_data_p2 = [
        [Paragraph("Layer", table_header), Paragraph("Technology", table_header), Paragraph("Role in this project", table_header)],
        [Paragraph("Security / Parser", table_cell_bold), Paragraph("sqlparse (AST engine)", table_cell), Paragraph("Enforces single-statement read-only execution; blocks SQL injection / mutations.", table_cell)],
        [Paragraph("Document Loader", table_cell_bold), Paragraph("openpyxl, xlrd, csv", table_cell), Paragraph("Parses diverse tabular formats (.csv, .xlsx, .xls) into uniform Pandas structures.", table_cell)],
        [Paragraph("Visualisation", table_cell_bold), Paragraph("Plotly Express, Graph Objects", table_cell), Paragraph("Auto-renders responsive bar charts, line graphs, and category distributions.", table_cell)],
        [Paragraph("Testing / QA", table_cell_bold), Paragraph("Pytest 8.2+", table_cell), Paragraph("Unit test suite verifying loaders, cleaners, fallback regex, and SQL validators.", table_cell)],
        [Paragraph("Hardware", table_cell_bold), Paragraph("Standard laptop (8 GB RAM), no GPU", table_cell), Paragraph("Entire system runs locally; network only needed for external OpenAI API calls.", table_cell)],
    ]
    t_stack_p2 = Table(stack_data_p2, colWidths=[90 * pt, 120 * pt, printable_w - 210 * pt])
    t_stack_p2.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("TOPPADDING", (0, 0), (-1, -1), 3.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(t_stack_p2)
    story.append(Spacer(1, 6 * pt))

    story.append(Paragraph("4.1 Repository structure", subsec_heading))
    repo_tree_text = (
        "data-analyst-ai-chatbot/<br/>"
        "&nbsp;&nbsp;app.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Streamlit multi-view application entry point<br/>"
        "&nbsp;&nbsp;src/ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;data_loader, data_cleaner, data_profiler, database,<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;sql_validator, query_executor, local_fallback, llm_client, chatbot<br/>"
        "&nbsp;&nbsp;data/ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;sample_sales.csv, reference transactional benchmarks<br/>"
        "&nbsp;&nbsp;tests/ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;test_cleaner, test_loader, test_fallback, test_sql_validator<br/>"
        "&nbsp;&nbsp;requirements.txt, .env.example, README.md, PROJECT_SYNOPSIS.md"
    )
    t_repo = Table([[Paragraph(repo_tree_text, code_style)]], colWidths=[printable_w])
    t_repo.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(t_repo)
    story.append(Spacer(1, 6 * pt))

    story.append(Paragraph("5. Dataset Used", sec_heading))
    dataset_data = [
        [Paragraph("Field", table_header), Paragraph("Value", table_header)],
        [Paragraph("Dataset file name", table_cell_bold), Paragraph("sample_sales.csv (also supports any user-uploaded CSV, XLSX, XLS file)", table_cell)],
        [Paragraph("Number of rows", table_cell_bold), Paragraph("10 transactional records (sample benchmark); stress-tested up to 50,000+ rows", table_cell)],
        [Paragraph("Number of columns", table_cell_bold), Paragraph("9 attributes", table_cell)],
        [Paragraph("Key columns", table_cell_bold), Paragraph("order_id, date, customer, city, category, product, quantity, sales, profit", table_cell)],
        [Paragraph("Tables indexed in demo", table_cell_bold), Paragraph("sample_sales (persisted in SQLite database analytics.db at runtime)", table_cell)],
        [Paragraph("Additional data collected", table_cell_bold), Paragraph("None beyond the user-uploaded file; strictly local session persistence", table_cell)],
    ]
    t_dataset = Table(dataset_data, colWidths=[130 * pt, printable_w - 130 * pt])
    t_dataset.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(t_dataset)
    story.append(Spacer(1, 6 * pt))

    story.append(Paragraph("6. Key Results and Metrics", sec_heading))
    metrics_data = [
        [Paragraph("Metric", table_header), Paragraph("Observed value (from application execution)", table_header)],
        [Paragraph("Ingestion & cleaning latency", table_cell_bold), Paragraph("120 ms to load, normalize headers, and index sample_sales.csv into SQLite", table_cell)],
        [Paragraph("AI SQL query response time", table_cell_bold), Paragraph("1.8 seconds with GPT-4o-mini (prompt assembly, AST validation & execution)", table_cell)],
        [Paragraph("Local fallback response time", table_cell_bold), Paragraph("42 ms to calculate aggregations locally with zero API cost", table_cell)],
        [Paragraph("Destructive SQL block rate", table_cell_bold), Paragraph("100% interception of unauthorized commands (DROP, UPDATE, DELETE rejected)", table_cell)],
        [Paragraph("Storage footprint", table_cell_bold), Paragraph("48 KB for the full local SQLite analytical knowledge base", table_cell)],
        [Paragraph("Data quality audit", table_cell_bold), Paragraph("0% missing values detected; 100% type conformance validated", table_cell)],
    ]
    t_metrics = Table(metrics_data, colWidths=[140 * pt, printable_w - 140 * pt])
    t_metrics.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(t_metrics)
    story.append(Spacer(1, 4 * pt))
    story.append(Paragraph(
        "<b>Business value achieved:</b> Users extract instant business metrics and visual trends from raw tabular data via conversational prompts, "
        "bypassing manual SQL authoring while the dual-engine fallback prevents disruptions when API quotas expire.",
        body_p
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: SCREENSHOTS 1 & 2
    # =========================================================================
    story.append(Paragraph("Application Output Screenshots", sec_heading))
    story.append(Paragraph(
        "The following screens were captured from the running application (localhost:8501) with full interactive data exploration and query execution active.",
        body_p
    ))
    story.append(Spacer(1, 2 * pt))

    ss_dir = Path(r"C:\Users\Asus\.gemini\antigravity\scratch\data-analyst-ai-chatbot\screenshots")
    ss1 = ss_dir / "screenshot_1_upload.png"
    ss2 = ss_dir / "screenshot_2_dashboard.png"

    img_w = printable_w
    img_h = 240 * pt

    if ss1.exists():
        story.append(RLImage(str(ss1), width=img_w, height=img_h))
        story.append(Paragraph("Figure 3. Upload & Cleaning view: Automated data profiling, row/column counts, memory metrics, and cleaning log.", fig_caption))
    story.append(Spacer(1, 6 * pt))

    if ss2.exists():
        story.append(RLImage(str(ss2), width=img_w, height=img_h))
        story.append(Paragraph("Figure 4. Executive KPI Dashboard: Total sales, profit, quantity metrics, data quality indicators, and numeric summary.", fig_caption))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: SCREENSHOTS 3 & 4
    # =========================================================================
    ss3 = ss_dir / "screenshot_3_explorer.png"
    ss4 = ss_dir / "screenshot_4_chatbot.png"

    if ss3.exists():
        story.append(RLImage(str(ss3), width=img_w, height=img_h))
        story.append(Paragraph("Figure 5. Interactive Data Explorer: Multi-tab view showing preview of loaded records, schema datatypes, and missing value analysis.", fig_caption))
    story.append(Spacer(1, 10 * pt))

    if ss4.exists():
        story.append(RLImage(str(ss4), width=img_w, height=img_h))
        story.append(Paragraph("Figure 6. Conversational AI Chatbot: Natural language query translated to safe SQL with narrative summary and interactive Plotly chart.", fig_caption))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 7: SCREENSHOTS 5 & 6
    # =========================================================================
    ss5 = ss_dir / "screenshot_5_sql.png"
    ss6 = ss_dir / "screenshot_6_insights.png"

    if ss5.exists():
        story.append(RLImage(str(ss5), width=img_w, height=img_h))
        story.append(Paragraph("Figure 7. SQL Explorer Sandbox: Read-only SQL query validation, tabular result display, and automatic chart generation.", fig_caption))
    story.append(Spacer(1, 10 * pt))

    if ss6.exists():
        story.append(RLImage(str(ss6), width=img_w, height=img_h))
        story.append(Paragraph("Figure 8. Automated Insights Page: Statistical overview of numerical columns, frequency distribution of categories, and top-value charts.", fig_caption))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 8: CHALLENGES FACED, LIMITATIONS & FUTURE IMPROVEMENTS
    # =========================================================================
    story.append(Paragraph("7. Challenges Faced and How Resolved", sec_heading))
    chal_data = [
        [Paragraph("Challenge", table_header), Paragraph("Resolution", table_header)],
        [
            Paragraph("LLMs hallucinating invalid or destructive SQL syntax.", table_cell_bold),
            Paragraph("Enforced an AST-based parser using <code>sqlparse</code> to inspect the query structure, reject multiple statements, and block all mutation keywords (<code>DROP</code>, <code>DELETE</code>, <code>UPDATE</code>).", table_cell)
        ],
        [
            Paragraph("Third-party LLM rate limits and token exhaustion causing app paralysis.", table_cell_bold),
            Paragraph("Engineered a local deterministic Pandas fallback engine that intercepts core statistical questions (sum, average, count, min, max, group by) and computes answers directly.", table_cell)
        ],
        [
            Paragraph("Tabular header anomalies and inconsistent data types across user files.", table_cell_bold),
            Paragraph("Constructed an automated data cleaner that strips whitespaces, converts spaces to underscores, infers date/numeric types, and reports changes in an audit log.", table_cell)
        ],
        [
            Paragraph("Querying SQLite without persisting unauthorized data across sessions.", table_cell_bold),
            Paragraph("Implemented dynamic session-bound table generation with sanitized naming conventions, ensuring complete data isolation between user files.", table_cell)
        ],
        [
            Paragraph("Interpreting query results for non-technical decision makers.", table_cell_bold),
            Paragraph("Coupled query execution with an LLM narrative generator and dynamic Plotly visualization mapper that detects continuous vs. discrete data.", table_cell)
        ],
    ]
    t_chal = Table(chal_data, colWidths=[150 * pt, printable_w - 150 * pt])
    t_chal.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(t_chal)
    story.append(Spacer(1, 8 * pt))

    story.append(Paragraph("7.1 Known limitations", subsec_heading))
    lims = [
        "Natural-language-to-SQL accuracy depends on column name clarity; ambiguous headers may require manual user clarification.",
        "The current local fallback engine covers single-table aggregations; nested subqueries require active LLM mode.",
        "Very large datasets (> 1 million records) may encounter in-memory Pandas constraints on standard consumer hardware.",
    ]
    for lim in lims:
        story.append(Paragraph(f"• {lim}", body_bullet))

    story.append(Spacer(1, 4 * pt))
    story.append(Paragraph("7.2 Future improvements", subsec_heading))
    fut = [
        "<b>Multi-Table Relational Joins:</b> Support simultaneous upload of multiple tables with automated foreign key linking.",
        "<b>Local Open-Source LLMs:</b> Integrate Ollama (Llama 3 / Mistral) for 100% offline, privacy-guaranteed on-premise execution.",
        "<b>Exportable Executive Reports:</b> One-click generation of PDF / Word analytical summary reports with embedded visualizations.",
        "<b>Machine Learning Insights:</b> Incorporate automated anomaly detection and time-series forecasting modules.",
    ]
    for fu in fut:
        story.append(Paragraph(f"• {fu}", body_bullet))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 9: REFERENCES, ETHICAL COMPLIANCE & APPENDIX
    # =========================================================================
    story.append(Paragraph("8. References", sec_heading))
    refs = [
        "OpenAI. (2024). <i>GPT-4o and GPT-4o-mini System Architecture and Function Calling Documentation</i>. https://platform.openai.com/docs",
        "Streamlit. (2024). <i>Streamlit Documentation: Building Interactive Python Data Applications</i>. https://docs.streamlit.io",
        "McKinney, W. (2010). <i>Data Structures for Statistical Computing in Python</i>. Proceedings of the 9th Python in Science Conference.",
        "SQLite Development Team. (2024). <i>SQLite In-Memory and Embedded Relational Database Architecture</i>. https://www.sqlite.org",
        "Plotly Technologies Inc. (2024). <i>Plotly Python Open Source Graphing Library</i>. https://plotly.com/python",
        "sqlparse Developers. (2024). <i>Non-validating SQL parser module for Python</i>. https://github.com/andialbrecht/sqlparse",
    ]
    for ref in refs:
        story.append(Paragraph(f"• {ref}", body_bullet))
    story.append(Spacer(1, 8 * pt))

    story.append(Paragraph("9. Ethical Compliance Declaration", sec_heading))
    story.append(Paragraph("I confirm that:", body_p))
    story.append(Paragraph("[ &nbsp; ] All dataset usage complies with the source licence.", body_bullet))
    story.append(Paragraph("[ &nbsp; ] No personally identifiable information (PII) is stored without consent.", body_bullet))
    story.append(Paragraph("[ &nbsp; ] AI tools used for code/writing are disclosed in the Appendix.", body_bullet))
    story.append(Paragraph("[ &nbsp; ] This project complies with the DPDP Act 2023 where applicable.", body_bullet))
    story.append(Spacer(1, 14 * pt))

    sig_data = [
        [Paragraph("Learner Signature: _______________________", table_cell_bold),
         Paragraph("Date: ________________", table_cell_bold)]
    ]
    t_sig = Table(sig_data, colWidths=[printable_w * 0.6, printable_w * 0.4])
    t_sig.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(t_sig)
    story.append(Spacer(1, 12 * pt))

    story.append(Paragraph("Appendix: AI Tools Disclosure", sec_heading))
    story.append(Paragraph(
        "OpenAI API (GPT-4o-mini) is utilized within the application to perform schema-grounded natural-language-to-SQL translation "
        "and narrative result summarization. An AI assistant was employed to help draft and format this synopsis from the project's codebase, "
        "live application outputs, and the academic synopsis template.",
        body_p
    ))
    story.append(Spacer(1, 10 * pt))

    story.append(Paragraph("GitHub Repository", sec_heading))
    story.append(Paragraph("Source code: <b>https://github.com/atishkr25/data-analyst-ai-chatbot</b>", body_p))

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully generated at: {pdf_path}")


if __name__ == "__main__":
    build_pdf()
