from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt


OUTPUT_PATH = Path(__file__).resolve().parents[1] / "slides" / "dark-mode-private-preview-leadership-review.pptx"


def set_run_font(run, size, bold=False, color=(0, 0, 0), name="Aptos"):
    run.font.name = name
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = RGBColor(*color)


def add_textbox(slide, left, top, width, height, text, size, color, bold=False, name="Aptos", margin=0.06, align=PP_ALIGN.LEFT):
    box = slide.shapes.add_textbox(left, top, width, height)
    frame = box.text_frame
    frame.word_wrap = True
    frame.margin_left = Inches(margin)
    frame.margin_right = Inches(margin)
    frame.margin_top = Inches(margin)
    frame.margin_bottom = Inches(margin)
    paragraph = frame.paragraphs[0]
    paragraph.alignment = align
    run = paragraph.add_run()
    run.text = text
    set_run_font(run, size=size, bold=bold, color=color, name=name)
    return box


def add_panel(slide, left, top, width, height, fill_rgb, line_rgb=(220, 226, 232), radius_shape=MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE):
    panel = slide.shapes.add_shape(radius_shape, left, top, width, height)
    panel.fill.solid()
    panel.fill.fore_color.rgb = RGBColor(*fill_rgb)
    panel.line.color.rgb = RGBColor(*line_rgb)
    panel.line.width = Pt(1)
    return panel


def add_bullet_list(slide, left, top, width, height, items, font_size=14, color=(22, 33, 43)):
    box = slide.shapes.add_textbox(left, top, width, height)
    frame = box.text_frame
    frame.word_wrap = True
    frame.margin_left = Inches(0.08)
    frame.margin_right = Inches(0.04)
    frame.margin_top = Inches(0.04)
    frame.margin_bottom = Inches(0.04)
    frame.clear()
    for index, item in enumerate(items):
        paragraph = frame.paragraphs[0] if index == 0 else frame.add_paragraph()
        paragraph.level = 0
        paragraph.bullet = True
        paragraph.space_after = Pt(7)
        run = paragraph.add_run()
        run.text = item
        set_run_font(run, size=font_size, color=color)
    return box


def add_table_header(slide, left, top, col_widths, headers, colors):
    """Draw table header row with columns."""
    current_left = left
    for i, (width, header, color) in enumerate(zip(col_widths, headers, colors)):
        cell = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE, current_left, top, width, Inches(0.28))
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(*color)
        cell.line.color.rgb = RGBColor(150, 160, 170)
        cell.line.width = Pt(0.5)
        add_textbox(slide, current_left + Inches(0.06), top + Inches(0.05), width - Inches(0.12), Inches(0.18), header, 9.5, (22, 33, 43), bold=True)
        current_left += width


def add_table_row(slide, left, top, col_widths, data, is_alternate=False):
    """Draw a single table row with three columns."""
    bg_color = (247, 249, 250) if is_alternate else (255, 255, 255)
    current_left = left
    for i, (width, value) in enumerate(zip(col_widths, data)):
        cell = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE, current_left, top, width, Inches(0.32))
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(*bg_color)
        cell.line.color.rgb = RGBColor(215, 220, 228)
        cell.line.width = Pt(0.5)
        
        font_size = 9 if i == 2 else 10
        font_bold = i == 2
        font_color = (15, 108, 189) if i == 2 else (22, 33, 43)
        
        add_textbox(slide, current_left + Inches(0.06), top + Inches(0.07), width - Inches(0.12), Inches(0.18), value, font_size, font_color, bold=font_bold)
        current_left += width


