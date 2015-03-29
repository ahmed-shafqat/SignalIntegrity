import unittest

import SignalIntegrity as si
from numpy import linalg
from numpy import matrix
from TestHelpers import *

class TestTransistor(unittest.TestCase,SourcesTesterHelper,RoutineWriterTesterHelper):
    def __init__(self, methodName='runTest'):
        RoutineWriterTesterHelper.__init__(self)
        unittest.TestCase.__init__(self,methodName)
    def testTransistorSimpleSymbolic(self):
        symbolic=si.sd.Symbolic(size='small',eqprefix='\\begin{equation}',eqsuffix='\\end{equation}')
        symbolic._AddEq('\\mathbf{S}='+symbolic._LaTeXMatrix(si.sy.TransconductanceAmplifierThreePort('-g_m', 'r_{\\pi}', 'r_o')))
        symbolic.m_lines = [line.replace('--','+') for line in symbolic.m_lines]
        symbolic.Emit()
        # exclude
        self.CheckSymbolicResult(self.id(),symbolic,'Simple Transistor')    
    def testTransistorSimpleSymbolic2(self):
        sdp=si.p.SystemDescriptionParser()
        sdp.AddLines(['device DC 4',
            'device HIE 2',
            'port 1 HIE 1 2 DC 4 3 DC 3',
            'connect HIE 2 DC 1',
            'connect DC 2 DC 4'])
        # exclude
        # sdp.WriteToFile('TransistorSimpleNetList.txt',False)
        # include
        ssps=si.sd.SystemSParametersSymbolic(sdp.SystemDescription(),size='small')
        ssps.AssignSParameters('DC',si.sy.CurrentControlledCurrentSource('\\beta'))
        ssps.AssignSParameters('HIE',si.sy.SeriesZ('h_{ie}'))
        ssps.LaTeXSolution(size='big').Emit()
        # exclude
        self.CheckSymbolicResult(self.id(),ssps,'Simple Transistor 2')
    def testTransistorSymbolic(self):
        sdp=si.p.SystemDescriptionParser()
        sdp.AddLines(['device T 3','device rb 2','device Cm 2','device Cp 2','device rx 2',
                      'device rc 2','device Cc 2',
                      'port 1 rb 1 2 rc 2 3 rx 2 4 Cc 2',
                      'connect rb 2 Cp 1 Cm 1 T 1','connect T 2 rc 1 Cm 2 Cc 1',
                      'connect Cp 2 T 3 rx 1'])
        ssps=si.sd.SystemSParametersSymbolic(sdp.SystemDescription(),size='small')
        ssps.LaTeXSolution(size='biggest').Emit()
        # exclude
        self.CheckSymbolicResult(self.id(),ssps,'Transistor')
    def testTransistorWithShuntsSymbolic(self):
        sdp=si.p.SystemDescriptionParser()
        sdp.AddLines(['device T 3','device rb 2','device Cms 4','device Cps 4','device rx 2',
                      'device rc 2','device Ccs 3',
                      'port 1 rb 1 2 rc 2 3 rx 2 4 Ccs 3',
                      'connect rb 2 Cms 1','connect Cms 3 Cps 1','connect Cps 3 T 1',
                      'connect T 3 Cps 4','connect Cps 2 rx 1','connect T 2 Ccs 1',
                      'connect Ccs 2 Cms 4','connect Cms 2 rc 1'])
        ssps=si.sd.SystemSParametersSymbolic(sdp.SystemDescription(),size='small')
        ssps._AddEq('\\mathbf{rb}='+ssps._LaTeXMatrix(si.sy.SeriesZ('r_b')))
        ssps._AddEq('\\mathbf{rc}='+ssps._LaTeXMatrix(si.sy.SeriesZ('r_c')))
        ssps._AddEq('\\mathbf{rx}='+ssps._LaTeXMatrix(si.sy.SeriesZ('r_ex')))
        ssps._AddEq('\\mathbf{Cms}='+ssps._LaTeXMatrix(si.sy.ShuntZ(4,'\\frac{1}{C_{\\mu}\\cdot s}')))
        ssps._AddEq('\\mathbf{Ccs}='+ssps._LaTeXMatrix(si.sy.ShuntZ(3,'\\frac{1}{C_{cs}\\cdot s}')))
        ssps._AddEq('\\mathbf{Cps}='+ssps._LaTeXMatrix(si.sy.ShuntZ(4,'\\frac{1}{C_{\\pi}\\cdot s}')))
        ssps._AddEq('\\mathbf{T}='+ssps._LaTeXMatrix(si.sy.TransconductanceAmplifierThreePort('-g_m', 'r_{\\pi}', 'r_o')))
        ssps.m_lines = [line.replace('--','+') for line in ssps.m_lines]
        ssps.LaTeXSolution(size='biggest').Emit()
        # exclude
        self.CheckSymbolicResult(self.id(),ssps,'Transistor')
    def testTransistorSymbolicZO(self):
        sdp=si.p.SystemDescriptionParser()
        sdp.AddLines(['device DC 4',
            'device HIE 2',
            'device ZO 2',
            'port 1 HIE 1 2 DC 4 3 DC 3',
            'connect HIE 2 DC 1',
            'connect DC 2 DC 4',
            'connect ZO 1 DC 3',
            'connect ZO 2 DC 4'])
        # exclude
        # sdp.WriteToFile('TransistorSimpleNetList.txt',False)
        # include
        ssps=si.sd.SystemSParametersSymbolic(sdp.SystemDescription(),size='small')
        ssps.AssignSParameters('DC',si.sy.CurrentControlledCurrentSource('\\beta'))
        ssps.AssignSParameters('HIE',si.sy.SeriesZ('Z_{\\pi}'))
        ssps.AssignSParameters('ZO',si.sy.SeriesZ('Z_o'))
        ssps.LaTeXSolution(size='big').Emit()
        # exclude
        self.CheckSymbolicResult(self.id(),ssps,'Transistor Zo')
    def testTransistorSimpleSymbolicCode(self):
        self.WriteCode('TestTransistor.py','testTransistorSimpleSymbolic2(self)',self.standardHeader)
    def testTransistorZoSymbolicCode(self):
        self.WriteCode('TestTransistor.py','testTransistorZOSymbolic(self)',self.standardHeader)
    def testTransistorSymbolicCode(self):
        self.WriteCode('TestTransistor.py','testTransistorSymbolic(self)',self.standardHeader)
    def testTransistorWithShuntsSymbolicCode(self):
        self.WriteCode('TestTransistor.py','testTransistorWithShuntsSymbolic(self)',self.standardHeader)

if __name__ == '__main__':
    unittest.main()

