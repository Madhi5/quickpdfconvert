from flask import Flask, request, send_file
import fitz  # PyMuPDF
import os

app = Flask(__name__)

@app.route('/compress', methods=['POST'])
def compress_pdf():
    file = request.files['file']
    input_path = 'input.pdf'
    output_path = 'compressed.pdf'
    file.save(input_path)

    # Open and compress using PyMuPDF
    doc = fitz.open(input_path)
    doc.save(output_path, garbage=4, deflate=True, clean=True)
    doc.close()

    return send_file(output_path, as_attachment=True)

# ✅ Important: Bind to Render-assigned port
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
