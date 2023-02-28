def countOnes(member):
    res=0
    for m in member:
        res+=int(m)
    return res

def calcFitnessOnes(member):
   return countOnes(member)

def calcFitnessTrap(member,k=4,d=1):
   calcTrapFunction(member,k,d)

def calcFitnessDeceptiveTrap(member,k=4,d=2.5):
   calcTrapFunction(member,k,d)

def calcTrapFunction(member,k,d):
    ones=countOnes(member)
    if ones==k:
        return k
    else:
        res = k- d - ((k-d)/(k-1))*ones
        return res