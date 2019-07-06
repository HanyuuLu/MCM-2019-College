from data import Data
from node import SysInfo
import node
from sympy import symbols,solve,sin,cos,pi
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
    objectList['pipe'] = pipe
    objectList['drums'] = drums
    objectList['chain'] = chain
    objectList['buoy'] = buoy
    for i in objectList:
        print(objectList[i])
    # 未知数队列
    varList = list()
    # 计算式
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
    for i in objectList['Chain']:
        i.gamma = symbols('GammaChainNode')
        varList.append(i.gamma)
    for i in objectList['Pipe']:
        i.gamma = symbols('GammaPipe')
        varList.append(i.gamma)
    for i in objectList['Drum']:
        i.gamma = symbols('GammaDrum')
        varList.append(i.gamma)
    # 计算队列
    calcList = \
        [
            FBuoyancysystem - FChainend *
            sin(GammaLast)-MSys*sysInfo.gravityRate,
            FWindBuoy+FFlowSystem-FChainend*sin(GammaLast),


        ]


