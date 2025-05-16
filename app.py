### app.py
#```python
from flask import Flask, render_template, request, send_file, redirect, url_for
from transcription import transcribe_and_generate_pdf
import os

def create_app():
    app = Flask(__name__)
    app.config['OUTPUT_FOLDER'] = 'outputs'
    os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            youtube_url = request.form['youtube_url']
            try:
                pdf_path = transcribe_and_generate_pdf(youtube_url, app.config['OUTPUT_FOLDER'])
                return send_file(pdf_path, as_attachment=True)
            except Exception as e:
                return render_template('index.html', error=str(e))
        return render_template('index.html')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
#```
