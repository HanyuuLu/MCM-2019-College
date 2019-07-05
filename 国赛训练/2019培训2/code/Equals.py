from data import Data
from node import SysInfo
import node
from sympy import symbols,solve,sin,cos
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
    # 计算式1
    MSys = symbols('MSys')
    varList.append(MSys)
    FByuoancysystem = symbols('FByuoancySystem')
    varList.append(FByuoancysystem)
    GammaLast = symbols('GammaList')
    varList.append(GammaLast)
    FChainend = symbols('FChainend')
    varList.append('FCsshainend')
    FWindBuoy = symbols('FWindBuoy')
    varList.append(FWindBuoy)
    FFlowSystem = symbols('FFlowSystem')
    varList.append(FFlowSystem)

    # 计算队列
    calcList = \
        [
            FByuoancysystem - FChainend *
            sin(GammaLast)-MSys*sysInfo.gravityRate,
            FWindBuoy+FFlowSystem

        ]


