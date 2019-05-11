################   IMPORTING PACKAGES      ########################
import matplotlib.pyplot as plt
from scipy import signal
from scipy.signal import butter, filtfilt
import scipy.signal as sc
import csv
import time
import datetime
import pandas as pd
import numpy as np
import math
import random
import string

###################### Paitent detail entry ##################
global bpm
global co
global stroke
global dT
global SI
global augument
global pwv


def get_result(height, arr):

    ###############    READING DATA      ###################

    data1 = np.array(arr)

    # data1 = np.loadtxt('C:\Users\hp\Desktop\Project_Final\diagnosis-webserver\api\results.txt')
    # plt.plot(data1)
    # plt.show()

    # SMOOTHING VIA BUTTER FILTER #########################3

    N = 3    # Filter order
    Wn = 0.1  # Cutoff frequency
    B, A = sc.butter(N, Wn, output='ba')
    data = sc.filtfilt(B, A, data1[0:600])
    # plt.plot(data1[0:500],'r-')
    # plt.plot(data[0:600],'b-')
    # plt.show()

    ################# REMOVING BASELINE WANDERING    ###########

    fs = 100
    cutoff = 0.001
    order = 3

    def butter_highpass(cutoff, fs, order=3):
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype='high', analog=False)
        return b, a

    def butter_highpass_filter(data, cutoff, fs, order=3):
        b, a = butter_highpass(cutoff, fs, order=order)
        y1 = filtfilt(b, a, data)
        return y1

    signal = data

    z112 = butter_highpass_filter(signal, cutoff, fs, order)
    z12 = z112+abs(min(z112))
    # plt.subplot(2,1,1)
    # plt.plot(data)
    # plt.subplot(2,1,2)
    # plt.plot(z12)
    # plt.show()

    ################    Normalisation     ##########################
    maxi = max(z12)
    z1 = []
    for i in range(1, len(z12)):  # to normalise the filtered signal
        z = z12[i]/maxi
        z1.append(z)  # normalised signal

    ########################  FINDING THE SYSTOLIC AND DIASTOLIC PEAKS   #################################
    listpos = []
    diaspos = []
    x = max(z1)  # maximum value of squared data
    # print(x)
    n = min(z1)  # minimum value of squared data
    l = len(z1)
    for i in range(2, l-2):
        if z1[i] > (0.75*x):  # Threshold setting for systolic peak
            if (z1[i-1] < z1[i]) and (z1[i] > z1[i+1]):
                # Finding the position of beat with turning point algorithm
                listpos.append(i)
                # print(listpos)
        else:  # to find diastolic peak
            if (z1[i-1] < z1[i]) and (z1[i] > z1[i+1]):
                # Finding the position of beat with turning point algorithm
                diaspos.append(i)
    ##################################     FIXING APPROPRIATE DIASTOLIC PEAK          #############################
    e = len(listpos)
    diaspos1 = []

    for i in range(listpos[0], listpos[e-1]):
        if z1[i] < (0.75*x):  # Threshold setting for diastolic peak
            if (z1[i-1] < z1[i]) and (z1[i] > z1[i+1]):
                # Finding the position of beat with turning point algorithm
                diaspos1.append(i)
                # print(diaspos1)
    f = 0
    diaspos11 = []
    len1111 = len(listpos)
    len2111 = len(diaspos1)
    LENGTH = min(len1111, len2111)
    for i in range(0, LENGTH-1):
        if(diaspos1[f]-listpos[i]) < 35 and (diaspos1[f]-listpos[i]) > 0:
            diaspos11.append(diaspos1[f])

        elif(diaspos1[f]-listpos[i]) < 0:
            while (diaspos1[f]-listpos[i]) < 0:
                f = f+1
                if(diaspos1[f]-listpos[i]) < 35:
                    diaspos11.append(diaspos1[f])
                else:
                    continue
        else:
            continue

        f = f+1

    ############### CALCULATION FOR HEART RATE   ####################
    L1 = len(listpos)
    l2 = len(diaspos11)
    L = min(L1, l2)

    ct = []
    ct1 = []
    for i in range(0, L1-1):
        ct = float(listpos[i])/100  # converted to seconds
        ct1.append(ct)
    cnt = 0
    s = 0
    RR_int = []
    while (cnt < (len(ct1)-1)):
        # Calculate distance between beats in # of samples
        RR_interval = (ct1[cnt+1] - ct1[cnt])
        RR_int.append(RR_interval)
        s = s+RR_interval
        cnt += 1
    # print(ct1)
    RR_mean = (s/len(RR_int))
    bpm = (60/(RR_mean))

    #################################   DICROTIC NOTCH    ##################
    dicrot_pos = []
    for i in range(listpos[0], l-1):
        if z1[i] < (0.75*x):
            if (z1[i-1] > z1[i]) and (z1[i] < z1[i+1]):
                dicrot_pos.append(i)

    f = 0
    dicrot_pos11 = []
    for i in range(0, len(listpos)-1):
        if(dicrot_pos[f]-listpos[i]) < 20 and (dicrot_pos[f]-listpos[i]) > 0:
            dicrot_pos11.append(dicrot_pos[f])

        elif(dicrot_pos[f]-listpos[i]) < 0:
            while (dicrot_pos[f]-listpos[i]) < 0:
                f = f+1
            if (dicrot_pos[f]-listpos[i]) < 20:
                dicrot_pos11.append(dicrot_pos[f])
            else:
                continue

        else:
            continue

        f = f+1

    # print(dicrot_pos11)
    ################################printing the peak position of dicrotic notch,systolic and diastolic peak ###########

    # Get the y-value of all peaks for plotting purposes
    ybeat = [z1[x] for x in listpos]
    ybeats = [z1[s] for s in diaspos11]
    ybeatss = [z1[t] for t in dicrot_pos11]
    plt.title("Detected peaks in signal")
    plt.xlim(0, 1000)
    plt.plot(z1, alpha=0.5, color='blue')  # Plot semi-transparent HR
    plt.scatter(listpos, ybeat, color='red')  # Plot detected peaks
    plt.scatter(diaspos11, ybeats, color='black')  # Plot detected peaks
    plt.scatter(dicrot_pos11, ybeatss, color='yellow')

    def randomString(stringLength=10):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(stringLength))

    file_name = randomString(10)
    plt.savefig('%s' % file_name)

    ################################################# AI, SI, DELTA T, PWV #################################
    AI = []
    c = 0
    d = 0
    for i in range(1, L):
        j = listpos[i]
        # print(j)
        x = z1[j]  # amplitude of systolic peak
        k = diaspos11[i]
        # absolute value of time interval between systolic and diastolic peak
        T = abs(j-k)
        d = d+T
        y = z1[k]  # amplitude of diastolic peak
        ai = ((x-y)/x)  # equation for calculating augumented index
        c = c+ai  # sum of AI values for computing average
        AI.append(ai)  # array containing AI values whose average is to be taken

    augument = (c/len(AI)*100)
    dT = (d/i)*10
    SI = (height/dT)*1000
    pwv = (RR_mean*100)/dT
    # print(AI)
    # print(c)
    # print(len(AI))

    ##print("Augumented Index(in percentage) equals",(c/len(AI)*100),"%")

    ##print(" delta T for SI (in milli sec) : ", dT,"ms")
    # 163: assumed height of the person , needs to be imported from the database later
    ##print("Stiffness Index for a person with height 175cm:",SI*1000,"cm/sec")
    ##print("Pulse wave velocity",dT/RR_mean)

    ####################################     Cardiac Output    ########################
    count1 = 0
    ss = 0
    ab = 0
    RR_intt = []
    while(count1 < (len(listpos)-1)):
        RR_intt.append(int((listpos[count1+1]-listpos[count1])/2))
        ss = ss+(int((listpos[count1+1]-listpos[count1])/2))
        count1 += 1
    print(len(RR_intt))
    print(ss)
    mean = (int(ss/(len(RR_intt))))
    print(mean)
    xss = []
    xs = 0

    for i in range(1, len(listpos)-2):
        for j in range(listpos[i]-mean, listpos[i]+mean):
            xs = xs+z1[j]
        xss.append(int(xs))
    sums = sum(xss)
    stroke = sums/len(xss)
    co = (stroke*bpm)/1000
    #print("Stroke Volume : " ,sums/i)
    #print("CO :", (stroke*bpm)/1000,"L/min")

    ####################################### FINAL RESULTS ######################

    return {"bpm": bpm, "cardiac_output": co, "stroke": stroke, "delta": dT, "stiffness_index": SI, "augmented_index": augument, "pulse_wave_velocity": pwv, "filename":'graph/'+file_name}
