import csv
import unittest
import datetime
import random
import Bipartite


class Rule:
    Item = None
    Other = None
    Stringified = None

    def __init__(self, item, other, stringified):
        self.Item = item
        self.Other = other
        self.Stringified = stringified

    def __eq__(self, another):
        return hasattr(another, 'Item') and \
               hasattr(another, 'Other') and \
               self.Item == another.Item and \
               self.Other == another.Other

    def __hash__(self):
        return hash(self.Item) * 397 ^ hash(self.Other)

    def __str__(self):
        return self.Stringified


class GraphColoringTests(unittest.TestCase):
    def test(self):
        # loadtxt()
        states = loadData("gadget_big.csv")  # its a dictionary
        rules = buildRules(states)
        #print(len(rules))
        colors = ["R", "Y", "G", "B"]
        colorLookup = {}
        for color in colors:
            colorLookup[color[0]] = color
        geneset = list(colorLookup.keys())
        optimalValue = len(rules)
        startTime = datetime.datetime.now()
        fnDisplay = lambda candidate: display(candidate, startTime)
        fnGetFitness = lambda candidate: getFitness(candidate, rules)
        best = getBest(fnGetFitness, fnDisplay, len(states), optimalValue, geneset)
        self.assertEqual(best.Fitness, optimalValue)

        keys = sorted(states.keys())
        helper_dict = {}  # mine
        for index in range(len(states)):
            helper_dict[keys[index]] = colorLookup[best.Genes[index]]  # mine
            #print(keys[index] + " is " + colorLookup[best.Genes[index]])
            # preparation to call my algorithm
        end_dict = {}
        for state in states:
            buildList = []
            for neighbor in states[state]:
                if neighbor != "":
                    buildList.append(helper_dict[neighbor] + neighbor)
            end_dict[helper_dict[state] + state] = buildList
        #
        #
        #
        Bipartite.find_other_color_combinations(end_dict)  # call my algorithm


class Individual:
    Genes = None
    Fitness = None

    def __init__(self, genes, fitness):
        self.Genes = genes
        self.Fitness = fitness


def display(candidate, startTime):
    timeDiff = datetime.datetime.now() - startTime
    print("%s\t%i\t%s" % (''.join(map(str, candidate.Genes)), candidate.Fitness, str(timeDiff)))


def getFitness(candidate, rules):
    rulesThatPass = 0
    for rule in rules:
        if candidate[rule.Item] != candidate[rule.Other]:
            rulesThatPass += 1
    return rulesThatPass


def mutate(parent, geneSet, get_fitness):
    geneIndex = random.randint(0, len(geneSet) - 1);
    index = random.randint(0, len(parent.Genes) - 1)
    genes = list(parent.Genes)
    genes[index] = geneSet[geneIndex]
    childGenes = (''.join(genes))
    fitness = get_fitness(childGenes)
    return Individual(childGenes, fitness)


def generateParent(length, geneSet, get_fitness):
    genes = list("")
    for i in range(0, length):
        geneIndex = random.randint(0, len(geneSet) - 1);
        genes.append(geneSet[geneIndex])
    childGenes = (''.join(genes))
    fitness = get_fitness(childGenes)
    return Individual(childGenes, fitness)


def getBest(get_fitness, display, targetLen, optimalFitness, geneSet):
    random.seed()
    bestParent = generateParent(targetLen, geneSet, get_fitness)
    display(bestParent)

    while bestParent.Fitness < optimalFitness:
        parent = generateParent(targetLen, geneSet, get_fitness)
        attemptsSinceLastImprovement = 0
        while attemptsSinceLastImprovement < 128:
            child = mutate(parent, geneSet, get_fitness)
            if child.Fitness > parent.Fitness:
                parent = child
                attemptsSinceLastImprovement = 0
            attemptsSinceLastImprovement += 1

        if bestParent.Fitness < parent.Fitness:
            bestParent, parent = parent, bestParent
            display(bestParent)
    return bestParent


def loadData(localFileName):
    # expects: AA,BB;CC;DD where BB, CC and DD are the initial column values in other rows
    with open(localFileName, mode='r') as infile:
        reader = csv.reader(infile)
        mydict = {row[0]: row[1].split(';') for row in reader if row}
        return mydict


def buildLookup(items):
    itemToIndex = {}
    index = 0
    for key in sorted(items):
        itemToIndex[key] = index
        index += 1
    return itemToIndex


def buildRules(items):  # items : dict
    itemToIndex = buildLookup(items.keys())  # {key: number}
    rulesAdded = {}
    rules = []
    keys = sorted(list(items.keys()))  # list of all keys(vertices)

    for key in sorted(items.keys()):
        keyIndex = itemToIndex[key]
        adjacentKeys = items[key]
        for adjacentKey in adjacentKeys:
            if adjacentKey == '':
                continue
            adjacentIndex = itemToIndex[adjacentKey]
            temp = keyIndex
            if adjacentIndex < temp:  # I changed a line
                temp, adjacentIndex = adjacentIndex, temp
            ruleKey = keys[temp] + "->" + keys[adjacentIndex]
            rule = Rule(temp, adjacentIndex, ruleKey)
            if rule in rulesAdded:
                rulesAdded[rule] += 1
            else:
                rulesAdded[rule] = 1
                rules.append(rule)

    for k, v in rulesAdded.items():
        if v == 1:
            print("rule %s is not bidirectional" % k)

    return rules


colors = ["Orange", "Yellow", "Green", "Blue"]
colorLookup = {}

for color in colors:
    colorLookup[color[0]] = color
geneset = list(colorLookup.keys())




