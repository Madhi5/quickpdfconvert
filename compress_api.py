from flask import Flask, request, send_file
from flask_cors import CORS
import fitz  # PyMuPDF
from PIL import Image
import os
import io

app = Flask(__name__)
CORS(app)

@app.route('/compress', methods=['POST'])
def compress_pdf():
    try:
        file = request.files['file']
        input_path = 'input.pdf'
        output_path = 'compressed.pdf'
        file.save(input_path)

        doc = fitz.open(input_path)
        new_doc = fitz.open()
        zoom = 0.5
        mat = fitz.Matrix(zoom, zoom)

        for page in doc:
            pix = page.get_pixmap(matrix=mat)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

            img_io = io.BytesIO()
            img.save(img_io, format='JPEG', quality=250)  # Balanced compression
            img_bytes = img_io.getvalue()

            new_page = new_doc.new_page(width=pix.width, height=pix.height)
            new_page.insert_image(fitz.Rect(0, 0, pix.width, pix.height), stream=img_bytes)

        new_doc.save(output_path, garbage=4, deflate=True)
        new_doc.close()
        doc.close()

        return send_file(output_path, as_attachment=True)

    except Exception as e:
        print(f"Error during compression: {e}")
        return {"error": str(e)}, 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
