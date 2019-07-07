from sympy import cos, pi, sin, solve, symbols, sign

import node
from data import Data
from node import SysInfo
import sys

def findUpper(objectList, item):
    for key in objectList:
        if item in objectList[key]:
            p = objectList[key].index(item)
            if p > 0:
                return objectList[key][p-1]
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
        if item in objectList[key]:
            p = objectList[key].index(item)
            if p < len(objectList[key])-1:
                return objectList[key][p+1]
            else:
                if key == 'buoy':
                    return objectList['pipe'][0]
                elif key == 'pipe':
                    return objectList['drum'][0]
                elif key == 'drum':
                    return objectList['chain'][0]
                elif key == 'chain':
                    return None


if __name__ == '__main__':
    sys.setrecursionlimit(int(1e6))
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
        i.gamma = symbols('GammaChainNode_%d' % objectList['chain'].index(i))
        varList.append(i.gamma)
        i.FFlow = symbols('FFlowChainNode_%d' % objectList['chain'].index(i))
        varList.append(i.FFlow)
        i.Falpha = symbols('FalphaChainNode_%d' % objectList['chain'].index(i))
        varList.append(i.Falpha)
        i.alpha = symbols('alphaChainNode_%d' % objectList['chain'].index(i))
        varList.append(i.alpha)
        i.Fbeta = symbols('FbetaChainNode_%d' % objectList['chain'].index(i))
        varList.append(i.Fbeta)
        i.beta = symbols('betaChainNode_%d' % objectList['chain'].index(i))
        varList.append(i.beta)
    for i in objectList['pipe']:
        i.gamma = symbols('GammaPipeNode_%d' % objectList['pipe'].index(i))
        varList.append(i.gamma)
        i.FFlow = symbols('FFlowPipeNode_%d' % objectList['pipe'].index(i))
        varList.append(i.FFlow)
        i.Falpha = symbols('FalphaPipeNode_%d' % objectList['pipe'].index(i))
        varList.append(i.Falpha)
        i.alpha = symbols('alphaPipeNode_%d' % objectList['pipe'].index(i))
        varList.append(i.alpha)
        i.Fbeta = symbols('FbetaPipeNode_%d' % objectList['pipe'].index(i))
        varList.append(i.Fbeta)
        i.beta = symbols('betaPipeNode_%d' % objectList['pipe'].index(i))
        varList.append(i.beta)
    for i in objectList['drum']:
        i.gamma = symbols('GammaDrumNode_%d' % objectList['drum'].index(i))
        varList.append(i.gamma)
        i.FFlow = symbols('FFlowDrumNode_%d' % objectList['drum'].index(i))
        varList.append(i.FFlow)
        i.Falpha = symbols('FalphaDrumNode_%d' % objectList['drum'].index(i))
        varList.append(i.Falpha)
        i.alpha = symbols('alphaDrumNode_%d' % objectList['drum'].index(i))
        varList.append(i.alpha)
        i.Fbeta = symbols('FbetaDrumNode_%d' % objectList['drum'].index(i))
        varList.append(i.Fbeta)
        i.beta = symbols('betaDrumNode_%d' % objectList['drum'].index(i))
        varList.append(i.beta)
    # 系统总质量
    MSys = 0
    for key in objectList:
        for x in objectList[key]:
            MSys += x.M
    # 浮筒吃水线
    objectList['buoy'][0].HeightWaterLine = symbols('BuoyHeightWaterLine')
    varList.append(objectList['buoy'][0].HeightWaterLine)
    # 浮筒浮力
    objectList['buoy'][0].buoyancy = symbols('BuoyFBuoyancy')
    varList.append(objectList['buoy'][0].buoyancy)
    # 游动半径
    activityR = symbols('ActivityR')
    varList.append(activityR)
    # ####################################################################
    FBuoyancySystem = symbols('FBuoyancySystem')
    varList.append(FBuoyancySystem)
    # FChainend = symbols('FChainend')
    # varList.append('FCsshainend')
    objectList['buoy'][0].FWind = symbols('FWindBuoy')
    varList.append(objectList['buoy'][0].FWind)
    FFlowSystem = symbols('FFlowSystem')
    varList.append(FFlowSystem)
    FBuoyancyBuoy = symbols('FBuoYancyBuoy')
    # varList.append(FBuoyancySystem)
    # SpeedWind = symbols('SpeedWind')
    # varList.append(SpeedWind)
    # Rbuoy = symbols('Rbuoy')
    # varList.append('Rbuoy')
    # HBuoy = symbols('HBuoy')
    # varList.append(HBuoy)
    # FFlowBuoy = symbols('FFlowBuoy')
    # varList.append(FFlowBuoy)
    # SpeedWater = symbols('SpeedWater')
    # varList.append(SpeedWater)
    # FFlowDrum = symbols('FFlowDrum')
    # varList.append(FFlowDrum)
    # RDrums = symbols('RDrums')
    # varList.append(RDrums)
    # HDrums = symbols('HDrums')
    # varList.append(HDrums)
    # FFlowPipe = symbols('FFlowPipe')
    # varList.append(FFlowPipe)
    # RPipe = symbols('RPipe')
    # varList.append(RPipe)
    # HPipe = symbols('HPipe')
    # varList.append(HPipe)
    # FBuoyancyDrum = symbols('FBuoyancyDrum')
    # varList.append(FBuoyancyDrum)
    # FBuoyancyPipe = symbols('FBuoyancyPipe')
    # varList.append(FBuoyancyPipe)
    # MBuoy = symbols('MBuoy')
    # varList.append(MBuoy)
    # FBuoyPipe = symbols('FBuoyPipe')
    # varList.append(FBuoyPipe)
    # AngleAlphaPipeBuoy = symbols('AngleAlphaPipeBuoy')
    # varList.append(AngleAlphaPipeBuoy)
    # FPipeSecondPipeFirst = symbols('FPipeSecondPipeFirst')
    # varList.append(FPipeSecondPipeFirst)
    # AngleBetaPipeFirst = symbols('AngleBetaPipeFirst')
    # varList.append(AngleBetaPipeFirst)
    # FBuoyPipeFirst = symbols('FBuoyPipeFirst')
    # varList.append(FBuoyPipeFirst)
    # AngleAlphaPipeFitst = symbols('AngleAlphaPipeFitst')
    # varList.append(AngleAlphaPipeFitst)
    # FPipeSecondPipefirst = symbols('FPipeSecondPipefirst')
    # varList.append(FPipeSecondPipefirst)
    # FPipeLastDrum = symbols('FPipeLastDrum')
    # varList.append(FPipeLastDrum)
    # AngleAlpha = symbols('AngleAlpha')
    # varList.append(AngleAlpha)
    # FChainDrum = symbols('FChainDrum')
    # varList.append(FChainDrum)
    # AngleBeta = symbols('AngleBeta')
    # varList.append(AngleBeta)
    # FPipeLastDrum = symbols('FPipeLastDrum')
    # varList.append(FPipeLastDrum)
    # # print(varList)

    # 计算队列
    calcList = \
        [
            # 系统受力
            MSys*sysInfo.gravityRate-FBuoyancySystem-objectList['chain'][-1].Fbeta *
            cos(objectList['chain'][-1].gamma),
            # 系统受力
            objectList['buoy'][0].FWind+FFlowSystem - \
            objectList['chain'][-1].Fbeta*sin(objectList['chain'][-1].gamma),
            # 浮标受力
            FBuoyancyBuoy-sysInfo.rhoWater*sysInfo.gravityRate*pi *
            (objectList['buoy'][0].R)**2 *
            objectList['buoy'][0].HeightWaterLine,
            # 浮标风力
            objectList['buoy'][0].FWind-sign(sysInfo.WindSpeed)*0.625*2 *
            objectList['buoy'][0].R*(objectList['buoy'][0].H-objectList['buoy']
                                     [0].HeightWaterLine)*sysInfo.WindSpeed**2
        ]
    tempB = 0
    tempW = 0
    # 系统浮力，水流的力的方程
    for key in objectList:
        if key == 'buoy':
            for x in objectList[key]:
                tempB += x.R ** 2 * x.HeightWaterLine
                tempW += x.R*x.HeightWaterLine
        else:
            for x in objectList[key]:
                tempB += x.R ** 2 * x.H
                tempW += x.R*x.H*cos(x.gamma)
    tempB *= sysInfo.rhoWater * sysInfo.gravityRate * pi
    tempW *= sign(sysInfo.WaterSpeed)*374*sysInfo.WaterSpeed**2*2
    calcList.append(
        tempB - FBuoyancySystem
    )
    calcList.append(
        tempW - FFlowSystem
    )

    # 所有节点受到水流产生的力
    for key in objectList:
        # 浮标高度特殊
        if key == 'buoy':
            for x in objectList[key]:
                calcList.append(
                    x.FFlow-374*sysInfo.WaterSpeed **
                    2 * x.R * x.HeightWaterLine * cos(x.gamma)
                )
        else:
            for x in objectList[key]:
                calcList.append(
                    x.FFlow-374*sysInfo.WaterSpeed ** 2 *
                    x.R * x.H * cos(x.gamma)
                )
    # 浮力,其他节点的计算在初始化时已经完成，浮筒此处覆盖
    calcList.append(
        -objectList['buoy'][0].buoyancy+sysInfo.rhoWater *
        sysInfo.gravityRate * pi *
        objectList['buoy'][0].R ** 2 * objectList['buoy'][0].HeightWaterLine
    )
    # 节点牛顿第三定律受力方程
    for key in objectList:
        if key == 'buoy':
            for x in objectList[key]:
                calcList.append(x.Falpha)
        else:
            for x in objectList[key]:
                calcList.append(
                    x.Falpha - findUpper(objectList, x).Fbeta
                )
    # 节点力矩方程
    for key in objectList:
        if key == 'buoy':
            continue
        else:
            for x in objectList[key]:
                calcList.append(
                    x.Fbeta * sin(x.beta) - x.Falpha * sin(x.alpha)
                )
                calcList.append(
                    x.Fbeta*sin(x.beta)+x.Falpha*sin(x.alpha)*sin(x.gamma) -
                    x.M * sysInfo.gravityRate *
                    sin(x.gamma) - x.FFlow * cos(x.gamma)
                )
                calcList.append(
                    x.Fbeta*cos(x.beta)+(x.M*sysInfo.gravityRate)
                    * cos(x.gamma) - x.FFlow * sin(x.gamma) - x.Falpha * cos(x.alpha)
                )
    # 钢桶系统
    calcList.append(
        objectList['drum'][0].Falpha*sin(objectList['drum'][0].alpha) -
        objectList['drum'][0].M*sin(objectList['drum'][0].beta)
    )
    calcList.append(
        objectList['drum'][0].Falpha *
        sin(objectList['drum'][0].alpha) +
        objectList['drum'][0].buoyancy*sin(objectList['drum'][0].gamma)+objectList['drum'][0].Fbeta*sin(
            objectList['drum'][0].beta)-(objectList['drum'][0].M+objectList['drum'][0].MBall)*sysInfo.gravityRate*cos(objectList['drum'][0].gamma)-objectList['drum'][0].Fbeta*cos(objectList['drum'][0].beta)
    )
    calcList.append(
        objectList['drum'][0].Falpha*cos(objectList['drum'][0].alpha)+objectList['drum'][0].buoyancy*cos(objectList['drum'][0].gamma)+objectList['drum'][0].FFlow*sin(objectList['drum'][0].gamma)-(
            objectList['drum'][0].M+objectList['drum'][0].MBall)*sysInfo.gravityRate*cos(objectList['drum'][0].gamma)-objectList['drum'][0].Fbeta*cos(objectList['drum'][0].beta)
    )
    # 水深公式
    ds = 0
    for key in objectList:
        if key == 'buoy':
            for i in objectList[key]:
                ds += i.HeightWaterLine
        else:
            for i in objectList[key]:
                ds += i.H
    calcList.append(
        ds-sysInfo.WaterDeepth
    )
    expR = 0
    for key in objectList:
        for i in objectList[key]:
            expR += i.H*sin(i.gamma)
    expR += objectList['buoy'][0].R
    calcList.append(
        activityR-expR
    )
    for i in calcList:
        print(i)
    result = solve(calcList, varList)
    print(result)
    with open('res.txt', 'w') as printer:
        printer.write(str(result))
