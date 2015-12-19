# 6.00.2x Problem Set 4

#
# PROBLEM 1


import numpy
import random
import pylab
from ps3b_precompiled_27 import *    


''' 
Begin helper code
'''

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """

'''
End helper code
'''

#
# PROBLEM 2
#

class SimpleVirus(object):

    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):
        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).
        """

        self.maxBirthProb=maxBirthProb
        self.clearProb=clearProb

    def getMaxBirthProb(self):
        """
        Returns the max birth probability.
        """
        return self.maxBirthProb

    def getClearProb(self):
        """
        Returns the clear probability.
        """
        return self.clearProb

    def doesClear(self):
        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step. 
        returns: True with probability self.getClearProb and otherwise returns
        False.
        """

        if random.random()<self.clearProb:
            return True
        else:
            return False

    
    def reproduce(self, popDensity):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient and
        TreatedPatient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).         

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.         
        
        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.               
        """

        if random.random()< self.maxBirthProb*(1-popDensity):
            self.child=SimpleVirus(self.maxBirthProb, self.clearProb)
            return self.child
        else:
            raise NoChildException()
            
class Patient(object):
    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """    

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the maximum virus population for this patient (an integer)
        """

        self.viruses=viruses
        self.maxPop=maxPop
        
    def getViruses(self):
        """
        Returns the viruses in this Patient.
        """
        return self.viruses


    def getMaxPop(self):
        """
        Returns the max population.
        """
        return self.maxPop


    def getTotalPop(self):
        """
        Gets the size of the current total virus population. 
        returns: The total virus population (an integer)
        """
        return len(self.viruses)   


    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:
        
        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.   
        
        - The current population density is calculated. This population density
          value is used until the next call to update() 
        
        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.                    

        returns: The total virus population at the end of the update (an
        integer)
        """
        tempviruses=[]    
        for i in range(len(self.viruses)):
            tempviruses.append(self.viruses[i])

        for i in range(len(self.viruses)):
            if self.viruses[i].doesClear():
                tempviruses.remove(self.viruses[i])
        
        self.viruses=tempviruses
        popDensity=self.getTotalPop()/self.maxPop
        
        for i in range(len(tempviruses)):
            try:
                babyvirus=self.viruses[i].reproduce(popDensity)
                self.viruses.append(babyvirus)
            except NoChildException:
                pass

        return len(self.viruses)

#
# PROBLEM 3
#
def simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb,
                          numTrials):
    """
    Run the simulation and plot the graph for problem 3 (no drugs are used,
    viruses do not have any drug resistance).    
    For each of numTrials trial, instantiates a patient, runs a simulation
    for 300 timesteps, and plots the average virus population size as a
    function of time.

    numViruses: number of SimpleVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: Maximum clearance probability (a float between 0-1)
    numTrials: number of simulation runs to execute (an integer)
    """

    #Generate a virus list of numViruses instances of SimpleViruses, 
    #each with maxBirthProb and clearProb
    singlevirus= SimpleVirus(maxBirthProb, clearProb)
    allviruses= [singlevirus] * numViruses
    
    # Generate a instance of patient
    patient= Patient(allviruses,maxPop)
    
    #Generate a list for average virus population size after a function of time 
    sumviruspop = [0] * 300
    
    #Iterate over number of trials
    for i in range(numTrials):
        #Get rid of the new viruses from last trials
        patient= Patient(allviruses,maxPop)
        #Update for patient over 300 time steps (first update is time 0)
        for j in range(300):
            #generate a sum of each element of virus population list with each trial
            sumviruspop[j]=sumviruspop[j]+patient.update()
    #Divide entire list over number of trials
    avgviruspop=[0]*300
    for j in range(300):
        avgviruspop[j]=sumviruspop[j]/float(numTrials)
       
    plot=pylab.plot(avgviruspop) 
    pylab.title('SimpleVirus simulation')
    pylab.xlabel('Time Steps')
    pylab.legend(plot)
    pylab.ylabel('Average Virus Population')
    pylab.show()
    
#simulationWithoutDrug(1, 10 , 1.0, 0.0, 1)

#
# PROBLEM 4
#

class ResistantVirus(SimpleVirus):
    """
    Representation of a virus which can have drug resistance.
    """   

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        """
        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)       

        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'srinol':False}, means that this virus
        particle is resistant to neither guttagonol nor srinol.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.
        """
        SimpleVirus.__init__(self, maxBirthProb, clearProb)
        self.resistances=resistances
        self.mutProb=mutProb
        
    def getResistances(self):
        """
        Returns the resistances for this virus.
        """
        return self.resistances

    def getMutProb(self):
        """
        Returns the mutation probability for this virus.
        """
        return self.mutProb

    def isResistantTo(self, drug):
        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in TreatedPatient to determine how many virus
        particles have resistance to a drug.       

        drug: The drug (a string)

        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        
        return self.resistances[drug]


    def reproduce(self, popDensity, activeDrugs):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the TreatedPatient class.

        A virus particle will only reproduce if it is resistant to ALL the drugs
        in the activeDrugs list. For example, if there are 2 drugs in the
        activeDrugs list, and the virus particle is resistant to 1 or no drugs,
        then it will NOT reproduce.

        Hence, if the virus is resistant to all drugs
        in activeDrugs, then the virus reproduces with probability:      

        self.maxBirthProb * (1 - popDensity).                       

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). The offspring virus
        will have the same maxBirthProb, clearProb, and mutProb as the parent.

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.       

        For example, if a virus particle is resistant to guttagonol but not
        srinol, and self.mutProb is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90%
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        srinol and a 90% chance that the offspring will not be resistant to
        srinol.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population       

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings).

        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
        """
        
        if len(activeDrugs)!=0:
            for i in range(len(activeDrugs)):
                if not self.isResistantTo(activeDrugs[i]):
                    raise NoChildException()
        
        if random.random()< self.maxBirthProb*(1-popDensity):
            child=ResistantVirus(self.maxBirthProb, self.clearProb, self.resistances, self.mutProb)
        
        if len(activeDrugs)==0:
            child=ResistantVirus(self.maxBirthProb, self.clearProb, self.resistances, self.mutProb)
            return child
        else: 
            for i in range(len(activeDrugs)):
                if self.isResistantTo(activeDrugs[i]):
                    if random.random()<self.mutProb:
                        child.resistances[i]=False
                    else:
                        child.resistances[i]=True
                else:
                    if random.random()<1-self.mutProb:
                        child.resistances[i]=False
                    else:
                        child.resistances[i]=True
                return child

