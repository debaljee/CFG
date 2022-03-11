import networkx as nx
import matplotlib.pyplot as plt
class GraphVisualization:
    def __init__(self):
        self.visual=[]
    def addEdge(self,a,b):
        temp=[a,b]
        self.visual.append(temp)
    def visualize(self):
        G=nx.DiGraph()
        G.add_edges_from(self.visual)
        nx.draw_networkx(G)
        fig=plt.gcf()
        ax=fig.gca()
        ax.axis("off")
        plt.show()

numVertices=20
maxIndex=0

myFile=open('myCode.txt','r')
txt=myFile.read()
txt=txt+'endingString'

characters=[char for char in txt]



class node:
    def __init__(self):
        self.right=None
        self.index=-1

def initGraph(n):
    arr=[None for i in range(n)]
    return(arr)
def insertEdge(myGraph,i,j):
    myNode=node()
    myNode.index=j
    myNode.right=myGraph[i]
    myGraph[i]=myNode
def displayGraph(myGraph):
    for i in range(len(myGraph)):
        myNode=myGraph[i]
        myString=''
        myString=myString+str(i)
        while(myNode!=None):
            myString=myString+'->'+str(myNode.index)
            myNode=myNode.right
        print(myString)



def copyEdges(myGraph,vertex1,vertex2):
    myNode=myGraph[vertex1]
    while(myNode!=None):
        insertEdge(myGraph,vertex2,myNode.index)
        myNode=myNode.right
def showGraph(myGraph):
    G=GraphVisualization()
    for i in range(0,len(myGraph)):
        myNode=myGraph[i]
        while(myNode!=None):
            G.addEdge(i,myNode.index)
            myNode=myNode.right
    G.visualize()

class tokenNode:
    def __init__(self):
        self.right=None
        self.char=''
class myTokens:
    def __init__(self):
        self.front=None
        self.back=None
def initTokens():
    tokenList=myTokens()
    tokenList.front=None
    tokenList.back=None
    return(tokenList)
def insertToken(tokenList,character):
    if(tokenList.front==None and tokenList.back==None):
        tokenList.front=tokenNode
        tokenList.back=tokenList.front
        temp=tokenList.front
        temp.right=None
        temp.char=character
    else:
        tokenList.back.right=tokenNode()
        temp=tokenList.back.right
        temp.right=None
        temp.char=character
        tokenList.back=temp
def printList(tokenList):
    myNode=tokenList.front
    while(myNode!=None):
        print(myNode.char)
        myNode=myNode.right

def tokenize(characters):
    global txt
    myList=initTokens()
    for i in range(10):
        characters.append(' ')
        txt=txt+' '
    i=0
    while(i<len(characters)-6):
        if(txt[i:i+3]=='for'):
            insertToken(myList,txt[i:i+3])
            i+=3
        elif(txt[i:i+5]=='while'):
            insertToken(myList,txt[i:i+5])
            i+=5
        elif(txt[i:i+2]=='if'):
            insertToken(myList,txt[i:i+2])
            i+=2
        elif(txt[i:i+2]=='do'):
            insertToken(myList,txt[i:i+2])
            i+=2
        elif(txt[i:i+4]=='else'):
            insertToken(myList,txt[i:i+4])
            i+=4
        elif(txt[i:i+5]=='break'):
            insertToken(myList,txt[i:i+5])
            i+=5
        elif(txt[i]!=' ' and txt[i]!='\n'):
            insertToken(myList,txt[i])
            i+=1
        else:
            i+=1
    return(myList)

def seekBlockClosure(location):
    parenthesisCount=0
    while(True):
        if(location.char=='{'):
            parenthesisCount+=1
        elif(location.char=='}'):
            parenthesisCount-=1
        if(parenthesisCount==0):
            break
        location=location.right
    return(location)
