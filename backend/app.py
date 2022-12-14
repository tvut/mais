from flask import Flask, request
from flask_cors import CORS

import tensorflow as tf
import numpy as np
from tensorflow import keras
import cv2 as cv
from keras.preprocessing import image
import json

model2 = keras.models.load_model('model')

app = Flask(__name__)
cors = CORS(app, resources={r'/*': {"origins": '*'}})
# app.config['CORS_HEADER'] = 'Content-Type'


@app.route('/upload', methods=['POST'])
def upload_file():
    formData = request.files.get('file','')
    print(type(formData))

    filestr = formData.read()
    #convert string data to numpy array
    npimg = np.fromstring(filestr, np.uint8)
    # convert numpy array to image
    img = cv.imdecode(npimg, cv.IMREAD_COLOR)
    print(img.shape)

    img = cv.resize(img, (128,128))
    print(img.shape)
    x = np.expand_dims(img, axis=0)

    print(x.shape)
    results = model2.predict(x)[0]

    labels = ['Battery', 'Biological', 'Brown Glass', 'Cardboard', 'Clothes', 'Green Glass', 'Metal', 'Paper', 'Plastic', 'Shoes', 'Trash', 'White Glass']

    ret = dict()

    for r in range(len(labels)):
        ret[labels[r]] = json.dumps(results[r].item())


    # print(request.file)
    # uploaded_file = request.files['file']
    # if uploaded_file.filename != '':
    #     uploaded_file.save(uploaded_file.filename)
    # return redirect(url_for('index'))
    return ret

@app.route('/')
def simple():
    return dict()