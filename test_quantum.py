import unittest
import QuantumTeleportation
from unittest.mock import Mock
from qiskit import *


class TestQuantum(unittest.TestCase):
    def test_string_to_binary(self):
        helloWorld = [1001000 , 1100101, 1101100, 1101100, 1101111, 100000, 1110111, 1101111, 1110010, 1101100, 1100100]
        result = QuantumTeleportation.string_to_binary("Hello world")
        self.assertEqual(result ,helloWorld)

    def test_binary_to_string(self):
        helloWorld = [1001000 , 1100101, 1101100, 1101100, 1101111, 100000, 1110111, 1101111, 1110010, 1101100, 1100100]
        result = QuantumTeleportation.binary_to_string(helloWorld)
        self.assertEqual(result, "Hello world")

    
    def test_Send_Message(self):
        result = QuantumTeleportation.Send_Message(0)
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
        
        result = QuantumTeleportation.executeCircuits([circuit, circuit])
        self.assertEqual(result[0] , [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]) # there will most likely be an error eventually





if __name__ == "__main__":
    unittest.main()