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
Iterations=1

fitnessCalculations=[]
iterationsCount=[]

shouldPlot=True
dataForOnesPlot=[]
dataForSchemataPlot=[]
dataForSchemataOnesFitness=[]
dataForSchemataZerosFitness=[]
dataForCorrectDecisionsPlot=[]
hexadecimal_alphabets = '0123456789ABCDEF'
colorsHex = ["#" + ''.join([random.choice(hexadecimal_alphabets) for _ in range(6)]) for _ in range(20)]

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
    fitnessOnes=[]
    fitnessZeros=[]
    res=0
    for p in population:
        if(p[0]=='1'):
            res+=1
            fitnessOnes.append(fitnesses.calcFitnessOnes(p))
        else:
            fitnessZeros.append(fitnesses.calcFitnessOnes(p))
    
    return (res,fitnessOnes,fitnessZeros)

def areChildrenGettingBetter(sortedCompetition):
    minFitnessOfParents = 500000
    maxFitnessOfChildren = -1

    for (fitness,ischild,_) in sortedCompetition:
        if fitness<=minFitnessOfParents and ischild==0:
            minFitnessOfParents=fitness
        
        if fitness>maxFitnessOfChildren and ischild==1:
            maxFitnessOfChildren=fitness

    return maxFitnessOfChildren>minFitnessOfParents

