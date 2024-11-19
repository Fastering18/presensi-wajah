import face_recognition
from flask import Flask, jsonify, request, redirect
from facepresence import recognize_face

app = Flask(__name__)

@app.route('/presensi', methods=['GET', 'POST'])
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
    
    return '''POST ONLY'''

@app.route('/', methods=['GET'])
def index():
    return '''
    <!doctype html>
    <html>
    <head>
    <title>Presensi Kelas</title>
    <meta name="viewport" content= "width=device-width, initial-scale=1.0"> 
    </head>
    <body>
    <h1>Presensi wajah</h1>
    <hr>
    <p>upload foto</p>
    <form method="POST" enctype="multipart/form-data">
      <input type="file" name="file" accept="image/*">
      <!--input type="submit" value="Upload"-->
    </form>
    <br />
    <div class="preview">
        <canvas id="preview_presensi" width="2000" height="2000">
        Browser tidak support canvas
        </canvas>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
    <script>
    const input = document.querySelector("input");
    const previewDiv = document.querySelector(".preview");

    previewDiv.style.visibility = "hidden";

    function updateImageDisplay() {
        let file = input.files[0];
        if (!file) return;

        let c_preview = document.querySelector("#preview_presensi");
        let ctx = c_preview.getContext("2d");
        ctx.clearRect(0, 0, c_preview.width, c_preview.height);

        let image = new Image() 
        image.src = URL.createObjectURL(file);
        image.alt = image.title = file.name;
        image.onload = function() {
            ctx.drawImage(image,0,0)
        }

        previewDiv.style.visibility = "visible";

        var formData = new FormData();
        formData.append("file", file);
        axios.post('/presensi', formData, {
            headers: {
            'Content-Type': 'multipart/form-data'
            }
        }).then(function(r) {
            let data = r.data;
            if (!data || !data.found) return;
            console.log(data);

            for (let i = 0; i < data.found.length; i++){
            let [y1,x2,y2,x1] = data.found[i].lokasi;
            ctx.lineWidth = "6";
            ctx.strokeStyle = "red";
            ctx.rect(x1, y1, (x2-x1), (y2-y1));
            ctx.stroke();
            ctx.font = "bold 30px Arial";
            ctx.strokeText(data.found[i].nama, x1+6, y2+20);
            console.log(x1, y1, (x2-x1), (y2-y1))
            }
        })
        .catch(e => alert(e.toString()));
    }
    input.addEventListener("change", updateImageDisplay);
    </script>
    </body>
    </html>
    '''

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)