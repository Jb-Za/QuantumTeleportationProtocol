import unittest
import QuantumTeleportation
from unittest.mock import Mock
from qiskit import *
import matplotlib.pyplot as plt


class TestQuantum(unittest.TestCase):
    def test_string_to_binary(self):
        helloWorld = [1001000 , 1100101, 1101100, 1101100, 1101111, 100000, 1110111, 1101111, 1110010, 1101100, 1100100]
        result = QuantumTeleportation.string_to_binary("Hello world")
        #print("\nstring to binary expected output: " , helloWorld)
        #print("string to binary given output: " , result)
        self.assertEqual(result ,helloWorld)

    def test_binary_to_string(self):
        helloWorld = [1001000 , 1100101, 1101100, 1101100, 1101111, 100000, 1110111, 1101111, 1110010, 1101100, 1100100]
        result = QuantumTeleportation.binary_to_string(helloWorld)
        #print("\nbinary to string expected output: Hello world" )
        #print("binary to string given output: " , result)
        self.assertEqual(result, "Hello world")

    
    def test_Send_Message(self):
        result = QuantumTeleportation.Send_Message(0)
        print("\nsend individual bit expected output: 0" )
        print("send individual bit given output: " , result)
        self.assertEqual(result ,0)
        
        #self.assertEqual()

    def test_executeCircuits(self):
        eight_bits = [False , False ,False ,False ,False ,False ,False ,False ]
        circuit = QuantumCircuit(24 , 8)
        for j in range(8):
            if eight_bits[j] == False:
                circuit.x(j)
            
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

        for k in range(8):      
            circuit.measure(k + 16, k ) 

        #circuit.draw(output='mpl', fold= -1)
        #plt.show()
        
        result = QuantumTeleportation.executeCircuits([circuit, circuit])
        print("\nsend eight bits expected output: ", eight_bits, eight_bits  )
        print("send eight bits given output: " , result[0])
        print("this is sending two circuits at once, so the output is 16 bits")
        self.assertEqual(result[0] , [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]) # given the fact that it is a quantum circuit, there tends to be individual incorrect values sometimes. this is normal





if __name__ == "__main__":
    unittest.main()