import math
import numpy
import copy

# Get the list of vectors from the language model in a list called Vectors
# Vectors = [v_1, v_2, v_3, ..., v_n]
newVectors = []
for vector in originalVectors:
    for e in vector:
        e += 1
    w = vector[1:]
    newVectors.append(w)

# Then we want to search for a = (v_j + ... + v_k)/n such that the norm of a is minimized. Note that the "neutral" vectors is the vector of all 1s. 
# In other words, find a subgroup of vectors such that adding them all together gives you something that is close to zero as possible. 
    
# helper funtions
def subgroupSum(vectorList):
    sum = []
    for vector in vectorList:
        sum = numpy.add(sum, vector)
    return sum

def subgroupAverage(vectorList):
    sum = subgroupSum(vectorList)
    return numpy.divide(sum, len(vectorList))

# Greedy algorithm
copiedVectors = copy.deepcopy(newVectors)
def findSomeSubgroup(vector):
    subgroup = set(vector)
    n = numpy.linalg.norm(vector)
    for v in copiedVectors:
        if numpy.linalg.norm(numpy.add(subgroupAverage(subgroup), v)) < n:
            subgroup.add(v)
    return subgroup
    
# We want all subgroups, so we'll have a set of sets (to avoid duplicate subgroups)
allSubgroups = set()
for vector in newVectors:
    if len(findSomeSubgroup(vector)) > 1:
        allSubgroups.add(findSomeSubgroup(vector))

def seeSubgroups():
    print(allSubgroups)
    return

# Here is a function to exclude vectors
def exclude(vector):
    newSubgroups = set()
    for subgroup in allSubgroups:
        if vector not in subgroup:
            newSubgroups.add(subgroup)
    return















