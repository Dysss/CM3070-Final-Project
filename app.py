import numpy as np
import tensorflow as tf
import skimage as skimg
import tkinter as tk
from tkinter import filedialog
from tkinter.ttk import *

# model = tf.keras.models.load_model('models/final_model.keras')
model = None

# Initialize window
window = tk.Tk()

# Initialize frames
modelSelectFrame = tk.Frame(window)
fileSelectFrame = tk.Frame(window)
textFrame = tk.Frame(window)
predictFrame = tk.Frame(window)

# Initialize string variables
imgName = tk.StringVar()
predictionResult = tk.StringVar()
modelName = tk.StringVar()

def selectModel():
    global model

    filetypes = (
        ('TensorFlow Model', '.keras'),
        ('All files', '.')
    )

    modelFile = filedialog.askopenfile(
        title='Select model',
        initialdir='/',
        filetypes=filetypes
    )

    if modelFile:
        if model is None:
            modelSelectFrame.configure(height=10)
            modelSelectBtn.pack_configure(fill='x', expand=False)
            showSelect()

        modelSelectBtn.configure(text=modelFile.name)
        model = tf.keras.models.load_model(modelFile.name)

# Show file selection window
def selectFile():
    filetypes = (
        ('Image files', '.jpg .png'),
        ('All files', '.')
    )

    imgFile = filedialog.askopenfile(
        title='Select image',
        initialdir='/',
        filetypes=filetypes)
    
    # print(filename.name)
    if imgFile:
        hideSelect(imgFile)

# Hide "Select file" button and show "Predict" widget(s)
def hideSelect(image):
    fileSelectFrame.pack_forget()
    
    imgName.set('Selected image: ' + image.name)
    predictBtn.configure(command=lambda: predict(image))

    textFrame.pack(expand=True, side='top')
    predictFrame.pack(expand=True, side='bottom')

# Show "Select file" button
def showSelect():
    textFrame.pack_forget()
    predictFrame.pack_forget()
    predictionResult.set('')
    fileSelectFrame.pack(expand=True, fill='both')

# Predict function
def predict(imageFileObj):
    img = skimg.io.imread(imageFileObj.name)

    if img.shape != (32, 32, 3):
        img = skimg.transform.resize(img, (32, 32), anti_aliasing=False)

    img = np.array(img)
    img = img/255
    img = np.expand_dims(img, axis=0)

    prediction = model.predict(img)
    result = np.where(prediction > 0.5, "Synthetic", "Authentic")

    predictionResult.set(result[0][0])

# Model select button
modelSelectBtn = tk.Button(
    modelSelectFrame,
    text='Select model',
    command=selectModel
)

# Select file button
fileSelectBtn = tk.Button(
    fileSelectFrame,
    text='Select image',
    command=selectFile
)

# Pack file select button
fileSelectBtn.pack()

# Initialize "selected file" text and "choose another" btn
selectedText = tk.Label(textFrame, textvariable=imgName, wraplength=300)
selectOtherBtn = tk.Button(
    textFrame,
    text='Choose another',
    command=showSelect
)

# Initialize "predict" btn and prediction result
predictBtn = tk.Button(
    predictFrame,
    text='Predict!'
)
predictionText = tk.Label(predictFrame, textvariable=predictionResult)

# Pack textFrame and predictFrame children
selectedText.pack()
selectOtherBtn.pack()
predictBtn.pack()
predictionText.pack()

# Configure GUI
window.title('Synthetic Image Detector')
window.geometry('450x300')

# Pack initial widgets
modelSelectBtn.pack(expand=True, fill='both')
modelSelectFrame.pack(expand=True, fill='both')

window.geometry("800x400")
window.mainloop()