# import cv2
# import numpy as np
# from flask import Flask, request, jsonify

# app = Flask(__name__)

# @app.route('/', methods=['GET'])
# def index():
#     return jsonify({"status": "Coin Detection API is running!"})

# @app.route('/detect-coins', methods=['POST'])
# def detect_coins():
#     if 'image' not in request.files:
#         return jsonify({"error": "No image provided"}), 400
        
#     file = request.files['image']
    
#     try:
#         # Read image from request
#         file_bytes = np.fromfile(file, np.uint8)
#         img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        
#         if img is None:
#             return jsonify({"error": "Invalid image file"}), 400
            
#         # Convert to Grayscale
#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
#         # Blur the image
#         blurred = cv2.GaussianBlur(gray, (31, 31), cv2.BORDER_DEFAULT)
        
#         # Detect circles using the tuned parameters
#         circles_float = cv2.HoughCircles(
#             blurred, 
#             cv2.HOUGH_GRADIENT, 
#             dp=0.9, 
#             minDist=50, 
#             param1=50, 
#             param2=30, 
#             minRadius=50, 
#             maxRadius=200
#         )
        
#         coin_count = 0
#         if circles_float is not None:
#             # Number of coins is the length of the 2nd dimension
#             coin_count = circles_float.shape[1]
            
#         return jsonify({
#             "success": True,
#             "coin_count": coin_count
#         })
        
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)



import cv2
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Enable CORS for all domains
CORS(app)

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "status": "Coin Detection API is running!"
    })

@app.route('/detect-coins', methods=['POST'])
def detect_coins():

    if 'image' not in request.files:
        return jsonify({
            "success": False,
            "error": "No image provided"
        }), 400

    try:
        file = request.files['image']

        # Read uploaded image
        file_bytes = np.frombuffer(
            file.read(),
            np.uint8
        )

        img = cv2.imdecode(
            file_bytes,
            cv2.IMREAD_COLOR
        )

        if img is None:
            return jsonify({
                "success": False,
                "error": "Invalid image file"
            }), 400

        # Convert to grayscale
        gray = cv2.cvtColor(
            img,
            cv2.COLOR_BGR2GRAY
        )

        # Blur image
        blurred = cv2.GaussianBlur(
            gray,
            (31, 31),
            0
        )

        # Detect circles (coins)
        circles = cv2.HoughCircles(
            blurred,
            cv2.HOUGH_GRADIENT,
            dp=0.9,
            minDist=50,
            param1=50,
            param2=30,
            minRadius=50,
            maxRadius=200
        )

        coin_count = 0

        if circles is not None:
            coin_count = circles.shape[1]

        return jsonify({
            "success": True,
            "coin_count": int(coin_count)
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
