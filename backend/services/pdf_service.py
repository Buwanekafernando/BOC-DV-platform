from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
import json

def generate_dashboard_pdf(dashboard, output_path):
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph(
        f"<b>Dashboard:</b> {dashboard['name']}", styles["Title"]
    ))
    elements.append(Spacer(1, 20))

    elements.append(Paragraph("<b>Filters</b>", styles["Heading2"]))
    elements.append(Paragraph(str(dashboard["filters"]), styles["Normal"]))
    elements.append(Spacer(1, 15))

    elements.append(Paragraph("<b>Charts</b>", styles["Heading2"]))

    table_data = [["Chart Type", "X Axis", "Y Axis", "Aggregation"]]

    for chart in json.loads(dashboard["charts"]):
        table_data.append([
            chart["chart_type"],
            chart["x_axis"],
            chart["y_axis"],
            chart["aggregation"]
        ])

    table = Table(table_data)
    elements.append(table)

    doc.build(elements)
