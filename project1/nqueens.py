#Global Variables
#   These could be local variables that we just pass to search(...)
q = []         # queen location array
n = 4          # number of board / size
t = [[0 for x in range(n)] for y in range(n)]        # n x n threat array
nsols = 0  # number of solutions found
debug = False # should output

def main():
  # start search on row/queen 0
  search(0) 
  if( nsols == 0):
    print("No sol!")
  return 0

def search(row):
  if(row == n):
    nsols+=1
    printSolution() # solved!
    return True
  else:
    # try every column and recurse
    for q[row] in range(n):
      # check that col: q[row] is safe
      if(t[row][q[row]] == 0):
        # if safe place and continue
        addToThreats(row, q[row], 1)

        if(debug):
          printEntry(row, q[row])

        # Recurse to next
        status = search(row+1)
        if status:
          return True 
        # if returned, remove placement
        addToThreats(row, q[row], -1)
  # Backtrack to previous row
  return False


def addToThreats(row, col, change):
  for j in range(row+1, n):
    # go down column
    t[j][col] += change
    # go down right diagonal
    if( col+(j-row) < n ):
       t[j][col+(j-row)] += change
    # go down left diagonal
    if( col-(j-row) >= 0):
       t[j][col-(j-row)] += change

def printSolution():
  print("\n\nSolution ", nsols, ": ")
  for i in range(n):
    for j in range(n):
      if(j == q[i]):
        print("Q")
      else:
        print("*")
    print()

def printEntry(r, c):
  for i in range(r):
    print("  ")
  print("Checked r,c = ", r, ",", c)


main()