def generateCfg(myGraph,body,exit,myList,listEnd):
    global maxIndex
    while(myList!=listEnd):
        if(myList.char=='if'):
            while(myList.char!='{'):
                myList=myList.right
            myNode=seekBlockClosure(myList)
            if(myNode.right.char!='else'):
                maxIndex+=2
                copyEdges(myGraph,body,maxIndex)
                myGraph[body]=None
                insertEdge(myGraph,body,maxIndex-1)
                insertEdge(myGraph,maxIndex-1,maxIndex)
                insertEdge(myGraph,body,maxIndex)
                generateCfg(myGraph,maxIndex-1,exit,myList,myNode)
                myList=myNode.right
                continue
            else:
                maxIndex+=1
                copyEdges(myGraph,body,maxIndex)
                myGraph[body]=None
                destinationNode=maxIndex
                
                maxIndex+=1
                insertEdge(myGraph,maxIndex,destinationNode)
                insertEdge(myGraph,body,maxIndex)
                generateCfg(myGraph,maxIndex,exit,myList,myNode)
                
                while(myNode.right.char=='else' and myNode.right.right.char=='if'):
                    maxIndex+=1
                    insertEdge(myGraph,maxIndex,destinationNode)
                    insertEdge(myGraph,body,maxIndex)
                    while(myNode.char!='{'):
                        myNode=myNode.right
                    newNode=seekBlockClosure(myNode)
                    generateCfg(myGraph,maxIndex,exit,myNode,newNode)
                    myNode=newNode
                if(myNode.right.char!='else'):
                    insertEdge(myGraph,body,destinationNode)
                else:
                    maxIndex+=1
                    insertEdge(myGraph,maxIndex,destinationNode)
                    insertEdge(myGraph,body,maxIndex)
                    while(myNode.char!='{'):
                        myNode=myNode.right
                    newNode=seekBlockClosure(myNode)
                    generateCfg(myGraph,maxIndex,exit,myNode,newNode)
                    myNode=newNode
                myList=myNode.right
                continue
        elif(myList.char=='while' or myList.char=='for'):
            while(myList.char!='{'):
                myList=myList.right
            myNode=seekBlockClosure(myList)
            maxIndex+=2
            copyEdges(myGraph,body,maxIndex)
            myGraph[body]=None
            insertEdge(myGraph,body,maxIndex-1)
            insertEdge(myGraph,maxIndex-1,body)
            insertEdge(myGraph,body,maxIndex)
            generateCfg(myGraph,maxIndex-1,maxIndex,myList,myNode)
            myList=myNode.right
            continue
        elif(myList.char=='do'):
            while(myList.char!='{'):
                myList=myList.right
            myNode=seekBlockClosure(myList)
            maxIndex+=2
            copyEdges(myGraph,body,maxIndex)
            myGraph[body]=None
            insertEdge(myGraph,body,maxIndex-1)
            insertEdge(myGraph,maxIndex-1,maxIndex)
            insertEdge(myGraph,maxIndex-1,body)
            generateCfg(myGraph,body,maxIndex,myList,myNode)
            while(myNode.char!='while'):
                myNode=myNode.right
            while(myNode.char!=')'):
                myNode=myNode.right
            myList=myNode.right
            continue
        elif(myList.char=='break'):
            insertEdge(myGraph,body,exit)
        myList=myList.right

def independentPaths(myGraph,edges,i,numVertices,mySequence):
    global maxIndex
    global destinationSequence
    numVertices=numVertices+1
    myNode=myGraph[i]
    tempSequence=mySequence+'->'+str(i)
    undiscoveredFlag=0
    while(myNode!=None):
        if(edges[i][myNode.index]==0):
            undiscoveredFlag=1
            edges[i][myNode.index]=1
            independentPaths(myGraph,edges,myNode.index,numVertices,tempSequence)
            edges[i][myNode.index]=0
        myNode=myNode.right
    if(undiscoveredFlag==0):
        destinationSequence=destinationSequence+'['+tempSequence[2:len(tempSequence)]+'],'
def initMatrix(n):
    arr=[[0 for i in range(n)]for j in range(n)]
    return(arr)        

def countNumEdges(myGraph):
    edges=0
    for i in range(len(myGraph)):
        myNode=myGraph[i]
        while(myNode!=None):
            edges+=1
            myNode=myNode.right
    return(edges)

myGraph=initGraph(1000)
myList=tokenize(characters)
generateCfg(myGraph,0,-1,myList.front,None)


myEdges=initMatrix(maxIndex+1)
mySequence=''
destinationSequence=''
independentPaths(myGraph,myEdges,0,0,mySequence)
print('Independent paths:')
print(destinationSequence[0:len(destinationSequence)-1])
cyclomaticComplexity=countNumEdges(myGraph)-(maxIndex+1)+2
outputString='Cyclomatic complexity='+str(cyclomaticComplexity)
print(outputString)


showGraph(myGraph)



