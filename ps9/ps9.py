# 6.00 Problem Set 9
# Intelligent Course Advisor
# Denis Savenkov
# ps9.py

SUBJECT_FILENAME = "subjects.txt"
SHORT_SUBJECT_FILENAME = "shortened_subjects.txt"
VALUE, WORK = 0, 1

#
# Problem 1: Building A Subject Dictionary
#
def loadSubjects(filename):
    """
    Returns a dictionary mapping subject name to (value, work), where the name
    is a string and the value and work are integers. The subject information is
    read from the file named by the string filename. Each line of the file
    contains a string of the form "name,value,work".

    returns: dictionary mapping subject name to (value, work)
    """

    # The following sample code reads lines from the specified file and prints
    # each one.
    #inputFile = open(filename)
    #for line in inputFile:
    #    print line

    # Instead of printing each line, modify the above to parse the name,
    # value, and work of each subject and create a dictionary mapping the name
    # to the (value, work).
    
    # MY CODE
    result = {}
    inputFile = open(filename)
    for line in inputFile:
        lineSplit = line.split(",")
        name, value, work = lineSplit[0], lineSplit[1], lineSplit[2] 
        result[name] = (int(value), int(work))
                
    return result

def printSubjects(subjects):
    """
    Prints a string containing name, value, and work of each subject in
    the dictionary of subjects and total value and work of all subjects
    """
    totalVal, totalWork = 0,0
    if len(subjects) == 0:
        return 'Empty SubjectList'
    res = 'Course\tValue\tWork\n======\t====\t=====\n'
    subNames = subjects.keys()
    subNames.sort()
    for s in subNames:
        val = subjects[s][VALUE]
        work = subjects[s][WORK]
        res = res + s + '\t' + str(val) + '\t' + str(work) + '\n'
        totalVal += val
        totalWork += work
    res = res + '\nTotal Value:\t' + str(totalVal) +'\n'
    res = res + 'Total Work:\t' + str(totalWork) + '\n'
    print res

#
# Problem 2: Subject Selection By Greedy Optimization
#

def cmpValue(subInfo1, subInfo2):
    """
    Returns True if value in (value, work) tuple subInfo1 is GREATER than
    value in (value, work) tuple in subInfo2
    """
    # MY CODE
    return subInfo1[VALUE] > subInfo2[VALUE]

def cmpWork(subInfo1, subInfo2):
    """
    Returns True if work in (value, work) tuple subInfo1 is LESS than than work
    in (value, work) tuple in subInfo2
    """
    # MY CODE
    return subInfo1[WORK] < subInfo2[WORK]

def cmpRatio(subInfo1, subInfo2):
    """
    Returns True if value/work in (value, work) tuple subInfo1 is 
    GREATER than value/work in (value, work) tuple in subInfo2
    """
    # MY CODE
    return (float(subInfo1[VALUE]) / subInfo1[WORK]) >\
           (float(subInfo2[VALUE]) / subInfo2[WORK])

# helper key functions for sorting
##########################################
def keyValue(subject):
    return subject[1][VALUE]

def keyWork(subject):
    return 1.0 / subject[1][WORK]

def keyRatio(subject):
    return float(subject[1][VALUE]) / subject[1][WORK]

def keySum(subject):
    return sum(subject[1])
##########################################

def greedyAdvisor(subjects, maxWork, comparator):
    """
    Returns a dictionary mapping subject name to (value, work) which includes
    subjects selected by the algorithm, such that the total work of subjects in
    the dictionary is not greater than maxWork.  The subjects are chosen using
    a greedy algorithm.  The subjects dictionary should not be mutated.

    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    comparator: function taking two tuples and returning a bool
    returns: dictionary mapping subject name to (value, work)
    """
    # MY CODE
    if comparator.__name__ == 'cmpValue':
        subjectsSorted = sorted(subjects.items(), key = keyValue, reverse = True)
    elif comparator.__name__ == 'cmpWork':
        subjectsSorted = sorted(subjects.items(), key = keyWork, reverse = True)
    elif comparator.__name__ == 'cmpRatio':
        subjectsSorted = sorted(subjects.items(), key = keyRatio, reverse = True)
    else:
        subjectsSorted = sorted(subjects.items(), key = keySum, reverse = True)
        
    result = {}
    totalWork = 0.0
    for subject in subjectsSorted:
        if (totalWork + subject[1][WORK]) <= maxWork:
            totalWork += subject[1][WORK]
            result[subject[0]] = subject[1]

    return result

#
# Problem 3: Subject Selection By Brute Force
#

# helper functions
def getBinaryRep(n, numDigits):
    """
    Assumes n and numDigits are non-negative ints.
    Returns a numDigits str that is a binary representation of n.
    """
    result = ''
    while n > 0:
        result = str(n%2) + result
        n = n//2
    if len(result) > numDigits:
        raise ValueError('not enough digits')
    for i in range(numDigits - len(result)):
        result = '0' + result
        
    return result

def genPowerset(L):
    """
    Assumes L is a list.
    Returns a list of lists that contains all possible combinations
    of the elements of L. E.g., if L is [1, 2] it will return a list
    with elements [], [1], [2], and [1,2].
    """
    powerset = []
    for i in range(0, 2**len(L)):
        binStr = getBinaryRep(i, len(L))
        subset = []
        for j in range(len(L)):
            if binStr[j] == '1':
                subset.append(L[j])
        powerset.append(subset)
        
    return powerset
# end helper functions

def bruteForceAdvisor(subjects, maxWork):
    """
    Returns a dictionary mapping subject name to (value, work), which
    represents the globally optimal selection of subjects using a brute force
    algorithm.

    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    returns: dictionary mapping subject name to (value, work)
    """
    # MY CODE
    pset = genPowerset(subjects.items())
    bestVal = 0.0
    bestSet = None
    for subs in pset:
        subsVal = 0.0
        subsWork = 0.0
        for subject in subs:
            subsVal += subject[1][VALUE]
            subsWork += subject[1][WORK]
        if subsWork <= maxWork and subsVal > bestVal:
            bestVal = subsVal
            bestSet = subs

    result = {}
    for subject in bestSet:
        result[subject[0]] = subject[1]

    return result

     