class TreatedPatient(Patient):
    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).              

        viruses: The list representing the virus population (a list of
        virus instances)

        maxPop: The  maximum virus population for this patient (an integer)
        """

        Patient.__init__(self, viruses, maxPop)
        self.prescription=[]

    def addPrescription(self, newDrug):
        """
        Administer a drug to this patient. After a prescription is added, the
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: The list of drugs being administered to a patient is updated
        """

        if newDrug not in self.prescription:
            self.prescription.append(newDrug)


    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.

        returns: The list of drug names (strings) being administered to this
        patient.
        """

        return self.prescription


    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in
        drugResist.       

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'srinol'])

        returns: The population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        count=0
        for i in range(len(self.viruses)):
            j=0
            while j< len(drugResist):
                if self.viruses[i].isResistantTo(drugResist[j]):
                    j+=1
                else:
                    break
            if j==len(drugResist):
                count+=1
        
        return count
            
                    


    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:

        - Determine whether each virus particle survives and update the list of
          virus particles accordingly

        - The current population density is calculated. This population density
          value is used until the next call to update().

        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.
          The list of drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces.

        returns: The total virus population at the end of the update (an
        integer)
        """
        
        tempviruses=[]    
        for i in range(len(self.viruses)):
            tempviruses.append(self.viruses[i])
        
        for i in range(len(self.viruses)):
            if self.viruses[i].doesClear():
                tempviruses.remove(self.viruses[i])
        
        self.viruses=tempviruses

        density=len(self.viruses)/self.maxPop
        
        prodoviruses=[]
        
        for i in range(len(self.viruses)):
            j=0
            while j< len(self.prescription):
                if viruses[i].isResistantTo(self.prescription[j]):
                    j+=1
                else:
                    break
            if j==len(self.prescription):
                prodoviruses.append(self.viruses[i])
                
        for i in range(len(prodoviruses)):
            try:
                babyvirus=prodoviruses[i].reproduce(density, self.prescription)
                self.viruses.append(babyvirus)
            except NoChildException:
                pass

        return len(self.viruses)

#
# PROBLEM 5
#
def simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances,
                       mutProb, numTrials):
    """
    Runs simulations and plots graphs for problem 5.

    For each of numTrials trials, instantiates a patient, runs a simulation for
    150 timesteps, adds guttagonol, and runs the simulation for an additional
    150 timesteps.  At the end plots the average virus population size
    (for both the total virus population and the guttagonol-resistant virus
    population) as a function of time.

    numViruses: number of ResistantVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: maximum clearance probability (a float between 0-1)
    resistances: a dictionary of drugs that each ResistantVirus is resistant to
                 (e.g., {'guttagonol': False})
    mutProb: mutation probability for each ResistantVirus particle
             (a float between 0-1). 
    numTrials: number of simulation runs to execute (an integer)
    
    """
    #Generate a virus list of numViruses instances of SimpleViruses, 
    #each with maxBirthProb and clearProb
    singlevirus= ResistantVirus(maxBirthProb, clearProb, resistances, mutProb)
    allviruses= [singlevirus] * numViruses

    #Generate a list for average virus population size after a function of time 
    sumviruspop = [0] * 300
    resviruspop = [0] * 300
    
    #Iterate over number of trials
    for i in range(numTrials):
        #Get rid of the new viruses from last trials
        patient= TreatedPatient(allviruses,maxPop)
        #Update for patient over 300 time steps (first update is time 0)
        for j in range(150):
            #generate a sum of each element of virus population list with each trial
            patient.update()
            resistantpop=0
            for h in range(len(patient.viruses)):
                try:
                    if patient.viruses[h].resistances['guttagonol']==True:
                        resistantpop=resistantpop+1
                except KeyError:
                    pass
            resviruspop[j]=resviruspop[j]+resistantpop
        patient.addPrescription('guttagonol')
        for j in range(150,300):
            patient.update()
            resistantpop=0
        
    return patient.getTotalPop()

    #Divide entire list over number of trials
    avgviruspop=[0]*300
    avgresviruspop=[0]*300
    for j in range(300):
        avgviruspop[j]=sumviruspop[j]/float(numTrials)
        avgresviruspop[j]=resviruspop[j]/float(numTrials)
      
def simulationDelayedTreatment(numTrials):
    """
    Runs simulations and make histograms for problem 1.

    Runs numTrials simulations to show the relationship between delayed
    treatment and patient outcome using a histogram.

    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).

    numTrials: number of simulation runs to execute (an integer)
    """
    
    plot1=pylab.plot(avgviruspop) 
    pylab.title('ResistantVirus simulation')
    pylab.xlabel('time step')
    pylab.legend("virus population")
    pylab.ylabel('# viruses')
    pylab.show()
    
print simulationWithDrug(100, 1000, .1, 0.05, {'guttagonol': False}, .005, 5)





#
# PROBLEM 2
#
def simulationTwoDrugsDelayedTreatment(numTrials):
    """
    Runs simulations and make histograms for problem 2.

    Runs numTrials simulations to show the relationship between administration
    of multiple drugs and patient outcome.

    Histograms of final total virus populations are displayed for lag times of
    300, 150, 75, 0 timesteps between adding drugs (followed by an additional
    150 timesteps of simulation).

    numTrials: number of simulation runs to execute (an integer)
    """
    # TODO
