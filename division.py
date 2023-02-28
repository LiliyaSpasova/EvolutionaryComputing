def divideSequentially(member):
    couter=0
    divided=[]
    temp=""
    for i in member:
        temp+=i
        if couter==3:
            divided.append(temp)
            temp=""
            couter=-1
        couter+=1
    return divided
def divideNonSequtially(member):
    lenght=len(member)/4
    divided=[''] * int(lenght)
    counter=0
    for i in member:
        val=int(counter%lenght)
        divided[val]+=i
        counter+=1
    return divided