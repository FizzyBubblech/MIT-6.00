# 6.00 Problem Set 8
# Denis Savenkov
# ps8.py


import numpy
import random
import pylab
from ps7 import *

#
# PROBLEM 1
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
        e.g. {'guttagonol':False, 'grimpex':False}, means that this virus
        particle is resistant to neither guttagonol nor grimpex.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.        
        """
        
        # MY CODE
        SimpleVirus.__init__(self, maxBirthProb, clearProb)
        self.resistances = resistances
        self.mutProb = mutProb 

    def isResistantTo(self, drug):

        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in Patient to determine how many virus
        particles have resistance to a drug.    

        drug: The drug (a string)
        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        
        # MY CODE
        assert drug in self.resistances.keys()
        return self.resistances[drug]

    def reproduce(self, popDensity, activeDrugs):

        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient class.

        If the virus particle is not resistant to any drug in activeDrugs,
        then it does not reproduce. Otherwise, the virus particle reproduces
        with probability:       
        
        self.maxBirthProb * (1 - popDensity).                       
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). 

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.        

        For example, if a virus particle is resistant to guttagonol but not
        grimpex, and `self.mutProb` is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90% 
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        grimpex and a 90% chance that the offspring will not be resistant to
        grimpex.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population        

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings). 
        
        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus  particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.         
        """
        
        # MY CODE
        for drug in activeDrugs:
            if not self.isResistantTo(drug):
                raise NoChildException()
   
        if random.random() < self.maxBirthProb * (1 - popDensity):
            childResistances = {}
            for drug in self.resistances.keys():
                if random.random() < self.mutProb:
                    childResistances[drug] = not self.resistances[drug]
                else:
                    childResistances[drug] = self.resistances[drug]
                    
            child = ResistantVirus(self.maxBirthProb, self.clearProb, childResistances,
                                   self.mutProb)
            return child
        else:
            raise NoChildException()

        
class Patient(SimplePatient):

    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).               

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)
        
        maxPop: the  maximum virus population for this patient (an integer)
        """
        
        # MY CODE
        SimplePatient.__init__(self, viruses, maxPop)
        self.drugs = []

    def addPrescription(self, newDrug):

        """
        Administer a drug to this patient. After a prescription is added, the 
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: list of drugs being administered to a patient is updated
        """
        
        # MY CODE
        # should not allow one drug being added to the list multiple times
        if newDrug not in self.drugs:
            self.drugs.append(newDrug)

    def getPrescriptions(self):

        """
        Returns the drugs that are being administered to this patient.
        returns: The list of drug names (strings) being administered to this
        patient.
        """
        
        # MY CODE
        return self.drugs
        

    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in 
        drugResist.        

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'grimpex'])

        returns: the population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        
        # MY CODE
        numResistantViruses = 0
        for virus in self.viruses:
            resistant = True
            for drug in drugResist:
                if not virus.isResistantTo(drug):
                    resistant = False
                    break
            if resistant:
                numResistantViruses += 1

        return numResistantViruses


    def update(self):

        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:
        
        - Determine whether each virus particle survives and update the list of 
          virus particles accordingly          
        - The current population density is calculated. This population density
          value is used until the next call to update().
        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient. 
          The listof drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces. 

        returns: the total virus population at the end of the update (an
        integer)
        """
        
        # MY CODE
        survivors = []
        for virus in self.viruses:
            if not virus.doesClear():
                survivors.append(virus)

        popDensity = len(survivors) / float(self.maxPop)
        reproduced = survivors[:]
        for virus in survivors:
            try:
                child = virus.reproduce(popDensity, self.drugs)
                reproduced.append(child)
            except NoChildException:
                pass

        self.viruses = reproduced[:]
        return self.getTotalPop()


