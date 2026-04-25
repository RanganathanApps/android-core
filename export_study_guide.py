from pathlib import Path
import re

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import PageBreak, Paragraph, Preformatted, SimpleDocTemplate, Spacer

from content import CONTENT

BASE_DIR = Path(__file__).resolve().parent
MARKDOWN_OUTPUT = BASE_DIR / "senior-modern-android-interview-guide.md"
PDF_OUTPUT = BASE_DIR / "senior-modern-android-interview-guide.pdf"


def normalize_text(value: str) -> str:
    text = str(value or "")
    replacements = {
        "â€¢": "-",
        "â†’": "->",
        "â€™": "'",
        "â€œ": '"',
        "â€": '"',
        "â€“": "-",
        "â€”": "-",
        "\xa0": " ",
    }
    for source, target in replacements.items():
        text = text.replace(source, target)
    return re.sub(r"[ \t]+", " ", text).strip()


def split_points(points: list[str]) -> list[str]:
    normalized_points = []
    for point in points:
        text = normalize_text(point)
        if not text:
            continue

        if text.startswith("- "):
            parts = re.split(r"\s+-\s+", text)
            normalized_points.extend(
                f"- {part.lstrip('- ').strip()}" for part in parts if part.strip()
            )
        else:
            normalized_points.append(text)
    return normalized_points


