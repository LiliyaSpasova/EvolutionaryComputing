import division
def countOnes(member):
    res=0
    for m in member:
        res+=int(m)
    return res

def calcFitnessOnes(member):
   return countOnes(member)

def calcFitnessTrap(member,isTightlyLinked,k=4,d=1):
    if isTightlyLinked:
       divided=division.divideSequentially(member)
    else:
       divided=division.divideNonSequtially(member)
    totalFitnes=calcTrapFunction(divided,k,d)
    return totalFitnes

def calcFitnessDeceptiveTrap(member,isTightlyLinked,k=4,d=2.5):
    if isTightlyLinked:
       divided=division.divideSequentially(member)
    else:
       divided=division.divideNonSequtially(member)
    totalFitnes=calcTrapFunction(divided,k,d)
    return totalFitnes

def calcTrapFunction(divided,k,d):
    result=0
    for div in divided:
        ones=countOnes(div)
        if ones==k:
            return k
        else:
            res = k- d - ((k-d)/(k-1))*ones
        result+=res
    return result
