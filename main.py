import crossovers
import generateInitialPopulation
import numpy
import random
import fitnesses
import time
import matplotlib.pyplot as plt
import pandas as pd

length=40
populationSize=200
isUniformCrossover=True
isTighlyLinked=True
fitness=0
dataForOnesPlot=[]
Iterations=20

dataForSchemataPlot=[]
hexadecimal_alphabets = '0123456789ABCDEF'
fitnessCalculations=[]
iterationsCount=[]
colors = ["#" + ''.join([random.choice(hexadecimal_alphabets) for _ in range(6)]) for _ in range(20)]
optimalSolution=""
for i in range(0,length):
    optimalSolution+="1"

n_correct=0
n_errors=0

# we say that counting ones i 0, trap func is 1 and, deceptive trap is 2
def countOnesInPopulation(population):
    res=0
    for p in population:
        res+=fitnesses.calcFitnessOnes(p)
    return res

def countMembersOfSchemata(population):
    res=0
    for p in population:
        if(p[0]=='1'):
            res+=1
    return res

def areChildrenGettingBetter(sortedCompetition):
    minFitnessOfParents = 500000
    maxFitnessOfChildren = -1

    for (fitness,ischild,_) in sortedCompetition:
        if fitness<=minFitnessOfParents and ischild==0:
            minFitnessOfParents=fitness
        
        if fitness>maxFitnessOfChildren and ischild==1:
            maxFitnessOfChildren=fitness

    return maxFitnessOfChildren>minFitnessOfParents

def getBestMembers (contendors, fitness,isTighlyLinked):
    # we make tuples with 3 elements and add them to a list (fitness,isChild,and the member itself)
    competition=[]
    for (cont,isChild) in contendors:
        if fitness==0:
            competition.append((fitnesses.calcFitnessOnes(cont),isChild,cont))
        elif fitness==1:
            competition.append((fitnesses.calcFitnessTrap(cont,isTighlyLinked),isChild,cont))
        elif fitness==2:
            competition.append((fitnesses.calcFitnessDeceptiveTrap(cont,isTighlyLinked),isChild,cont))
        # we sort it first based on fitness and then based on whether or not is a child, and then reutrn the firts two elements
    sortedCompetition = sorted(competition,reverse=True)
    areChildrenBetter=areChildrenGettingBetter(sortedCompetition)
    return  (sortedCompetition[0][2],sortedCompetition[1][2],areChildrenBetter)

def pickAncestors(firstParent,secondParent,length,isUniformCrossover,fitness,isTighlyLinked):
    contendors=[]
    if(isUniformCrossover):
        children=crossovers.uniformCrossover(firstParent,secondParent,length)
    else:
        children=crossovers.twoPointCrossover(firstParent,secondParent,length)
    contendors.append((firstParent,0))
    contendors.append((secondParent,0))
    contendors.append((children[0],1))
    contendors.append((children[1],1))

    global n_errors
    global n_correct

    n_correct+=children[2]
    n_errors+=children[3]

    return getBestMembers(contendors,fitness,isTighlyLinked)

def isSolutionFound(population):

    for candidate in population:
        if candidate==optimalSolution:
           return True        

    return False

