import os
from flask import Flask, request, send_from_directory, jsonify
from utils import detect
from flask_cors import CORS
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)
cors = CORS(app, resource={r"/*": {"origins": "*"}})

# Get environment variables
BASE_URL = os.environ.get("BASE_URL", "http://localhost:8003")
PORT = os.environ.get("PORT", 8003)
DEBUG = int(os.environ.get("DEBUG", 1))

UPLOAD_PATH = "uploads"
if not os.path.exists(UPLOAD_PATH):
    os.makedirs(UPLOAD_PATH)

app.config['UPLOAD_PATH'] = UPLOAD_PATH

# Create directory for results
RESULT_PATH = "results"
if not os.path.exists(RESULT_PATH):
    os.makedirs(RESULT_PATH)

app.config["RESULT_PATH"] = RESULT_PATH

ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg"])


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def home():
    return "This app is for ID Card and Mask detection."


@app.route("/api/image/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["RESULT_PATH"], filename)


@app.route("/api/id-card-detection/process-image", methods=["POST"])
def hello():
    if "file" not in request.files:
        return jsonify({"success": False, "error": "No file part"})
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"success": False, "error": "No image selected for uploading"})
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOAD_PATH"], filename))
        is_detected = detect(os.path.join(UPLOAD_PATH, filename))
        if is_detected:
            return (
                jsonify(
                    {
                        "success": True,
                        "image_url": f"{BASE_URL}/api/image/{filename}",
                        "message": "Image processed successfully.",
                    }
                ),
                200,
            )
        else:
            return (
                jsonify(
                    {
                        "success": False,
                        "message": "Unable to process request. Please check with administrator",
                    }
                ),
                400,
            )
    else:
        result = {"success": False, 'message': 'Incorrect file format. Allowed only (jpg, jpeg, png)'}
        return result, 400


if __name__ == "__main__":
    app.run(debug=DEBUG, host="0.0.0.0", port=PORT)
