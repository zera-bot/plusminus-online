import re as regex
import sympy as s
from sympy import *
from sympy.parsing.latex import parse_latex

x = symbols("x")
defaultSubsDictionary = { Symbol('pi'): s.pi,
                          Symbol('tau'): Integer(2) * s.pi,
                          Symbol('e'): s.E,
                          Symbol('phi'): s.GoldenRatio,
                          Symbol('i'): s.I
                        }

def parseInp(st):
  st = regex.sub('(?<=(\w|[a-zA-Z]))(?=([a-zA-Z]))', '*', st, flags=regex.X)
  st = regex.sub('(?<=(\d|[(]))(?=[(])', '*', st)
  st = st.replace(")(",")*(")
  st = st.replace("^","**")
  #add exceptions for variables (dont add a times when there's a variable named "ab")
  return st

def asEq(st):
  l = regex.findall(r"=",st)
  if len(l) == 1:
    splitl = st.split("=")
    return Eq(parse_expr(splitl[0]),parse_expr(splitl[1]))
  else:
    print("error")

def isNumberClass(i):
  if i.atoms(Symbol) == set():
    return True
  else:
    return False

def sN(q,ans): #try to solve with N(q)
  print(q,ans)
  try:
    return N(q)
  except:
    return ans

def mainSolve(lv,i=""): #equation, latexversion
  lv = regex.sub(r"((?<=\^)[^{]{1})",r"{\1}",lv)
  lv = regex.sub(r"((?<=\_)[^{]{1})",r"{\1}",lv)
  eq = parse_latex(lv).subs(defaultSubsDictionary)
  intention = i
  def isExpression(q): #will upgrade soon
    if len(regex.findall(r"=",q)) == 0:
      return True
    else:
      return False
      
  def miniSolve(q):
    result = None

    if type(q)==type(Eq(symbols('x'),0)): #is an equation
      results = solve(q)
      if (intention == "decimal" or intention == "approx"):
        if type(results) == type([]):
          results = [N(k) for k in results]
      if results != simplify(q):
        return results

    if intention == "factor":
      result = factor(q)
    elif intention == "expand":
      result = expand(q)
    elif intention == "cancel":
      result = cancel(q)
    elif intention == "apart":
      result = apart(q)
    elif intention == "simplify":
      result = simplify(q)
    #elif intention == "inverse":
    #  result = inverse(q)
    elif intention == "decimal" or intention == "approx":
      result = N(q)
    else:
      result = q.doit()
      if result == simplify(q):
        if simplify(q).has(Integral):
          return sN(q,result)
        if simplify(q).has(Derivative):
          return sN(q,result)

    if result != None:
      return simplify(result)

  
  if type(eq) == type([]):
    outputList = []
    for i in eq:
      outputList.append(miniSolve(i))
    distinctOutput = list(set(outputList))
    if len(distinctOutput) == 1:
      return distinctOutput[0]
    return distinctOutput
      
  #parsedInput = parseInp(eq)
  #answer = latex(solve(asEq(parsedInput),x)))
  else:
    return miniSolve(eq)