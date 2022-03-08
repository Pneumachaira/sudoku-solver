#Welcome to the Sudoku Solver!
#You better be ready to give me that dollar, Graves.

#We'll need a handful of lists to check numbers by.
#Each list will be cleared after a check.
listCol = [0, 0, 0, 0, 0, 0, 0, 0, 0]
listRow = [0, 0, 0, 0, 0, 0, 0, 0, 0]
listBox = [0, 0, 0, 0, 0, 0, 0, 0, 0]
listSole = [0, 0, 0, 0, 0, 0, 0, 0, 0]
listUnique = [1, 1, 1, 1, 1, 1, 1, 1, 1]
listGuess = [0, 0, 0, 0, 0, 0, 0, 0, 0]

#This function prints out the Sudoku format to make sure user input was correct
#It also will print out the completed Sudoku at the end!
def printSudoku():
    for row in range (0, 9):
        for x in range (0, 9): #Where x goes down the row
            if bool(sudokuPuzzle[row * 9 + x]) == 1:
                print(sudokuPuzzle[row * 9 + x], end='')
            else:
                print(' ', end = '')
            if (x == 2 or x == 5):
                print('|', end = '')
        print('')


#This function checks which 3x3 block column the cell is in
def findCol(i): #Should return 0, 1, or 2
    x = i % 9
    x = x // 3
    return x
    
#This function checks which 3x3 block row the cell is in
def findRow(i): #Should return 0, 1, or 2
    x = i // 27
    return x

#This function checks the column
def checkCol(i):
    x = i - 9 #Starting at one above i
    while (x >= 0): #Checks earlier list items (above)
        if sudokuPuzzle[x] != '':
            listSole[int(sudokuPuzzle[x])-1] = 1
        x -= 9
    x = i + 9 #Starting at one below i
    while (x <= 80): #Checks later list items (below)
        if sudokuPuzzle[x] != '':
            listSole[int(sudokuPuzzle[x])-1] = 1
        x += 9

#This function checks the row
def checkRow(i):
    x = i
    y = 8
    while (y >= x % 9): #Checks to the left, the y keeps it from looping around
        if sudokuPuzzle[x] != '':
            listSole[int(sudokuPuzzle[x])-1] = 1
        y = x % 9
        x -= 1
    x = i + 1
    while (x % 9 > 0):
        if sudokuPuzzle[x] != '':
            listSole[int(sudokuPuzzle[x])-1] = 1
        x += 1

#This function checks the block
def checkBlock(i): #First we set the boundaries
    for y in range(findCol(i) * 3 + findRow(i) * 27, findCol(i) * 3 + findRow(i) * 27 + 19, 9): #Starts at upper-left cell of that particular 3x3 block, then increments by 9
        if sudokuPuzzle[y] != '':
            listSole[int(sudokuPuzzle[y])-1] = 1
        if sudokuPuzzle[y+1] != '':
            listSole[int(sudokuPuzzle[y+1])-1] = 1
        if sudokuPuzzle[y+2] != '':
            listSole[int(sudokuPuzzle[y+2])-1] = 1

#This function checks listSole for a unique 0 and inputs its index+1 into the Sudoku if found
def checkSole(cell): #Where i is the cell we're checking, 0-80
    checkCol(cell)
    checkRow(cell)
    checkBlock(cell)
    sumSole = 0 #Keeps track of how many 1s are in listSole
    for each in range (0, 9):
        sumSole = sumSole + listSole[each]
    if (sumSole == 8): #If there's only a single 0 in listSole
        sudokuPuzzle[cell] = str(listSole.index(0) + 1) #Grab its index+1 and put it in
    for each in range (0, 9): #Resets listSole
        listSole[each] = 0
        
