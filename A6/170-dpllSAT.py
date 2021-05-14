# Implement David-Putnam algorithm for checking the satisfiability of a sentence represented in propositional logic

def findSymbols(clauses):
    symbols = {}
    for clause in clauses:
        for symbol in clause:
            if symbol[-1] not in symbols:
                symbols[symbol[-1]] = 1
    return symbols

def evaluateClause(clause, model):
    flag = 0
    count = 0
    for symbol in clause:
        if symbol[-1] in model:
            if symbol[0]=='!':
                val = not model[symbol[-1]]
            else:
                val = model[symbol[-1]] 
            flag = flag or val
            if flag == 1:
                return 1
            count+=1

    if count == len(clause):
        return 0
    return -1

def isAllTrue(clauses,model):
    for clause in clauses:
        value = evaluateClause(clause,model)
        if value == 0:
            return False
    return True


def isSomeFalse(clauses,model):
    for clause in clauses:
        value = evaluateClause(clause,model)
        if value == 0:
            return True
    return False


def find_pure_symbol(symbols,clauses,model):
    P = {}
    notP = {}

    for clause in clauses:
        for symbol in clause:
            if symbol[-1] in symbols:
                if symbol[0] == '!':
                    notP[symbol[-1]] = 1
                else:
                    P[symbol[-1]] = 1
    for p in P:
        if p not in notP:
            return p,True

    for p in notP:
        if p not in P:
            return p,False

    return None, None

def find_unit_clause(caluses,model):
    for clause in clauses:
        if len(clause) == 1:
            symbol = clause[0]
            if symbol[-1] not in model:
                if symbol[0] == '!':
                    return symbol[-1], False
                return symbol[-1], True
    return None, None

def First(symbols):
    for temp in symbols:
        return temp

def Rest(symbols):
    for temp in symbols:
        symbols.pop(temp)
        return symbols

def DPLL(clauses, symbols, model):
    if isAllTrue(clauses,model):
        return True
    if isSomeFalse(clauses,model):
        return False
    P, value = find_pure_symbol(symbols,clauses,model)
    if P:
        symbols.pop(P)
        model[P] = value
        print("pure")
        return DPLL(clauses,symbols,model)
    P, value = find_unit_clause(clauses,model)
    if P:
        symbols.pop(P)
        model[P] = value
        return DPLL(clauses,symbols,model)
    P = First(symbols)
    rest = Rest(symbols)
    m1 = model
    m2 = model
    m1[P] = True
    m2[P] = False
    return DPLL(clauses, rest,m1) or DPLL(clauses, rest,m2)



clauses = [['a' ,'b', 'c', 'd', 'e', 'f'],['a', 'c','!f'],['c'],['d'],['!a', '!b', '!c', '!d'],['!e', '!f']]
'''
n = int(input("Enter number of clauses : "))
for i in range(n):
    clause = list(input().split())
    clauses.append(clause)
'''
symbols = findSymbols(clauses)

model = {}
if DPLL(clauses,symbols,model):
    print("One satisfying assignment: ")
    for symbol in symbols:
        if symbol not in model:
            model[symbol] = 'False'
    for symbol in sorted(model.keys()):
        print(symbol,":",model[symbol])
else:
    print("No satisfying assignment assignment")

'''
One satisfying assignment: 
a : False
b : False
c : True
d : True
e : False
f : False
'''
