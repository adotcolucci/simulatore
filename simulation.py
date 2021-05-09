import pandas as pd
import numpy  as np
import math

# Model parameter
# mean and standard deviation we describe the parameter of the model
# acceleration and velocity are student mouvement caractheristics
# and we are modeled by the mean of exponential distribution
#
a_mean = 0.08
v_mean = 0.8
#
# The number of student per classes is modeled by the mean and the variance of normal (Gaussian) distribution
p_mean, p_sigma = 23, 5

#
# The initial school configuration is modeled by multiply the class section for the number of age of courses for the random
# number of student per class
sezioni = ['A','B','C']
corso   = [1,2,3,4,5]
#
# The spatial caracteristicts are calculated to rappresent all necessary
# room to contains the classes into unique floor

l       = len(sezioni)*len(corso)
pos    = {}
#lato aula
l_aula  = 5
#larghezza (dx) e lunghezza (dy) del corridoio
dx,dy   = 3,l_aula*(int(l/2)+1)
for i in range(int(l/2)+1):
    pos[2*i]={2*i:[l_aula,l_aula*i+2.5]}
    pos[2*i+1]={2*i+1:[l_aula+dx,l_aula*i+2.5]}

#Popolo le classi col numero di alunni
s       = np.random.normal(p_mean, p_sigma, l)
s       = s.astype('int')

#Associo gli alunni alle aule
aule    = {}
id      = 0
mtr     = 0
xsz,ysz = 0,0
for sz in sezioni:
    for c in corso:
        for i in range(s[id]):
            mtr = mtr+1
            aule[mtr]={'sezione':sz
            ,'anno':c
            ,'matricola':'MTR'+('00000'+str(mtr))[-5:]
            ,'x':pos[id][id][0]
            ,'y':pos[id][id][1]
            ,'a0':np.round(np.random.exponential(a_mean),3)
            ,'V0':np.round(np.random.exponential(v_mean),2)
}
        id = id+1

df_aule = pd.DataFrame.from_dict(aule,orient='index')

# Y axes model mouvement
def sy(s0,a0,v0,t0,T):
    '''
    spazio
    '''
    step=[]
    a0=max(0,a0)
    v0=max(0,v0)
    for t in range(0,T):
        if t<t0:
            step.extend([s0])
        else:
            ss=0.5*a0*(t-t0)*(t-t0)+v0*(t-t0)+s0
            step.extend([ss])
    return step

# X axes model mouvement
def sx(s0,xmin,xmax,a0,v0,t0,T):
    '''
    spazio
    '''
    step=[]
    a0=max(0,a0)
    v0=max(0,v0)
    dx=xmin+(xmax-xmin)/2
    omg= 2*math.pi/T
    for t in range(0,T):
        if t<t0:
            step.extend([s0])
        else:
            ss=-a0*math.sin(omg*(t-t0))/(omg*omg)+v0*(t-t0)+s0
            if s0>=dx:
                ss=min(s0,ss)
                ss=max(dx,ss)
            else:
                ss=min(dx,ss)
                ss=max(s0,ss)
            step.extend([ss])
    return step

#%%
df_aule=df_aule.reset_index(inplace=False)
T=5*60
S = pd.DataFrame()
for i in df_aule.index:
    print(i)
    t0=np.random.randint(5*60)
    p=pd.DataFrame([sx(s0=df_aule.iloc[i]['x']
        ,xmin=l_aula,xmax=l_aula+dx
        , a0=df_aule.iloc[i]['a0'],v0=df_aule.iloc[i]['V0']
        ,t0=t0,T=T)
    ,sy(s0=df_aule.iloc[i]['y']
    ,a0=0,v0=df_aule.iloc[i]['V0']
    ,t0=t0,T=T)]).T
    p.columns=['x','y']
    p['sezione']    = df_aule.iloc[i]['sezione']
    p['anno']       = df_aule.iloc[i]['anno']
    p['matricola']  = df_aule.iloc[i]['matricola']
    p['a0']         = df_aule.iloc[i]['a0']
    p['V0']         = df_aule.iloc[i]['V0']
    S=S.append(p)

S.to_csv('chiara.csv',sep=';')
# %%
