from flask import Flask, request, send_file
import fitz  # PyMuPDF

app = Flask(__name__)

@app.route('/compress', methods=['POST'])
def compress_pdf():
    file = request.files['file']
    input_path = 'input.pdf'
    output_path = 'compressed.pdf'
    file.save(input_path)

    doc = fitz.open(input_path)
    doc.save(output_path, garbage=4, deflate=True, clean=True)
    doc.close()

    return send_file(output_path, as_attachment=True)