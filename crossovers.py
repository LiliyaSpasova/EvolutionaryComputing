import numpy

#Correct occurs when at a position i parent1[i]!=parent2[i] and child1[i]==child2[i]==1
def countCorrect(firstParent,secondParent,firstChild,secondChild):
    correct=0

    length = len(firstParent)

    for (i) in range(length):
        a=firstParent[i]
        b=secondParent[i]
        if (a!=b):
            c=firstChild[i]
            d=secondChild[i]
            if (c==d) and (c=='1'):
                correct+=1
    return correct

#Error occurs when at a position i parent1[i]!=parent2[i] and child1[i]==child2[i]==0
def countErrors(firstParent,secondParent,firstChild,secondChild):
    errors=0
    length = len(firstParent)

    for (i) in range(length):
        a=firstParent[i]
        b=secondParent[i]
        if (a!=b):
            c=firstChild[i]
            d=secondChild[i]
            if (c==d) and (c=='0'):
                errors+=1
    return errors

def uniformCrossover(firstParent, secondParent, lenght):
    firstChild=""
    secondChild=""
    n_correct=0
    n_errors=0
    
    for i in range(0,lenght):
        val=numpy.random.uniform(0,1)
        if val>0.5:
           firstChild+=str(firstParent[i])
           secondChild+=str(secondParent[i])
        else:
           firstChild+=str(secondParent[i])
           secondChild+=(firstParent[i])
    n_correct+=countCorrect(firstParent,secondParent,firstChild,secondChild)
    n_errors=+countErrors(firstParent,secondParent,firstChild,secondChild)
    return (firstChild,secondChild,n_correct,n_errors)

def twoPointCrossover(firstParent, secondParent, length):
    n_correct=0
    n_errors=0
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
    n_correct+=countCorrect(firstParent,secondParent,firstChild,secondChild)
    n_errors+=countErrors(firstParent,secondParent,firstChild,secondChild)
    return (firstChild,secondChild,n_correct,n_errors)