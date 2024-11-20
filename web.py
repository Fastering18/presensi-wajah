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

    const compressImage = async (file, { quality = 1, type = file.type }) => {
        // Get as image data
        const imageBitmap = await createImageBitmap(file);

        // Draw to canvas
        const canvas = document.createElement('canvas');
        canvas.width = imageBitmap.width;
        canvas.height = imageBitmap.height;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(imageBitmap, 0, 0);
        if (canvas.width > 1000)
            ctx.scale(0.8, 1);
        if (canvas.height > 1000)
            ctx.scale(1, 0.8);

        // Turn into Blob
        const blob = await new Promise((resolve) =>
            canvas.toBlob(resolve, type, quality)
        );

        // Turn Blob into File
        return new File([blob], file.name, {
            type: blob.type,
        });
    };

    async function updateImageDisplay(e) {
        let file = e.target.files[0];
        if (!file) return;

        let qcompress = 0.5;
        if (file.size > 1_000_080)
            qcompress = 0.1
        else if (file.size > 400_080)
            qcompress = 0.22
        else if (file.size > 100_080)
            qcompress = 0.38

        const dataTransfer = new DataTransfer();
        const compressedFile = await compressImage(file, {
            quality: qcompress,
            type: 'image/jpeg',
        });
        dataTransfer.items.add(compressedFile);
        e.target.files = dataTransfer.files;
        file = compressedFile;
        console.log("compressed file: " + file.size);

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

            let tx = Math.max(x1-10,0);
            let ty = Math.min(y2+20, 2000);
            let nama = data.found[i].nama;
            ctx.font = "bold 40px Arial";
            //ctx.strokeStyle = "black";
            let txtinfo = ctx.measureText(nama);
            console.log("txtinfo", txtinfo.width)

            ctx.fillStyle = "red";
            ctx.fillRect(tx - 5, ty - 5, txtinfo.width + 30, 20);
            ctx.fillStyle = "white";
            ctx.fillText(nama, tx, ty, 350);
            console.log(x1, y1, (x2-x1), (y2-y1));
            }
            if (data.found.length>0) alert("presensi " + data.found[0].nama + (data.found.length>1?" dan lainnya":"") + " berhasil");
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