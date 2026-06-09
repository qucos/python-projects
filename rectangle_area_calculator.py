#InputValidation_v2-4 
import validation

decTotalArea = 0.0
intRectangleCounter = 0



decLength =   validation.input_length()

#Main Line  do while number>= 0
while decLength >= 0:
    decWidth = validation.input_width()
    decArea = decLength * decWidth
    print (f"Area of the Rectangle: {decArea:,.2f}")
    intRectangleCounter += 1
    decTotalArea +=  decArea
    
    decLength = validation.input_length()
#print total
decAverageArea = decTotalArea / intRectangleCounter
print(f"Number of rectanlges entered: {intRectangleCounter}")
print(f"The average area is: {decAverageArea:,.2f}")