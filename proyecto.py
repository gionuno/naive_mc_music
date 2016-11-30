# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np;
import numpy.random as rd;

import OSC;


def mcmc(P,N):
    X = [rd.randint(P.shape[0])];
    for n in range(1,N):
        X.append(rd.choice(np.arange(P.shape[0]),p=P[X[n-1],:]));
    return X;

def make_P(s,m):
    P = np.random.rand(m*len(s),m*len(s));
    for i in range(P.shape[0]):
        P[i,:] /= np.sum(P[i,:]);
    return P;
    
def genpart2(N,j=0,c=[0,0,0,0]):
    if N == 0:
        yield [c[0],c[1],c[2],c[3]];
    else:
        for i in range(j,4):
            if 2**(3-i) <= N:
               c[i] += 1;
               aux2 = genpart2(N-2**(3-i),i,c);
               for a in aux2:
                   yield a;
               c[i] -= 1;

def iden(x):
    return x;
def flip(x):
    return x[::-1];
def shift_left(x):
    return x[1::]+[x[0]];
def shift_right(x):
    return [x[-1]]+x[:-1];

beat_mod = [iden,flip,shift_left,shift_right];

def getrhythm(N,rep,P_beats):
    global beat_mod;
    R = list(genpart2(N));
    S = [];
    for r in R:
        if r not in S:
            S.append(r);
    aux1 = S[rd.choice(np.arange(len(S)))];
    aux2 = [];
    print aux1;
    for i in range(4):
        aux2 += aux1[i]*[i];
    print aux2;
    aux2 = list(rd.permutation(aux2));
    print aux2;
    aux3 = mcmc(P_beats,rep);
    b = [];#list(aux2);
    for j in range(rep):
        aux4 = beat_mod[aux3[j]](aux2);
        b += aux4;
    return b;

def getmelody(bpm,s,P_notes,P_beats,N,r,o):
    aux2 = getrhythm(N,r,P_beats);
    aux1  = mcmc(P_notes,len(aux2));
    notes = [ 12*(aux1[i]/len(s)+o) + s[aux1[i]%len(s)] for i in range(len(aux1))];
    beats = [ (120.0/bpm)*2.0**(-aux2[i]) for i in range(len(aux2))]; 
    return notes,beats;       

scale = {'ionian'    :[0,2,4,5,7,9,11],
         'dorian'    :[0,2,3,5,7,9,10],
         'phrygian'  :[0,1,3,5,7,8,10],
         'lydian'    :[0,2,4,6,7,9,11],
         'myxolydian':[0,2,4,5,7,9,10],
         'aeolian'   :[0,2,3,5,7,8,10],
         'locrian'   :[0,1,3,5,6,8,10],
         'hindu'     :[0,2,4,5,7,8,10],
         'jap_a'     :[0,1,5,7,8],
         'jap_b'     :[0,2,5,7,8],
         'chinese'   :[0,4,6,7,11],
         'persian'   :[0,1,4,5,6,8,11]};

client = OSC.OSCClient()
client.connect( ( '127.0.0.1', 57120 ) )

s = scale['chinese']

b = [ 5, 2, 4]
r = [ 2, 7, 1]
o = [ 0, 1, 2]
bpm = 110
for t in range(2):
    P_notes = make_P(s,1);
    P_beats = make_P(beat_mod,1);
    notes,beats = getmelody(bpm,s,P_notes,P_beats,b[t],r[t],o[t])
    data = []
    for i in range(len(notes)):
        data.append(notes[i]);
        data.append(beats[i]);
    msg = OSC.OSCMessage()
    msg.setAddress("/print")
    msg.append(data);
    client.send(msg)

