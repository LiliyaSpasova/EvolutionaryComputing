import numpy
def generateMember(length):
    member=""
    for i in range(0, length):
        member+=str(numpy.random.randint(0,2))
    return member

def generateInitialPopulation(length, populationSize):
    population=[]
    for i in range(0,populationSize):
        population.append(generateMember(length))
    return population