def getDataForDecisionPlot(firsParent,secondParent,firstWinner,secondWinner):
    correct=0
    errors=0
    for (p1,p2,w1,w2) in zip (firsParent,secondParent,firstWinner,secondWinner):
        if p1!=p2:
            if w1=='0' and w2=='0': 
                errors+=1
            elif w1=='1' and w2=='1': 
                correct+=1
    return (correct,errors)

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

    dataForDecisionsX=[]
    dataForDecisionCorrect=[]
    dataForDecisionInCorrect=[]

    schemataOnesFitness=[]
    schemataOnesFitnessX=[]
    schemataOnesFitnessSD=[]

    schemataZerosFitness=[]
    schemataZerosFitnessX=[]
    schemataZerosFitnessSD=[]

    population=generateInitialPopulation.generateInitialPopulation(length=length,populationSize=populationSize)
    counter=0
    countIterations=0
    while True:      
        random.shuffle(population)
        newPopulation=[]
        areBetterForGeneration=False
        correct=0
        incorrect=0
        for i in range (0,populationSize-1,2):
            areBetter=False
            ancestors=pickAncestors(population[i],population[i+1],length,isUniformCrossover,fitness,isTighlyLinked)
            newPopulation.append(ancestors[0])
            newPopulation.append(ancestors[1])
            decisionData=getDataForDecisionPlot(population[i],population[i+1],ancestors[0],ancestors[1])
            correct+=decisionData[0]
            incorrect+=decisionData[1]
            areBetter=ancestors[2]
            if areBetter :
                areBetterForGeneration=True
        schemataData=countMembersOfSchemata(population)

        countMembersOfSchemataOne=schemataData[0]
        schemataDataX.append(countIterations)
        schemataDataOne.append(countMembersOfSchemataOne)
        schemataDataZero.append(populationSize-countMembersOfSchemataOne)
        
        fitnessOnes=schemataData[1]
        schemataOnesFitness.append(numpy.mean(fitnessOnes))
        schemataOnesFitnessSD.append(numpy.std(fitnessOnes))
        schemataOnesFitnessX.append(countIterations)

        fitnessZeros=schemataData[2]
        schemataZerosFitness.append(numpy.mean(fitnessZeros))
        schemataZerosFitnessSD.append(numpy.std(fitnessZeros))
        schemataZerosFitnessX.append(countIterations)

        dataForOnesPlotX.append(countIterations)
        dataForOnesPlotY.append(countOnesInPopulation(population)/(populationSize*length))

        dataForDecisionsX.append(countIterations)
        dataForDecisionCorrect.append(correct)
        dataForDecisionInCorrect.append(incorrect)

        population=newPopulation
        
        if areBetterForGeneration:
            counter=0 
        else:
            counter+=1
        countIterations+=1
        if isSolutionFound(population):
            dataForOnesPlot.append((dataForOnesPlotX,dataForOnesPlotY))
            dataForSchemataPlot.append((schemataDataX,schemataDataZero,schemataDataOne))
            dataForCorrectDecisionsPlot.append((dataForDecisionsX,dataForDecisionInCorrect,dataForDecisionCorrect))
            dataForSchemataOnesFitness.append((schemataOnesFitnessX,schemataOnesFitness,schemataOnesFitnessSD))
            dataForSchemataZerosFitness.append((schemataZerosFitnessX,schemataZerosFitness,schemataZerosFitnessSD))
            dataForOnesPlotX=[]
            dataForOnesPlotY=[]
            schemataDataX=[]
            schemataDataOne=[]
            schemataDataZero=[]
            dataForDecisionsX=[]
            dataForDecisionCorrect=[]
            dataForDecisionInCorrect=[]
            schemataOnesFitness=[]
            schemataOnesFitnessSD=[]
            schemataOnesFitnessX=[]
            schemataZerosFitness=[]
            schemataZerosFitnessSD=[]
            schemataZerosFitnessX=[]
            return (True,countIterations)
        if counter==10:
            dataForOnesPlot.append((dataForOnesPlotX,dataForOnesPlotY))
            dataForSchemataPlot.append((schemataDataX,schemataDataZero,schemataDataOne))
            dataForCorrectDecisionsPlot.append((dataForDecisionsX,dataForDecisionInCorrect,dataForDecisionCorrect))
            dataForSchemataOnesFitness.append((schemataOnesFitnessX,schemataOnesFitness,schemataOnesFitnessSD))
            dataForSchemataZerosFitness.append((schemataZerosFitnessX,schemataZerosFitness,schemataZerosFitnessSD))
            dataForOnesPlotX=[]
            dataForOnesPlotY=[] 
            schemataDataX=[]
            schemataDataOne=[]
            schemataDataZero=[]
            dataForDecisionsX=[]
            dataForDecisionCorrect=[]
            dataForDecisionInCorrect=[]
            schemataOnesFitness=[]
            schemataOnesFitnessSD=[]
            schemataOnesFitnessX=[]
            schemataZerosFitness=[]
            schemataZerosFitnessSD=[]
            schemataZerosFitnessX=[]
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
        if shouldPlot:
            res=iterateWithPlots(isUniformCrossover,fitness,isTighlyLinked)
        else:
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
    if shouldPlot:
        fig, axs = plt.subplots(2, 3)

        colors = {'zeroes':'red', 'ones':'blue'}         
        labels = list(colors.keys())
        handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in labels]
        axs[0, 0].set_title("Members of schematas")
        axs[0,0].legend(handles,labels)
        for (iteartions,ones,zeros) in dataForSchemataPlot:
            axs[0,0].bar(iteartions, ones, width=0.3, color='red', align='edge')
            axs[0,0].bar(iteartions, zeros, width=0.3, color='blue', align='center')
            break

        axs[0, 1].set_title("Fitness of 0 schemata")
        colors = {'mean':'red', 'sd':'blue'}         
        labels = list(colors.keys())
        handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in labels]
        axs[0,1].legend(handles,labels)
        for (iteartions,mean,sd) in dataForSchemataZerosFitness:
            axs[0,1].bar(iteartions, mean, width=0.3, color='red', align='edge')
            axs[0,1].bar(iteartions, sd, width=0.3, color='blue', align='center')
            break

        axs[0, 2].set_title("Fitness of 1 schemata")
        colors = {'mean':'red', 'sd':'blue'}         
        labels = list(colors.keys())
        handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in labels]
        axs[0,2].legend(handles,labels)
        for (iteartions,mean,sd) in dataForSchemataOnesFitness:
            axs[0,2].bar(iteartions, mean, width=0.3, color='red', align='edge')
            axs[0,2].bar(iteartions, sd, width=0.3, color='blue', align='center')
            break

        colors = {'correct':'blue', 'incorrect':'red'}         
        labels = list(colors.keys())
        handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in labels]
        axs[1, 1].set_title("Correct and incorrect decisions")
        axs[1, 1].legend(handles,labels)
        for (iteartions,incorrect,correct) in dataForCorrectDecisionsPlot:
            axs[1,1].bar(iteartions, correct, width=0.3, color='blue', align='edge')
            axs[1,1].bar(iteartions, incorrect, width=0.3, color='red', align='center')
            break

        axs[1, 0].set_title("Number of ones")
        for (x,y) in dataForOnesPlot:
            i=1
            axs[1,0].plot(x,y,color=colorsHex[i])
            i+=1
        plt.show()

    #test code
   # print("correct = ", n_correct)
   # print("errors = ", n_errors)

    return successes>=19
t0 = time.time()

main()
   





