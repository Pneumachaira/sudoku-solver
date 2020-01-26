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
def printSudoku(i):
    if bool(sudokuPuzzle[i]) == 1:
        print(sudokuPuzzle[i], end='')
    else:
        print(' ', end='')
    for x in range (1, 9):
        if bool(sudokuPuzzle[i+x]) == 1:
            print(sudokuPuzzle[i+x], end='')
        else:
            print(' ', end='')
        if (i + x + 1) % 3 == 0 and (i + x + 1) % 9 != 0:
            print('|', end='')
    print('')


#This function checks which column the cell is in, then isolates which grid
def findCol(i):
    x = i % 9
    x = x // 3
    return x
    
#This function checks which row the cell is in
def findRow(i):
    x = i // 27
    return x

#This function checks the column
def checkCol(i):
    x = i
    while (x >= 0): #Checks earlier list items (above)
        if sudokuPuzzle[x] != '':
            listCol[int(sudokuPuzzle[x])-1] = 1
        x = x - 9
    x = i
    while (x <= 80): #Checks later list items (below)
        if sudokuPuzzle[x] != '':
            listCol[int(sudokuPuzzle[x])-1] = 1
        x = x + 9

#This function checks the row
def checkRow(i):
    x = i
    y = 8
    while (y >= x % 9): #Checks to the left, the y keeps it from looping around
        if sudokuPuzzle[x] != '':
            listRow[int(sudokuPuzzle[x])-1] = 1
        y = x % 9
        x = x - 1
    x = i
    if (x % 9 == 0): #Keeps the next function from getting stuck on the left side
        x = x + 1 #We already hit the initial x with the last if statement, so adding one here is harmless
    while (x % 9 > 0):
        if sudokuPuzzle[x] != '':
            listRow[int(sudokuPuzzle[x])-1] = 1
        x = x + 1

#This function checks the block
def checkBlock(i): #First we set the boundaries
    for y in range(findCol(i) * 3 + findRow(i) * 27, findCol(i) * 3 + findRow(i) * 27 + 19, 9):
        if sudokuPuzzle[y] != '':
            listRow[int(sudokuPuzzle[y])-1] = 1
        if sudokuPuzzle[y+1] != '':
            listRow[int(sudokuPuzzle[y+1])-1] = 1
        if sudokuPuzzle[y+2] != '':
            listRow[int(sudokuPuzzle[y+2])-1] = 1

#This function combines the three lists into the listCheck list
#This function also actually inputs the number into sudokuPuzzle
def checkSole(i):
    for k in range (0, 9):
        if (listCol[k] == 1 or listRow[k] == 1 or listBox[k] == 1):
            listSole[k] = 1
    sumSole = 0
    for k in range (0, 9):
        sumSole = sumSole + listSole[k]
    if (sumSole == 8 and sudokuPuzzle[i] == ''):
        sudokuPuzzle[i] = str(listSole.index(0) + 1)
    for z in range (0, 9):
        listCol[z] = 0
        listRow[z] = 0
        listBox[z] = 0
        listSole[z] = 0
        
