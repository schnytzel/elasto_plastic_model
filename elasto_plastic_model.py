# coding: utf-8
import numpy as np
import matplotlib.pylab as plt

def findLin( tab , band , crossSec ):
    aq = []
    list = tab.tolist()
    for i in list:
        if ( band[0] < i[3] and i[3] < band[1] ):  
            aq = aq + [i]
    tmp = np.array(aq)
    strain = tmp[:,3]
    stress = tmp[:,2] / crossSec * 1000
    plt.plot(strain , stress , '.' )
    Young , coeffB = np.polyfit( strain , stress , 1)
    labelPlotLin = 'Young='+str(int(Young))+'MPa coeffB='+str(int(coeffB))
    plt.plot(strain , Young * strain + coeffB , label = labelPlotLin ,  )
    plt.xlabel('strain [mm/mm]')
    plt.ylabel('stress [MPa]')
    plt.legend(loc = 'best')
    return Young , coeffB


def findPlastStrain( tab , Young , coeffB , crossSec ):
    strainPlasticList = []
    dataList = tab.tolist()
    for i in dataList:
        stress = i[2] / crossSec * 1000
        strainLin = ( stress - coeffB ) / Young 
        strainPlast = i[3] - strainLin
        strainPlasticList = strainPlasticList + [[stress , strainPlast]] 
    return np.array( strainPlasticList )


def stressPt( data , step , cross ):
    maxStress = np.max(data[:,0])
    i = 0
    stressPt = step
    aq = []
    while  stressPt < maxStress and i < len(data) :
        if stressPt < data[i,0] :
            stressPt += step
            if data[i,1] > 1e-4 :
                aq = aq + [[ data[i,0] , data[i,1] ]]
        i += 1
    return np.array(aq)

tab = np.loadtxt('4.dat' , skiprows=10)
band = [0.0002 , 0.0005]
crossSec = np.pi * 7.82**2 / 4 
Young , coeffB = findLin( tab , band , crossSec )
strainPlasticList = findPlastStrain( tab , Young , coeffB , crossSec )
step = 10
plasticTable = stressPt( strainPlasticList , step , crossSec )
np.savetxt( 'plasticTable.txt' , plasticTable )