#
# PROBLEM 2
#
def simulationWithDrug(numTrials):

    """
    Runs simulations and plots graphs for problem 2.
    
    For each of numTrials trials, instantiates a patient, runs a simulation for
    150 timesteps, adds guttagonol, and runs the simulation for an additional
    150 timesteps. At the end plots the average virus population size
    (for both the total virus population and the guttagonol-resistant virus
    population) as a function of time.

    numTrials: number of simulation runs to execute (an integer)
    """
    
    # MY CODE
    resultTotalPop = None
    resultResistantPop = None
    for i in range(numTrials):
        virusTotPop, virusResPop = runDrugSim(150)
        if resultTotalPop == None and resultResistantPop == None:
            resultTotalPop = virusTotPop
            resultResistantPop = virusResPop
        else:
            for j in range(len(resultTotalPop)):
                resultTotalPop[j] += virusTotPop[j]
                resultResistantPop[j] += virusResPop[j]

    for i in range(len(resultTotalPop)):
        resultTotalPop[i] /= float(numTrials)
        resultResistantPop[i] /= float(numTrials)
        
    pylab.plot(resultTotalPop, label = "Total virus pop")
    pylab.plot(resultResistantPop, label = "Resistant virus pop")
    pylab.title('Simulation with drug')
    pylab.xlabel('Time steps')
    pylab.ylabel('Popupalation of the virus')
    pylab.legend(loc = "best")
    pylab.show()
    
#MY CODE 
def runDrugSim(delay):

    """
    Helper function for doing one actual simulation run with drug applied

    delay: number of steps to simulate before prescripting drug (an integer)
    
    returns: a total and resistant virus population each step (a tuple) 
    """
    
    viruses = []
    for i in range(100):
        viruses.append(ResistantVirus(0.1, 0.05, {'guttagonol':False}, 0.005))
    patient = Patient(viruses, 1000)

    virusTotPop = []
    virusResPop = []
    for step in range(delay + 150):
        if step == delay - 1:
            patient.addPrescription('guttagonol')
        virusTotPop.append(patient.update())
        virusResPop.append(patient.getResistPop(['guttagonol']))

    return (virusTotPop, virusResPop)
    

#
# PROBLEM 3
#        
def simulationDelayedTreatment(numTrials):

    """
    Runs simulations and make histograms for problem 3.
    Runs multiple simulations to show the relationship between delayed treatment
    and patient outcome.
    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).

    numTrials: number of simulation runs to execute (an integer)
    """

    # MY CODE
    results = {}
    delays = [300, 150, 75, 0]
    for delay in delays:
        result = []
        for i in range(numTrials):
            virusTotPop, virusResPop = runDrugSim(delay)
            result.append(virusTotPop[-1])
        results[delay] = result
        
    numPlot = 1
    for delay in delays:
        pylab.subplot(2, 2, numPlot)
        pylab.title("delay: " + str(delay))
        pylab.xlabel("final virus counts")
        pylab.ylabel("# trials")
        pylab.hist(results[delay], bins = 12, range = (0, 600))
        numPlot += 1
    pylab.show()
#
# PROBLEM 4
#

def simulationTwoDrugsDelayedTreatment(numTrials):

    """
    Runs simulations and make histograms for problem 4.
    Runs multiple simulations to show the relationship between administration
    of multiple drugs and patient outcome.
   
    Histograms of final total virus populations are displayed for lag times of
    150, 75, 0 timesteps between adding drugs (followed by an additional 150
    timesteps of simulation).
    """

    # MY CODE
    results = {}
    delays = [300, 150, 75, 0]
    for delay in delays:
        result = []
        for i in range(numTrials):
            virusTotPop, b, c, d = runTwoDrugSim(delay)
            result.append(virusTotPop[-1])
        results[delay] = result
        
    numPlot = 1
    for delay in delays:
        pylab.subplot(2, 2, numPlot)
        pylab.title("delay: " + str(delay))
        pylab.xlabel("final virus counts")
        pylab.ylabel("# trials")
        pylab.hist(results[delay], bins = 12, range = (0, 600))
        numPlot += 1
    pylab.show()

