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
    <title>Cek rai</title>
    <h1>Upload</h1>
    <form method="POST" enctype="multipart/form-data">
      <input type="file" name="file">
      <input type="submit" value="Upload">
    </form>
    '''

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=46464, debug=True)