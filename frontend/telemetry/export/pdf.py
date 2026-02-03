import plotly.graph_objects as go
import plotly.io as pio
import base64
import pdfkit
from jinja2 import Environment, FileSystemLoader
import os

# Graphs
from telemetry.graphs.generate_graphs import return_Graphs

def fig_to_base64(fig):
    fig.update_layout(
        width=700,
        height=350,
        margin=dict(l=30, r=30, t=40, b=30),
        font=dict(size=10)
    )
    img_bytes = pio.to_image(
        fig, 
        format="png",
        scale=2
    )
    return base64.b64encode(img_bytes).decode("utf-8")

def convert_to_image(fig):
    return "data:image/png;base64," + fig_to_base64(fig)

def generate_pdf(session_data, rowing_data, name_array, request):
    # Config
    config = pdfkit.configuration(
        wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
    )

    # Render template
    templates_dir = os.path.join(os.path.dirname(__file__), "templates")

    css_path = os.path.join(templates_dir, "styles.css")
    css_path_url = f"file:///{css_path.replace(os.sep, '/')}"

    env = Environment(loader=FileSystemLoader(templates_dir))

    # Create Graphs
    collected_Graphs = return_Graphs(
        'all', 
        session_data,
        rowing_data,
        name_array,
        request,
        selected_sample=None,
        isPdf=True,
    )

    converted_Graphs = {}
    for key, value in collected_Graphs.items():
        print(key)
        # Check for sample lists
        if not type(value) == list:
            converted_Graphs[key] = convert_to_image(value)
        else:
            a=2
            #converted_Graphs[key] = [convert_to_image(v) for v in value]

  
    #converted_Graphs[key] = convert_to_image(value)

    # Create pages
    template = env.get_template('template.html')
    html = template.render(
        rowers=rowing_data,
        boat_data=session_data,
        graphs=converted_Graphs,
        css_path=css_path_url
    )

    options = {
        "page-size": "A4",
        "margin-top": "5mm",
        "margin-bottom": "5mm",
        "margin-left": "5mm",
        "margin-right": "5mm",
        "disable-smart-shrinking": False,
        "zoom": "0.85",
        'enable-local-file-access': '',
        "encoding": "UTF-8",
    }
    
    # Convert HTML -> PDF
    pdf_bytes = pdfkit.from_string(
        html, 
        False, 
        configuration=config,
        options=options
    )
    return pdf_bytes