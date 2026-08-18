from io import BytesIO
from django.http import FileResponse
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph


def download_pdf(student, assessment, ai_response):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("<b>AI Career Guidance Report</b>", styles["Title"]))

    story.append(Paragraph(f"<b>Student:</b> {student.full_name}", styles["BodyText"]))
    story.append(Paragraph(f"<b>Email:</b> {student.email}", styles["BodyText"]))
    story.append(Paragraph(f"<b>Education:</b> {student.education}", styles["BodyText"]))
    story.append(Paragraph(f"<b>Branch:</b> {student.branch}", styles["BodyText"]))
    story.append(Paragraph(f"<b>Skills:</b> {student.skills}", styles["BodyText"]))
    story.append(Paragraph(f"<b>Interests:</b> {student.interests}", styles["BodyText"]))

    story.append(Paragraph("<br/>", styles["BodyText"]))

    story.append(Paragraph(
        f"<b>Selected Role:</b> {assessment.role}",
        styles["BodyText"]
    ))

    story.append(Paragraph(
        f"<b>Aptitude Score:</b> {assessment.score}/{assessment.total_questions}",
        styles["BodyText"]
    ))

    story.append(Paragraph("<br/>", styles["BodyText"]))

    story.append(Paragraph("<b>AI Recommendation</b>", styles["Heading2"]))

    story.append(Paragraph(ai_response.replace("\n", "<br/>"), styles["BodyText"]))

    doc.build(story)

    buffer.seek(0)

    return FileResponse(
        buffer,
        as_attachment=True,
        filename="AI_Career_Report.pdf"
    )