#This function that checks for Unique Candidates in a column
#That is, does a number have only one possible place within the column for it to reside?
def checkColUnique():
    for col in range (0, 9): #Where col is the column we're checking, 0-8
        #So! For each number, 1-9, we go through the column.
        for num in range (1, 10): #Where num is the number of the candidate
            #First off, is the num candidate already in the column?
            alreadyHere = False
            for y in range (0, 9): #Here we check all values in the column
                if sudokuPuzzle[col + y * 9] == str(num): #If we already have our num in the column...
                    alreadyHere = True #There's no space for it!
                    break #Break out of the for y loop...
            if (alreadyHere):
                continue #And continue through the for num loop!
            #Assuming that's all good...
            for each in range (0, 9):
                listUnique[each] = 1 #Resets listUnique for each num
            #Now we look at each cell in the column to see if it's occupied
            for row in range (0, 9):
                #If occupied, we can't put another number there, so we change that index of listUnique to 0
                if sudokuPuzzle[(row * 9) + col] != '': #This spot already occupied
                    listUnique[row] = 0
                    continue #No need to check the other constraints
                #Check the rows! Is the number present in that row?
                for x in range (0, 9): #Start from the left and move right
                    if (sudokuPuzzle[row * 9 + x] == str(num)): #If the row already contains our num
                        listUnique[row] = 0 #The candidate cannot fit in this row
                        break #And we move on to the next row
            #Check the blocks!
            for vertBlock in range (0, 3): #Where vertBlock is the vertical position 0-2 of the 3x3 blocks
                alreadyHere = False #The num candidate hasn't been found in this block... yet...
                for y in range (0, 3): #Where y is the vertical value within the 3x3 block
                    #If we find the num candidate in a block, we get rid of three possible locations
                    for x in range (0, 3):
                        if (sudokuPuzzle[(vertBlock * 27) + (col // 3 * 3) + (y * 9) + x] == str(num)): #Starts at the top-left of a 3x3 block
                            for index in range (vertBlock * 3, vertBlock * 3 + 3):
                                listUnique[index] = 0
                            alreadyHere = True
                            break #Break out of the for x loop
                    if (alreadyHere): #If we find the num candidate within the 3x3 block, we can move onto the next block
                        break #Break out of the for y loop
            sumUnique = 0 #How many potential spots could the num candidate be in?
            for each in range (0, 9):
                sumUnique += listUnique[each]
            if (sumUnique == 1): #If there's only one potential spot, we've found it!
                sudokuPuzzle[(listUnique.index(1) * 9) + col] = str(num) #Put 'er there, pal

#This function checks for Unique Candidates in a row
#That is, does a number have only one possible place within the row for it to reside?
def checkRowUnique(): 
    for row in range (0, 9): #Where row is the row we're checking, 0-8
        #So! For each number, 1-9, we go through the row
        for num in range(1, 10): #Where num is the number of the candidate, 1-9
            #First, is the num candidate already in the row?
            alreadyHere = False
            for x in range (0, 9): #Here we check all values in the row
                if sudokuPuzzle[row * 9 + x] == str(num): #If the number already exists in the row
                    alreadyHere = True
                    break #Break out of the for x loop...
            if (alreadyHere):
                continue #Onto the next number!
            #Now that we know the num candidate isn't already in the row, let's do the rest of it!
            for each in range (0, 9):
                listUnique[each] = 1 #Resets listUnique for each num
            #Now we look at each cell in the row to see if it's occupied
            for col in range (0, 9):
                #If occupied, we can't put a number there
                if sudokuPuzzle[(row * 9) + col] != '':
                    listUnique[col] = 0
                    continue #No need to check the other constraints for this cell; it's already taken
                #Check the column each cell is in to see if the num candidate is present
                for y in range (0, 9): #Start from the top and move down
                    if (sudokuPuzzle[col + y * 9] == str(num)): #If the num candidate is present in that column...
                        listUnique[col] = 0 #It can't fit in that cell
                        break #Break out of the for y loop; onto the next column
            #Check the blocks!
            for horizBlock in range (0, 3): #Where horizBlock is the horizontal position 0-2 of the 3x3 blocks
                alreadyHere = False #The num candidate hasn't been found in this block... yet...
                for y in range (0, 3): #Where y is the vertical value within the 3x3 block
                    #If we find the num candidate in a block we get rid of three possible locations
                    for x in range (0, 3): #Where x is the horizontal value within the 3x3 block
                        if (sudokuPuzzle[(horizBlock * 3) + (row // 3 * 27) + (y * 9) + x] == str(num)): #Starts at the top-left of a 3x3 block
                            for index in range (horizBlock * 3, horizBlock * 3 + 3):
                                listUnique[index] = 0
                            alreadyHere = True
                            break #Break out of the for x loop
                        if (alreadyHere):
                            break #Break out of the for y loop
            sumUnique = 0 #How many potential spots could the num candidate be in?
            for each in range (0, 9):
                sumUnique += listUnique[each]
            if (sumUnique == 1): #If there's only one potential spot, we've found it!
                sudokuPuzzle[(row * 9) + listUnique.index(1)] = str(num) #Put 'er there, pal

#This function checks for Unique Candidates in a block
def checkBlockUnique():
    for horizBlock in range (0, 3): #Where horizBlock is the horizontal value of blocks we're checking, 0-2
        for vertBlock in range(0, 3): #Where vertBlock is the vertical value of the block we're checking, 0-2
            for num in range(1, 10): #Where num is the number of the candidate
                alreadyHere = False
                #First, check if the num candidate is in the 3x3 block already
                for y in range(0, 3): #Where y is the vertical value of the row in the 3x3 block
                    if sudokuPuzzle[(vertBlock * 27) + (horizBlock * 3) + (y * 9)] == str(num): #If the num candidate is present...
                        alreadyHere = True
                        break #We can break out of the for y loop
                    if sudokuPuzzle[(vertBlock * 27) + (horizBlock * 3) + (y * 9) + 1] == str(num):
                        alreadyHere = True
                        break
                    if sudokuPuzzle[(vertBlock * 27) + (horizBlock * 3) + (y * 9) + 2] == str(num):
                        alreadyHere = True
                        break
                if (alreadyHere): #If the num candidate's already here...
                    continue #We can move on to the next num candidate
                #Otherwise we'll continue looking for a unique possible location
                for each in range (0, 9):
                    listUnique[each] = 1 #Resets listUnique
                for y in range (0, 3): #Where y is the vertical value of the row in the 3x3 block
                    #This part looks at each row in the 3x3 blocks and knocks out already-populated cells
                    if sudokuPuzzle[(vertBlock * 27) + (horizBlock * 3) + (y * 9)] != '':
                        listUnique[y * 3] = 0
                    if sudokuPuzzle[(vertBlock * 27) + (horizBlock * 3) + (y * 9) + 1] != '':
                        listUnique[y * 3 + 1] = 0
                    if sudokuPuzzle[(vertBlock * 27) + (horizBlock * 3) + (y * 9) + 2] != '':
                        listUnique[y * 3 + 2] = 0
                #Check the columns!
                for y in range (0, 9): #Where y is the vertical value of the column
                    if sudokuPuzzle[(horizBlock * 3) + (y * 9)] == str(num):
                        listUnique[0] = 0
                        listUnique[3] = 0
                        listUnique[6] = 0
                    if sudokuPuzzle[(horizBlock * 3) + (y * 9) + 1] == str(num):
                        listUnique[1] = 0
                        listUnique[4] = 0
                        listUnique[7] = 0
                    if sudokuPuzzle[(horizBlock * 3) + (y * 9) + 2] == str(num):
                        listUnique[2] = 0
                        listUnique[5] = 0
                        listUnique[8] = 0
                for x in range (0, 9): #Where x is the horizontal value of the row
                    if sudokuPuzzle[(vertBlock * 27) + x] == str(num):
                        listUnique[0] = 0
                        listUnique[1] = 0
                        listUnique[2] = 0
                    if sudokuPuzzle[(vertBlock * 27) + x + 9] == str(num):
                        listUnique[3] = 0
                        listUnique[4] = 0
                        listUnique[5] = 0
                    if sudokuPuzzle[(vertBlock * 27) + x + 18] == str(num):
                        listUnique[6] = 0
                        listUnique[7] = 0
                        listUnique[8] = 0
                sumUnique = 0
                for each in range(0, 9): #Where each just goes through the list
                    sumUnique = sumUnique + listUnique[each]
                if (sumUnique == 1): #If only one spot can be found for m
                    sudokuPuzzle[(vertBlock * 27) + (horizBlock * 3) + (9 * (listUnique.index(1) // 3)) + (listUnique.index(1) % 3)] = str(num)

#This function determines the most influential spots (blocks with most openings), and then plugs numbers in.
#The Sudoku will be run through with the plugged-in number, and if it cannot be completed, we try another
def guess(cell): #Where cell is the starting point for looking for empty spots
    #First we make a copy of the puzzle thus far
    global sudokuPuzzle
    sudokuBackup = sudokuPuzzle.copy()
    #Then we find the first empty spot
    while (sudokuBackup[cell] != ''):
        cell += 1
    #Next we determine which numbers can fit in the spot
    possibleNumbers = list()
    for num in range (1, 10):
        alreadyHere = False
        #First let's check the row to see if the number is already there
        for x in range (0, 9): #Where x is the horizontal value within the row
            if (sudokuPuzzle[(cell // 9) * 9 + x] == str(num)):
                alreadyHere = True
                break #Break out of the for x loop
        if (alreadyHere):
            continue #Onto the next number
        #Now let's check the column to see if the number is already there
        for y in range (0, 9): #Where y is the vertical value within the column
            if (sudokuPuzzle[(cell % 9) + (y * 9)] == str(num)):
                alreadyHere = True
                break #Break out of the for y loop
        if (alreadyHere):
            continue #Onto the next number
        #Now we check the 3x3 block to see if the number is already there
        for y in range (0, 2): #Where y is the vertical value of the row in the 3x3 block
            for x in range (0, 2): #Where x is the vertical value of the row in the 3x3 block
                if (sudokuPuzzle[(findCol(cell) * 3) + (findRow(cell) * 27) + (y * 9) + x] == str(num)):
                    alreadyHere = True
                    break #Break out of the for x loop
            if (alreadyHere):
                break #Break out of the for y loop
        if (not alreadyHere): #If we get to the end and haven't found a number...
            possibleNumbers.append(num) #We add it to the list of possible numbers
    #Now that we have our list of possible numbers, we'll just go through them and see if it works
    for each in range (0, len(possibleNumbers)):
        input()
        print(possibleNumbers)
        print(f'Let\'s try to put {str(possibleNumbers[each])} in cell {str(cell)}!')
        sudokuPuzzle[cell] = str(possibleNumbers[each])
        printSudoku()
        while True: #Now we go through our main loop and see if we can get it to work!
            input()
            sudokuOld = sudokuPuzzle.copy()
            print('checkSole') #Sole Candidate search
            for i in range (0, 81):
                if (sudokuPuzzle[i] == ''):
                    checkSole(i)
            if '' not in sudokuPuzzle:
                break
            printSudoku() #Progress report
            
            input()
            print('checkColUnique')
            checkColUnique() #Unique Candidate search
            if '' not in sudokuPuzzle:
                break
            printSudoku() #Progress report

            input()
            print('checkRowUnique')
            checkRowUnique() #Unique Candidate search
            if '' not in sudokuPuzzle:
                break
            printSudoku() #Progress report

            input()
            print('checkBlockUnique')
            checkBlockUnique()
            if '' not in sudokuPuzzle:
                break
            printSudoku()

            input()
            if sudokuOld == sudokuPuzzle:
                print('Looks like a dead end. Let\'s try a different number or cell.')
                sudokuPuzzle = sudokuBackup.copy()
                break
        if '' not in sudokuPuzzle:
            break #Breaks out of for each in possibleNumbers loop
    if '' in sudokuPuzzle: #If we go through all of the possibleNumbers and the puzzle still isn't done...
        guess(cell + 1) #We guess again, except a different cell

##########################################################
#MAIN FUNCTION
#MAIN FUNCTION
#MAIN FUNCTION
##########################################################

#First we need to input the Sudoku puzzle   
sudokuPuzzle = list()
print('Please enter the values of the Sudoku puzzle one by one, row by row.')
print('For blank spots, hit "Enter" without entering a value.')

#Below are pre-set Sudoku puzzles
#Easy:
# sudokuPuzzle = ['5', '', '', '', '', '', '', '', '8', '', '', '', '8', '2', '', '3', '', '', '6', '8', '2', '5', '', '', '', '', '', '', '1', '', '', '', '', '', '9', '', '', '', '', '4', '3', '8', '6', '', '1', '', '6', '5', '7', '', '', '8', '', '2', '7', '9', '', '2', '', '6', '', '', '4', '', '', '3', '1', '', '7', '', '', '', '8', '', '', '', '', '', '', '', '']
#Very Hard (mostly complete, is for guess() testing):
# sudokuPuzzle = ['', '', '', '2', '4', '6', '1', '5', '7', '2', '7', '5', '8', '1', '3', '6', '9', '4', '4', '6', '1', '9', '7', '5', '2', '8', '3', '', '', '', '4', '', '', '8', '', '', '', '', '4', '6', '', '8', '7', '', '', '', '', '8', '3', '5', '', '4', '', '', '1', '9', '2', '5', '6', '4', '3', '7', '8', '', '', '6', '7', '3', '2', '9', '4', '1', '3', '4', '7', '1', '8', '9', '5', '6', '2']

while len(sudokuPuzzle) != 81:
    sudokuPuzzle.append(input())

printSudoku()
print('Is this correct? If not, restart the program. Otherwise, hit Enter to start.')
input()

while True: #Main loop starts here
    sudokuOld = sudokuPuzzle.copy() #We save a copy of the puzzle each loop so we can see if anything changes
    
    print('checkSole') #Sole Candidate search
    for i in range (0, 81): #Checks each cell if neighbors (vertical, horizontal, block) contain all but one value
        if (sudokuPuzzle[i] == ''): #Only need to check if it's empty
            checkSole(i)
    if '' not in sudokuPuzzle: #This part checks to see if the puzzle is complete
        break
        
    printSudoku() #Progress report

    input()
    print('checkColUnique')
    checkColUnique() #Unique Candidate search
    if '' not in sudokuPuzzle: #This part checks to see if the puzzle is complete
        break

    printSudoku() #Progress report

    input()
    print('checkRowUnique')
    checkRowUnique() #Unique Candidate search
    if '' not in sudokuPuzzle: #This part checks to see if the puzzle is complete
        break

    printSudoku() #Progress report

    input()
    print('checkBlockUnique')
        
    checkBlockUnique()
    if '' not in sudokuPuzzle: #This part checks to see if the puzzle is complete
        break

    printSudoku() #Progress report
        
    input()

    if sudokuOld == sudokuPuzzle:
        print('There is nothing more I can do for you.')
        print('Time to start guessing!')
        guess(0)

    if '' not in sudokuPuzzle: #This part checks to see if the puzzle is complete
        break

print('Success!!!!!!')
printSudoku()