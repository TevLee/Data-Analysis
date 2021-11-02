# 현재 경로(./)에 아래내용으로 파일만들기
import numpy as np
import matplotlib.pyplot as plt

def plotSinWave(**kwargs): #keyword arguments
    """
    [Dostring] : plotSineWave...\n
    plotsinwave
    y = a sin(2 pi ft + t_0)+b
    """
    #기본값 설정
    import matplotlib.pyplot as plt
    endTime = kwargs.get("endTime",1)
    sampleTime = kwargs.get("sampleTime",0.01)
    amp = kwargs.get("amp",1)
    freq = kwargs.get("freq",1)
    startTime = kwargs.get("startTime",0)
    bias = kwargs.get("bias",0)
    figsize = kwargs.get("figsize",(12,6))

    time = np.arange(startTime, endTime, sampleTime)
    result = amp*np.sin(2*np.pi * freq*time+startTime)+bias

    plt.figure(figsize=(12,6))
    plt.plot(time,result)
    plt.grid(True)
    plt.xlabel("time")
    plt.ylabel("sin")
    plt.title("한글테스트"+str(amp)+"*sin(2*pi "+str(freq)+"*t"+str(startTime)+")+"+str(bias))
    plt.show()

if __name__ == "__main__":
    print("hello word!")
    print("this is test graph!!")
    plotSinWave(amp=1,endTime=10)
