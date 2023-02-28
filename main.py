import crossovers
import generateInitialPopulation
import numpy
import random
import fitnesses
import time

length=40
populationSize=40
isUniformCrossover=True
isTighlyLinked=False
fitness=0
iterations=20

# we say that counting ones i 0, trap func is 1 and, deceptive trap is 2

def areChildrenGettingBetter(sortedCompetition):
    minFitnessOfParents = 500000
    maxFitnessOfChildren = -1

    for (fitness,ischild,member) in sortedCompetition:
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
            competition.append((fitnesses.calcFitnessDeceptiveTrap(cont),isChild,cont,isTighlyLinked))
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

    found_res=False
    optimalSolution=""

    for i in range(0,length):
        optimalSolution+="1"
        
    l= len(optimalSolution)
    for candidate in population:
        if candidate==optimalSolution:
           found_res = True        

    return found_res

def iterate(isUniformCrossover,fitness,isTighlyLinked):
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
    for i in range(0,20):
        res=iterate(isUniformCrossover,fitness,isTighlyLinked)
        if res[0]:
            successes+=1
            allIterations+=res[1]
            fitnessEvals+=res[1]*populationSize*4
    t1 = time.time()
    totalTime = t1-t0  
    print("number of successes=",successes)
    print("average iterations=",allIterations/20)
    print("average fitness evaluations",fitnessEvals/20)
    print("total time",totalTime)
    return successes>=19
t0 = time.time()

main()
   





