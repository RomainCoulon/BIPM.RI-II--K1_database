from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
import xml.etree.ElementTree as ET
from fastapi.templating import Jinja2Templates
from fastapi import Request

app = FastAPI()

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Root route - Serve HTML form for file upload
@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("upload_form.html", {"request": request})

# Route to handle XML file upload and parsing
@app.post("/upload/")
async def upload_xml(request: Request, file: UploadFile = File(...)):
    try:
        # Read the uploaded XML file
        xml_content = await file.read()
        
        # Parse the XML content
        root = ET.fromstring(xml_content)

        # Extract data from the kc:generalInformation tag
        parsed_data = parse_xml(root)

        # Return parsed data as HTML
        return templates.TemplateResponse("result.html", {"request": request, "parsed_data": parsed_data})

    except Exception as e:
        return {"error": str(e)}

# Function to parse the XML structure and extract kc:generalInformation
def parse_xml(root):
    # Define namespace prefix if the XML uses namespaces
    namespaces = {'kc': 'KC_model_RI_II.xsd'}  # Replace with actual namespace URI if known
    
    # Find the kc:generalInformation element
    general_info = root.find('kc:generalInformation', namespaces)
    
    if general_info is not None:
        return f"Tag: kc:generalInformation, Text: {general_info.text}"
    else:
        return "kc:generalInformation tag not found"
