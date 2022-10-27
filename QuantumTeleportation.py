#from functools import reduce
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#from qiskit.tools.visualization import plot_histogram
#from matplotlib.figure import Figure
#from math import pi

from qiskit import *
import tkinter as tk
from ipywidgets.widgets import *
from qiskit.tools.visualization import plot_histogram
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk 
import numpy as np
from qiskit.providers.aer.noise import NoiseModel
import io
from qiskit.providers.aer.noise import NoiseModel
from qiskit.providers.aer.noise.errors import pauli_error, depolarizing_error
from qiskit.result import marginal_counts
import pandas as pd



qasm_sim = Aer.get_backend('qasm_simulator')

error_list = []
def add_to_error(error_val):
    error_percent = error_val/128 * 100
    error_list.append(error_percent)

def place_plot(plot_x, plot_y, plot, heading, x_axisHeading):
    plt.clf()
    plt.plot(plot)
    plt.title(heading, fontsize=14)
    plt.xlabel(x_axisHeading, fontsize=14)
    plt.ylabel('Error Percent', fontsize=14)
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png')
    im = Image.open(img_buf)
    tk_image = ImageTk.PhotoImage(im)
    chart= Label(canvas, image = tk_image)
    chart.image = tk_image
    chart.place(x = plot_x , y = plot_y, width = 650, height = 500)
    canvas.pack()

def get_noise(p_meas,p_gate):
    error_meas = pauli_error([('X',p_meas), ('I', 1 - p_meas)])
    error_gate1 = depolarizing_error(p_gate, 1)
    error_gate2 = error_gate1.tensor(error_gate1)

    noise_model = NoiseModel()
    noise_model.add_all_qubit_quantum_error(error_meas, "measure") # measurement error is applied to measurements
    noise_model.add_all_qubit_quantum_error(error_gate1, ["x"]) # single qubit gate error is applied to x gates
    noise_model.add_all_qubit_quantum_error(error_gate2, ["cx"]) # two qubit gate error is applied to cx gates
        
    return noise_model

noise_model = get_noise(0.01,0.01)

############################# String message transferral #############################
def string_to_binary(message):
    l = []
    m = []
    for i in message:
        l.append(ord(i)) # convert each letter to unicode
    for i in l:
        m.append(int(bin(i)[2:])) # return the binary representation of the unicode input
    return m

def binary_to_string(binary):
  l=[]
  m=""
  for i in binary:
    b=0
    c=0
    k=int(math.log10(i))+1
    for j in range(k):  # binary to decimal conversion
      b=((i%10)*(2**j))   
      i=i//10
      c=c+b
    l.append(c)
  for x in l:
    m=m+chr(x) # returned as a string 
  return m

def send_message(): # retrieves the message from the input box, sends it to be turned into circuits and executed, then places the returned message into an output box. 
    recieved_binary_message = []
    message = input_display.get()
    
    if message != 'Enter a message...':
        binary = string_to_binary(message)
        
        for k in binary:
            binary_string = str(k)
            teleported = [ Send_Message(int(binary_string[i])) for i in range(len(binary_string)) ]
            recieved_binary_message.append(int(''.join(str(e) for e in teleported)))

        revieved_message = binary_to_string(recieved_binary_message)
        output_display.delete(0, tk.END)
        output_display.insert(0,revieved_message)
    else:
        messagebox.showerror("No Message", "Please type a message in the input box on the left")
 #Image.fromarray(pix)

def Send_Message(binary): # creates and runs the circuits to send the message. 
    circuit = QuantumCircuit(3 , 1)
    # alice
    if binary == 1: # circuits values are 0 by default
        circuit.x(0)
    circuit.barrier()
    circuit.h(1)
    circuit.cx(1 , 2)
    circuit.cx(0 , 1)
    circuit.h(0)
    circuit.barrier()

    #bob
    circuit.cx(1 , 2)
    circuit.cz(0 , 2)
    circuit.measure(2, 0) # measure q2 and store into classical register 0

    #circuit.draw(output='mpl')
    #plt.show()
    noise_model = get_noise(meas_scale.get() / 100,gate_scale.get() / 100) #get the measurements from the ui sliders
    sim_result = qasm_sim.run(circuit, qasm_sim, noise_model = noise_model, shots = 512, optimization_level = 3).result() # executes the circuit
    if sim_result.get_counts()[str(1)] > sim_result.get_counts()[str(0)]: # hardware error comes with the number of shots taken. for quantum it will simulate
        error_val = sim_result.get_counts()[str(0)]                       # the circuit 512 times, and the results will be shown as 98% bit = 0 and 2% bit = 1  
        add_to_error(error_val)
        return 1
    else:
        error_val = sim_result.get_counts()[str(1)]
        add_to_error(error_val)
        return 0

############################# String message transferral #############################



    
############################# Image transferral ######################################

