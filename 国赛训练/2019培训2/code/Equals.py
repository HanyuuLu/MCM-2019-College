from sympy import cos, pi, sin, solve, symbols, sign

import node
from data import Data
from node import SysInfo


def findUpper(objectList, item):
    for key in objectList:
        for x in objectList[key]:
            if item in x:
                p = x.index(item)
                if p > 0:
                    return x[p-1]
                else:
                    if key == 'buoy':
                        return None
                    elif key == 'pipe':
                        return objectList['buoy'][-1]
                    elif key == 'drum':
                        return objectList['pipe'][-1]
                    elif key == 'chain':
                        return objectList['drum'][-1]
                    else:
                        raise(Exception('Not in system.'))


def findLower(objectList, item):
    for key in objectList:
        for x in objectList[key]:
            if item in x:
                p = x.index(item)
                if p < len(x)-1:
                    return x[p+1]
                else:
                    if key == 'bouy':
                        return objectList['pipe'][0]
                    elif key == 'pipe':
                        return objectList['drum'][0]
                    elif key == 'drum':
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
    # 各个节点的gamma角和水流产生的力
    for i in objectList['chain']:
        i.gamma = symbols('GammaChainNode_%d'%objectList['chain'].index(i))
        varList.append(i.gamma)
        i.FFlow = symbols('FFlowChainNode_%d'%objectList['chain'].index(i))
        varList.append(i.FFlow)
    for i in objectList['pipe']:
        i.gamma = symbols('GammaPipe_%d'%objectList['pipe'].index(i))
        varList.append(i.gamma)
        i.FFlow = symbols('FFlowPipe_%d'%objectList['pipe'].index(i))
        varList.append(i.FFlow)
    for i in objectList['drum']:
        i.gamma = symbols('GammaDrum_i%d'%objectList['drum'].index(i))
        varList.append(i.gamma)
        i.FFlow = symbols('FFlowDrum_i%d'%objectList['drum'].index(i))
        varList.append(i.FFlow)
    # 系统总质量
    MSys = symbols('MSys')
    varList.append(MSys)
    # 浮筒吃水线
    objectList['buoy'][0].HeightWaterLine = symbols('BuoyHeightWaterLine')
    varList.append(objectList['buoy'][0].HeightWaterLine)
    # 浮筒浮力
    objectList['buoy'][0].buoyancy = symbols('BuoyFBuoyancy')
    varList.append(objectList['buoy'][0].buoyancy)
    ####################################################################
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
    # print(varList)


    # 计算队列
    calcList = \
        [
            MSys*sysInfo.gravityRate-FBuoyancysystem-FChainend *
            cos(objectList['chain'][-1].gamma),
            FWindBuoy+FFlowSystem-FChainend*sin(objectList['chain'][-1].gamma),
            FBuoyancyBuoy-sysInfo.rhoWater*sysInfo.gravityRate*pi *
            (objectList['buoy'][0].R)**2 *
            objectList['buoy'][0].HeightWaterLine,
            FWindBuoy-sign(sysInfo.WindSpeed)*0.625*2 *
            objectList['buoy'][0].R**(objectList['buoy'][0].H-objectList['buoy']
                                      [0].HeightWaterLine)*sysInfo.WindSpeed**2,
            FFlowBuoy-sign(sysInfo.WaterSpeed)*374 *
            sysInfo.WaterSpeed**2*2 *
            objectList['buoy'][0].R*objectList['buoy'][0].HeightWaterLine,
            FFlowDrum -374*sysInfo.WaterSpeed**2*objectList['drum'][0].R*cos(objectList['drum'][0].gamma),
        ]
    # 水流产生的力
    for key in objectList:
        for x in objectList[key]:
            calcList.append(x.FFlow-374*sysInfo.WaterSpeed**2*x.R*x.H*cos(x.gamma))
    # 浮力,其他节点的计算在初始化时已经完成，浮筒此处覆盖
    objectList['Buoy'][0].FFlow
    
    for i in calcList:
        print(i)

