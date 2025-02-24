import base64
from datetime import datetime
import logging
from io import StringIO
import os

class TestCaseLogHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.log_records = []
        self.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    def emit(self, record):
        self.log_records.append(self.format(record))

    def get_logs(self):
        return '\n'.join(self.log_records)

def image_to_base64(image_path):
    """Convert image to base64 string"""
    if not image_path:
        logging.warning(f"No screenshot path provided")
        return None
    
    if not os.path.exists(image_path):
        logging.error(f"Screenshot file does not exist: {image_path}")
        return None
        
    try:
        logging.info(f"Reading image file: {image_path}")
        with open(image_path, "rb") as image_file:
            base64_data = base64.b64encode(image_file.read()).decode()
            if base64_data:
                logging.info(f"Successfully converted image to base64 (length: {len(base64_data)})")
                return base64_data
            else:
                logging.error("Base64 conversion resulted in empty string")
                return None
    except Exception as e:
        logging.error(f"Failed to convert image to base64: {str(e)}", exc_info=True)
        return None

def create_test_case_html(name, status, duration, error=None, screenshot_path=None, logs=None):
    """Create HTML for a single test case with improved debugging"""
    try:
        logging.info(f"Creating HTML for test case: {name}")
        html_parts = []
        
        # Generate test header
        status_class = status.lower()
        duration_seconds = duration if isinstance(duration, float) else duration / 1000000
        html_parts.append(f'''
        <div class="test-case">
            <div class="test-header {status_class}">
                <span>{name}</span>
                <span>{duration_seconds:.2f}s</span>
            </div>
            <div class="test-content">
        ''')
        
        # Add logs if available
        if logs and logs.strip():
            logging.info(f"Adding logs for {name} (length: {len(logs)})")
            html_parts.append(f'''
            <div class="logs-section">
                <h4>Test Logs:</h4>
                <pre class="logs">{logs}</pre>
            </div>
            ''')
        else:
            logging.warning(f"No logs available for {name}")
            html_parts.append('<div class="logs-section"><h4>No logs available</h4></div>')
        
        # Add error message for failed tests
        if error:
            html_parts.append(f'<div class="error-message">{error}</div>')
        
        # Add screenshot if available
        if screenshot_path:
            logging.info(f"Processing screenshot for {name}: {screenshot_path}")
            if os.path.exists(screenshot_path):
                base64_image = image_to_base64(screenshot_path)
                if base64_image:
                    html_parts.append(f'''
                    <div class="screenshot-section">
                        <h4>Screenshot:</h4>
                        <img class="screenshot" src="data:image/png;base64,{base64_image}" 
                             alt="Test Screenshot" 
                             style="cursor: pointer"/>
                    </div>
                    ''')
                else:
                    html_parts.append('<div class="error-message">Failed to convert screenshot to base64</div>')
            else:
                html_parts.append(f'<div class="error-message">Screenshot file not found: {screenshot_path}</div>')
        else:
            logging.warning(f"No screenshot path provided for {name}")
            html_parts.append('<div class="screenshot-section"><h4>No screenshot available</h4></div>')
        
        html_parts.append("</div></div>")
        return '\n'.join(html_parts)
        
    except Exception as e:
        logging.error(f"Error creating test case HTML: {str(e)}", exc_info=True)
        return f'<div class="error-message">Error generating test case content: {str(e)}</div>'
