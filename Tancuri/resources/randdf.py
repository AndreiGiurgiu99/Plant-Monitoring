import pandas as pd
import time
import random

def GetData2():
    
    data = [['Tanc TT1', random.randint(0,100)],['Tanc TT2', random.randint(0,100)],['Tanc TT3', random.randint(0,100)],['Tanc TT4', random.randint(0,100)],
            ['Tanc PT1', random.randint(0,100)],['Tanc PT2', random.randint(0,100)],['Tanc PT3', random.randint(0,100)],['Tanc PT4', random.randint(0,100)],
            ['Tanc PT5', random.randint(0,100)],['Tanc PT6', random.randint(0,100)],['Tanc PT7', random.randint(0,100)],['Tanc PT8', random.randint(0,100)],
            ['Tanc PT9', random.randint(0,100)],['Tanc PT10', random.randint(0,100)],['Tanc PT11', random.randint(0,100)],['Tanc C4', random.randint(0,100)],
            ['Tanc M4', random.randint(0,100)]]

    dF = pd.DataFrame(data,columns=['Tancuri','Procent'])
  
    return dF