def createCircuit(eight_bits):
    circuit = QuantumCircuit(24 , 8)
    for i in range(8):
        if eight_bits[i] == False:
            circuit.x(i)
        
    circuit.barrier()
    for i in range(8):    
        # alice
        circuit.h(i + 8)
        circuit.cx(i+8 , i+16)
        circuit.cx(i , i+8)
        circuit.h(i)
        circuit.barrier()   
        #bob
        circuit.cx(i+8 , i+16)
        circuit.cz(i , i+16)
        circuit.barrier()

    for i in range(8):      
        circuit.measure(i + 16, i ) # measure q2 and store into classical register 0

    #circuit.draw(output='mpl', fold= -1)
    #plt.show()
    return circuit



   
def executeCircuits(circuits):
    noise_model = get_noise(meas_scale.get() / 100,gate_scale.get() / 100) #get the measurements from the ui sliders
    sim_result = qasm_sim.run(circuits, qasm_sim, noise_model = noise_model, shots = 128).result()

    returnBits = []
    for i in range(8):
        #print(counts)
        column = []
        for counts in marginal_counts(sim_result ,indices=[i]).get_counts(): # need to get the error values out of the resulted circuit execution
            if str(1) in counts.keys() and str(0) in counts.keys(): # circuit can return {1 and 0} (some error) or {1} (no error) or {0} (no error). 
                if counts[str(1)] > counts[str(0)]:
                    error_val = counts[str(0)]
                    add_to_error(error_val)
                    column.append(False)
                else:
                    error_val = counts[str(1)]
                    add_to_error(error_val)
                    column.append(True)
            else:
                if str(0) in counts.keys():
                    error_val = 0
                    add_to_error(error_val)
                    column.append(False)
                else:
                    error_val = 0
                    add_to_error(error_val)
                    column.append(True)
        returnBits.append(column)
        #print(column)    
    
    columnCount = 0     
    if variable.get() == "80x80":
        columnCount = 80
    if variable.get() == "160x160":
        columnCount = 160
    if variable.get() == "200x200": 
        columnCount = 200
    

    returnBits_df = pd.DataFrame(returnBits).T # transpose the dataframe
    new_df = []
    for i in range(columnCount):
        new_df.insert( i , (returnBits_df.iloc[ int(columnCount / 8) * i : int(columnCount / 8) * (i + 1)]).to_numpy().flatten().tolist() ) # and change it to a list so that the image library can convert it to an image
        
    #print(new_df)
    return new_df

def chunker(seq, size): # used to iterate through the list in 'chunks' without needing to store them
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

saved_picture = None

def send_image():
    global teleported
    global saved_picture
    completed_image = []
    circuitList = []
    error_rate = []

    if saved_picture:
        columnCount = 0     
        if variable.get() == "80x80":
            columnCount = 80
        if variable.get() == "160x160":
            columnCount = 160
        if variable.get() == "200x200": 
            columnCount = 200

        sendPicture = saved_picture.resize((columnCount, columnCount))
        
        bnw_picture = sendPicture.convert('1')
        
        
        sendPicture = np.array(bnw_picture)
        for i in range(int(repeaters.get()) + 1):
            circuitList = []
            for column in sendPicture:
                circuitByte = [createCircuit(bits) for bits in chunker(column , 8)]
                circuitList = circuitList + circuitByte
            teleported = executeCircuits(circuitList)
            circuitList = [] #reset the list when done with it
            place_plot(50 , 400, error_list , 'Hardware Error Rate' , 'Bit Count')

            completed_image = np.array(teleported)
            
            
            error_count = 0
            count = 0
            for k in range(len(completed_image)):
                for l in range(len(completed_image[k])):
                    if count >= 8:
                        error_rate.append(error_count/8 * 100)
                        error_count = 0
                        count = 0
                    if completed_image[k][l] != sendPicture[k][l]:
                        error_count = error_count + 1    
                    count = count + 1
                    
            place_plot(800 , 400, error_rate , 'Transfer Error Rate per Byte', 'Byte Count')
            
            
            error_label = tk.Label(master = canvas, text = "Total bits that were different between transferral(s): " + str(sum(error_rate)/1000 * 8))
            error_label.place(x=850,y=400,width=400.0,height=25.0)
            
            recieved_image = Image.fromarray(completed_image)
            recieved_image = recieved_image.resize((200, 200))
            tk_image = ImageTk.PhotoImage(recieved_image)
            uploaded_image= Label(canvas, image = tk_image)
            uploaded_image.image = tk_image
            
            sendPicture = np.multiply(completed_image,1) # sets the next image in the loop to the results of the previous image (convert true/false to 0/1)

            if i == 0:
                uploaded_image.place(x = 850, y = 25, width = 200, height = 200)
            if i == 1:
                uploaded_image.place(x = 1060, y = 25, width = 200, height = 200)
            if i == 2:
                uploaded_image.place(x = 1270, y = 25, width = 200, height = 200)
    else:
        messagebox.showerror("No Image", "Please upload an image")

# (11111111 ,11111111 ,11111111 )  each pixel required to send a colored image is 3 bytes long... 24x transmission time.

