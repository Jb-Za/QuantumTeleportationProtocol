# Quantum Teleportation Protocol for a quantum internet

A Quantum Teleportation Protocol  used to transfer images using Qiskit and Python 3 

This project aims to focus on creating a proof-of-concept and to test the possibility of quantum teleportation being a viable method of transferal of information over a large distance. This communication method makes use of quantum entanglement to facilitate the transferal of information. Because the unusual laws involving quantum bits make the method of handling bits different to the current ‘classical’ ways of handling bits, a new protocol will need to be created to make an effective quantum communication protocol. 

## Installation: 
If you experience any other issues, please refer to the official documentation as given here: https://qiskit.org/documentation/getting_started.html

I suggest intially creating a seperate virtual environment for qiskit, however it is not required. refer to these docs for venv setup: https://docs.python.org/3/library/venv.html

```
python3 -m venv /path/to/new/virtual/environment
```
and
```
c:\>python -m venv c:\path\to\myenv
```

Once you are in that environment, you will need to install the dependancies 
```
pip install qiskit
``` 
```
pip install qiskit[visualization]
```
```
pip install -r requirements.txt
```

You can then run the application by typing: 
```
py QuantumTeleportation.py
```

## The User Interface

* Upload option to input an image
* Noise level sliders to add noise to the logic gates and measurement gate
* Repeater counts to repeat the quantum teleportation circuit again after every completion using the previous output
* Pixel density options (higher density = longer transfer)
* Text Input
* Image and Text teleportation buttons
* Quantum hardware and transfer error graphs

![alt text](https://i.imgur.com/YuJGkqx.png)

![alt text](https://i.imgur.com/VUj3ZEI.png)
