#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Mutant module for mutation testing, created by Jaime De la Vega
4 operators are defined to create mutants
"""
from qiskit.circuit import Instruction
from qiskit import QuantumCircuit
import random
import numpy as np
from qiskit.circuit.library.standard_gates import (
    IGate,
    U1Gate,
    U2Gate,
    U3Gate,
    XGate,
    YGate,
    ZGate,
    HGate,
    SGate,
    SdgGate,
    TGate,
    TdgGate,
    RXGate,
    RYGate,
    RZGate,
    CXGate,
    CYGate,
    CZGate,
    CHGate,
    CRZGate,
    CU1Gate,
    CU3Gate,
    SwapGate,
    RZZGate,
    CCXGate,
    CSwapGate,
)
#Primer tipo de operador, cambiar puertas consecutivas de orden, cambiando tambien el circuito

one_q_ops = [
        IGate,
        U1Gate,
        U2Gate,
        U3Gate,
        XGate,
        YGate,
        ZGate,
        HGate,
        SGate,
        SdgGate,
        TGate,
        TdgGate,    
        RXGate,
        RYGate,
        RZGate,
    ]
one_param = [U1Gate, RXGate, RYGate, RZGate, RZZGate, CU1Gate, CRZGate]
two_param = [U2Gate]
three_param = [U3Gate, CU3Gate]
two_q_ops = [CXGate, CYGate, CZGate, CHGate, CRZGate, CU1Gate, CU3Gate, SwapGate, RZZGate]
three_q_ops = [CCXGate, CSwapGate]
    
    
    
    
    
    
    


def change(ls,q1,q2):
    """
    Parameters
    ----------
    ls : lista
    q1 : elemento de la lista 
    q2 : Telemento de la lista
    
    Description
    -----------
    Modifica la lista ls para intercambiar el elemento q1 por el elemento q2

    Returns
    -------
    ls : lista

    """
    if q1 in ls:
        index = ls.index(q1)
        ls[index]=q2
    return ls
        

def replace(circ, origin: Instruction, instruction: Instruction):
    """
    Parameters
    ----------
    circ : QuantumCircuit
        circuito a modificar
    origin : Instruction
        puerta a eliminar
    instruction : Instruction
        puerta a insertar

    Description
    -----------
    Intercambia las puertas origin por la puerta instruction en el circuito circ
    
    Returns
    -------
    None.

    """
    circ._data = [(instruction, _inst[1], _inst[2]) if _inst[0] == origin  else _inst for _inst in circ._data]
    
    
    
def replace_target_qubit(circ,origin,target_qubit,final_qubit):
    """
    Parameters
    ----------
    circ : QuantumCircuit
    origin : Instruction
    target_qubit : Qubit
    final_qubit : Qubit

    Description
    -----------
    Dada una puerta origin, intercambia target_qubit por final_qubit en el conjunto de los qubits a los que afecta la puerta
    
    Returns
    -------
    None.

    """
    circ._data = [(_inst[0], change(_inst[1],target_qubit,final_qubit), _inst[2]) if _inst[0] == origin  else _inst for _inst in circ._data]





def replace_target_clbit(circ,origin,target_clbit,final_clbit):
    """
    

    Parameters
    ----------
    circ : QuantumCircuit
    origin : Instruction
    target_clbit : Clbit
    final_clbit : Clbit

    Description
    -----------
    Dada una puerta que tenga bits clásicos, intercambia target_clbit por final_clbit en el conjunto de bits clásicos a los que afecta la puerta    

    Returns
    -------
    None.

    """
    circ._data = [(_inst[0], _inst[1], change(_inst[2],target_clbit,final_clbit)) if _inst[0] == origin  else _inst for _inst in circ._data]




        
    



def gate_mutant(circ1,input_gate=None,output_gate=None):
    """
    

    Parameters
    ----------
    circ1 : QuantumCircuit
    input_gate : Instruction
    output_gate : Instruction
        
    Description
    -----------
    Intercambia input_gate por output_gate en circ1, si no se especifica alguna de las dos, se toma de manera aleatoria.

    Returns
    -------
    circ : QuantumCircuit
        Mutant

    """
    circ = circ1.copy()
    if input_gate is None:
        n = len(circ.data)
        i=0
        num_clbits=-1
        while num_clbits!=0 and i<n:
            r = random.randint(0, n-1)
            inst = circ.data[r]
            input_gate=inst[0]
            num_clbits = input_gate.num_clbits
            i+=1
    if output_gate is None:
        """
        Si no le decimos lo contrario, cambia puertas que afectan a la misma cantidad de bits
        """
        num_qubits=input_gate.num_qubits
        if num_qubits==1:
            GATE = one_q_ops[random.randint(0, len(one_q_ops)-1)]
        elif num_qubits==2:
            GATE = two_q_ops[random.randint(0, len(two_q_ops)-1)]
        elif num_qubits==3:
            GATE = three_q_ops[random.randint(0, len(three_q_ops)-1)]
        if GATE in one_param:
            p = random.uniform(0, 2*np.pi)
            output_gate = GATE(p)
        elif GATE in two_param:
            p1 = random.uniform(0, 2*np.pi)
            p2 = random.uniform(0, 2*np.pi)
            output_gate = GATE(p1,p2)
        elif GATE in three_param:
            p1=random.uniform(0, 2*np.pi)
            p2=random.uniform(0, 2*np.pi)
            p3=random.uniform(0, 2*np.pi)
            output_gate = GATE(p1,p2,p3)
        else:
            output_gate = GATE()     
    replace(circ,input_gate,output_gate)
    print('Se reemplaza la puerta ',input_gate.name,' por la puerta ',output_gate.name)
    return circ


def targetqubit_mutant(circ1,gate=None,target_qubit=None,final_qubit=None):
    """
    

    Parameters
    ----------
    circ1 : QuantumCircuit
    gate : Instruction
    target_qubit : Qubit
    final_qubit : Quibit

    Description
    -----------
    Intercambia, en gate, target_qubit por final_qubit. Los parámetros no especificados se seleccionan de manera aleatoria

    Returns
    -------
    circ : QuantumCircuit
        Mutant

    """
    circ = circ1.copy()
    if gate is None:
        n = len(circ.qubits)
        if n<3:
            raise Exception('Impossible to change target qubits for any gate as there are less than 3 qubits')
        else:
            i=0
            num_qubits=0
            while num_qubits<2 and i<n:  
                r = random.randint(0, n-1)
                inst = circ.data[r]
                num_qubits = inst[0].num_qubits
                i+=1
                gate=inst[0]            
    if gate.num_qubits<2:
        raise Exception('Could not find multi qubit gates, change the circuit or try again')
    else:
        if target_qubit is None:
            target_qubit = inst[1][random.randint(0, len(inst[1])-1)]
        if final_qubit is None:
            final_qubit = circ.qubits[random.randint(0,len(circ.qubits)-1)]
        replace_target_qubit(circ, gate, target_qubit, final_qubit)
    return circ
        

    

def targetclbit_mutant(circ1,gate=None,target_clbit=None,final_clbit=None):
    """
    

    Parameters
    ----------
    circ1 : QuantumCircuit
    gate : Instruction
    target_clbit : Clbit
    final_clbit : Clbit


    Description
    -----------
    Intercambia, en gate, target_clbit por final_clbit. Los parámetros no especificados se seleccionan de manera aleatoria


    Returns
    -------
    circ : QuantumCircuit
        Mutant

    """
    circ = circ1.copy()
    if gate is None:
        n = len(circ.data)
        if len(circ.clbits)<2:
            raise Exception('Impossible to change target clbits as there are less than 2')
        else:
            i=0
            num_clbits=0
            while num_clbits==0 and i<n:  
                r = random.randint(0, n-1)
                inst = circ.data[r]
                num_clbits = inst[0].num_clbits
                i+=1
                gate=inst[0]
    if gate.num_clbits==0:
        raise Exception('Could not find gates with classical bits or meaurements, change the circuit or try again')
    else:
        if target_clbit is None:
            target_clbit = inst[2][random.randint(0, len(inst[2])-1)]
        if final_clbit is None:
            final_clbit = circ.clbits[random.randint(0,len(circ.clbits)-1)]
        replace_target_clbit(circ, gate, target_clbit, final_clbit)
    print('Se ha cambiado los bits clásicos afectados')
    return circ
    
    
def measure_mutant(circ1,target_qubit=None,final_qubit=None):
    """
    

    Parameters
    ----------
    circ1 : TQuantumCircuit 
    target_qubit : Qubit
    final_qubit : Qubit

    Description
    -----------
    Intercambia, en una medición, target_qubit por final_qubit. Los parámetros no especificados se seleccionan de manera aleatoria

    
    Returns
    -------
    circ : QuantumCircuit
        Mutant
    """
    circ=circ1.copy()
    n=len(circ.data)
    if len(circ.clbits)<2:
        raise Exception('Impossible to change target clbits as there are less than 2')
    if target_qubit is None:
        i=0
        found=False
        while i<n and not found:
            r = random.randint(0, n-1)
            inst = circ.data[r]
            if inst[0].name=='measure':
                found=True
            i+=1
            gate=inst[0]
        target_qubit=inst[1][0]
    if gate.name != 'measure':
        raise Exception('Could not find measurement gate, change the circuit or try again')
    if final_qubit is None:
        final_qubit = circ.qubits[random.randint(0,len(circ.qubits)-1)]
    print('Se cambia el qubit al que afecta la medición')
    replace_target_qubit(circ, gate, target_qubit, final_qubit)
    return circ


def mutant(circ,gate=True,target_qubit=True,target_clbit=True,measure=True):
    """
    

    Parameters
    ----------
    circ : QuantumCircuit
    gate : bool
    target_qubit : bool
    target_clbit : bool
    measure : bool
        Indica si se quiere dar la opción de usar al operador measure

    
    Description
    -----------
    Garantiza que devuelve un mutante del circuito original de manera aleatoria seleccionando unos de los cuatro operadores, si se indica que alguno de los tres es falso, no se generará el mutante usando ese operador


    Returns
    -------
    result : QuantumCircuit
        Mutant

    

    """
    
    r = random.randint(1, 4)
    if r==1 and gate:
        result = gate_mutant(circ)
    elif r==2 and target_qubit:
        result = targetqubit_mutant(circ)
    elif r==3 and target_clbit:
        result = targetclbit_mutant(circ)
    elif measure:
        result = measure_mutant(circ)
    if result == circ:
        result = mutant(circ,gate,target_qubit,target_clbit,measure)
    return result





QuantumCircuit.mutant = mutant
QuantumCircuit.gate_mutant = gate_mutant
QuantumCircuit.targetqubit_mutant = targetqubit_mutant
QuantumCircuit.targetclbit_mutant = targetclbit_mutant
QuantumCircuit.measure_mutant = measure_mutant