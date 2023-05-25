import js
import json
import pyodide_http

from js import console
from pyodide.ffi import create_proxy
from files.evaluate import mainSolve
from sympy.parsing.latex import parse_latex
from sympy.printing.latex import latex

pyodide_http.patch_all()

def reformatLatexExpression(l:str):
    l = l.replace(r'\operatorname{asin}',r'\sin^{-1}')
    l = l.replace(r'\operatorname{acos}',r'\cos^{-1}')
    l = l.replace(r'\operatorname{atan}',r'\tan^{-1}')
    l = l.replace(r'\operatorname{acot}',r'\cot^{-1}')
    l = l.replace(r'\operatorname{asec}',r'\sec^{-1}')
    l = l.replace(r'\operatorname{acsc}',r'\csc^{-1}')
    l = l.replace(r'\operatorname{asinh}',r'\sinh^{-1}')
    l = l.replace(r'\operatorname{acosh}',r'\cosh^{-1}')
    l = l.replace(r'\operatorname{atanh}',r'\tanh^{-1}')
    l = l.replace(r'\operatorname{acoth}',r'\coth^{-1}')
    return l

s = js.document.getElementById('evaluateButton')
def getEvaluate(event):
  v = Element('latex').innerHtml
  i = ""
  if r"\&" in v:
    v,i = v.split(r"\&")[0],v.split(r"\&")[1][4:]
    
  solution = mainSolve(v,i)
  latexFromSolution = latex(solution)
  Element('answer').write(f"$$ {reformatLatexExpression(latexFromSolution)} $$")
  js.renderMathInElement(js.document.body)

e = create_proxy(getEvaluate)
s.addEventListener("click",e)