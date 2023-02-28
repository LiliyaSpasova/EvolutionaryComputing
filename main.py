import crossovers
import generateInitialPopulation
import numpy
import random
import fitnesses

length=6
populationSize=20
population=generateInitialPopulation.generateInitialPopulation(length,populationSize)
iterations=20

#test commit


# we say that counting ones i 0, trap func is 1 and, deceptive trap is 2

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
    return False
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

finalPop=iterate(1)
print(finalPop)




