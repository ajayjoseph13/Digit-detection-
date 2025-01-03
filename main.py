import tkinter as tk
from tkinter import messagebox
import numpy as np
from PIL import Image, ImageDraw
import tensorflow as tf

# Load the pre-trained model
model = tf.keras.models.load_model('mnist_model.h5')

# Function to handle drawing and predictions
class DrawApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Handwritten Digit Recognition")

        # Create a canvas to draw
        self.canvas = tk.Canvas(self.root, width=280, height=280, bg="white")
        self.canvas.grid(row=0, column=0, padx=10, pady=10)

        # To store the coordinates of the drawing
        self.points = []

        # Clear button to reset the canvas
        self.clear_button = tk.Button(self.root, text="Clear", command=self.clear_canvas)
        self.clear_button.grid(row=1, column=0, pady=10)

        # Predict button to recognize the drawing
        self.predict_button = tk.Button(self.root, text="Predict", command=self.predict)
        self.predict_button.grid(row=2, column=0, pady=10)

    def draw(self, event):
        """ Capture points where the user is drawing """
        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)
        self.canvas.create_oval(x1, y1, x2, y2, fill="black", width=8)
        self.points.append((event.x, event.y))

    def clear_canvas(self):
        """ Clear the drawing canvas """
        self.canvas.delete("all")
        self.points = []

    def predict(self):
        """ Process the drawing and predict using the model """
        # Create an image from the canvas
        self.canvas.update()  # Update the canvas
        self.canvas.postscript(file="drawing.eps", colormode='color')

        # Convert postscript to image
        img = Image.open("drawing.eps")
        img = img.convert('L')  # Convert to grayscale
        img = img.resize((28, 28), Image.ANTIALIAS)  # Resize to match MNIST input size

        # Invert the colors (black on white becomes white on black)
        img = Image.eval(img, lambda x: 255 - x)

        # Convert image to numpy array
        img_array = np.array(img)
        img_array = img_array / 255.0  # Normalize

        # Reshape image for the model (28x28x1)
        img_array = np.reshape(img_array, (1, 28, 28, 1))

        # Predict the digit
        prediction = model.predict(img_array)
        predicted_digit = np.argmax(prediction)

        # Show prediction result
        print(prediction)
        messagebox.showinfo("Prediction", f"The digit you drew is: {predicted_digit}")


# Run the Tkinter application
if __name__ == "__main__":
    root = tk.Tk()
    app = DrawApp(root)
    root.bind("<B1-Motion>", app.draw)  # Draw on the canvas
    root.mainloop()