# MY CODE
def runTwoDrugSim(delay):

    """
    Helper function for doing one actual simulation run with two drugs applied

    delay: number of steps to simulate before prescripting drug (an integer)
    
    returns: a total virus population and population resistant to 'grimpex',
    'guttagonol' and both drugs each step (a tuple) 
    """
    
    viruses = []
    for i in range(100):
        viruses.append(ResistantVirus(0.1, 0.05, {'guttagonol':False, 'grimpex':False},\
                                      0.005))
    patient = Patient(viruses, 1000)

    virusTotPop = []
    virusResPop = []
    virusGutPop = []
    virusGrimPop = []
    for step in range(150 + delay + 150):
        if step == 149:
            patient.addPrescription('guttagonol')
        if step == 149 + delay:
            patient.addPrescription('grimpex')
        virusTotPop.append(patient.update())
        virusGutPop.append(patient.getResistPop(['guttagonol']))
        virusGrimPop.append(patient.getResistPop(['grimpex']))
        virusResPop.append(patient.getResistPop(['guttagonol', 'grimpex']))

    return (virusTotPop, virusResPop, virusGutPop, virusGrimPop)


#
# PROBLEM 5
#    
def simulationTwoDrugsVirusPopulations(numTrials):
    
    """
    Run simulations and plot graphs examining the relationship between
    administration of multiple drugs and patient outcome.
    Plots of total and drug-resistant viruses vs. time are made for a
    simulation with a 300 time step delay between administering the 2 drugs and
    a simulations for which drugs are administered simultaneously.        
    """
    
    # MY CODE
    for sim in range(2):
        resultTotalPop = None
        resultResistantPop = None
        resultGuttagonolPop = None
        resultGrimpexPop = None
        for i in range(numTrials):
            if sim == 0:
                virusTotPop, virusResPop, virusGutPop, virusGrimPop = runTwoDrugSim(300)
            else:
                virusTotPop, virusResPop, virusGutPop, virusGrimPop = runSimultaneousSim()
            if resultTotalPop == None:
                resultTotalPop = virusTotPop
                resultResistantPop = virusResPop
                resultGuttagonolPop = virusGutPop
                resultGrimpexPop = virusGrimPop
            else:
                for j in range(len(resultTotalPop)):
                    resultTotalPop[j] += virusTotPop[j]
                    resultResistantPop[j] += virusResPop[j]
                    resultGuttagonolPop[j] += virusGutPop[j]
                    resultGrimpexPop[j] += virusGrimPop[j]
                    
        for i in range(len(resultTotalPop)):
            resultTotalPop[i] /= float(numTrials)
            resultResistantPop[i] /= float(numTrials)
            resultGuttagonolPop[i] /= float(numTrials)
            resultGrimpexPop[i] /= float(numTrials)

        pylab.figure(sim)
        pylab.plot(resultTotalPop, label = "Total virus pop")
        pylab.plot(resultResistantPop, label = "Resistant to both drugs pop")
        pylab.plot(resultGuttagonolPop, label = "Resistant to 'guttagonol' pop")
        pylab.plot(resultGrimpexPop, label = "Resistant to 'grimpex' pop")
        if sim == 0:
            pylab.title('Simulation with two drugs')
        else:
            pylab.title('Simulation with two drugs prescribed simultaniously')
        pylab.xlabel('Time steps')
        pylab.ylabel('Popupalation of the virus')
        pylab.legend(loc = "best")
             
    pylab.show()
                          
# MY CODE
def runSimultaneousSim():

    """
    Helper function for doing one actual simulation run with two drugs
    applied simultaniously
    
    returns: a total virus population and population resistant to 'grimpex',
    'guttagonol' and both drugs each step (a tuple) 
    """
    
    viruses = []
    for i in range(100):
        viruses.append(ResistantVirus(0.1, 0.05, {'guttagonol':False, 'grimpex':False},\
                                      0.005))
    patient = Patient(viruses, 1000)

    virusTotPop = []
    virusResPop = []
    virusGutPop = []
    virusGrimPop = []
    for step in range(300):
        if step == 149:
            patient.addPrescription('guttagonol')
            patient.addPrescription('grimpex')
        virusTotPop.append(patient.update())
        virusGutPop.append(patient.getResistPop(['guttagonol']))
        virusGrimPop.append(patient.getResistPop(['grimpex']))
        virusResPop.append(patient.getResistPop(['guttagonol', 'grimpex']))

    return (virusTotPop, virusResPop, virusGutPop, virusGrimPop)
    
                           

