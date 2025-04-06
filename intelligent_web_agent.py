import google.generativeai as genai
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import json
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.linecharts import HorizontalLineChart
import matplotlib.pyplot as plt
import io
import base64
from PIL import Image as PILImage
from urllib.parse import urljoin
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the Gemini client with API key from .env
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env file")
genai.configure(api_key=GOOGLE_API_KEY)

def interpret_task(task_description):
    """Use Gemini to interpret the web task and determine the website to visit"""
    # Use the latest Gemini model
    model = genai.GenerativeModel('gemini-1.5-pro')
    prompt = f"""Given this task: '{task_description}', provide a JSON response with these fields: 
    'website_url' (the most appropriate website URL to visit), 
    'extraction_targets' (list of information categories to extract like 'overview', 'key_details', 'recent_updates', etc.), 
    'search_query' (if applicable). 
    Format as valid JSON only."""
    
    response = model.generate_content(prompt)
    
    # Parse the JSON response
    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
      
        response_text = response.text
        if '{' in response_text and '}' in response_text:
            json_str = response_text[response_text.find('{'):response_text.rfind('}')+1]
            return json.loads(json_str)
        return {"error": "Could not parse response", "raw_response": response.text}

def fetch_webpage(url, max_retries=3):
    """Fetch the content of a webpage with retry logic"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    for attempt in range(max_retries):
        try:
            # Add timeout to prevent hanging
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()  # Raise an exception for bad status codes
            return response.text
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1: 
                print(f"Failed to fetch {url} after {max_retries} attempts.")
                print(f"Error: {str(e)}")
                # Try an alternative URL if possible
                alternative_url = get_alternative_url(url)
                if alternative_url:
                    print(f"Trying alternative URL: {alternative_url}")
                    try:
                        response = requests.get(alternative_url, headers=headers, timeout=10)
                        response.raise_for_status()
                        return response.text
                    except:
                        pass
                return ""  # Return empty string if all attempts fail
            print(f"Attempt {attempt + 1} failed. Retrying...")
            time.sleep(2)  # Wait 2 seconds between retries

def get_alternative_url(url):
    """Get an alternative URL for the same content"""
    # Map of alternative URLs for common sites
    alternatives = {
        'www.fs.usda.gov': 'en.wikipedia.org/wiki/Yana_Caves',
        
    }
    
    for domain, alt in alternatives.items():
        if domain in url:
            return f"https://{alt}"
    return None

def extract_information(html_content, extraction_targets, task_description):
    """Use Gemini to extract the relevant information from the webpage"""
    # Create a simplified version of the HTML using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract text content to reduce token usage
    page_text = soup.get_text(separator='\n', strip=True)
    
    # Limit text to avoid token limits
    if len(page_text) > 10000:
        page_text = page_text[:10000] + "..."
    
    
    model = genai.GenerativeModel('gemini-1.5-pro')
    prompt = f"""
Task: {task_description}
Extraction targets: {', '.join(extraction_targets)}
Webpage content:
{page_text}

Extract the requested information from the webpage content above. Provide your response as a valid JSON object with the following structure:
{{
    "overview": [],
    "key_details": [],
    "recent_updates": [],
    "related_information": [],
    "additional_facts": []
}}
Include only the fields that are relevant and available in the content. Format as valid JSON only.
"""
    response = model.generate_content(prompt)
    
    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        
        response_text = response.text
        if '{' in response_text and '}' in response_text:
            json_str = response_text[response_text.find('{'):response_text.rfind('}')+1]
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                return {"error": "Could not parse JSON from response", "raw_response": response_text}
        return {"error": "Could not parse response", "raw_response": response_text}

def execute_web_task(task_description):
    """Main function to execute a web task using Gemini"""
    print(f"Interpreting task: {task_description}")
    
    task_info = interpret_task(task_description)
    
    if "error" in task_info:
        return task_info
    
    print(f"Navigating to: {task_info['website_url']}")
    
    html_content = fetch_webpage(task_info['website_url'])
    
    if not html_content:
        return {
            "error": "Failed to fetch webpage content",
            "overview": ["Unable to retrieve information. Please try again later."]
        }
    
    print(f"Extracting information: {task_info['extraction_targets']}")
    result = extract_information(html_content, task_info['extraction_targets'], task_description)
    
    # Save results with visual elements
    save_results_to_file(
        result, 
        task_description, 
        html_content=html_content, 
        base_url=task_info['website_url']
    )
    
    return result

def download_image(url, max_size=(800, 800)):
    """Download and process an image from URL"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        img = PILImage.open(io.BytesIO(response.content))
        
        # Convert to RGB if necessary
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
        
        
        if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
            img.thumbnail(max_size, PILImage.Resampling.LANCZOS)
        
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')
        img_byte_arr.seek(0)
        
        return Image(img_byte_arr, width=300, height=200)
    except Exception as e:
        print(f"Failed to download image from {url}: {str(e)}")
        return None

