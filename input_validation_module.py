#validation.py
def input_length():
    #Priming Input
    bolBadData=True
    while bolBadData==True:
        #input length
        try:
            decLength = float(input("Enter length or negative number to stop: "))
            bolBadData=False
            if decLength >= 0:
                if decLength < 1 or decLength > 100:
                    print('Invalid range of data')
                    bolBadData = True
        except:
            print("Must be numeric data. Please try again!")
    #end while
    return decLength

def input_width():
    #Input width
    bolBadData=True
    while bolBadData==True:
        try:
            decWidth = float(input("Enter width: "))
            bolBadData=False 
            if decWidth < 1 or decWidth >100:
                print("Invalid range of data")
                bolBadData = True   
        except:
            print("Must be numeric data. Please try again!")
    #end while 
    return decWidth