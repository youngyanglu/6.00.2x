def noReplacementSimulation(numTrials):
    '''
    Runs numTrials trials of a Monte Carlo simulation
    of drawing 3 balls out of a bucket containing
    3 red and 3 green balls. Balls are not replaced once
    drawn. Returns the a decimal - the fraction of times 3 
    balls of the same color were drawn.
    '''
    
    import random
    success=0
    for i in range(numTrials):
        L=['R','R','R','G','G','G']
        choosen=[]
        for j in range(3):
            ball=random.choice(L)
            choosen.append(ball)
            L.remove(ball)
        if choosen==['R','R','R'] or choosen==['G','G','G']:
            success+= 1.0
    return success / numTrials 
    
print noReplacementSimulation(1000000)