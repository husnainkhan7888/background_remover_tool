import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from rembg import remove
from PIL import Image

app = Flask(__name__)

# Set up a folder to store uploaded and processed images
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the uploads folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    """Home page with navigation to different tools or pages."""
    return render_template('home.html')

@app.route('/remove-bg', methods=['GET', 'POST'])
def remove_bg():
    """Page to upload an image and remove its background."""
    if request.method == 'POST':
        if 'image' not in request.files:
            return redirect(request.url)
        
        file = request.files['image']
        if file.filename == '':
            return redirect(request.url)
        
        if file:
            # Save the original image
            original_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(original_path)

            # Remove background using rembg
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], f"bg_removed_{file.filename}")
            with Image.open(original_path) as input_image:
                processed = remove(input_image)
                processed.save(output_path)

            # Redirect to a results page to display both images
            return redirect(url_for('result', original=file.filename, processed=f"bg_removed_{file.filename}"))

    return render_template('remove_bg.html')

@app.route('/result')
def result():
    """Display the original and processed images."""
    original_filename = request.args.get('original')
    processed_filename = request.args.get('processed')
    return render_template('result.html',
                           original_image=original_filename,
                           processed_image=processed_filename)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files from the UPLOAD_FOLDER."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
