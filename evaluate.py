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

#input = r"\int_{0}^{3}\prod_{k=1}^{7}\sin(kx) dx"
#input = r"2x+5\sin x +3=0"

#input = r"(3,4,5,6,7)"
#input = r"\int_{1}^{2} e^{-\sin x}"

def parseInp(st):
  st = regex.sub('(?<=(\w|[a-zA-Z]))(?=([a-zA-Z]))', '*', st, flags=regex.X)
  st = regex.sub('(?<=(\d|[(]))(?=[(])', '*', st)
  st = st.replace(")(",")*(")
  st = st.replace("^","**")
  return st

def errors(ty:int):
  if ty == 0:
    return r"Error 0: Unexpected error"
  elif ty == 1:
    return r"Error 1: Can not solve"
  elif ty == 2:
    return r"Error 2: Parsing error"
  elif ty == 3:
    return r"Error 3: Type error"
  elif ty == 4:
    return r"Error 4: Precision exhausted"
  
def get_median(k):
  if len(k) == 0:
    return errors(1)

  sorted_list = sorted(k)
  l_length = len(k)
  l_index = (l_length -1) // 2

  if l_length % 2:
    return sorted_list[l_index]
  else:
    return (sorted_list[l_index] + sorted_list[l_index + 1]) / 2

def isNumberClass(i):
  if i.atoms(Symbol) == set():
    return True
  else:
    return False

def sN(q,ans): #try to solve with N(q)
  try:
    return N(q)
  except:
    return ans

def mainSolve(lv,i=""):
  try:
    lv = regex.sub(r"((?<=\^)[^{\ ]{1})",r"{\1}",lv) #makes ^3x ^{3}x (fixes exponents probably)
    lv = regex.sub(r"((?<=\_)[^{\ ]{1})",r"{\1}",lv)

    if "," in lv:
      eq_list = [parse_latex(k).subs(defaultSubsDictionary) for k in lv.split(",")]
      eq = None
    else:
      eq = parse_latex(lv).subs(defaultSubsDictionary)
    intention = i
  except:
    return errors(2)
      
  def miniSolve(q):
    result = None

    if type(q)==type(Eq(symbols('x'),0)): #is an equation
      results = solve(q)
      if (intention == "decimal" or intention == "approx"):
        if type(results) == type([]):
          results = [N(k) for k in results]
      elif intention == "inverse":
        try:
          swap = q.subs({Symbol("x"):Symbol("y"),Symbol("y"):Symbol("x")}, simultaneous=True)
          results = solve(swap,Symbol('y'),dict=True)
        except:
          return errors(1)
      return results
    
    if type(q)==type([]): #intentions with multiple inputs
      if intention == "system":
        try:
          return solve(q,Symbol('x'),Symbol('y'),dict=True)
        except:
          return errors(1)
      elif intention == "solvefor":
        try:
          return solve(q[0],q[1],dict=True)
        except:
          return errors(1)
      elif intention == "count":
        return len(q)
      elif intention == "countif":
        return len([simplify(k) for k in q[:-1] if k == simplify(q[-1])])
      elif intention == "gcd":
        try:
          return gcd(*q)
        except:
          return errors(3)
      elif intention == "max":
        try:
          return max(q)
        except:
          return errors(3)
      elif intention == "min":
        try:
          return min(q)
        except:
          return errors(3)
      elif intention == "mean":
        return simplify(sum(q)/len(q))
      elif intention == "median":
        return get_median(q)
      elif intention == "mad":
        mean = simplify(sum(q)/len(q))
        deviation = [abs(k-mean) for k in q]
        return simplify(sum(deviation)/len(deviation))
      elif intention == "iqr":
        try:
          splitNum = Number(len(q) // 2)
          q = sorted(q)
          l1 = q[:splitNum]
          l2 = q[-splitNum:]
          return get_median(l2)-get_median(l1)
        except:
          return errors(3)

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
    elif intention == "erf":
      result = N(erf(q))
    elif intention == "isprime":
      result = isprime(q)
    elif intention == "isreal":
      try:
        result = q.is_real
      except:
        return errors(3)
    elif intention == "conj":
      result = conjugate(q) 
    elif intention == "imag":
      try:
        result = [re(q),im(q)]
      except:
        return errors(3)
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
      if type(result) != type([]):
        return simplify(result)
      else:
        return [simplify(k) for k in result]
    

  try:
    if eq == None:
      return miniSolve(eq_list)
    elif type(eq) == type([]):
      outputList = []
      for i in eq:
        outputList.append(miniSolve(i))
      distinctOutput = list(set(outputList))
      if len(distinctOutput) == 1:
        return distinctOutput[0]
      return distinctOutput
    else:
      return miniSolve(eq)
  except NotImplementedError:
    return errors(1)
  except PrecisionExhausted:
    return errors(4)
  except:
    return errors(0)
  