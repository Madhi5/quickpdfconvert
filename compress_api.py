from flask import Flask, request, send_file
from flask_cors import CORS
import fitz  # PyMuPDF
import os

app = Flask(__name__)
CORS(app)  # ✅ Enable CORS for all domains (Netlify, localhost, etc.)

@app.route('/compress', methods=['POST'])
def compress_pdf():
    try:
        file = request.files['file']
        input_path = 'input.pdf'
        output_path = 'compressed.pdf'
        file.save(input_path)

        # Compress the PDF using PyMuPDF
        doc = fitz.open(input_path)
        doc.save(output_path, garbage=4, deflate=True, clean=True)
        doc.close()

        return send_file(output_path, as_attachment=True)
    except Exception as e:
        print(f"Error during compression: {e}")
        return {"error": str(e)}, 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
