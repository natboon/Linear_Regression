import csv
import tkinter as tk
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
from tkinter import ttk
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def calculate():
    weight = float(entry_weight.get())
    height = float(entry_height.get())
    height = height / 100  # Convert height to meters

    bmi = weight / (height * height)
    bmi_result.config(text="Your BMI: {:.2f}".format(bmi))

    if bmi <= 18.4:
        status.config(text="Status: Underweight", fg="#FFD95A")
    elif 18.5 <= bmi <= 24.9:
        status.config(text="Status: Normal", fg="#47A992")
    elif 25.0 <= bmi <= 29.9:
        status.config(text="Status: Overweight", fg="#E57C23")
    else:
        status.config(text="Status: Obese", fg="#F45050")

    # Get other user inputs
    sex = entry_sex.get()
    age = entry_age.get()
    image_path = entry_pic_path.get()

    # Write data to a CSV file
    with open('user_data.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([sex, age, weight, height * 100, bmi, image_path])

def clear():
    entry_height.delete(0, tk.END)
    entry_weight.delete(0, tk.END)
    entry_sex.delete(0, tk.END)
    entry_age.delete(0, tk.END)

def selectPic():
    global img
    filename = filedialog.askopenfilename(initialdir="/images", title="Select Image",
                                          filetypes=(("png images", "*.png"), ("jpg images", "*.jpg")))

    img = Image.open(filename)

    # Calculate new dimensions while maintaining aspect ratio
    width, height = img.size
    new_width = 200
    new_height = int((new_width / width) * height)

    img = img.resize((new_width, new_height), Image.LANCZOS)
    img = ImageTk.PhotoImage(img)

    label_show_pic['image'] = img
    entry_pic_path.insert(0, filename)

def openCSV():
    file_path = filedialog.askopenfilename(title="Open CSV file", filetypes=(("CSV files", "*.csv"),))
    if file_path:
        df = pd.read_csv(file_path)
        showTable(df)

def showTable(df):
    top = tk.Toplevel()
    top.title("CSV Data Table")

    tree = ttk.Treeview(top)
    tree["columns"] = tuple(df.columns)

    # Configure columns
    for col in df.columns:
        tree.column(col, anchor="center", width=50)
        tree.heading(col, text=col, anchor="center")

    # Insert data into treeview
    for index, row in df.iterrows():
        tree.insert("", index, values=tuple(row))

    tree.pack(expand=YES, fill=BOTH)

bg_color = '#2A3457'
fg_color = '#F2EAED'
highlight_color = '#FFD95A'

window = tk.Tk()
window.title("Linear Regression Prediction")
window.geometry("1500x800")
window.config(bg=bg_color)
window.resizable(0, 0)

# Mockup data generation for demonstration purposes
np.random.seed(42)
data_size = 100
features = pd.DataFrame({
    'Feature1': np.random.rand(data_size),
    'Feature2': np.random.rand(data_size),
    'Feature3': np.random.rand(data_size),
    'Feature4': np.random.rand(data_size),
    'Feature5': np.random.rand(data_size),
    'Target': 3 * np.random.rand(data_size) + 2
})

# Linear Regression model training
X = features[['Feature1', 'Feature2', 'Feature3', 'Feature4', 'Feature5']]
y = features['Target']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

# Frame for input and prediction
input_frame = ttk.Frame(window, padding="10")
input_frame.pack(side="left", fill="both", expand=True)

# Label and Entry for Features
label_features = ttk.Label(input_frame, text="Enter Features:", font=("Rockwell", 15, "bold"))
label_features.grid(row=0, column=0, columnspan=2, pady=10)

feature_entries = []
for i, feature in enumerate(X.columns):
    label = ttk.Label(input_frame, text=f"{feature}:", font=("Rockwell", 12))
    label.grid(row=i+1, column=0, sticky="e", pady=5)

    entry = ttk.Entry(input_frame, font=("Rockwell", 12))
    entry.grid(row=i+1, column=1, pady=5)
    feature_entries.append(entry)

# Button to Predict
button_predict = ttk.Button(input_frame, text="Predict", command=lambda: predict())
button_predict.grid(row=len(X.columns)+1, column=0, columnspan=2, pady=10)

# Label for Prediction Result
label_result = ttk.Label(input_frame, text="", font=("Rockwell", 15))
label_result.grid(row=len(X.columns)+2, column=0, columnspan=2, pady=10)

# Frame for displaying training data
display_frame = ttk.Frame(window, padding="10")
display_frame.pack(side="right", fill="both", expand=True)

# Treeview for Displaying Data
treeview_columns = ['Feature1', 'Feature2', 'Feature3', 'Feature4', 'Feature5', 'Target']
treeview = ttk.Treeview(display_frame, columns=treeview_columns, show='headings')

for col in treeview_columns:
    treeview.heading(col, text=col)

for index, row in features.iterrows():
    treeview.insert("", index, values=tuple(row))

treeview.pack(expand=tk.YES, fill=tk.BOTH)

# Function to Predict and Display Result
def predict():
    try:
        input_values = [float(entry.get()) for entry in feature_entries]
        prediction_result = model.predict([input_values])[0]
        label_result.config(text=f"Predicted Target: {prediction_result:.2f}")
    except ValueError:
        label_result.config(text="Invalid input. Please enter numeric values for all features.")

# Styles
font_style = ("Rockwell", 15)
entry_style = {"font": font_style, "bg": "#2E3D4E", "fg": fg_color, "insertbackground": fg_color}
button_style = {"font": font_style, "bg": "#4E6272", "fg": fg_color, "activebackground": highlight_color, "activeforeground": bg_color}

#create the labels
label_sex = tk.Label(window, text="sex :", font=("Rockwell", 15, "bold",),
                bg=bg_color, fg=fg_color)
label_sex.pack(pady=10)

entry_sex = tk.Entry(window, font=("Rockwell", 15))
entry_sex.pack()

label_age = tk.Label(window, text="age :", font=("Rockwell", 15, "bold"),
                bg=bg_color, fg=fg_color)
label_age.pack(pady=15)

entry_age = tk.Entry(window, font=("Rockwell", 15))
entry_age.pack() 

label_weight = tk.Label(window, text="weight (kg) :", font=("Rockwell", 15, "bold"),
                bg=bg_color, fg=fg_color)
label_weight.pack(pady=10)

entry_weight = tk.Entry(window, font=("Rockwell", 15))
entry_weight.pack()

label_height = tk.Label(window, text="height (cm) :", font=("Rockwell", 15, "bold"),
                bg=bg_color, fg=fg_color)
label_height.pack(pady=15)

entry_height = tk.Entry(window, font=("Rockwell", 15))
entry_height.pack() 

# create a frame for buttons
frame = tk.Frame(window, bg=bg_color)
frame.pack(pady=30)

calculate_button = tk.Button(frame, text="Calculate", **button_style, command=calculate)
calculate_button.grid(row=0, column=0, padx=10)

clear_button = tk.Button(frame, text="Clear", **button_style, command=clear)
clear_button.grid(row=0, column=1, padx=10)


# create label for the result
bmi_result = tk.Label(window, text="", font=font_style, bg=bg_color, fg=fg_color)
bmi_result.pack()

status = tk.Label(window, text="", font=font_style, bg=bg_color, fg=fg_color)
status.pack(pady=10)

# Create image
label_pic_path = tk.Label(frame, text='Image Path : ', padx=25, pady=25, font=font_style, bg=bg_color, fg=fg_color)
label_show_pic = tk.Label(frame, bg=bg_color)
entry_pic_path = tk.Entry(frame, **entry_style)
button_browse = tk.Button(frame, text='Select Image', **button_style, command=selectPic)

def selectPic():
    global img
    filename = filedialog.askopenfilename(initialdir="/images", title="Select Image",
                                          filetypes=(("png images", "*.png"), ("jpg images", "*.jpg")))
    
    img = Image.open(filename)
    
    # Calculate new dimensions while maintaining aspect ratio
    width, height = img.size
    new_width = 200
    new_height = int((new_width / width) * height)
    
    img = img.resize((new_width, new_height), Image.LANCZOS)
    img = ImageTk.PhotoImage(img)
    
    label_show_pic['image'] = img
    entry_pic_path.insert(0, filename)

button_browse['command'] = selectPic

# Create a button to open CSV file
button_open_csv = tk.Button(frame, text="Open CSV", **button_style, command=openCSV)
button_open_csv.grid(row=8, column=2, columnspan="2", padx=10, pady=10)

# Place widgets on the grid
label_pic_path.grid(row=5, column=0)
entry_pic_path.grid(row=5, column=5, padx=(0, 20))
label_show_pic.grid(row=6, column=0, columnspan="2")
button_browse.grid(row=0, column=10, columnspan="2", padx=10, pady=10)
button_open_csv.grid(row=50, column=10, columnspan="2", padx=10, pady=10)

window.mainloop()