def iterateWithPlots(isUniformCrossover,fitness,isTighlyLinked):    
    dataForOnesPlotX=[]
    dataForOnesPlotY=[]
    schemataDataX=[]
    schemataDataOne=[]
    schemataDataZero=[]
    population=generateInitialPopulation.generateInitialPopulation(length=length,populationSize=populationSize)
    counter=0
    countIterations=0
    while True:      
        random.shuffle(population)
        newPopulation=[]
        areBetterForGeneration=False
        for i in range (0,populationSize-1,2):
            areBetter=False
            ancestors=pickAncestors(population[i],population[i+1],length,isUniformCrossover,fitness,isTighlyLinked)
            newPopulation.append(ancestors[0])
            newPopulation.append(ancestors[1])
            areBetter=ancestors[2]
            if areBetter :
                areBetterForGeneration=True
        schemataDataX.append(countIterations)
        countMembersOfSchemataOne=countMembersOfSchemata(population)
        schemataDataOne.append(countMembersOfSchemataOne)
        schemataDataZero.append(populationSize-countMembersOfSchemataOne)
        dataForOnesPlotX.append(countIterations)
        dataForOnesPlotY.append(countOnesInPopulation(population)/(populationSize*length))
        population=newPopulation
        #TODO point 3
        if areBetterForGeneration:
            counter=0 
        else:
            counter+=1
        countIterations+=1
        if isSolutionFound(population):
            dataForOnesPlot.append((dataForOnesPlotX,dataForOnesPlotY))
            dataForSchemataPlot.append((schemataDataX,schemataDataZero,schemataDataOne))
            dataForOnesPlotX=[]
            dataForOnesPlotY=[]
            schemataDataX=[]
            schemataDataOne=[]
            schemataDataZero=[]
            return (True,countIterations)
        if counter==10:
            dataForOnesPlot.append((dataForOnesPlotX,dataForOnesPlotY))
            dataForSchemataPlot.append((schemataDataX,schemataDataZero,schemataDataOne))
            dataForOnesPlotX=[]
            dataForOnesPlotY=[] 
            schemataDataX=[]
            schemataDataOne=[]
            schemataDataZero=[]
            return (False,countIterations)
        
def iterateWithoutPlots(isUniformCrossover,fitness,isTighlyLinked):    
    population=generateInitialPopulation.generateInitialPopulation(length=length,populationSize=populationSize)
    counter=0
    countIterations=0
    while True:      
        random.shuffle(population)
        newPopulation=[]
        areBetterForGeneration=False
        for i in range (0,populationSize-1,2):
            areBetter=False
            ancestors=pickAncestors(population[i],population[i+1],length,isUniformCrossover,fitness,isTighlyLinked)
            newPopulation.append(ancestors[0])
            newPopulation.append(ancestors[1])
            areBetter=ancestors[2]
            if areBetter :
                areBetterForGeneration=True
        population=newPopulation
        if areBetterForGeneration:
            counter=0 
        else:
            counter+=1
        countIterations+=1
        if isSolutionFound(population):
            return (True,countIterations)
        if counter==10:
            return (False,countIterations)
        

def main ():
    successes=0
    allIterations=0
    fitnessEvals=0
    for i in range(0,Iterations):
        res=iterateWithoutPlots(isUniformCrossover,fitness,isTighlyLinked)
        if res[0]:
            successes+=1
        allIterations+=res[1]
        iterationsCount.append(res[1])
        fitnessEvals+=res[1]*populationSize*4
        fitnessCalculations.append(res[1]*populationSize*4)
    t1 = time.time()
    totalTime = t1-t0  
    print("number of successes=",successes)
    print("average iterations=",allIterations/20)
    print ("iterations count standard deviation=",numpy.std(iterationsCount))
    print("average fitness evaluations",fitnessEvals/20)
    print ("fitness evals count standard deviation=",numpy.std(fitnessCalculations))
    print("total time",totalTime)
    i=0
   
    fig, (ax1, ax2,ax3) = plt.subplots(1, 3)
    fig.suptitle('Plots')
    for (iteartions,ones,zeros) in dataForSchemataPlot:
        ax1.bar(iteartions, ones, width=0.3, color='red', align='edge')
        ax1.bar(iteartions, zeros, width=0.3, color='blue', align='center')
        break
    for (x,y) in dataForOnesPlot:
        ax2.plot(x,y,color=colors[i])
        ax3.plot(x,y,color=colors[i])
        i+=1
    plt.show()

    #test code
    print("correct = ", n_correct)
    print("errors = ", n_errors)

    return successes>=19
t0 = time.time()

main()
   





