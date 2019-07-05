from data import Data
import node
import sympy
if __name__=='__main__':
	objectList = dict()
	data = Data()
	pipe = list()
	for i in range(4):
		pipe.append(node.Pipe(node = data.pipe))
	chain = list()
	for i in range(210):
		chain.append(node.Chain(node = data.chain))
	drums = [node.Drums(node = data.drums)]
	buoy = [node.Buoy(node = data.buoy)]
	objectList['pipe']=pipe
	objectList['drums']=drums
	objectList['chain']=chain
	objectList['buoy']=buoy
	for i in objectList:
		print(i)
	