def build_markdown() -> str:
    lines = [
        "# Senior Modern Android Interview Guide",
        "",
        "Structured for senior Android interview preparation across fundamentals, modern Android development, system design, delivery, and leadership.",
        "",
        "## Study Roadmap",
        "",
    ]

    for section_index, section in enumerate(CONTENT, start=1):
        lines.append(f"- {section_index}. {normalize_text(section['title'])}")

    lines.append("")

    for section_index, section in enumerate(CONTENT, start=1):
        section_title = normalize_text(section["title"])
        lines.append(f"## {section_index}. {section_title}")
        lines.append("")
        section_description = normalize_text(section.get("description", ""))
        if section_description:
            lines.append(section_description)
            lines.append("")

        for topic_index, topic in enumerate(section.get("topics", []), start=1):
            topic_number = f"{section_index}.{topic_index}"
            topic_title = normalize_text(topic["title"])
            lines.append(f"### {topic_number} {topic_title}")
            lines.append("")

            description = normalize_text(topic.get("description", ""))
            if description:
                lines.append(description)
                lines.append("")

            for content_section in topic.get("content_sections", []):
                heading = normalize_text(content_section.get("heading", ""))
                if heading:
                    lines.append(f"#### {heading}")
                    lines.append("")

                for point in split_points(content_section.get("points", [])):
                    lines.append(point if point.startswith("- ") else f"- {point}")

                subtopics = content_section.get("subtopics", [])
                if subtopics and content_section.get("points"):
                    lines.append("")

                for subtopic in subtopics:
                    title = normalize_text(subtopic.get("title", ""))
                    description = normalize_text(subtopic.get("description", ""))
                    if title and description:
                        lines.append(f"- **{title}**: {description}")
                    elif title:
                        lines.append(f"- **{title}**")
                    elif description:
                        lines.append(f"- {description}")

                if heading or content_section.get("points") or subtopics:
                    lines.append("")

            for block in topic.get("code_blocks", []):
                title = normalize_text(block.get("title", "Code Example"))
                language = normalize_text(block.get("language", "text")) or "text"
                code = str(block.get("code", "")).strip("\n")
                lines.append(f"#### {title}")
                lines.append("")
                lines.append(f"```{language}")
                lines.append(code)
                lines.append("```")
                lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def build_pdf() -> None:
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "GuideTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=28,
        textColor=colors.HexColor("#0f766e"),
        spaceAfter=10,
    )
    section_style = ParagraphStyle(
        "GuideSection",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=16,
        leading=21,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=10,
        spaceAfter=8,
    )
    topic_style = ParagraphStyle(
        "GuideTopic",
        parent=styles["Heading3"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#134e4a"),
        spaceBefore=8,
        spaceAfter=6,
    )
    body_style = ParagraphStyle(
        "GuideBody",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        spaceAfter=6,
    )
    bullet_style = ParagraphStyle(
        "GuideBullet",
        parent=body_style,
        leftIndent=14,
        firstLineIndent=-8,
    )
    code_title_style = ParagraphStyle(
        "GuideCodeTitle",
        parent=styles["Heading4"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#1d4ed8"),
        spaceBefore=6,
        spaceAfter=4,
    )

    story = [
        Paragraph("Senior Modern Android Interview Guide", title_style),
        Paragraph(
            "Structured for senior Android interview preparation across fundamentals, modern Android development, system design, delivery, and leadership.",
            body_style,
        ),
        Spacer(1, 0.1 * inch),
    ]

    for section_index, section in enumerate(CONTENT, start=1):
        if section_index > 1:
            story.append(PageBreak())

        story.append(
            Paragraph(f"{section_index}. {normalize_text(section['title'])}", section_style)
        )
        section_description = normalize_text(section.get("description", ""))
        if section_description:
            story.append(Paragraph(section_description, body_style))

        for topic_index, topic in enumerate(section.get("topics", []), start=1):
            topic_number = f"{section_index}.{topic_index}"
            story.append(
                Paragraph(
                    f"{topic_number} {normalize_text(topic['title'])}",
                    topic_style,
                )
            )

            description = normalize_text(topic.get("description", ""))
            if description:
                story.append(Paragraph(description, body_style))

            for content_section in topic.get("content_sections", []):
                heading = normalize_text(content_section.get("heading", ""))
                if heading:
                    story.append(Paragraph(heading, topic_style))

                for point in split_points(content_section.get("points", [])):
                    point_text = point[2:] if point.startswith("- ") else point
                    story.append(Paragraph(f"• {point_text}", bullet_style))

                for subtopic in content_section.get("subtopics", []):
                    title = normalize_text(subtopic.get("title", ""))
                    description = normalize_text(subtopic.get("description", ""))
                    if title and description:
                        story.append(Paragraph(f"• <b>{title}</b>: {description}", bullet_style))
                    elif title:
                        story.append(Paragraph(f"• <b>{title}</b>", bullet_style))
                    elif description:
                        story.append(Paragraph(f"• {description}", bullet_style))

            for block in topic.get("code_blocks", []):
                story.append(
                    Paragraph(
                        normalize_text(block.get("title", "Code Example")),
                        code_title_style,
                    )
                )
                story.append(
                    Preformatted(
                        str(block.get("code", "")).strip("\n"),
                        ParagraphStyle(
                            "GuideCode",
                            parent=body_style,
                            fontName="Courier",
                            fontSize=8,
                            leading=10,
                            textColor=colors.HexColor("#111827"),
                            backColor=colors.HexColor("#edf2f7"),
                            borderPadding=6,
                            borderWidth=0.5,
                            borderColor=colors.HexColor("#cbd5e1"),
                        ),
                    )
                )

            story.append(Spacer(1, 0.08 * inch))

    output_path = PDF_OUTPUT
    try:
        with open(output_path, "ab"):
            pass
    except PermissionError:
        output_path = output_path.with_name(f"{output_path.stem}-updated{output_path.suffix}")

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        leftMargin=0.65 * inch,
        rightMargin=0.65 * inch,
        topMargin=0.6 * inch,
        bottomMargin=0.6 * inch,
        title="Senior Modern Android Interview Guide",
    )
    doc.build(story)
    return output_path


def main() -> None:
    MARKDOWN_OUTPUT.write_text(build_markdown(), encoding="utf-8")
    pdf_path = build_pdf()
    print(f"Wrote {MARKDOWN_OUTPUT.name}")
    print(f"Wrote {pdf_path.name}")


if __name__ == "__main__":
    main()