def upload_image():
    global saved_picture
    path= filedialog.askopenfilename(filetypes=[("Image File",'.jpg')])
    picture = Image.open(path)
    saved_picture = picture
    picture = picture.resize((200, 200))
    tk_image = ImageTk.PhotoImage(picture)
    uploaded_image= Label(canvas, image = tk_image)
    uploaded_image.image = tk_image
    uploaded_image.place(x = 100, y = 25, width = 200, height = 200)
    #print(saved_picture)

############################# Image transferral ######################################


############################# tkinter stuff #############################
root = tk.Tk()
root.title('Quantum Teleportation Protocol')
root.geometry("1480x900")
canvas = Canvas(
        root,
        bg = "#FFFFFF",
        height = 960,
        width = 1600,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

meas_scale = Scale(master = canvas, from_=0, to=100,orient="horizontal")
gate_scale = Scale(master = canvas, from_=1, to=133,orient="horizontal")
OPTIONS = [
    "80x80",
    "160x160",
    "200x200"
    ] #etc
variable = StringVar(canvas)
variable.set(OPTIONS[0]) # default value
pixel_density = OptionMenu(canvas, variable, *OPTIONS)

QuantumOPTIONS = [
    "0",
    "1",
    "2"
    ] #etc
repeaters = StringVar(canvas)
repeaters.set(QuantumOPTIONS[0]) # default value
QuantumRepeaters = OptionMenu(canvas, repeaters, *QuantumOPTIONS)


def on_entry_click(event):
    """function that gets called whenever entry is clicked"""
    if input_display.get() == 'Enter a message...':
        input_display.delete(0, "end") # delete all the text in the entry
        input_display.insert(0, '') #Insert blank for user input
        input_display.config(fg = 'black')
def on_focusout(event):
    if input_display.get() == '':
        input_display.insert(0, 'Enter a message...')
        input_display.config(fg = 'grey')

input_display   = tk.Entry(master = canvas, width = 300 , bd = 1) 
input_display.insert(0, 'Enter a message...')
input_display.config(fg = 'grey')
input_display.bind('<FocusIn>', on_entry_click)
input_display.bind('<FocusOut>', on_focusout)
input_display.config(fg = 'grey')
input_display.pack(side="left")
output_display  = tk.Entry(master = canvas, width = 300) 


def createFrontend():
    global meas_scale, gate_scale, pixel_density
    global input_display , output_display
    
    canvas.place(x = 0, y = 0)
    canvas.create_rectangle( 40, 300, 360, 375, fill="grey", outline="black") # in
    canvas.create_rectangle( 790, 300, 1110, 375, fill="grey", outline="black") # out
    

    canvas.create_rectangle( 100, 25, 300, 225 , outline="black") # in
    canvas.create_rectangle( 850, 25, 1050, 225 , outline="black") # out
    canvas.create_rectangle( 1060, 25, 1260, 225 , outline="black") # out no.2
    canvas.create_rectangle( 1270, 25, 1470, 225 , outline="black") # out no.3

    button_1 = tk.Button(master = canvas, text = "teleport the image", command=lambda: send_image())
    button_1.place( x=500.0,y=200,width=200.0,height=50.0)

    button_2 = tk.Button(master = canvas, text = "teleport the message", command=lambda: send_message())
    button_2.place( x=500.0,y=300.0,width=200.0,height=50.0)

    upload_image_button = tk.Button(master = canvas, text = "upload your image", command=lambda: upload_image())
    upload_image_button.place( x=100,y=235,width=200.0,height=50.0)

    gate_label = tk.Label(master = canvas, text = "Gate Error %")
    gate_label.place(x=550,y=40,width=100.0,height=10.0)
    
    gate_scale.set(1)
    gate_scale.place( x=400,y=50,width=400.0,height=40.0)

    meas_label = tk.Label(master = canvas, text = "Measurement Error %")
    meas_label.place(x=540,y=140,width=120.0,height=10.0)
    
    meas_scale.set(1)
    meas_scale.place( x=400,y=150,width=400.0,height=40.0)

    pixels_label  = tk.Label(master = canvas, text = "80x80 (20 seconds)\n160x160 (150 seconds)\n200x200 (250 seconds)")
    pixels_label.place(x=850,y=240,width=125.0,height=50.0)

    pixel_density.place(x=725,y=220,width=100.0,height=50.0)

    Repeater_label = tk.Label(master = canvas, text = "Repeater Count")
    Repeater_label.place(x=375,y=210,width=100.0,height=15.0)
    QuantumRepeaters.place(x = 375 , y = 220 , width = 100 , height = 50)

    input_display.place(x=50.0,y=310,width=300.0,height=50.0)
    output_display.place(x=800,y=310,width=300.0,height=50.0)

    label1 = tk.Label(master = canvas, text = "OUTPUT")
    label1.place(x=850,y=0,width=200.0,height=25.0)

    root.resizable(False, False)  
    root.mainloop()

if __name__ == '__main__':
    createFrontend()




def unpack_teleported(teleported): # a useful function to keep around for debugging, isnt used in final code.
    binary_string = ''
    for i in teleported:
        for key, value in i.items():
            binary_string = binary_string + key
    return int(binary_string)
