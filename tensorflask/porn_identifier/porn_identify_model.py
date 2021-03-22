import yaml
import numpy as np
import tensorflow as tf


with open("tensorflask.yaml", , mode='r', encoding="utf-8") as f:
    CONFIG = yaml.load(f, Loader=yaml.FullLoader)["porn_identifier"]


class Vgg16:
    def __init__(self, imgs, weights=None):
        self.imgs = imgs
        self.convlayers()
        self.fc_layers()
        self.probs = tf.nn.softmax(self.fc3l)

        assert weights is not None
        self.vgg16_weights_file = weights

    def convlayers(self):
        self.parameters = []

        # zero-mean input
        with tf.name_scope('preprocess') as scope:
            mean = tf.constant([123.68, 116.779, 103.939], dtype=tf.float32, shape=[
                               1, 1, 1, 3], name='img_mean')
            images = self.imgs - mean

        # conv1_1
        with tf.name_scope('conv1_1') as scope:
            kernel = tf.Variable(tf.truncated_normal([3, 3, 3, 64], dtype=tf.float32,
                                                     stddev=1e-1), name='weights')
            conv = tf.nn.conv2d(images, kernel, [1, 1, 1, 1], padding='SAME')
            biases = tf.Variable(tf.constant(0.0, shape=[64], dtype=tf.float32),
                                 trainable=True, name='biases')
            out = tf.nn.bias_add(conv, biases)
            self.conv1_1 = tf.nn.relu(out, name=scope)
            self.parameters += [kernel, biases]

        # conv1_2
        with tf.name_scope('conv1_2') as scope:
            kernel = tf.Variable(tf.truncated_normal([3, 3, 64, 64], dtype=tf.float32,
                                                     stddev=1e-1), name='weights')
            conv = tf.nn.conv2d(self.conv1_1, kernel, [
                                1, 1, 1, 1], padding='SAME')
            biases = tf.Variable(tf.constant(0.0, shape=[64], dtype=tf.float32),
                                 trainable=True, name='biases')
            out = tf.nn.bias_add(conv, biases)
            self.conv1_2 = tf.nn.relu(out, name=scope)
            self.parameters += [kernel, biases]

        # pool1
        self.pool1 = tf.nn.max_pool(self.conv1_2,
                                    ksize=[1, 2, 2, 1],
                                    strides=[1, 2, 2, 1],
                                    padding='SAME',
                                    name='pool1')

        # conv2_1
        with tf.name_scope('conv2_1') as scope:
            kernel = tf.Variable(tf.truncated_normal([3, 3, 64, 128], dtype=tf.float32,
                                                     stddev=1e-1), name='weights')
            conv = tf.nn.conv2d(self.pool1, kernel, [
                                1, 1, 1, 1], padding='SAME')
            biases = tf.Variable(tf.constant(0.0, shape=[128], dtype=tf.float32),
                                 trainable=True, name='biases')
            out = tf.nn.bias_add(conv, biases)
            self.conv2_1 = tf.nn.relu(out, name=scope)
            self.parameters += [kernel, biases]

        # conv2_2
        with tf.name_scope('conv2_2') as scope:
            kernel = tf.Variable(tf.truncated_normal([3, 3, 128, 128], dtype=tf.float32,
                                                     stddev=1e-1), name='weights')
            conv = tf.nn.conv2d(self.conv2_1, kernel, [
                                1, 1, 1, 1], padding='SAME')
            biases = tf.Variable(tf.constant(0.0, shape=[128], dtype=tf.float32),
                                 trainable=True, name='biases')
            out = tf.nn.bias_add(conv, biases)
            self.conv2_2 = tf.nn.relu(out, name=scope)
            self.parameters += [kernel, biases]

        # pool2
        self.pool2 = tf.nn.max_pool(self.conv2_2,
                                    ksize=[1, 2, 2, 1],
                                    strides=[1, 2, 2, 1],
                                    padding='SAME',
                                    name='pool2')

        # conv3_1
        with tf.name_scope('conv3_1') as scope:
            kernel = tf.Variable(tf.truncated_normal([3, 3, 128, 256], dtype=tf.float32,
                                                     stddev=1e-1), name='weights')
            conv = tf.nn.conv2d(self.pool2, kernel, [
                                1, 1, 1, 1], padding='SAME')
            biases = tf.Variable(tf.constant(0.0, shape=[256], dtype=tf.float32),
                                 trainable=True, name='biases')
            out = tf.nn.bias_add(conv, biases)
            self.conv3_1 = tf.nn.relu(out, name=scope)
            self.parameters += [kernel, biases]

        # conv3_2
        with tf.name_scope('conv3_2') as scope:
            kernel = tf.Variable(tf.truncated_normal([3, 3, 256, 256], dtype=tf.float32,
                                                     stddev=1e-1), name='weights')
            conv = tf.nn.conv2d(self.conv3_1, kernel, [
                                1, 1, 1, 1], padding='SAME')
            biases = tf.Variable(tf.constant(0.0, shape=[256], dtype=tf.float32),
                                 trainable=True, name='biases')
            out = tf.nn.bias_add(conv, biases)
            self.conv3_2 = tf.nn.relu(out, name=scope)
            self.parameters += [kernel, biases]

        # conv3_3
        with tf.name_scope('conv3_3') as scope:
            kernel = tf.Variable(tf.truncated_normal([3, 3, 256, 256], dtype=tf.float32,
                                                     stddev=1e-1), name='weights')
            conv = tf.nn.conv2d(self.conv3_2, kernel, [
                                1, 1, 1, 1], padding='SAME')
            biases = tf.Variable(tf.constant(0.0, shape=[256], dtype=tf.float32),
                                 trainable=True, name='biases')
            out = tf.nn.bias_add(conv, biases)
            self.conv3_3 = tf.nn.relu(out, name=scope)
            self.parameters += [kernel, biases]

        # pool3
        self.pool3 = tf.nn.max_pool(self.conv3_3,
                                    ksize=[1, 2, 2, 1],
                                    strides=[1, 2, 2, 1],
                                    padding='SAME',
                                    name='pool3')

        # conv4_1
        with tf.name_scope('conv4_1') as scope:
            kernel = tf.Variable(tf.truncated_normal([3, 3, 256, 512], dtype=tf.float32,
                                                     stddev=1e-1), name='weights')
            conv = tf.nn.conv2d(self.pool3, kernel, [
                                1, 1, 1, 1], padding='SAME')
            biases = tf.Variable(tf.constant(0.0, shape=[512], dtype=tf.float32),
                                 trainable=True, name='biases')
            out = tf.nn.bias_add(conv, biases)
            self.conv4_1 = tf.nn.relu(out, name=scope)
            self.parameters += [kernel, biases]

        # conv4_2
        with tf.name_scope('conv4_2') as scope:
            kernel = tf.Variable(tf.truncated_normal([3, 3, 512, 512], dtype=tf.float32,
                                                     stddev=1e-1), name='weights')
            conv = tf.nn.conv2d(self.conv4_1, kernel, [
                                1, 1, 1, 1], padding='SAME')
            biases = tf.Variable(tf.constant(0.0, shape=[512], dtype=tf.float32),
                                 trainable=True, name='biases')
            out = tf.nn.bias_add(conv, biases)
            self.conv4_2 = tf.nn.relu(out, name=scope)
            self.parameters += [kernel, biases]

        # conv4_3
        with tf.name_scope('conv4_3') as scope:
            kernel = tf.Variable(tf.truncated_normal([3, 3, 512, 512], dtype=tf.float32,
                                                     stddev=1e-1), name='weights')
            conv = tf.nn.conv2d(self.conv4_2, kernel, [
                                1, 1, 1, 1], padding='SAME')
            biases = tf.Variable(tf.constant(0.0, shape=[512], dtype=tf.float32),
                                 trainable=True, name='biases')
            out = tf.nn.bias_add(conv, biases)
            self.conv4_3 = tf.nn.relu(out, name=scope)
            self.parameters += [kernel, biases]

        # pool4
        self.pool4 = tf.nn.max_pool(self.conv4_3,
                                    ksize=[1, 2, 2, 1],
                                    strides=[1, 2, 2, 1],
                                    padding='SAME',
                                    name='pool4')

        # conv5_1
        with tf.name_scope('conv5_1') as scope:
            kernel = tf.Variable(tf.truncated_normal([3, 3, 512, 512], dtype=tf.float32,
                                                     stddev=1e-1), name='weights')
            conv = tf.nn.conv2d(self.pool4, kernel, [
                                1, 1, 1, 1], padding='SAME')
            biases = tf.Variable(tf.constant(0.0, shape=[512], dtype=tf.float32),
                                 trainable=True, name='biases')
            out = tf.nn.bias_add(conv, biases)
            self.conv5_1 = tf.nn.relu(out, name=scope)
            self.parameters += [kernel, biases]

        # conv5_2
        with tf.name_scope('conv5_2') as scope:
            kernel = tf.Variable(tf.truncated_normal([3, 3, 512, 512], dtype=tf.float32,
                                                     stddev=1e-1), name='weights')
            conv = tf.nn.conv2d(self.conv5_1, kernel, [
                                1, 1, 1, 1], padding='SAME')
            biases = tf.Variable(tf.constant(0.0, shape=[512], dtype=tf.float32),
                                 trainable=True, name='biases')
            out = tf.nn.bias_add(conv, biases)
            self.conv5_2 = tf.nn.relu(out, name=scope)
            self.parameters += [kernel, biases]

        # conv5_3
        with tf.name_scope('conv5_3') as scope:
            kernel = tf.Variable(tf.truncated_normal([3, 3, 512, 512], dtype=tf.float32,
                                                     stddev=1e-1), name='weights')
            conv = tf.nn.conv2d(self.conv5_2, kernel, [
                                1, 1, 1, 1], padding='SAME')
            biases = tf.Variable(tf.constant(0.0, shape=[512], dtype=tf.float32),
                                 trainable=True, name='biases')
            out = tf.nn.bias_add(conv, biases)
            self.conv5_3 = tf.nn.relu(out, name=scope)
            self.parameters += [kernel, biases]

        # pool5
        self.pool5 = tf.nn.max_pool(self.conv5_3,
                                    ksize=[1, 2, 2, 1],
                                    strides=[1, 2, 2, 1],
                                    padding='SAME',
                                    name='pool4')

    def fc_layers(self):
        # fc1
        with tf.name_scope('fc1') as scope:
            shape = int(np.prod(self.pool5.get_shape()[1:]))
            fc1w = tf.Variable(tf.truncated_normal([shape, 4096],
                                                   dtype=tf.float32,
                                                   stddev=1e-1), name='weights')
            fc1b = tf.Variable(tf.constant(1.0, shape=[4096], dtype=tf.float32),
                               trainable=True, name='biases')
            pool5_flat = tf.reshape(self.pool5, [-1, shape])
            fc1l = tf.nn.bias_add(tf.matmul(pool5_flat, fc1w), fc1b)
            self.fc1 = tf.nn.relu(fc1l)
            self.parameters += [fc1w, fc1b]

        # fc2
        with tf.name_scope('fc2') as scope:
            fc2w = tf.Variable(tf.truncated_normal([4096, 4096],
                                                   dtype=tf.float32,
                                                   stddev=1e-1), name='weights')
            fc2b = tf.Variable(tf.constant(1.0, shape=[4096], dtype=tf.float32),
                               trainable=True, name='biases')
            fc2l = tf.nn.bias_add(tf.matmul(self.fc1, fc2w), fc2b)
            self.fc2 = tf.nn.relu(fc2l)
            self.parameters += [fc2w, fc2b]

        # fc3
        with tf.name_scope('fc3') as scope:
            fc3w = tf.Variable(tf.truncated_normal([4096, 1000],
                                                   dtype=tf.float32,
                                                   stddev=1e-1), name='weights')
            fc3b = tf.Variable(tf.constant(1.0, shape=[1000], dtype=tf.float32),
                               trainable=True, name='biases')
            self.fc3l = tf.nn.bias_add(tf.matmul(self.fc2, fc3w), fc3b)
            self.parameters += [fc3w, fc3b]

    def load_weights(self, sess):
        weights = np.load(self.vgg16_weights_file)
        keys = sorted(weights.keys())
        for i, k in enumerate(keys):
            print(i, k, np.shape(weights[k]))
            sess.run(self.parameters[i].assign(weights[k]))


