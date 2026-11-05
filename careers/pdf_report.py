from io import BytesIO
from xml.sax.saxutils import escape

from django.http import FileResponse

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    KeepTogether,
)


# ============================================================
# CAREERFLOW PDF THEME
# ============================================================

PRIMARY = colors.HexColor("#5B4BDB")
PRIMARY_DARK = colors.HexColor("#373083")
BLUE = colors.HexColor("#63B2FA")

INK = colors.HexColor("#17233E")
MUTED = colors.HexColor("#68738A")

BG = colors.HexColor("#F7F8FF")
CARD = colors.HexColor("#FFFFFF")
LINE = colors.HexColor("#E7E9F8")

LIGHT_PURPLE = colors.HexColor("#F0EFFF")
LIGHT_BLUE = colors.HexColor("#EDF7FF")
LIGHT_GREEN = colors.HexColor("#EDF8F1")


# ============================================================
# HELPERS
# ============================================================

def safe(value, default="—"):
    """
    Convert values into safe display text.
    """
    if value is None:
        return default

    if isinstance(value, (list, tuple)):
        return ", ".join(str(item) for item in value) or default

    text = str(value).strip()

    return text if text else default


def paragraph_text(value):
    """
    Escape text before sending it to ReportLab Paragraph.
    """
    return escape(safe(value))


def list_value(value):
    """
    Convert a value into a clean list.
    """
    if not value:
        return []

    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]

    if isinstance(value, tuple):
        return [str(item).strip() for item in value if str(item).strip()]

    if isinstance(value, str):
        return [
            item.strip()
            for item in value.split(",")
            if item.strip()
        ]

    return [str(value).strip()]


def make_link(url, label):
    """
    Create a clickable PDF hyperlink.
    """
    if not url:
        return paragraph_text(label)

    return (
        f'<link href="{escape(str(url))}" color="#5B4BDB">'
        f"<u>{paragraph_text(label)}</u>"
        "</link>"
    )


# ============================================================
# PAGE HEADER / FOOTER
# ============================================================

def draw_page(canvas, doc):
    """
    Draw CareerFlow header/footer on every page.
    """

    canvas.saveState()

    width, height = A4

    # Header line
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.6)
    canvas.line(
        18 * mm,
        height - 15 * mm,
        width - 18 * mm,
        height - 15 * mm,
    )

    # Header branding
    canvas.setFillColor(PRIMARY)
    canvas.setFont("Helvetica-Bold", 9)
    canvas.drawString(
        18 * mm,
        height - 11.5 * mm,
        "CAREERFLOW",
    )

    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawRightString(
        width - 18 * mm,
        height - 11.5 * mm,
        "AI Career Guidance System",
    )

    # Footer line
    canvas.setStrokeColor(LINE)
    canvas.line(
        18 * mm,
        13 * mm,
        width - 18 * mm,
        13 * mm,
    )

    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7.5)

    canvas.drawString(
        18 * mm,
        8 * mm,
        "CareerFlow • Personalised Career Development Report",
    )

    canvas.drawRightString(
        width - 18 * mm,
        8 * mm,
        f"Page {doc.page}",
    )

    canvas.restoreState()


# ============================================================
# MAIN PDF FUNCTION
# ============================================================

