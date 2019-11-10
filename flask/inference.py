
# coding: utf-8


import numpy as np
import tensorflow as tf
print(tf.__version__)
from PIL import Image
from PIL import Image
from tensorflow.lite.python import interpreter as interpreter_wrapper





#Load TFLite model and allocate tensors.
def model(filename):
    interpreter = tf.lite.Interpreter(model_path="model.tflite")
    interpreter.allocate_tensors()
    file_name = r"ID_RANDOM_DATA\voter_card\voter_card\15389_Voter_ID_CKF6244640_1.jpeg"
    interpreter = tf.lite.Interpreter(model_path="model.tflite")
    interpreter.allocate_tensors()
    file_name = r"ID_RANDOM_DATA\voter_card\voter_card\15389_Voter_ID_CKF6244640_1.jpeg"






    #Get input and output tensors.
    input_mean = 127.5
    input_std = 127.5
    floating_model = False
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    if input_details[0]['dtype'] == type(np.float32(1.0)):
        floating_model = True

    print("here done")
    def load_labels(filename):
        my_labels = []
        input_file = open(filename, 'r')
        for l in input_file:
            my_labels.append(l.strip())
        return my_labels
#Get input and output tensors.
    input_mean = 127.5
    input_std = 127.5
    floating_model = False
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    if input_details[0]['dtype'] == type(np.float32(1.0)):
        floating_model = True


    def load_labels(filename):
        my_labels = []
        input_file = open(filename, 'r')
        for l in input_file:
            my_labels.append(l.strip())
        return my_labels


    # NxHxWxC, H:1, W:2
    height = input_details[0]['shape'][1]
    width = input_details[0]['shape'][2]
    img = Image.open(file_name)
    img = img.resize((width, height))
    label_file = "labels.txt"

    # add N dim
    input_data = np.expand_dims(img, axis=0)
    input_data = np.expand_dims(img, axis=0)

    if floating_model:
        input_data = (np.float32(input_data) - input_mean) / input_std

    interpreter.set_tensor(input_details[0]['index'], input_data)

    interpreter.invoke()

    output_data = interpreter.get_tensor(output_details[0]['index'])
    results = np.squeeze(output_data)

    top_k = results.argsort()[-1:][::-1]
    labels = load_labels(label_file)
    for i in top_k:
        if floating_model:
            print('{0:08.6f}'.format(float(results[i]))+":", labels[i])
        else:
            print('{0:08.6f}'.format(float(results[i]/255.0))+":", labels[i])
        print("got results")

        top_k = results.argsort()[-1:][::-1]
        labels = load_labels(label_file)
        for i in top_k:
            if floating_model:
                print('{0:08.6f}'.format(float(results[i]))+":", labels[i])
            else:
                print('{0:08.6f}'.format(float(results[i]/255.0))+":", labels[i])

