

from flask import Flask, render_template, request, session, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
from keras.models import load_model
import matplotlib.pyplot as plt
import cv2
import numpy as np
import tensorflow as tf

# Load model


UPLOAD_FOLDER = './flask app/assets/images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
# Create Database if it doesnt exist

app = Flask(__name__,static_url_path='/assets',
            static_folder='./flask app/assets', 
            template_folder='./flask app')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def root():
   return render_template('index.html')

@app.route('/index.html')
def index():
   return render_template('index.html')

@app.route('/contact.html')
def contact():
   return render_template('contact.html')

@app.route('/news.html')
def news():
   return render_template('news.html')

@app.route('/about.html')
def about():
   return render_template('about.html')

@app.route('/faqs.html')
def faqs():
   return render_template('faqs.html')

@app.route('/prevention.html')
def prevention():
   return render_template('prevention.html')

@app.route('/upload.html')
def upload():
   return render_template('upload.html')

@app.route('/upload_chest.html')
def upload_chest():
   return render_template('upload_chest.html')


@app.route('/upload_ct.html')
def upload_ct():
   return render_template('upload_ct.html')

@app.route('/uploaded_chest', methods = ['POST', 'GET'])
def uploaded_chest():
   if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            # filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'upload_chest.jpg'))

   inception_chest = tf.keras.models.load_model("inceptionv3_chest.h5")
   
   image = cv2.imread('./flask app/assets/images/upload_chest.jpg') # read file 
   image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # arrange format as per keras
   image = cv2.resize(image,(224,224))
   image = np.array(image) / 255
   image = np.expand_dims(image, axis=0)
   
   inception_pred = inception_chest.predict(image)
   probability = inception_pred[0]
   print("Inception Predictions:")
   if probability[0] > 0.5:
      inception_chest_pred = str('%.2f' % (probability[0]*100) + '% COVID') 
   else:
      inception_chest_pred = str('%.2f' % ((1-probability[0])*100) + '% NonCOVID')
   print(inception_chest_pred)

   return render_template('results_chest.html',inception_chest_pred=inception_chest_pred)
@app.route('/uploaded_ct', methods = ['POST', 'GET'])
def uploaded_ct():
   if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            # filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'upload_ct.jpg'))

   inception_ct=tf.keras.models.load_model("inception_ct.h5")   
   image = cv2.imread('./flask app/assets/images/upload_ct.jpg') # read file 
   image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # arrange format as per keras
   image = cv2.resize(image,(224,224))
   image = np.array(image) / 255
   image = np.expand_dims(image, axis=0)
   
   inception_pred = inception_ct.predict(image)
   probability = inception_pred[0]
   print("Inception Predictions:")
   if probability[0] > 0.5:
      inception_ct_pred = str('%.2f' % (probability[0]*100) + '% COVID') 
   else:
      inception_ct_pred = str('%.2f' % ((1-probability[0])*100) + '% NonCOVID')
   print(inception_ct_pred)
   return render_template('results_ct.html',inception_ct_pred=inception_ct_pred)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