def build_slide():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    bg = slide.background.fill
    bg.solid()
    bg.fore_color.rgb = RGBColor(244, 239, 230)

    # Accent bands
    band_top = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.34))
    band_top.fill.solid()
    band_top.fill.fore_color.rgb = RGBColor(21, 35, 46)
    band_top.line.fill.background()

    band_right = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE, Inches(12.93), Inches(0), Inches(0.403), Inches(7.5))
    band_right.fill.solid()
    band_right.fill.fore_color.rgb = RGBColor(15, 108, 189)
    band_right.line.fill.background()

    add_textbox(
        slide,
        Inches(0.45),
        Inches(0.18),
        Inches(2.7),
        Inches(0.24),
        "LEADERSHIP REVIEW | FABRIC DARK MODE",
        10,
        (255, 255, 255),
        bold=True,
    )

    add_textbox(
        slide,
        Inches(0.5),
        Inches(0.65),
        Inches(7.55),
        Inches(1.0),
        "Private Preview Plan: deliver a credible, customer-visible dark mode experience in Fabric by 5/29/2026.",
        24,
        (22, 33, 43),
        bold=True,
    )
    add_textbox(
        slide,
        Inches(0.55),
        Inches(1.53),
        Inches(7.35),
        Inches(0.78),
        "Dark mode reduces eye strain, modernizes the Fabric shell, and gives customers a consistent visual experience across the shell and priority creator workloads in private preview scope.",
        12.5,
        (83, 97, 112),
    )

    # Date card
    add_panel(slide, Inches(9.12), Inches(0.62), Inches(3.55), Inches(1.42), (21, 35, 46), line_rgb=(21, 35, 46))
    add_textbox(slide, Inches(9.34), Inches(0.8), Inches(2.9), Inches(0.22), "PRIVATE PREVIEW TARGET", 9.5, (202, 217, 227), bold=True)
    add_textbox(slide, Inches(9.3), Inches(1.03), Inches(3.0), Inches(0.44), "May 29, 2026", 24, (255, 255, 255), bold=True)
    add_textbox(slide, Inches(9.3), Inches(1.45), Inches(3.0), Inches(0.34), "As of May 11: adoption on track. Align on scope, readiness bar, and preview message.", 10.5, (221, 231, 238))

    # Left scope panel
    add_panel(slide, Inches(0.45), Inches(2.28), Inches(3.2), Inches(4.35), (255, 252, 247))
    add_textbox(slide, Inches(0.63), Inches(2.43), Inches(2.4), Inches(0.25), "IN PREVIEW SCOPE", 10, (83, 97, 112), bold=True)
    scope_items = [
        "Fabric Shell | Train 5.1",
        "Workloads Hub L1 | Released",
        "OneLake Category | Train 5.2",
        "Lakehouse | Released",
        "Variable Library | Train 4.2",
        "Notebook | Train 5.3",
        "Real-Time Hub | Train 3.1",
        "Kusto | Independent deployment",
        "Warehouse & Azure SQL DW | Released",
        "Data Science | Train 3.1",
    ]
    add_bullet_list(slide, Inches(0.62), Inches(2.76), Inches(2.82), Inches(3.62), scope_items, font_size=11.2)

    # Middle adoption status panel
    add_panel(slide, Inches(3.82), Inches(2.28), Inches(5.1), Inches(4.35), (255, 252, 247))
    add_textbox(slide, Inches(4.0), Inches(2.43), Inches(3.6), Inches(0.25), "DARK MODE ADOPTION STATUS (MAY 11)", 10, (83, 97, 112), bold=True)

    chips = [
        (Inches(4.0), Inches(2.78), Inches(2.22), Inches(0.88), (231, 244, 231), "Adoption Signal: Strong", "Bug bash complete with no sev1 or sev2 blockers; pilot signal is stable."),
        (Inches(6.4), Inches(2.78), Inches(2.22), Inches(0.88), (232, 241, 251), "Activation Path Working", "Users enable in Settings, persist after refresh, and remain dark across shell entry points."),
        (Inches(4.0), Inches(3.79), Inches(2.22), Inches(0.88), (232, 241, 251), "Cross-Surface Adoption", "Supported workloads declare dark mode; unsupported experiences fall back safely."),
        (Inches(6.4), Inches(3.79), Inches(2.22), Inches(0.88), (250, 242, 220), "Adoption Is Scoped", "A strong first milestone focused on high-value surfaces, not full Fabric-wide completion."),
    ]
    for left, top, width, height, color, title, body in chips:
        add_panel(slide, left, top, width, height, color, line_rgb=(220, 226, 232))
        add_textbox(slide, left + Inches(0.1), top + Inches(0.07), width - Inches(0.2), Inches(0.18), title, 10.5, (22, 33, 43), bold=True)
        add_textbox(slide, left + Inches(0.1), top + Inches(0.28), width - Inches(0.2), Inches(0.48), body, 8.8, (22, 33, 43))

    add_textbox(slide, Inches(4.02), Inches(4.95), Inches(4.45), Inches(0.22), "CUSTOMER STORY FOR LEADERSHIP", 10, (83, 97, 112), bold=True)
    story_items = [
        "Customer turns on dark mode in Settings and sees the shell switch immediately.",
        "Preference persists after refresh and continues across Home, Browse, Workspace list, and Monitoring Hub.",
        "Supported workloads deliver dark mode; unsupported experiences fall back safely instead of shipping a broken mixed theme.",
    ]
    add_bullet_list(slide, Inches(4.0), Inches(5.22), Inches(4.55), Inches(1.1), story_items, font_size=10)

    # Right customer selection and post-preview plan panel
    add_panel(slide, Inches(9.12), Inches(2.28), Inches(3.55), Inches(4.35), (255, 252, 247))
    add_textbox(slide, Inches(9.3), Inches(2.43), Inches(3.0), Inches(0.25), "PRIVATE PREVIEW CUSTOMER SELECTION", 10, (83, 97, 112), bold=True)
    add_textbox(
        slide,
        Inches(9.28),
        Inches(2.69),
        Inches(3.05),
        Inches(0.34),
        "Target preview customers who maximize visible value and fast product learning in supported dark-mode workloads.",
        8.7,
        (83, 97, 112),
    )
    add_panel(slide, Inches(9.28), Inches(3.04), Inches(3.05), Inches(1.02), (232, 241, 251), line_rgb=(210, 223, 237))
    selection_items = [
        "Active creators in supported workloads: Lakehouse, Warehouse, Notebook, Real-Time Hub, Data Science, and Kusto.",
        "Customers with long working sessions where eye strain reduction and visual comfort are immediately noticeable.",
        "Design partners willing to give fast feedback on shell consistency, persistence, and extension transitions.",
    ]
    add_bullet_list(slide, Inches(9.34), Inches(3.12), Inches(2.9), Inches(0.82), selection_items, font_size=8.4)
    add_textbox(slide, Inches(9.3), Inches(4.14), Inches(3.0), Inches(0.22), "POST PRIVATE PREVIEW PLAN", 10, (83, 97, 112), bold=True)
    add_textbox(
        slide,
        Inches(9.28),
        Inches(4.35),
        Inches(3.05),
        Inches(0.24),
        "Next-wave onboarding after the 5/29 preview milestone, based on current owners and target release buckets.",
        8.4,
        (83, 97, 112),
    )
    plan_rows = [
        ("Functions Hub", "Sunitha Muthukrishna", "Post-RB"),
        ("OneLake Catalog - Govern", "Naama Tsafrir", "Q2 RB"),
        ("Deployment Pipelines", "Nimrod Shalit", "Q2 RB"),
        ("Power BI", "Kay Unkroth", "Post-RB"),
        ("Data flow", "Miguel Escobar", "Post-RB"),
        ("Event Stream", "Alicia Li", "Q1 RB"),
        ("Azure Data Factory", "Hao Chen", "Q1 RB"),
        ("Data Activator", "Amanda Rivera", "Q2 RB or Post-RB"),
        ("Spark Job Definition", "Qixiao Wang", "Q2 RB"),
    ]
    
    table_left = Inches(9.28)
    table_top = Inches(4.63)
    col_widths = [Inches(1.6), Inches(1.05), Inches(0.4)]
    headers = ["Item", "Owner", "Plan"]
    header_colors = [(207, 220, 234), (207, 220, 234), (207, 220, 234)]
    
    add_table_header(slide, table_left, table_top, col_widths, headers, header_colors)
    
    row_top = table_top + Inches(0.28)
    for idx, (item, owner, plan) in enumerate(plan_rows):
        add_table_row(slide, table_left, row_top, col_widths, [item, owner, plan], is_alternate=(idx % 2 == 1))
        row_top += Inches(0.32)

    # Footer note
    footer = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE, Inches(0.45), Inches(6.78), Inches(12.2), Inches(0.43))
    footer.fill.solid()
    footer.fill.fore_color.rgb = RGBColor(250, 247, 240)
    footer.line.color.rgb = RGBColor(226, 219, 206)
    footer.line.width = Pt(1)
    add_textbox(
        slide,
        Inches(0.62),
        Inches(6.88),
        Inches(11.8),
        Inches(0.16),
        "Private preview customer selection focuses on supported creator workloads and fast-feedback partners; the items at right show the next expansion wave after launch.",
        9.5,
        (83, 97, 112),
    )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    prs.save(OUTPUT_PATH)
    return OUTPUT_PATH


if __name__ == "__main__":
    output = build_slide()
    print(output)