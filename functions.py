## import ## 
import xmltodict
import pandas as pd
import numpy as np
from IPython.display import display
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

def load_leads(input_file):
    with open(input_file) as fd:
        doc = xmltodict.parse(fd.read())
    print("File has been loaded")
    df = pd.json_normalize(doc['exportHeader']['patient']['examination']['analysis']['blockExtended']['signal']['wave'])
    for row, lead in enumerate(df['@lead']):
        str_list = [int(index) for index in df['#text'][row].split()] # split the text into list of integers with space as separator
        if row == 0:
            df_signal = pd.DataFrame(str_list)
            df_signal.columns = [lead]
        else:
            df_signal[lead] = pd.DataFrame(str_list)
    print("Table of leads has been prepared")
    
    return df_signal, doc

def show_signal(df_signal, example_of_signal = False):
    if example_of_signal == True:
        f = plt.figure()
        f.set_figwidth(16)
        f.set_figheight(4)
        print('Example of a signal for the lead I')
        plt.plot(df_signal['I'])
        plt.gca().set(xlabel='Frequency [Hz]', ylabel='Signal')
        plt.show()
    
    return df_signal
    
def R_range(doc, df_signal, plot_R = False):
    print('Calculation of the R value...')
    R = int(doc['exportHeader']['patient']['examination']['analysis']['blockStandard']['eventTable']['event']['@tickOffset'])
    QRSon = int(doc['exportHeader']['patient']['examination']['analysis']['blockStandard']['eventTable']['event']['leadValues'][0]['value'][7]['#text'])
    QRSoff = int(doc['exportHeader']['patient']['examination']['analysis']['blockStandard']['eventTable']['event']['leadValues'][0]['value'][8]['#text'])
    R_500 = R / 4 # from frequency 2000 Hz to 500 Hz
    real_start_500 = int(R_500 - QRSon)
    real_end_500 = int(R_500 + QRSoff)
    print('Real start is {}, real end is {}, R position is {}'.format(real_start_500,real_end_500,R_500))
    
    if plot_R == True:
        print('Plotting the R wave for the lead I')
        df_signal_QRS = df_signal[real_start_500:real_end_500]
        plt.plot(df_signal_QRS['I'])
        plt.gca().set(xlabel='Frequency [Hz]', ylabel='Signal', title = 'R wave')
        plt.show()
    
    return

def R_calculation(inputs, example_of_signal, plot_R):
    for item in inputs:
        print('Calculation of R wave for the input:', item)
        df, doc = load_leads(item)
        df_signal = show_signal(df, example_of_signal)
        R = R_range(doc, df_signal, plot_R)
    
    return