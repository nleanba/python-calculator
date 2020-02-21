import math, tty, sys, time
from copy import deepcopy
from decimal import Decimal
import re

class InputError(Exception):
  """Exception raised for errors in the input.

  Attributes:
      expression -- input expression in which the error occurred
      message -- explanation of the error
  """
  def __init__(self, expression, message):
    self.expression = expression
    self.message = message

  def __str__(self):
    return f'\x1b[31m{self.expression}: {self.message}\x1b[0m'

def _cclen(string):
  """Return printable length of string.

  Attributes:
      string -- string to be measured
  """
  sequence = re.compile(r"\x1b\[([0-9]|[:;<=>?])*[ !\"#$%&'()*+,\-./]*([A–Z]|[a-z]|[\\\]^_`{|}~])", re.IGNORECASE)
  string = sequence.sub('', string)
  count = 0
  escaped = False
  for char in string:
    if char == '\x1b': # escape
      escaped = True
    elif escaped:
      escaped = False
    elif not escaped:
      count += 1
  return count

operators = {
  '+': lambda x : x[-2] + x[-1],
  '-': lambda x : x[-2] - x[-1],
  '/': lambda x : x[-2] / x[-1],
  '*': lambda x : x[-2] * x[-1],
  '**': lambda x : x[-2] ** x[-1],
  '^': lambda x : x[-2] ** x[-1],
  'mod': lambda x : math.fmod(x[-2], x[-1]),
  '%': lambda x : math.fmod(x[-2], x[-1]),
  'log': lambda x : math.log(x[-2], x[-1]),
}
singleops = {
  'ceil': lambda x : math.ceil(x[-1]),
  'fabs': lambda x : math.fabs(x[-1]),
  'factorial': lambda x : math.factorial(x[-1]),
  '!': lambda x : math.factorial(x[-1]),
  'floor': lambda x : math.floor(x[-1]),
  'exp': lambda x : math.exp(x[-1]), # e^x
  'sqrt': lambda x : math.sqrt(x[-1]),
  'acos': lambda x : math.acos(x[-1]),
  'asin': lambda x : math.asin(x[-1]),
  'atan': lambda x : math.atan(x[-1]),
  'cos': lambda x : math.cos(x[-1]),
  'sin': lambda x : math.sin(x[-1]),
  'tan': lambda x : math.tan(x[-1]),
  'ln': lambda x : math.log(x[-1]),
  'round': lambda x : round(x[-1]),
}
consts = {
  __doc__: '''π τ e''',
  'pi': math.pi,
  'tau': math.tau,
  'e': math.e,
}
printconsts = {
  math.pi: f'\u001b[35;1mπ\x1b[0m ({str(math.pi)[:6] + "…"})',
  math.tau: f'\u001b[35;1mτ\x1b[0m ({str(math.tau)[:6] + "…"})',
  math.e: f'\u001b[35;1me\x1b[0m ({str(math.e)[:6] + "…"})',
}

flags = {
  'help': False,
}

helps = [
   "┢ x y operator (1 2 + -> 3)",
  f"┡ {' '.join(operators.keys())}",
   "┢ x operator (16 sqrt -> 4)",
  f"┡ {' '.join(singleops.keys())}",
   "┝ constants `pi` `tau` `e`"
]

def _mark (inp = ''):
  temp = inp.split()
  for i, t in enumerate(temp):
    if t in operators:
      temp[i] = '\x1b[34m' + t + '\x1b[0m'
    if t in singleops:
      temp[i] = '\x1b[36m' + t + '\x1b[0m'
    if t in consts:
      temp[i] = '\u001b[35;1m' + t + '\x1b[0m'
  return ' '.join(temp)

