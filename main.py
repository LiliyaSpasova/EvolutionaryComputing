import crossovers
import generateInitialPopulation
import numpy
import random
import fitnesses

length=6
populationSize=20
iterations=20
isUniformCrossover=1
fitness=0

#test commit

# we say that counting ones i 0, trap func is 1 and, deceptive trap is 2

def areChildrenGettingBetter(sortedCompetition):
    maxFitnessOfParents = 0
    maxFitnessOfChildren = 0

    fitness_res=False

    for (fitness,ischild,member) in sortedCompetition:
        if fitness>maxFitnessOfParents and ischild==0:
            maxFitnessOfParents=fitness
        
        if fitness>maxFitnessOfChildren and ischild==1:
            maxFitnessOfChildren==fitness

    if maxFitnessOfChildren>maxFitnessOfParents:
        fitness_res=True

    return fitness_res

def getBestMembers (contendors, fitness):
    # we make tuples with 3 elements and add them to a list (fitness,isChild,and the member itself)
    competition=[]
    for (cont,isChild) in contendors:
        if fitness==0:
            competition.append((fitnesses.calcFitnessOnes(cont),isChild,cont))
        elif fitness==1:
            competition.append((fitnesses.calcFitnessTrap(cont),isChild,cont))
        elif fitness==2:
            competition.append((fitnesses.calcFitnessDeceptiveTrap(cont),isChild,cont))
        # we sort it first based on fitness and then based on whether or not is a child, and then reutrn the firts two elements
    sortedCompetition = sorted(competition,reverse=True)
    areChildrenGettingBetter(sortedCompetition)
    return  (sortedCompetition[0][2],sortedCompetition[1][2])

def pickAncestors(firstParent,secondParent,length,isUniformCrossover,fitness):
    contendors=[]
    if(isUniformCrossover):
        children=crossovers.uniformCrossover(firstParent,secondParent,length)
    else:
        children=crossovers.twoPointCrossover(firstParent,secondParent,length)
    contendors.append((firstParent,0))
    contendors.append((secondParent,0))
    contendors.append((children[0],1))
    contendors.append((children[1],1))
    return getBestMembers(contendors,fitness)

def isSolutionFound(population):

    found_res=False
    optimalSolution=""

    for i in length:
        optimalSolution+="1"

    for candidate in population:
        if candidate==optimalSolution:
           found_res = True        

    return found_res

def iterate(isUniformCrossover,fitness):
    population=generateInitialPopulation.generateInitialPopulation(length=length,populationSize=populationSize)
    counter=0
    for i in (0,iterations):
        random.shuffle(population)
        newPopulation=[]
        for i in range (0,populationSize-1,2):
            ancestors=pickAncestors(population[i],population[i+1],length,isUniformCrossover,fitness)
            newPopulation.append(ancestors[0])
            newPopulation.append(ancestors[1])
        population=newPopulation
        if isSolutionFound(population):
            return
        if counter==10:
            return
    return population

finalPop=iterate(isUniformCrossover,fitness)
print(finalPop)




