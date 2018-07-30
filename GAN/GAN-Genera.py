import tensorflow as tf
import numpy as np
from scipy import misc

x_input = tf.placeholder(tf.float32, [None, 49])
img_input = tf.cast(tf.reshape(x_input, [-1, 7, 7, 1]), tf.float32)

weights_init = tf.truncated_normal_initializer(stddev=.05)

conv1_w = tf.Variable(tf.truncated_normal([7, 7, 1, 32]))
conv1_b = tf.zeros([32])
conv1 = tf.nn.conv2d(img_input, conv1_w, strides=[1, 1, 1, 1], padding='SAME') + conv1_b

conv_one = tf.layers.conv2d_transpose(inputs=conv1, filters=1024, kernel_size=5, padding='same',
                                      activation=tf.nn.relu)

conv_two = tf.layers.conv2d_transpose(inputs=conv_one, filters=512, kernel_size=5, padding='same',
                                      activation=tf.nn.relu, kernel_initializer=weights_init)

conv_three = tf.layers.conv2d_transpose(inputs=conv_two, filters=256, kernel_size=5, padding='same',
                                        activation=tf.nn.relu, kernel_initializer=weights_init)

conv_four = tf.layers.conv2d_transpose(inputs=conv_three, filters=128, kernel_size=5, padding='same', strides=2,
                                       activation=tf.nn.relu, kernel_initializer=weights_init)

final_layer = tf.layers.conv2d_transpose(inputs=conv_four, filters=1, kernel_size=5, padding='same', strides=2,
                                         activation=tf.nn.relu, kernel_initializer=weights_init)

flattened = tf.layers.flatten(final_layer)

output = tf.reshape(flattened, [-1, 28])

config = tf.ConfigProto()
config.gpu_options.allow_growth = True
with tf.Session(config=config) as sess:
    sess.run(tf.global_variables_initializer())

    reshaped = sess.run(img_input, feed_dict={x_input: [np.random.uniform(0, 1, 49)]})

    conv = sess.run(conv_one, feed_dict={x_input: [np.random.uniform(0,1, 49)]})
    print(conv)

    fake = sess.run(output)
    print(fake)
    # misc.toimage(fake).show()

sess.close()
