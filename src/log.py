import inspect

def log(str):
  # Print the output, along with an indent that depends on
  # how deep the call stack was leading to this.
  print "{indent}{str}".format(indent = " " * (len(inspect.stack()) - 1),
                               str = str)
  