def create_chart(data, chart_type='bar'):
    """Create a chart using the provided data"""
    drawing = Drawing(400, 200)
    
    if chart_type == 'bar':
        chart = VerticalBarChart()
        chart.x = 50
        chart.y = 50
        chart.height = 125
        chart.width = 300
        chart.data = [data['values']]
        chart.categoryAxis.categoryNames = data['labels']
        chart.valueAxis.valueMin = 0
        chart.valueAxis.valueMax = max(data['values']) * 1.2
        chart.bars[0].fillColor = colors.blue
        
    elif chart_type == 'pie':
        chart = Pie()
        chart.x = 150
        chart.y = 100
        chart.width = 150
        chart.height = 150
        chart.data = data['values']
        chart.labels = data['labels']
        chart.slices.strokeWidth = 0.5
        
    elif chart_type == 'line':
        chart = HorizontalLineChart()
        chart.x = 50
        chart.y = 50
        chart.height = 125
        chart.width = 300
        chart.data = [data['values']]
        chart.categoryAxis.categoryNames = data['labels']
        chart.lines[0].strokeColor = colors.blue
        
    drawing.add(chart)
    return drawing

def extract_visual_elements(html_content, base_url):
    """Extract images and data for charts from HTML content"""
    soup = BeautifulSoup(html_content, 'html.parser')
    visual_elements = {
        'images': [],
        'charts': []
    }
    
    # Extract images
    for img in soup.find_all('img'):
        src = img.get('src', '')
        if src:
            if not src.startswith(('http://', 'https://')):
                src = urljoin(base_url, src)
            visual_elements['images'].append(src)
    
    # Extract table data that could be visualized
    for table in soup.find_all('table'):
        # Process table data to create chart data
    
        data = {'labels': [], 'values': []}
        for row in table.find_all('tr'):
            cols = row.find_all(['td', 'th'])
            if len(cols) >= 2:
                try:
                    label = cols[0].get_text(strip=True)
                    value = float(cols[1].get_text(strip=True).replace(',', ''))
                    data['labels'].append(label)
                    data['values'].append(value)
                except (ValueError, IndexError):
                    continue
        
        if data['labels'] and data['values']:
            visual_elements['charts'].append(data)
    
    return visual_elements

def save_results_to_file(result, task_description, html_content=None, base_url=None, filename=None):
    """Save the extracted information to a PDF file with visual elements"""
    if filename is None:
        import re
        safe_task = re.sub(r'[^\w\s]', '', task_description)
        safe_task = safe_task.replace(' ', '_')[:30]
        filename = f"{safe_task}_results.pdf"
    
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []
    
   
    styles.add(ParagraphStyle(
        name='CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30
    ))
    styles.add(ParagraphStyle(
        name='CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12
    ))
    
    
    elements.append(Paragraph(f"Task: {task_description}", styles['CustomTitle']))
    elements.append(Paragraph(
        f"Timestamp: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
        styles['Normal']
    ))
    elements.append(Spacer(1, 0.2*inch))
    
    # Extract visual elements if HTML content is available
    if html_content and base_url:
        visual_elements = extract_visual_elements(html_content, base_url)
        
        # Add relevant images
        for img_url in visual_elements['images'][:3]:  # Limit to first 3 images
            img = download_image(img_url)
            if img:
                elements.append(img)
                elements.append(Spacer(1, 0.1*inch))
        
        # Add charts based on extracted data
        for chart_data in visual_elements['charts']:
            if len(chart_data['labels']) <= 5:
                chart = create_chart(chart_data, 'pie')
            else:
                chart = create_chart(chart_data, 'bar')
            elements.append(chart)
            elements.append(Spacer(1, 0.1*inch))
    
    # Add extracted information
    if "error" in result:
        elements.append(Paragraph(f"Error: {result['error']}", styles['CustomHeading']))
        if "raw_response" in result:
            elements.append(Paragraph(f"Raw Response:", styles['CustomHeading']))
            elements.append(Paragraph(result['raw_response'], styles['Normal']))
    else:
        elements.append(Paragraph("Extracted Information:", styles['CustomHeading']))
        for key, value in result.items():
            if isinstance(value, list):
                elements.append(Paragraph(f"{key}:", styles['CustomHeading']))
                
                # Check if the data can be visualized
                if len(value) > 0 and all(isinstance(item, (int, float)) for item in value):
                    chart_data = {
                        'labels': [str(i) for i in range(len(value))],
                        'values': value
                    }
                    elements.append(create_chart(chart_data, 'line'))
                    elements.append(Spacer(1, 0.1*inch))
                
                for i, item in enumerate(value, 1):
                    if isinstance(item, dict):
                        elements.append(Paragraph(f"{i}.", styles['Normal']))
                        for k, v in item.items():
                            elements.append(Paragraph(f"    {k}: {v}", styles['Normal']))
                    else:
                        elements.append(Paragraph(f"  {i}. {item}", styles['Normal']))
                elements.append(Spacer(1, 0.1*inch))
            else:
                elements.append(Paragraph(f"{key}: {value}", styles['Normal']))
    
    # Generate the PDF
    doc.build(elements)
    print(f"Results saved to {filename}")
    return filename

# Example usage
if __name__ == "__main__":
    # Get task description from user input
    print("Web Task Assistant")
    print("------------------")
    task = input("Enter your web task (e.g., 'Find the top 5 AI related headlines'): ")
    
    if not task:
        task = "Find the top 5 AI related headlines from a reputable tech news site"
        print(f"Using default task: {task}")
    
    # Execute the web task
    result = execute_web_task(task)
    print("\nExtracted Information:")
    print(json.dumps(result, indent=2))
    
    # Save results to a text file
    save_results_to_file(result, task)
