import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf
tf.logging.set_verbosity(tf.logging.ERROR)
import numpy as np
from scipy import misc
import random

x_size = 1400
y_size = 2800

coords = tf.placeholder(tf.float32, (None, 4), name='features')

k, l, m = 3000, 2500, 2000

w1 = tf.Variable(tf.random_normal([4, k], stddev=random.random(), mean=0), name="Weights1")
w2 = tf.Variable(tf.random_normal([k, l], stddev=.151, mean=0), name="Weights2")
w3 = tf.Variable(tf.random_normal([l, 3], stddev=.015, mean=0), name="Weights3")

y1 = tf.nn.tanh(tf.matmul(coords, w1), name="HLayer1")
y2 = tf.nn.tanh(tf.matmul(y1, w2), name="HLayer2")
pred = tf.nn.tanh(tf.matmul(y2, w3), name="OutputLayer")


def create_array():
    parameters = [[[] for _ in range(x_size)] for _ in range(y_size)]
    for y in range(y_size):
        for x in range(x_size):
            added_x = x + 50
            added_y = y + 25
            radius = np.sqrt(added_x ** 2 + added_y ** 2)
            parameters[y][x] = [added_y, added_x, radius, rand]
    return parameters


config = tf.ConfigProto()
config.gpu_options.allow_growth = True
with tf.Session(config=config) as sess:
    sess.run(tf.global_variables_initializer())
    rand = 1564

    features = create_array()

    rgb = [0 for _ in range(y_size)]
    for batch in range(y_size):
        feed = features[batch]
        result = sess.run(pred, feed_dict={coords: feed})
        rgb[batch] = result

    misc.imsave("images/" + "testing.png", rgb)

