import numpy

def countCorrect(firstParent,secondParent,firstChild,secondChild):
    result=0
    for (i,j,k,m) in zip(firstParent,secondParent,firstChild,secondChild):
        if (i==0 and j==1 ) or (i==1 and j==0):
            result +=1
    return result

def uniformCrossover(firstParent, secondParent, lenght):
    firstChild=""
    secondChild=""
    for i in range(0,lenght):
        val=numpy.random.uniform(0,1)
        if val>0.5:
           firstChild+=str(firstParent[i])
           secondChild+=str(secondParent[i])
        else:
           firstChild+=str(secondParent[i])
           secondChild+=(firstParent[i])
    countCorrect(firstParent,secondParent,firstChild,secondChild)
    return (firstChild,secondChild)

def twoPointCrossover(firstParent, secondParent, length):
    firstPoint = numpy.random.randint(0,length)
    secondPoint= numpy.random.randint(0,length+1)
    if firstPoint > secondPoint:
        temp=firstPoint
        firstPoint=secondPoint
        secondPoint=temp
    firstChild=""
    secondChild=""
    for i in range(0,firstPoint):
        firstChild+=(firstParent[i])
        secondChild+=(secondParent[i])
    for i in range(firstPoint,secondPoint):
        firstChild+=(secondParent[i])
        secondChild+=(firstParent[i])
    for i in range(secondPoint,length):
        firstChild+=(firstParent[i])
        secondChild+=(secondParent[i])
    countCorrect(firstParent,secondParent,firstChild,secondChild)
    return (firstChild,secondChild)