#Now for a function that checks for Unique Candidates in a column
def checkColUnique(i): #Where i is the column we're checking
    for k in range (1, 10): #Where k is the number of the candidate
        for z in range (0, 9):
            listUnique[z] = 1 #Reset the list        
        for m in range(0, 9): #Where m is the cell/row in question
            if sudokuPuzzle[(m * 9) + i] != '':
                listUnique[m] = 0
            openSpot = 1
            # i = 1, k = 9, m = 3
            for y in range(0, 9): #Here we check all values in the column
                if sudokuPuzzle[i + y * 9] == str(k):
                    openSpot = 0
                    break
            if (openSpot == 0):
                continue #If one of the numbers is k, we move to the next m
            #Check the rows!
            for x in range (0, 9): #Where x is the horizontal position in the row
                if (sudokuPuzzle[m * 9 + x] == str(k)):
                    listUnique[m] = 0 #The candidate cannot fit here
            #Check the blocks!
            for y in range (0, 3): #Where y is the vertical position in the block
                if sudokuPuzzle[(m // 3 * 27) + (i // 3 * 3) + (y * 9)] == str(k):
                    listUnique[m] = 0 #The candidate cannot fit here
                if sudokuPuzzle[(m // 3 * 27) + (i // 3 * 3) + (y * 9)+1] == str(k):
                    listUnique[m] = 0 #Or here
                if sudokuPuzzle[(m // 3 * 27) + (i // 3 * 3) + (y * 9)+2] == str(k):
                    listUnique[m] = 0 #Or here
        sumUnique = 0
        for z in range (0, 9): #Where z just goes through the list
            sumUnique = sumUnique + listUnique[z]
        if (sumUnique == 1 and openSpot == 1):
            sudokuPuzzle[(listUnique.index(1) * 9) + i] = str(k)
        for z in range (0, 9):
            listUnique[z] = 1 #Reset the list

#This function checks for Unique Candidates in a row
def checkRowUnique(i): #Where i is the row we're checking, 0-8
    for k in range(1, 10): #Where k is the number of the candidate
        for z in range (0, 9):
            listUnique[z] = 1 #Reset the list        
        for m in range(0, 9): #Where m is the cell/column in question
            openSpot = 1
            for x in range(0, 9): #Here we check all values in the row
                if sudokuPuzzle[i * 9 + x] == str(k):
                    openSpot = 0
                    break
            if (openSpot == 0):
                continue #If one of the numbers in the row is k, we move to next m
            if sudokuPuzzle[(i * 9) + m] != '':
                listUnique[m] = 0
            #Check the columns!
            for y in range(0, 9): #Where y is the vertical position in the column
                if (sudokuPuzzle[m + y * 9] == str(k)):
                    listUnique[m] = 0 #Candidate cannot fit in this cell
            #Check the blocks!
            for y in range(0, 3): #Where y is the vertical position in the block
                if sudokuPuzzle[(i // 3 * 27) + (m // 3 * 3) + (y * 9)] == str(k):
                    listUnique[m] = 0 #The candidate cannot fit here
                if sudokuPuzzle[(i // 3 * 27) + (m // 3 * 3) + (y * 9)+1] == str(k):
                    listUnique[m] = 0 #Or here
                if sudokuPuzzle[(i // 3 * 27) + (m // 3 * 3) + (y * 9)+2] == str(k):
                    listUnique[m] = 0 #Or here
        sumUnique = 0
        for z in range(0, 9): #Where z just goes through the list
            sumUnique = sumUnique + listUnique[z]
        if (sumUnique == 1 and openSpot == 1):
            sudokuPuzzle[listUnique.index(1) + i * 9] = str(k)
        for z in range (0, 9):
            listUnique[z] = 1 #Reset the list

#This function checks for Unique Candidates in a block
def checkBlockUnique(i): #Where i is the horizontal value of blocks we're checking, 0-2
    for j in range(0, 3): #Where j is the vertical value of block we're checking
        for k in range(1, 10): #Where k is the number of the candidate
            openSpot = 1
            for z in range (0, 9):
                listUnique[z] = 1 #Reset the list
            for m in range(0, 3): #This part knocks out already-populated cells
                if sudokuPuzzle[(j * 27) + (i * 3) + (m * 9)] != '':
                    listUnique[m * 3] = 0
                if sudokuPuzzle[(j * 27) + (i * 3) + (m * 9) + 1] != '':
                    listUnique[m * 3 + 1] = 0
                if sudokuPuzzle[(j * 27) + (i * 3) + (m * 9) + 2] != '':
                    listUnique[m * 3 + 2] = 0
            for m in range(0, 3): #Where m is the row of the cell in the block
                if sudokuPuzzle[(j * 27) + (i * 3) + (m * 9)] == str(k):
                    openSpot = 0
                    break
                if sudokuPuzzle[(j * 27) + (i * 3) + (m * 9) + 1] == str(k):
                    openSpot = 0
                    break
                if sudokuPuzzle[(j * 27) + (i * 3) + (m * 9) + 2] == str(k):
                    openSpot = 0
                    break
            if (openSpot == 0):
                continue
            #Check the columns!
            for y in range (0, 9): #Where y is the vertical value of the column
                if sudokuPuzzle[(i * 3) + (y * 9)] == str(k):
                    listUnique[0] = 0
                    listUnique[3] = 0
                    listUnique[6] = 0
                if sudokuPuzzle[(i * 3) + (y * 9) + 1] == str(k):
                    listUnique[1] = 0
                    listUnique[4] = 0
                    listUnique[7] = 0
                if sudokuPuzzle[(i * 3) + (y * 9) + 2] == str(k):
                    listUnique[2] = 0
                    listUnique[5] = 0
                    listUnique[8] = 0
            for x in range (0, 9): #Where x is the horizontal value of the row
                if sudokuPuzzle[(j * 27) + x] == str(k):
                    listUnique[0] = 0
                    listUnique[1] = 0
                    listUnique[2] = 0
                if sudokuPuzzle[(j * 27) + x + 9] == str(k):
                    listUnique[3] = 0
                    listUnique[4] = 0
                    listUnique[5] = 0
                if sudokuPuzzle[(j * 27) + x + 18] == str(k):
                    listUnique[6] = 0
                    listUnique[7] = 0
                    listUnique[8] = 0
            sumUnique = 0
            for z in range(0, 9): #Where z just goes through the list
                sumUnique = sumUnique + listUnique[z]
            if (sumUnique == 1 and openSpot == 1): #If only one spot can be found for m
                sudokuPuzzle[(j * 27) + (i * 3) + (9 * (listUnique.index(1) // 3)) + (listUnique.index(1) % 3)] = str(k)
            for z in range (0, 9):
                listUnique[z] = 1 #Reset the list

#This function determines the most influential spots (blocks with most openings), and then plugs numbers in.
#The Sudoku will be run through with the plugged-in number, and if it cannot be completed, we try another
def guess():
    for i in range(0, 81): #This part saves a backup of the Sudoku so that we can restore it if necessary
        sudokuBackup.append(sudokuPuzzle[i])
    #This part sees which block is most open
    guessFinal = 0
    for i in range(0, 3): #Horizontal value of 3x3 block
        for j in range(0, 3): #Vertical value of 3x3 block
            guessTemp = 0
            for m in range(0, 2): #Row of cells in block
                if sudokuPuzzle[(i * 3) + (j * 27) + (m * 9)] == '':
                    guessTemp = guessTemp + 1
                if sudokuPuzzle[(i * 3) + (j * 27) + (m * 9) + 1] == '':
                    guessTemp = guessTemp + 1
                if sudokuPuzzle[(i * 3) + (j * 27) + (m * 9) + 2] == '':
                    guessTemp = guessTemp + 1
            if guessTemp >= guessFinal:
                guessFinal = guessTemp
                guessX = i
                guessY = j
    #This part sees which cell is the most influential (has most vertical/horizontal empty neighbors)
    for m in range (0, 3): #Row of cell in block
        for n in range (0, 3): #Column of cell in block
            x = (guessX * 3) + (guessY * 27) + (m * 9) + n
            if sudokuPuzzle[x] == '': #Don't bother with cells already filled in
                #So first we gotta check the vertical
                while (x >= 0): #Checks earlier list items (above)
                    if sudokuPuzzle[x] == '':
                        listGuess[(m * 3) + n] += 1
                    x = x - 9
                x = (guessX * 3) + (guessY * 27) + (m * 9) + n
                x = x + 9
                while (x <= 80): #Checks later list items (below)
                    if sudokuPuzzle[x] == '':
                        listGuess[(m * 3) + n] += 1
                    x = x + 9
                #Now check the horizontal
                x = (guessX * 3) + (guessY * 27) + (m * 9) + n
                y = 8
                while (y >= x % 9): #Checks to the left, the y keeps it from looping around
                    if sudokuPuzzle[x] == '':
                        listGuess[(m * 3) + n] += 1
                    y = x % 9
                    x = x - 1
                x = (guessX * 3) + (guessY * 27) + (m * 9) + n
                x = x + 1
                while (x % 9 > 0): #Checks to the right
                    if sudokuPuzzle[x] == '':
                        listGuess[(m * 3) + n] += 1
                    x = x + 1
    #Now that we've got values for empty neighbors, we can see which one has the most
    guessTemp = 0
    for i in range(0, 8):
        if listGuess[i] > guessTemp:
            guessTemp = listGuess[i]
    guessFinal = listGuess.index(guessTemp) #We now have the index of the corresponding best cell
    #Now we plug in a number and see if we can get to the end
    for k in range(1, 10): #Where k is the plugged-in number
        for i in range(0, 81): #Here we reset the Sudoku to pre-guess state
            sudokuPuzzle[i] = sudokuBackup[i]
        sudokuPuzzle[(guessX * 3) + (guessY * 27) + (guessFinal // 3 * 9) + (guessFinal % 3)] = str(k)
        print('We\'ll put a ' + str(k) + ' in there.')
        for i in range(0, 81, 9):
            printSudoku(i)
        while True:
            for i in range(0, 81):
                sudokuOld[i] = sudokuPuzzle[i]

            input()
    
            print('checkSole Guess')
    
            for i in range(0, 81): #Sole Candidate search
                checkCol(i)
                checkRow(i)
                checkBlock(i)
                checkSole(i)
            if '' not in sudokuPuzzle: #This part checks to see if the puzzle is complete
                break
            
            for i in range(0, 81, 9): #Progress report
                printSudoku(i)

            input()
            print('checkColUnique Guess')

            for i in range(0, 9): #Unique Candidate search
                checkColUnique(i)
            if '' not in sudokuPuzzle: #This part checks to see if the puzzle is complete
                break
            
            for i in range(0, 81, 9): #Progress report
                printSudoku(i)

            input()
            print('checkRowUnique Guess')

            for i in range(0, 9):
                checkRowUnique(i)
            if '' not in sudokuPuzzle: #This part checks to see if the puzzle is complete
                break
            
            for i in range(0, 81, 9): #Progress report
                printSudoku(i)

            input()
            print('checkBlockUnique Guess')
        
            for i in range(0, 3):
                checkBlockUnique(i)
            if '' not in sudokuPuzzle: #This part checks to see if the puzzle is complete
                break
            
            for i in range(0, 81, 9): #Progress report
                printSudoku(i)

            if sudokuOld == sudokuPuzzle:
                print('Hrm.')
                print('Let\'s go back and try a different number!')
                break
        if '' not in sudokuPuzzle: #Gotta break out of the 1-10 guessing
            break

#MAIN FUNCTION
#MAIN FUNCTION
#MAIN FUNCTION
#MAIN FUNCTION
#MAIN FUNCTION
#MAIN FUNCTION
#MAIN FUNCTION
#MAIN FUNCTION


#First we need to input the Sudoku puzzle   
sudokuPuzzle = list()
sudokuOld = list()
sudokuBackup = list()
print('Please enter the values of the Sudoku puzzle one by one, row by row.')
print('For blank spots, hit "Enter" without entering a value.')
#while len(sudokuPuzzle) != 81:
 #   sudokuPuzzle.append(input())

#Below are pre-set Sudoku puzzles
#Easy:
#sudokuPuzzle = ['5', '', '', '', '', '', '', '', '8', '', '', '', '8', '2', '', '3', '', '', '6', '8', '2', '5', '', '', '', '', '', '', '1', '', '', '', '', '', '9', '', '', '', '', '4', '3', '8', '6', '', '1', '', '6', '5', '7', '', '', '8', '', '2', '7', '9', '', '2', '', '6', '', '', '4', '', '', '3', '1', '', '7', '', '', '', '8', '', '', '', '', '', '', '', '']
#Very Hard (mostly complete, was for guess() testing):
sudokuPuzzle = ['', '', '', '2', '4', '6', '1', '5', '7', '2', '7', '5', '8', '1', '3', '6', '9', '4', '4', '6', '1', '9', '7', '5', '2', '8', '3', '', '', '', '4', '', '', '8', '', '', '', '', '4', '6', '', '8', '7', '', '', '', '', '8', '3', '5', '', '4', '', '', '1', '9', '2', '5', '6', '4', '3', '7', '8', '', '', '6', '7', '3', '2', '9', '4', '1', '3', '4', '7', '1', '8', '9', '5', '6', '2']

for i in range(0, 81, 9):
    printSudoku(i)
print('Is this correct? If not, restart the program. Otherwise, hit Enter to start.')
input()
while True:
    if len(sudokuOld) != 81:
        for i in range(0, 81):
            sudokuOld.append(sudokuPuzzle[i])
    else:
        for i in range(0, 81):
            sudokuOld[i] = sudokuPuzzle[i]
    
    print('checkSole')
    
    for i in range(0, 81): #Sole Candidate search
        checkCol(i)
        checkRow(i)
        checkBlock(i)
        checkSole(i)
    if '' not in sudokuPuzzle: #This part checks to see if the puzzle is complete
        break
        
    for i in range(0, 81, 9): #Progress report
        printSudoku(i)

    input()
    print('checkColUnique')

    for i in range(0, 9): #Unique Candidate search
        checkColUnique(i)
    if '' not in sudokuPuzzle: #This part checks to see if the puzzle is complete
        break

    for i in range(0, 81, 9): #Progress report
        printSudoku(i)

    input()
    print('checkRowUnique')

    for i in range(0, 9):
        checkRowUnique(i)
    if '' not in sudokuPuzzle: #This part checks to see if the puzzle is complete
        break

    for i in range(0, 81, 9): #Progress report
        printSudoku(i)

    input()
    print('checkBlockUnique')
        
    for i in range(0, 3):
        checkBlockUnique(i)
    if '' not in sudokuPuzzle: #This part checks to see if the puzzle is complete
        break

    for i in range(0, 81, 9): #Progress report
        printSudoku(i)
        
    input()

    if sudokuOld == sudokuPuzzle:
        print('There is nothing more I can do for you.')
        print('Time to start guessing!')
        guess()

    if '' not in sudokuPuzzle: #This part checks to see if the puzzle is complete
        break

print('Success!!!!!!')
for z in range(0, 81, 9):
    printSudoku(z)
