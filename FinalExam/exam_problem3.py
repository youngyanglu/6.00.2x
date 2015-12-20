import random
import pylab
import pdb
import numpy

# Global Variables
MAXRABBITPOP = 1000
CURRENTRABBITPOP = 500
CURRENTFOXPOP = 30

def rabbitGrowth():
    """ 
    rabbitGrowth is called once at the beginning of each time step.

    It makes use of the global variables: CURRENTRABBITPOP and MAXRABBITPOP.

    The global variable CURRENTRABBITPOP is modified by this procedure.

    For each rabbit, based on the probabilities in the problem set write-up, 
      a new rabbit may be born.
    Nothing is returned.
    """
    # you need this line for modifying global variables
    global CURRENTRABBITPOP

    prob=1- CURRENTRABBITPOP/float(MAXRABBITPOP)

    if CURRENTRABBITPOP<=MAXRABBITPOP:
        for i in range(CURRENTRABBITPOP):
            if random.random()<prob and CURRENTRABBITPOP<MAXRABBITPOP:
                CURRENTRABBITPOP=CURRENTRABBITPOP+1
            
def foxGrowth():
    """ 
    foxGrowth is called once at the end of each time step.

    It makes use of the global variables: CURRENTFOXPOP and CURRENTRABBITPOP,
        and both may be modified by this procedure.

    Each fox, based on the probabilities in the problem statement, may eat 
      one rabbit (but only if there are more than 10 rabbits).

    If it eats a rabbit, then with a 1/3 prob it gives birth to a new fox.

    If it does not eat a rabbit, then with a 1/10 prob it dies.

    Nothing is returned.
    """
    # you need these lines for modifying global variables
    global CURRENTRABBITPOP
    global CURRENTFOXPOP

    prob=CURRENTRABBITPOP/float(MAXRABBITPOP)

    if CURRENTRABBITPOP>10:
        for i in range(CURRENTFOXPOP):
            if random.random()<prob and CURRENTRABBITPOP>10:
                CURRENTRABBITPOP=CURRENTRABBITPOP-1
                if random.random()<1/3.0:
                    CURRENTFOXPOP=CURRENTFOXPOP+1
            else:
                if random.random()<9/10.0:
                    CURRENTFOXPOP=CURRENTFOXPOP-1

            
def runSimulation(numSteps):
    """
    Runs the simulation for `numSteps` time steps.

    Returns a tuple of two lists: (rabbit_populations, fox_populations)
      where rabbit_populations is a record of the rabbit population at the 
      END of each time step, and fox_populations is a record of the fox population
      at the END of each time step.

    Both lists should be `numSteps` items long.
    """

    global CURRENTRABBITPOP
    global CURRENTFOXPOP

    if CURRENTRABBITPOP<10:
        return None

    rabbit_populations=[]
    fox_populations=[]

    for i in range(numSteps):
        rabbitGrowth()
        foxGrowth()
        rabbit_populations.append(CURRENTRABBITPOP)
        fox_populations.append(CURRENTFOXPOP)

    return (rabbit_populations,fox_populations)

populations= runSimulation(200)
pylab.plot(populations[0],'r')
pylab.plot(populations[1],'b')
coeffrabbit = numpy.polyfit(range(len(populations[1])), populations[1], 2)
coefffox = numpy.polyfit(range(len(populations[0])), populations[0], 2)
pylab.plot(numpy.polyval(coeffrabbit, range(len(populations[0]))),"b")
pylab.plot(numpy.polyval(coefffox, range(len(populations[1]))),"g")
pylab.show()




