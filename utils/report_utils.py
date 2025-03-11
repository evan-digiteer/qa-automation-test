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

class ReportGenerator:
    def __init__(self):
        self.logger = logging.getLogger('report')
        self.logger.setLevel(logging.INFO)

    def convert_image_to_base64(self, image_path):
        if not image_path:
            return None
        
        if not os.path.exists(image_path):
            return None
        
        try:
            with open(image_path, "rb") as image_file:
                base64_data = base64.b64encode(image_file.read()).decode()
                if base64_data:
                    return base64_data
                else:
                    return None
        except Exception as e:
            self.logger.error(f"Failed to process image: {str(e)}")
            return None

    def create_test_case_html(self, name, status, duration, error=None, screenshot_path=None, logs=None):
        self.logger.debug(f"Processing test: {name}")
        try:
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
            
            # Add error message for failed tests first
            if error:
                formatted_error = error.replace('<', '&lt;').replace('>', '&gt;')
                html_parts.append(f'''
                <div class="error-message">
                    <strong>Error:</strong><br/>
                    {formatted_error}
                </div>
                ''')
            
            # Add logs if available
            if logs and logs.strip():
                html_parts.append(f'''
                <div class="logs-section">
                    <h4>Test Logs:</h4>
                    <pre class="logs">{logs}</pre>
                </div>
                ''')
            
            # Add screenshot if available
            if screenshot_path:
                base64_image = self.convert_image_to_base64(screenshot_path)
                if base64_image:
                    html_parts.append(f'''
                    <div class="screenshot-section">
                        <h4>Screenshot:</h4>
                        <img class="screenshot" src="data:image/png;base64,{base64_image}" 
                             alt="Test Screenshot" />
                    </div>
                    ''')
            
            html_parts.append("</div></div>")
            return '\n'.join(html_parts)
            
        except Exception as e:
            self.logger.error(f"Error creating test case HTML: {str(e)}", exc_info=True)
            return f'<div class="error-message">Error generating test case content: {str(e)}</div>'

    def generate_report(self, results, output_path):
        self.logger.info("Generating test report...")
        # ...existing code...
        self.logger.info(f"Report generated: {output_path}")