def _pr (stack = [], inp = '', index = 0, warning = ''):
  st = deepcopy(stack[-4:])
  for i, t in enumerate(st):
    if t in printconsts:
      st[i] = printconsts[t]
    elif isinstance(t, Decimal):
      st[i] = 'D: ' + str(t)

  if len(st) < 4:
    st = [''] * (4 - len(st)) + st

  if warning:
    st[-4] = warning

  shift = max(8, _cclen(str(st[0])), _cclen(str(st[1])), _cclen(str(st[2])), _cclen(str(st[3])), _cclen(inp))

  sys.stdout.write(u"\u001b[1000D")   # Move all the way left
  sys.stdout.write('\u001b[4A')       # Move 4 lines up

  for i in range(4):
    sys.stdout.write(u"\u001b[0K")    # Clear the line
    if flags['help']:
      sys.stdout.write('  ' + str(st[i]) + ' ' * (shift - _cclen(str(st[i]))) + helps[i] + '\n')
    else:
      sys.stdout.write('  ' + str(st[i]) + '\n')
    sys.stdout.write(u"\u001b[1000D") # Move all the way left again

  sys.stdout.write(u"\u001b[0K")      # Clear the line
  if flags['help']:
    sys.stdout.write('> ' + _mark(inp = inp) + ' ' * (shift - _cclen(_mark(inp = inp))) + helps[4])
  else:
    sys.stdout.write('> ' + _mark(inp = inp))
  sys.stdout.write(u"\u001b[1000D")   # Move all the way left again
  sys.stdout.write(u"\u001b[" + str(index + 2) + "C") # Move cursor to index

  sys.stdout.flush()

def main():
  tty.setraw(sys.stdin)
  sys.stdout.write('\n\n\n\n> ') # initial prompt
  stack = []
  history = []
  histindex = 0
  inp = ''
  index = 0
  warning = ''
  while True: # loop for each line
    # Define data-model for an input-string with a cursor
    inp = ''
    index = 0
    histindex = 0
    warning = ''
    while True: # loop for each character
      char = ord(sys.stdin.read(1)) # read one char and get char code
      if char == 3: # CTRL-C
        inp = ""
        index = 0
      if char == 4: # CTRL-D / EOF
        exit()
      elif 32 <= char <= 126: # Printablee
          inp = inp[:index] + chr(char).lower() + inp[index:]
          index += 1
      elif char in {10, 13}: # Enter
        try:
          stack, history = parse(stack = stack, inputs = inp, history = history)
        except InputError as w:
          warning = w
        inp = ""
        index = 0
        _pr(stack = stack, inp = inp, index = index, warning = warning)
        break
      elif char == 27: # ESC
          next1, next2 = ord(sys.stdin.read(1)), ord(sys.stdin.read(1))
          if next1 == 91:

            if next2 == 65: # Up
              if len(history) >= histindex:
                histindex = min(len(history), histindex + 1)
                if histindex != 0:
                  inp = str(history[-histindex]) 
              if len(history) == 1:
                inp = str(history[0])
              index = len(inp)

            elif next2 == 66: # Down
              if len(history) >= histindex:
                histindex = max(0, histindex - 1)
                if histindex == 0:
                  inp = ''
                else:
                  inp = str(history[-histindex])
                index = len(inp)
              elif len(history) == 0:
                inp = str(history[0])
              index = len(inp)

            elif next2 == 67: # Right
              index = min(len(inp), index + 1)
            elif next2 == 68: # Left
              index = max(0, index - 1)
      elif char == 127: # DEL
          inp = inp[:index-1] + inp[index:]
          index = max(0, index - 1)
      # Print current inp-string
      _pr(stack = stack, inp = inp, index = index, warning = warning)

def _calculate (stack = [], inp = ''):
  temp = []
  if inp == '':
    return stack
  elif len(stack) < 2 and (inp in operators):
    raise InputError(inp, 'not enough values in stack')
  elif inp in singleops:
    temp = stack[:-1] + [singleops[inp](stack)]
  elif inp in consts:
    temp = stack[:] + [consts[inp]]
  elif inp in operators:
    temp = stack[:-2] + [operators[inp](stack)]
  else:
    raise InputError(inp, 'operator or flag unknown')
  if isinstance(temp[-1], complex):
    raise InputError('i', 'Complex numbers not supported')
  return temp

def _parse (stack = [], inp = '', history = []):
  if inp == 'exit':
    exit()
  history.append(inp)
  try:
    #temp = Decimal(inp)
    temp = float(inp)
    if temp.is_integer():
      temp = int(inp)
    stack.append(temp)
  except ValueError:
    if inp in flags:
      flags[inp] = not flags[inp]
    elif inp in ['del', 'delete']:
      stack = stack[:-1]
    elif inp == 'clear':
      stack = []
    else:
      stack = _calculate(stack = stack, inp = inp)
      if stack:
        history.append(stack[-1])
  return stack, history

def parse (stack = [], inputs = '', history = []):
  for inp in inputs.split():
    stack,history = _parse(stack = stack, inp = inp, history = history)
  return stack, history

if __name__ == '__main__':
  main()
