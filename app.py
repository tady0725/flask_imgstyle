import matplotlib.pyplot as plt
from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
import shutil
# from torch import randint
from werkzeug.utils import secure_filename
import tensorflow as tf
import tensorflow_hub as hub
import random
import matplotlib
matplotlib.use('Agg')

hub_module = hub.load(
    'https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')


def img_scaler(image, max_dim=512):

    # Casts a tensor to a new type.
    original_shape = tf.cast(tf.shape(image)[:-1], tf.float32)

    # Creates a scale constant for the image
    scale_ratio = max_dim / max(original_shape)

    # Casts a tensor to a new type.
    new_shape = tf.cast(original_shape * scale_ratio, tf.int32)

    # Resizes the image based on the scaling constant generated above
    return tf.image.resize(image, new_shape)


def load_img(path_to_img):

    # Reads and outputs the entire contents of the input filename.
    img = tf.io.read_file(path_to_img)

    # Detect whether an image is a BMP, GIF, JPEG, or PNG, and
    # performs the appropriate operation to convert the input
    # bytes string into a Tensor of type dtype
    img = tf.image.decode_image(img, channels=3)

    # Convert image to dtype, scaling (MinMax Normalization) its values if needed.
    img = tf.image.convert_image_dtype(img, tf.float32)

    # Scale the image using the custom function we created
    img = img_scaler(img)

    # Adds a fourth dimension to the Tensor because
    # the model requires a 4-dimensional Tensor
    return img[tf.newaxis, :]


app = Flask(__name__)


UPLOAD_FOLDER = 'static/uploads/'

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    file2 = request.files['file2']

    if file.filename == '' and file2.filename:
        flash('No image selected for uploading')
        return redirect(request.url)

    if file and allowed_file(file.filename) and file2 and allowed_file(file2.filename):
        filename = secure_filename(file.filename)
        filename2 = secure_filename(file2.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))
        #print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')

        if request.method == 'POST':
            if request.values['send'] == '送出':
                filen = 'static\\uploads\\' + filename
                filen2 = 'static\\uploads\\' + filename2
                content_image = load_img(filen)
                style_image = load_img(filen2)
                stylized_image = hub_module(tf.constant(
                    content_image), tf.constant(style_image))[0]

                img = stylized_image[0]
                plt.imshow(stylized_image[0])
                # plt.show(img)
                s = random.randint(1, 100000000000)

                plt.savefig('static\\uploads\\'+"style"+str(s)+'.jpeg')
                path = "style"+str(s)+".jpeg"

        return render_template('index.html', filename=filename, filename2=filename2, style=str(path))

    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)


@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


# @app.route('/', methods=['POST', 'GET'])
# def index():
#     if request.method == 'POST':
#         if request.values['send'] == '送出':
#             return render_template('test.html', name=request.values['user'], send="jp")
#     return render_template('index.html', name="")


# @app.route('/get', methods=['POST', 'GET'])
# def get():
#     return render_template('test.html')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
