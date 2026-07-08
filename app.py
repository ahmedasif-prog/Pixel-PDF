from flask import Flask,render_template, request, send_file
from io import BytesIO
from PIL import Image
from pypdf import PdfWriter

app = Flask(__name__)
supported_formats=["JPEG","GIF","PNG","WEBP"]
@app.route("/")
def home():
    return render_template('home.html')
@app.route("/imageconvertor", methods=["GET","POST"])
def imageconvertor():
    if(request.method=="POST"):
        file=request.files["image"]
        targeted_format=request.form["format"]
        
        img=Image.open(file)
        if targeted_format=="JPEG" and img.mode in ("RGBA","P"):
            img=img.convert("RGB")
        output=BytesIO()
        img.save(output,format=targeted_format)
        output.seek(0)
        return send_file(
            output,
            mimetype=f"image/{targeted_format.lower()}", 
            as_attachment=True, 
            download_name=f"converted.{targeted_format.lower()}"
        )

    return render_template('imageconvertor.html')
@app.route("/pdf_merger",methods=["GET","POST"])
def pdf_merger():
    if(request.method=="POST"):
        files=request.files.getlist("pdfs")
        if len(files) < 2:
            return render_template(
            "pdf_merger.html",
            error="Please select at least 2 PDF files."
    )
        merger=PdfWriter()
        for file in files:
            merger.append(file)
        output=BytesIO()
        merger.write(output)
        merger.close()
        output.seek(0)
        return send_file(output,
            mimetype="application/pdf",
            as_attachment=True,
            download_name="merged.pdf")
    return render_template('pdf_merger.html')
@app.route("/imagecompressor",methods=["GET","POST"])
def imagecompressor():
    if(request.method=="POST"):
        file=request.files["image"]
        img=Image.open(file)
        original_format=img.format
        output=BytesIO()
        img=img.convert("RGB")
        img.save(output,format="JPEG",quality=70,optimize=True)
        output.seek(0)
        return send_file(
            output,
            mimetype=f"image/jpg",
            as_attachment=True,
            download_name=f"compressed.jpg"
        )

    return render_template('imagecompressor.html')
import os

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=True
    )
