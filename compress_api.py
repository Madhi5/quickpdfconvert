from flask import Flask, request, send_file
from flask_cors import CORS
import fitz  # PyMuPDF
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for Netlify or other origins

@app.route('/compress', methods=['POST'])
def compress_pdf():
    try:
        file = request.files['file']
        input_path = 'input.pdf'
        output_path = 'compressed.pdf'
        file.save(input_path)

        # Open original PDF
        doc = fitz.open(input_path)
        new_doc = fitz.open()

        # Re-render each page as image and insert into new PDF
        zoom = 0.5  # 50% scale for compression
        mat = fitz.Matrix(zoom, zoom)

        for page in doc:
            pix = page.get_pixmap(matrix=mat)
            img_bytes = pix.tobytes("jpeg")
            img_page = new_doc.new_page(width=pix.width, height=pix.height)
            img_rect = fitz.Rect(0, 0, pix.width, pix.height)
            img_page.insert_image(img_rect, stream=img_bytes)

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