def download_pdf(student, assessment, ai_response):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=17 * mm,
        leftMargin=17 * mm,
        topMargin=22 * mm,
        bottomMargin=19 * mm,
        title="CareerFlow Career Development Report",
        author="CareerFlow",
    )

    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="CFTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=28,
            leading=32,
            textColor=INK,
            alignment=TA_LEFT,
            spaceAfter=10,
        )
    )

    styles.add(
        ParagraphStyle(
            name="CFSubtitle",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=10.5,
            leading=16,
            textColor=MUTED,
        )
    )

    styles.add(
        ParagraphStyle(
            name="CFSection",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=17,
            leading=21,
            textColor=INK,
            spaceAfter=9,
        )
    )

    styles.add(
        ParagraphStyle(
            name="CFHeading",
            parent=styles["Heading3"],
            fontName="Helvetica-Bold",
            fontSize=11.5,
            leading=15,
            textColor=INK,
            spaceAfter=5,
        )
    )

    styles.add(
        ParagraphStyle(
            name="CFBody",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=8.9,
            leading=14,
            textColor=MUTED,
            spaceAfter=5,
        )
    )

    styles.add(
        ParagraphStyle(
            name="CFSmall",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=7.8,
            leading=11,
            textColor=MUTED,
        )
    )

    styles.add(
        ParagraphStyle(
            name="CFWhiteTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=25,
            leading=29,
            textColor=colors.white,
            alignment=TA_LEFT,
        )
    )

    styles.add(
        ParagraphStyle(
            name="CFWhiteBody",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=10,
            leading=15,
            textColor=colors.HexColor("#E8E8FF"),
        )
    )

    styles.add(
        ParagraphStyle(
            name="CFLabel",
            parent=styles["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=7,
            leading=9,
            textColor=PRIMARY,
            spaceAfter=3,
        )
    )

    story = []

    analysis = assessment.analysis or {}

    # New roadmap structure is normally a list.
    roadmap = analysis.get("roadmap", [])

    if not isinstance(roadmap, list):
        roadmap = []

    role_results = analysis.get("role_results", [])

    if not isinstance(role_results, list):
        role_results = []

    best_match = analysis.get("best_match", {})

    if not isinstance(best_match, dict):
        best_match = {}

    strengths = list_value(
        analysis.get("strengths")
        or analysis.get("overall_strengths")
    )

    gaps = list_value(
        analysis.get("skill_gaps")
        or analysis.get("gaps")
        or analysis.get("overall_skill_gaps")
    )

    # ========================================================
    # COVER PAGE
    # ========================================================

    cover_data = [
        [
            Paragraph(
                "CAREERFLOW",
                ParagraphStyle(
                    "CoverBrand",
                    parent=styles["CFLabel"],
                    fontSize=10,
                    textColor=colors.HexColor("#B7DFFF"),
                ),
            )
        ],
        [
            Paragraph(
                "Your Career<br/>Development Report",
                styles["CFWhiteTitle"],
            )
        ],
        [
            Paragraph(
                "A personalised assessment, skill-gap analysis "
                "and practical learning roadmap designed around "
                "your career goals.",
                styles["CFWhiteBody"],
            )
        ],
        [
            Spacer(1, 8),
            Paragraph(
                f"<b>{paragraph_text(student.full_name)}</b>",
                ParagraphStyle(
                    "CoverName",
                    parent=styles["CFWhiteBody"],
                    fontSize=13,
                    textColor=colors.white,
                ),
            ),
        ],
        [
            Paragraph(
                f"Target role(s): {paragraph_text(assessment.roles_label)}",
                styles["CFWhiteBody"],
            )
        ],
    ]

    cover = Table(
        cover_data,
        colWidths=[165 * mm],
        rowHeights=[22 * mm, 48 * mm, 40 * mm, 22 * mm, 22 * mm],
    )

    cover.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    PRIMARY_DARK,
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    18 * mm,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    18 * mm,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    8 * mm,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    6 * mm,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
            ]
        )
    )

    story.append(Spacer(1, 18 * mm))
    story.append(cover)
    story.append(Spacer(1, 13 * mm))

    story.append(
        Paragraph(
            "Built from your profile, assessment performance and "
            "selected career direction.",
            styles["CFSubtitle"],
        )
    )

    story.append(PageBreak())

    # ========================================================
    # 1. STUDENT PROFILE
    # ========================================================

    story.append(
        Paragraph("01  •  YOUR PROFILE", styles["CFLabel"])
    )

    story.append(
        Paragraph("Student profile", styles["CFSection"])
    )

    profile_data = [
        [
            Paragraph("<b>Name</b>", styles["CFBody"]),
            Paragraph(paragraph_text(student.full_name), styles["CFBody"]),
        ],
        [
            Paragraph("<b>Email</b>", styles["CFBody"]),
            Paragraph(paragraph_text(student.email), styles["CFBody"]),
        ],
        [
            Paragraph("<b>Education</b>", styles["CFBody"]),
            Paragraph(paragraph_text(student.education), styles["CFBody"]),
        ],
        [
            Paragraph("<b>Branch / Specialisation</b>", styles["CFBody"]),
            Paragraph(paragraph_text(student.branch), styles["CFBody"]),
        ],
        [
            Paragraph("<b>Year</b>", styles["CFBody"]),
            Paragraph(paragraph_text(student.year), styles["CFBody"]),
        ],
        [
            Paragraph("<b>Experience Level</b>", styles["CFBody"]),
            Paragraph(
                paragraph_text(student.experience_level),
                styles["CFBody"],
            ),
        ],
        [
            Paragraph("<b>Skills</b>", styles["CFBody"]),
            Paragraph(paragraph_text(student.skills), styles["CFBody"]),
        ],
        [
            Paragraph("<b>Interests</b>", styles["CFBody"]),
            Paragraph(paragraph_text(student.interests), styles["CFBody"]),
        ],
    ]

    profile_table = Table(
        profile_data,
        colWidths=[48 * mm, 117 * mm],
    )

    profile_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    CARD,
                ),
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.7,
                    LINE,
                ),
                (
                    "INNERGRID",
                    (0, 0),
                    (-1, -1),
                    0.4,
                    LINE,
                ),
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    BG,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
            ]
        )
    )

    story.append(profile_table)
    story.append(Spacer(1, 12 * mm))

    # ========================================================
    # 2. ASSESSMENT OVERVIEW
    # ========================================================

    story.append(
        Paragraph("02  •  ASSESSMENT", styles["CFLabel"])
    )

    story.append(
        Paragraph("Assessment overview", styles["CFSection"])
    )

    score_percentage = 0

    if assessment.total_questions:
        score_percentage = round(
            (assessment.score / assessment.total_questions) * 100
        )

    overview_data = [
        [
            Paragraph(
                "<b>Overall score</b><br/>"
                f'<font size="20" color="#5B4BDB">{score_percentage}%</font>',
                styles["CFBody"],
            ),
            Paragraph(
                "<b>Correct answers</b><br/>"
                f'<font size="16" color="#17233E">'
                f"{assessment.score}</font>",
                styles["CFBody"],
            ),
            Paragraph(
                "<b>Total questions</b><br/>"
                f'<font size="16" color="#17233E">'
                f"{assessment.total_questions}</font>",
                styles["CFBody"],
            ),
        ]
    ]

    overview_table = Table(
        overview_data,
        colWidths=[55 * mm, 55 * mm, 55 * mm],
        rowHeights=[30 * mm],
    )

    overview_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, 0),
                    LIGHT_PURPLE,
                ),
                (
                    "BACKGROUND",
                    (1, 0),
                    (1, 0),
                    LIGHT_BLUE,
                ),
                (
                    "BACKGROUND",
                    (2, 0),
                    (2, 0),
                    BG,
                ),
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    .7,
                    LINE,
                ),
                (
                    "INNERGRID",
                    (0, 0),
                    (-1, -1),
                    .5,
                    LINE,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    9,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    9,
                ),
            ]
        )
    )

    story.append(overview_table)
    story.append(Spacer(1, 8 * mm))

    story.append(
        Paragraph(
            f"<b>Confirmed target roles:</b> "
            f"{paragraph_text(assessment.roles_label)}",
            styles["CFBody"],
        )
    )

    # ========================================================
    # 3. ROLE-WISE RESULTS
    # ========================================================

    if role_results:

        story.append(Spacer(1, 5 * mm))

        story.append(
            Paragraph("03  •  ROLE PERFORMANCE", styles["CFLabel"])
        )

        story.append(
            Paragraph(
                "Role-wise assessment results",
                styles["CFSection"],
            )
        )

        result_rows = [
            [
                Paragraph("<b>Target role</b>", styles["CFBody"]),
                Paragraph("<b>Score</b>", styles["CFBody"]),
                Paragraph("<b>Suitability</b>", styles["CFBody"]),
            ]
        ]

        for result in role_results:

            role = safe(result.get("role"))
            score = result.get("score", 0)
            suitability = safe(
                result.get("suitability"),
                "Not available",
            )

            result_rows.append(
                [
                    Paragraph(paragraph_text(role), styles["CFBody"]),
                    Paragraph(
                        f'<b>{paragraph_text(score)}%</b>',
                        styles["CFBody"],
                    ),
                    Paragraph(
                        paragraph_text(suitability),
                        styles["CFBody"],
                    ),
                ]
            )

        results_table = Table(
            result_rows,
            colWidths=[85 * mm, 30 * mm, 50 * mm],
            repeatRows=1,
        )

        results_table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        LIGHT_PURPLE,
                    ),
                    (
                        "BOX",
                        (0, 0),
                        (-1, -1),
                        .7,
                        LINE,
                    ),
                    (
                        "INNERGRID",
                        (0, 0),
                        (-1, -1),
                        .4,
                        LINE,
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "MIDDLE",
                    ),
                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        8,
                    ),
                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        8,
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        7,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        7,
                    ),
                ]
            )
        )

        story.append(results_table)

    # ========================================================
    # 4. BEST MATCH
    # ========================================================

    if best_match:

        story.append(Spacer(1, 8 * mm))

        story.append(
            Paragraph("04  •  BEST CURRENT MATCH", styles["CFLabel"])
        )

        best_role = (
            best_match.get("role")
            or best_match.get("best_role")
            or "Not available"
        )

        best_score = best_match.get(
            "score",
            best_match.get("percentage", ""),
        )

        best_reason = (
            best_match.get("reason")
            or best_match.get("explanation")
            or ""
        )

        best_data = [
            [
                Paragraph(
                    f"<b>{paragraph_text(best_role)}</b>",
                    ParagraphStyle(
                        "BestRole",
                        parent=styles["CFHeading"],
                        fontSize=15,
                        textColor=PRIMARY,
                    ),
                ),
                Paragraph(
                    f"<b>{paragraph_text(best_score)}%</b>"
                    if best_score != ""
                    else "",
                    styles["CFHeading"],
                ),
            ],
            [
                Paragraph(
                    paragraph_text(best_reason),
                    styles["CFBody"],
                ),
                "",
            ],
        ]

        best_table = Table(
            best_data,
            colWidths=[125 * mm, 40 * mm],
        )

        best_table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, -1),
                        LIGHT_PURPLE,
                    ),
                    (
                        "SPAN",
                        (0, 1),
                        (-1, 1),
                    ),
                    (
                        "BOX",
                        (0, 0),
                        (-1, -1),
                        .7,
                        colors.HexColor("#DDD9FA"),
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "TOP",
                    ),
                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        10,
                    ),
                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        10,
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        8,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        8,
                    ),
                ]
            )
        )

        story.append(best_table)

    # ========================================================
    # 5. STRENGTHS & SKILL GAPS
    # ========================================================

    if strengths or gaps:

        story.append(PageBreak())

        story.append(
            Paragraph("05  •  AI INSIGHTS", styles["CFLabel"])
        )

        story.append(
            Paragraph(
                "Strengths and priority gaps",
                styles["CFSection"],
            )
        )

        insight_data = []

        if strengths:

            strength_text = "<br/>".join(
                f"• {paragraph_text(item)}"
                for item in strengths
            )

            insight_data.append(
                [
                    Paragraph(
                        "<b>YOUR STRENGTHS</b><br/><br/>"
                        + strength_text,
                        styles["CFBody"],
                    )
                ]
            )

        if gaps:

            gap_text = "<br/>".join(
                f"• {paragraph_text(item)}"
                for item in gaps
            )

            insight_data.append(
                [
                    Paragraph(
                        "<b>PRIORITY SKILL GAPS</b><br/><br/>"
                        + gap_text,
                        styles["CFBody"],
                    )
                ]
            )

        insight_table = Table(
            insight_data,
            colWidths=[165 * mm],
        )

        insight_table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (0, 0),
                        LIGHT_GREEN if strengths else LIGHT_PURPLE,
                    ),
                    (
                        "BOX",
                        (0, 0),
                        (-1, -1),
                        .7,
                        LINE,
                    ),
                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        10,
                    ),
                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        10,
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        9,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        9,
                    ),
                ]
            )
        )

        story.append(insight_table)

    # ========================================================
    # 6. PERSONALIZED ROADMAP
    # ========================================================

    if roadmap:

        story.append(PageBreak())

        story.append(
            Paragraph("06  •  PERSONALIZED ROADMAP", styles["CFLabel"])
        )

        story.append(
            Paragraph(
                "Learn → Watch → Practice → Project",
                styles["CFSection"],
            )
        )

        story.append(
            Paragraph(
                "This roadmap turns your assessment gaps into a "
                "sequential learning path. Complete each stage "
                "before moving to the next one.",
                styles["CFSubtitle"],
            )
        )

        story.append(Spacer(1, 6 * mm))

        for index, stage in enumerate(roadmap, start=1):

            if not isinstance(stage, dict):
                continue

            number = stage.get("number", index)
            skill = safe(stage.get("skill"), "Skill development")
            priority = safe(stage.get("priority"), "Core")
            goal = safe(stage.get("goal"), "")
            concepts = list_value(stage.get("concepts"))
            reason = safe(stage.get("reason"), "")

            learn = safe(
                stage.get("learn"),
                "Study the core concepts for this skill.",
            )

            learn_url = stage.get("learn_url")
            learn_provider = safe(
                stage.get("learn_provider"),
                "Learning resource",
            )

            watch_query = safe(
                stage.get("watch_query"),
                skill,
            )

            watch_url = stage.get("watch_url")

            practice = safe(
                stage.get("practice"),
                "Practice the concepts using exercises.",
            )

            practice_url = stage.get("practice_url")
            practice_provider = safe(
                stage.get("practice_provider"),
                "Practice resource",
            )

            project = safe(
                stage.get("project"),
                "Build a small project using this skill.",
            )

            project_url = stage.get("project_url")
            project_resource_name = safe(
                stage.get("project_resource_name"),
                "Project references",
            )

            tasks = list_value(stage.get("tasks"))

            time_required = safe(
                stage.get("time"),
                "Estimated time not specified",
            )

            outcome = safe(
                stage.get("outcome"),
                "",
            )

            # Stage heading
            stage_header = Table(
                [
                    [
                        Paragraph(
                            f"<b>WEEK {paragraph_text(number)}</b>",
                            ParagraphStyle(
                                "StageNumber",
                                parent=styles["CFBody"],
                                fontSize=8,
                                textColor=colors.white,
                            ),
                        ),
                        Paragraph(
                            f"<b>{paragraph_text(skill)}</b>",
                            styles["CFHeading"],
                        ),
                        Paragraph(
                            paragraph_text(priority),
                            styles["CFSBody"]
                            if "CFSBody" in styles
                            else styles["CFSmall"],
                        ),
                    ]
                ],
                colWidths=[27 * mm, 103 * mm, 35 * mm],
            )

            stage_header.setStyle(
                TableStyle(
                    [
                        (
                            "BACKGROUND",
                            (0, 0),
                            (0, 0),
                            PRIMARY,
                        ),
                        (
                            "BACKGROUND",
                            (1, 0),
                            (2, 0),
                            LIGHT_PURPLE,
                        ),
                        (
                            "VALIGN",
                            (0, 0),
                            (-1, -1),
                            "MIDDLE",
                        ),
                        (
                            "LEFTPADDING",
                            (0, 0),
                            (-1, -1),
                            7,
                        ),
                        (
                            "RIGHTPADDING",
                            (0, 0),
                            (-1, -1),
                            7,
                        ),
                        (
                            "TOPPADDING",
                            (0, 0),
                            (-1, -1),
                            7,
                        ),
                        (
                            "BOTTOMPADDING",
                            (0, 0),
                            (-1, -1),
                            7,
                        ),
                        (
                            "BOX",
                            (0, 0),
                            (-1, -1),
                            .6,
                            LINE,
                        ),
                    ]
                )
            )

            story.append(stage_header)

            if goal != "—":

                story.append(
                    Paragraph(
                        f"<b>Goal:</b> {paragraph_text(goal)}",
                        styles["CFBody"],
                    )
                )

            if concepts:

                concept_text = " • ".join(
                    paragraph_text(item)
                    for item in concepts
                )

                story.append(
                    Paragraph(
                        f"<b>Concepts:</b> {concept_text}",
                        styles["CFSBody"]
                        if "CFSBody" in styles
                        else styles["CFBody"],
                    )
                )

            if reason != "—":

                story.append(
                    Paragraph(
                        f"<b>Why this matters:</b> "
                        f"{paragraph_text(reason)}",
                        styles["CFBody"],
                    )
                )

            # Resource cards
            resource_rows = []

            # Learn
            learn_content = (
                f"<b>01 · LEARN</b><br/>"
                f"{paragraph_text(learn)}<br/><br/>"
                f"<b>{paragraph_text(learn_provider)}</b>"
            )

            if learn_url:
                learn_content += (
                    "<br/>"
                    + make_link(
                        learn_url,
                        "Open learning resource ↗",
                    )
                )

            resource_rows.append(
                Paragraph(
                    learn_content,
                    styles["CFBody"],
                )
            )

            # Watch
            watch_content = (
                f"<b>02 · WATCH</b><br/>"
                f"Search YouTube for:<br/>"
                f"<i>{paragraph_text(watch_query)}</i>"
            )

            if watch_url:
                watch_content += (
                    "<br/><br/>"
                    + make_link(
                        watch_url,
                        "Open YouTube search ↗",
                    )
                )

            resource_rows.append(
                Paragraph(
                    watch_content,
                    styles["CFBody"],
                )
            )

            # Practice
            practice_content = (
                f"<b>03 · PRACTICE</b><br/>"
                f"{paragraph_text(practice)}<br/><br/>"
                f"<b>{paragraph_text(practice_provider)}</b>"
            )

            if practice_url:
                practice_content += (
                    "<br/>"
                    + make_link(
                        practice_url,
                        "Open practice resource ↗",
                    )
                )

            resource_rows.append(
                Paragraph(
                    practice_content,
                    styles["CFBody"],
                )
            )

            # Project
            project_content = (
                f"<b>04 · PROJECT</b><br/>"
                f"{paragraph_text(project)}<br/><br/>"
                f"<b>{paragraph_text(project_resource_name)}</b>"
            )

            if project_url:
                project_content += (
                    "<br/>"
                    + make_link(
                        project_url,
                        "Explore project references ↗",
                    )
                )

            resource_rows.append(
                Paragraph(
                    project_content,
                    styles["CFBody"],
                )
            )

            resource_table = Table(
                [
                    [resource_rows[0], resource_rows[1]],
                    [resource_rows[2], resource_rows[3]],
                ],
                colWidths=[82 * mm, 83 * mm],
            )

            resource_table.setStyle(
                TableStyle(
                    [
                        (
                            "BACKGROUND",
                            (0, 0),
                            (0, 0),
                            LIGHT_PURPLE,
                        ),
                        (
                            "BACKGROUND",
                            (1, 0),
                            (1, 0),
                            LIGHT_BLUE,
                        ),
                        (
                            "BACKGROUND",
                            (0, 1),
                            (0, 1),
                            BG,
                        ),
                        (
                            "BACKGROUND",
                            (1, 1),
                            (1, 1),
                            LIGHT_GREEN,
                        ),
                        (
                            "BOX",
                            (0, 0),
                            (-1, -1),
                            .6,
                            LINE,
                        ),
                        (
                            "INNERGRID",
                            (0, 0),
                            (-1, -1),
                            .4,
                            LINE,
                        ),
                        (
                            "VALIGN",
                            (0, 0),
                            (-1, -1),
                            "TOP",
                        ),
                        (
                            "LEFTPADDING",
                            (0, 0),
                            (-1, -1),
                            8,
                        ),
                        (
                            "RIGHTPADDING",
                            (0, 0),
                            (-1, -1),
                            8,
                        ),
                        (
                            "TOPPADDING",
                            (0, 0),
                            (-1, -1),
                            8,
                        ),
                        (
                            "BOTTOMPADDING",
                            (0, 0),
                            (-1, -1),
                            8,
                        ),
                    ]
                )
            )

            story.append(resource_table)

            if tasks:

                task_text = "<br/>".join(
                    f"• {paragraph_text(task)}"
                    for task in tasks
                )

                story.append(
                    Paragraph(
                        f"<b>Practical tasks</b><br/>{task_text}",
                        styles["CFBody"],
                    )
                )

            story.append(
                Paragraph(
                    f"<b>Estimated learning time:</b> "
                    f"{paragraph_text(time_required)}",
                    styles["CFBody"],
                )
            )

            if outcome != "—":

                story.append(
                    Paragraph(
                        f"<b>Expected outcome:</b> "
                        f"{paragraph_text(outcome)}",
                        styles["CFBody"],
                    )
                )

            story.append(Spacer(1, 7 * mm))

    # ========================================================
    # 7. AI CAREER INSIGHT
    # ========================================================

    if ai_response:

        story.append(PageBreak())

        story.append(
            Paragraph("07  •  AI CAREER INSIGHT", styles["CFLabel"])
        )

        story.append(
            Paragraph(
                "Why this direction",
                styles["CFSection"],
            )
        )

        clean_ai = paragraph_text(ai_response)

        # Preserve line breaks
        clean_ai = clean_ai.replace("\n", "<br/>")

        ai_table = Table(
            [
                [
                    Paragraph(
                        clean_ai,
                        styles["CFBody"],
                    )
                ]
            ],
            colWidths=[165 * mm],
        )

        ai_table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, -1),
                        BG,
                    ),
                    (
                        "BOX",
                        (0, 0),
                        (-1, -1),
                        .7,
                        LINE,
                    ),
                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        11,
                    ),
                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        11,
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        10,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        10,
                    ),
                ]
            )
        )

        story.append(ai_table)

    # ========================================================
    # 8. FINAL NEXT STEPS
    # ========================================================

    story.append(Spacer(1, 10 * mm))

    story.append(
        Paragraph("08  •  NEXT STEPS", styles["CFLabel"])
    )

    story.append(
        Paragraph(
            "Your action plan",
            styles["CFSection"],
        )
    )

    next_steps = [
        "Work through the roadmap in order.",
        "Practice every important skill instead of only watching tutorials.",
        "Complete projects that demonstrate your skills.",
        "Add strong projects, certifications and relevant experience to your resume.",
        "Reassess your career direction as your skills and interests develop.",
    ]

    next_text = "<br/>".join(
        f"<b>{index}.</b> {paragraph_text(step)}"
        for index, step in enumerate(next_steps, start=1)
    )

    next_table = Table(
        [
            [
                Paragraph(
                    next_text,
                    styles["CFBody"],
                )
            ]
        ],
        colWidths=[165 * mm],
    )

    next_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    LIGHT_PURPLE,
                ),
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    .7,
                    LINE,
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    11,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    11,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    10,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    10,
                ),
            ]
        )
    )

    story.append(next_table)

    story.append(Spacer(1, 15 * mm))

    story.append(
        Paragraph(
            "<b>CareerFlow</b><br/>"
            "AI-powered career guidance built around your profile, "
            "goals and continuous learning.",
            ParagraphStyle(
                "FinalBrand",
                parent=styles["CFBody"],
                alignment=TA_CENTER,
                textColor=MUTED,
                leading=14,
            ),
        )
    )

    # ========================================================
    # BUILD PDF
    # ========================================================

    doc.build(
        story,
        onFirstPage=draw_page,
        onLaterPages=draw_page,
    )

    buffer.seek(0)

    return FileResponse(
        buffer,
        as_attachment=True,
        filename="CareerFlow_Career_Development_Report.pdf",
    )