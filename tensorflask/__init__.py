import os
import cv2
import numpy as np
from PIL import Image
from io import BytesIO
from flask import Flask, request, render_template
import tensorflow as tf
from tensorflask.porn_identifier.model import PornIdentifier

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'tensorflask.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    sess = tf.Session()
    pron_identifier = PornIdentifier()
    sess.run(tf.global_variables_initializer())
    pron_identifier.load_vgg17_weights(sess)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
 
    @app.route('/up_photo', methods=['GET', 'POST'])
    def up_photo():
        img_file_storage = request.files.get('photo')
        if img_file_storage is None:
            return render_template('upload_image.html')
        img_name = img_file_storage.filename
        img_bytes = img_file_storage.read()
        img_pil = Image.open(BytesIO(img_bytes))
        img_pil_rgb = img_pil.convert("RGB")
        img = np.array(img_pil_rgb)
        img = np.divide(img, 255.0)
        assert (0 <= img).all() and (img <= 1.0).all()

        short_edge = min(img.shape[:2])
        yy = int((img.shape[0] - short_edge) / 2)
        xx = int((img.shape[1] - short_edge) / 2)
        crop_img = img[yy: yy + short_edge, xx: xx + short_edge]
        resized_img = cv2.resize(crop_img, (224, 224))
        pred = sess.run(pron_identifier.pred, feed_dict={pron_identifier.imgs: [resized_img]})
        print("pred: ", img_name, pred)
        return render_template('upload_image.html')

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app
