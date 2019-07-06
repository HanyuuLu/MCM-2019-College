from data import Data
from node import SysInfo
import node
from sympy import symbols,solve,sin,cos,pi

def findUpper(objectList,item):
    for key in objectList:
        for x in objectList[key]:
            if item in x:
                p = x.index(item)
                if p>0:
                    return x[p-1]
                else:
                    if key =='buoy':
                        return None
                    elif key=='pipe':
                        return objectList['buoy'][-1]
                    elif key =='drum':
                        return objectList['pipe'][-1]
                    elif key =='chain':
                        return objectList['drum'][-1]
                    else:
                        raise(Exception('Not in system.'))
def findLower(objectList,item):
    for key in objectList:
        for x in objectList[key]:
            if item in x:
                p = x.index(item)
                if p<len(x)-1:
                    return x[p+1]
                else:
                    if key == 'bouy':
                        return objectList['pipe'][0]
                    elif key == 'pipe':
                        return objectList['drum'][0]
                    elif key =='drum':
                        return objectList['chain'][0]
                    elif key == 'chain':
                        return None



if __name__ == '__main__':
    # 共有变量
    sysInfo = SysInfo()
    objectList = dict()
    data = Data()
    pipe = list()
    for i in range(4):
        pipe.append(node.Pipe(node=data.pipe))
    chain = list()
    for i in range(210):
        chain.append(node.Chain(node=data.chain))
    drums = [node.Drums(node=data.drums)]
    buoy = [node.Buoy(node=data.buoy)]
    objectList['buoy'] = buoy
    objectList['pipe'] = pipe
    objectList['drum'] = drums
    objectList['chain'] = chain
    # for i in objectList:
    #     print(objectList[i])
    # 未知数队列
    varList = list()
    # 计算式
    for i in objectList['chain']:
        i.gamma = symbols('GammaChainNode')
        varList.append(i.gamma)
    for i in objectList['pipe']:
        i.gamma = symbols('GammaPipe')
        varList.append(i.gamma)
    for i in objectList['drum']:
        i.gamma = symbols('GammaDrum')
        varList.append(i.gamma)
    MSys = symbols('MSys')
    varList.append(MSys)
    FBuoyancysystem = symbols('FBuoyancySystem')
    varList.append(FBuoyancysystem)
    FChainend = symbols('FChainend')
    varList.append('FCsshainend')
    FWindBuoy = symbols('FWindBuoy')
    varList.append(FWindBuoy)
    FFlowSystem = symbols('FFlowSystem')
    varList.append(FFlowSystem)
    FBuoyancyBuoy = symbols('FBuoYancyBuoy')
    varList.append(FBuoyancysystem)
    SpeedWind = symbols('SpeedWind')
    varList.append(SpeedWind)
    Rbuoy = symbols('Rbuoy')
    varList.append('Rbuoy')
    HBuoy = symbols('HBuoy')
    varList.append(HBuoy)
    FFlowBuoy = symbols('FFlowBuoy')
    varList.append(FFlowBuoy)
    SpeedWater = symbols('SpeedWater')
    varList.append(SpeedWater)
    FFlowDrum = symbols('FFlowDrum')
    varList.append(FFlowDrum)
    RDrums = symbols('RDrums')
    varList.append(RDrums)
    HDrums = symbols('HDrums')
    varList.append(HDrums)
    FFlowPipe = symbols('FFlowPipe')
    varList.append(FFlowPipe)
    RPipe = symbols('RPipe')
    varList.append(RPipe)
    HPipe = symbols('HPipe')
    varList.append(HPipe)
    FBuoyancyDrum = symbols('FBuoyancyDrum')
    varList.append(FBuoyancyDrum)
    FBuoyancyPipe = symbols('FBuoyancyPipe')
    varList.append(FBuoyancyPipe)
    MBuoy = symbols('MBuoy')
    varList.append(MBuoy)
    FBuoyPipe = symbols('FBuoyPipe')
    varList.append(FBuoyPipe)
    AngleAlphaPipeBuoy = symbols('AngleAlphaPipeBuoy')
    varList.append(AngleAlphaPipeBuoy)
    FPipeSecondPipeFirst = symbols('FPipeSecondPipeFirst')
    varList.append(FPipeSecondPipeFirst)
    AngleBetaPipeFirst = symbols('AngleBetaPipeFirst')
    varList.append(AngleBetaPipeFirst)
    FBuoyPipeFirst = symbols('FBuoyPipeFirst')
    varList.append(FBuoyPipeFirst)
    AngleAlphaPipeFitst = symbols('AngleAlphaPipeFitst')
    varList.append(AngleAlphaPipeFitst)
    FPipeSecondPipefirst = symbols('FPipeSecondPipefirst')
    varList.append(FPipeSecondPipefirst)
    FPipeLastDrum = symbols('FPipeLastDrum')
    varList.append(FPipeLastDrum)
    AngleAlpha = symbols('AngleAlpha')
    varList.append(AngleAlpha)
    FChainDrum = symbols('FChainDrum')
    varList.append(FChainDrum)
    AngleBeta = symbols('AngleBeta')
    varList.append(AngleBeta)
    FPipeLastDrum = symbols('FPipeLastDrum')
    varList.append(FPipeLastDrum)

    # 计算队列
    calcList = \
        [
            FBuoyancysystem - FChainend *
            sin(objectList['chain'][-1].gamma)-MSys*sysInfo.gravityRate,
            FWindBuoy+FFlowSystem-FChainend*sin(objectList['chain'][-1].gamma),


        ]


