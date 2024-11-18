import face_recognition
from flask import Flask, jsonify, request, redirect
from facepresence import recognize_face

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def upload_image():
    # Check if a valid image file was uploaded
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)
        
        img = face_recognition.load_image_file(file)
        res = recognize_face(img)
        print(res)
        return jsonify({'found': res})

    return '''
    <!doctype html>
    <html>
    <title>Cek rai</title>
    </html>
    <body>
    <h1>Presensi wajah</h1>
    <hr>
    <p>upload foto</p>
    <form method="POST" enctype="multipart/form-data">
      <input type="file" name="file" accept="image/*">
      <input type="submit" value="Upload">
    </form>
    <script>
    const input = document.querySelector("input");

    function updateImageDisplay() {
        let file = input.files[0]
        if (!file) return;

        let image = document.createElement("img");
        image.src = URL.createObjectURL(file);
        image.alt = image.title = file.name;
        document.appendChild(image);
    }
    input.addEventListener("change", updateImageDisplay);
    </script>
    </body>
    '''

#if __name__ == "__main__":
#    app.run(host='0.0.0.0', port=8000)