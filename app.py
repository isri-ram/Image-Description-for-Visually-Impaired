from PIL import UnidentifiedImageError
from flask import Flask, request, jsonify
from urllib.parse import urlparse
from flask_cors import CORS
import Inference
import requests
import os
app = Flask(__name__)
CORS(app)

@app.route('/health_check', methods=['GET'])
def health_check():
    return 'Server is running correctly', 200

@app.route('/process_image', methods=['POST'])
def process_image():
    image_url = request.json['image_url']
    response = requests.get(image_url)
    if response.status_code == 200:
        try:
            # Extract the original filename from the URL
            filename = os.path.basename(urlparse(image_url).path)

            # Generate the full file path, including the folder path
            image_filename = os.path.join("static", filename)

            # Save the image to the specified folder with the cleaned filename
            with open(image_filename, 'wb') as f:
                f.write(response.content)
            # Replace the 'alt' attribute with the generated caption (example caption)
            caption = Inference.caption_this_image(image_filename)
            return jsonify({'text': caption})
        except requests.exceptions.RequestException as e:
            return jsonify({'error': f'HTTP error: {str(e)}'})
        except UnidentifiedImageError:
            return jsonify({'error': 'Invalid image format.'})
        except Exception as e:
            return jsonify({'error': f'An error occurred: {str(e)}'})


if __name__ == '__main__':
    app.run(debug=True)