class PornIdentifier(Vgg16):
    def __init__(self):
        self.imgs = tf.placeholder(tf.float32, [None, 224, 224, 3])
        self.vgg17_weights_file = 'porn_identifier/vgg17_weights.npz'
        Vgg16.__init__(self, self.imgs, 'porn_identifier/vgg16_weights.npz')

        # fc4 added to fit nsfw dataset
        with tf.name_scope('fc4') as scope:
            fc4w = tf.Variable(tf.truncated_normal([1000, 3],
                                                   dtype=tf.float32,
                                                   stddev=1e-1), name='weights')
            fc4b = tf.Variable(tf.constant(1.0, shape=[3], dtype=tf.float32),
                               trainable=True, name='biases')
            self.fc4l = tf.nn.bias_add(tf.matmul(self.fc3l, fc4w), fc4b)
            self.parameters += [fc4w, fc4b]

        # loss function
        with tf.name_scope('loss') as scope:
            self.true_out = tf.placeholder(tf.float32, [None, 3])
            self.cross_entropy = tf.nn.softmax_cross_entropy_with_logits_v2(
                labels=self.true_out, logits=self.fc4l)
            self.loss = tf.reduce_mean(self.cross_entropy)

        # prediction
        with tf.name_scope('pred') as scope:
            self.probs = tf.nn.softmax(self.fc4l)
            self.pred = tf.argmax(self.probs, axis=1)
            self.pred_one_hot = tf.one_hot(self.pred, 3)

        # optimization
        with tf.name_scope('train') as scope:
            self.global_step = tf.Variable(
                0, name='global_step', trainable=False)
            if CONFIG["optimizer"] == "adam":
                self.optimizer = tf.train.AdamOptimizer(
                    learning_rate=CONFIG["learning_rate"])
            else:
                self.optimizer = tf.train.AdamOptimizer(
                    learning_rate=CONFIG["learning_rate"])
            self.train_op = self.optimizer.minimize(
                self.loss, global_step=self.global_step)

    def save_weights(self, sess):
        weights = {}
        for var in self.parameters:
            name = var.name
            name_list = name.split("/")
            if name_list[1] == "biases:0":
                name = "_".join([name_list[0], "b"])
            elif name_list[1] == "weights:0":
                name = "_".join([name_list[0], "W"])
            else:
                raise Exception("No such parameter: {}".format(name))
            value = sess.run(var)
            weights[name] = value
        np.savez(self.vgg17_weights_file, conv1_1_W=weights['conv1_1_W'], conv1_1_b=weights['conv1_1_b'],
                 conv1_2_W=weights['conv1_2_W'], conv1_2_b=weights['conv1_2_b'], conv2_1_W=weights['conv2_1_W'],
                 conv2_1_b=weights['conv2_1_b'], conv2_2_W=weights['conv2_2_W'], conv2_2_b=weights['conv2_2_b'],
                 conv3_1_W=weights['conv3_1_W'], conv3_1_b=weights['conv3_1_b'], conv3_2_W=weights['conv3_2_W'],
                 conv3_2_b=weights['conv3_2_b'], conv3_3_W=weights['conv3_3_W'], conv3_3_b=weights['conv3_3_b'],
                 conv4_1_W=weights['conv4_1_W'], conv4_1_b=weights['conv4_1_b'], conv4_2_W=weights['conv4_2_W'],
                 conv4_2_b=weights['conv4_2_b'], conv4_3_W=weights['conv4_3_W'], conv4_3_b=weights['conv4_3_b'],
                 conv5_1_W=weights['conv5_1_W'], conv5_1_b=weights['conv5_1_b'], conv5_2_W=weights['conv5_2_W'],
                 conv5_2_b=weights['conv5_2_b'], conv5_3_W=weights['conv5_3_W'], conv5_3_b=weights['conv5_3_b'],
                 fc1_W=weights['fc1_W'], fc1_b=weights['fc1_b'], fc2_W=weights['fc2_W'], fc2_b=weights['fc2_b'],
                 fc3_W=weights['fc3_W'], fc3_b=weights['fc3_b'], fc4_W=weights['fc4_W'], fc4_b=weights['fc4_b'])

    def load_vgg17_weights(self, sess):
        weights = np.load(self.vgg17_weights_file)
        keys = sorted(weights.keys())
        for i, k in enumerate(keys):
            print(i, k, np.shape(weights[k]))
            sess.run(self.parameters[i].assign(weights[k]))


if __name__ == "__main__":
    with tf.Session() as sess:
        pron_identifier = PornIdentifier()
        sess.run(tf.global_variables_initializer())
        # pron_identifier.vgg16_weights_file = 'vgg16_weights.npz'
        # pron_identifier.load_weights(sess)
        pron_identifier.vgg17_weights_file = 'vgg17_weights.npz'
        pron_identifier.load_vgg17_weights(sess)
