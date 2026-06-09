#ducos, bryan Hw00

strWorkersName=input("Enter worker's Name:")

fltHoursworked=float(input("Enter Hours worked: "))

fltPayRate=float(input("Enter Pay Rate: "))

fltGrossPay = (fltHoursworked * fltPayRate)

fltGrossPay = round(fltGrossPay,2)

print(strWorkersName, fltGrossPay)
