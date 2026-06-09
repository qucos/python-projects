#BasketPlusCreate
#   Basket ID     9999  (1000-9999)
#   Description   x(25)
#   Unit Price    99.99 (5.95-75.95)
#   Quantity      999   (0-999)

def ValidateBasketID():
     bad_data = True
     intBasketID = 0
     while bad_data == True:
          try:
               #read basket id
               intBasketID = int(input("Enter Basket ID or negative value to stop: "))
               bad_data = False
               if intBasketID >= 0:
                    if intBasketID not in range(1000, 10000):  #check for 1000-9999
                         #display error message
                         print("Basket ID must be between 1000 and 9999")
                         bad_data = True
                    #end if
               #end if
          except:
               print("non-numeric data entered")
               bad_data = True
     #end while
     return intBasketID

def ValidateDescription():
     bad_data = True
     strDescription = ""
     while bad_data == True:
          strDescription = input("Enter Product Description: ")
          if strDescription != "" and len(strDescription) <= 25:  #check for missing and max 25
               bad_data = False
          else:
               print("Invalid Description - must be 1 to 25 characters")
          #end if
     #end while
     return strDescription

def ValidateUnitPrice():
     bad_data = True
     fltUnitPrice = 0.0
     while bad_data == True:
          try:
               #read unit price
               fltUnitPrice = float(input("Enter Unit Price: "))
               bad_data = False
               if fltUnitPrice < 5.95 or fltUnitPrice > 75.95:  #check for 5.95-75.95
                    #display error message
                    print("Unit Price must be between 5.95 and 75.95")
                    bad_data = True
               #end if
          except:
               print("non-numeric data entered")
               bad_data = True
     #end while
     return fltUnitPrice

def ValidateQuantity():
     bad_data = True
     intQuantity = 0
     while bad_data == True:
          try:
               #read quantity
               intQuantity = int(input("Enter Quantity: "))
               bad_data = False
               if intQuantity not in range(0, 1000):  #check for 0-999
                    #display error message
                    print("Quantity must be between 0 and 999")
                    bad_data = True
               #end if
          except:
               print("non-numeric data entered")
               bad_data = True
     #end while
     return intQuantity

intRecordCount = 0
#Open file
with open('baskets.txt', 'w') as basket_file:
     intBasketID = 0
     strDescription = ""
     fltUnitPrice = 0.0
     intQuantity = 0
     intBasketID = ValidateBasketID()
     while intBasketID > 0:
          strDescription = ValidateDescription()
          fltUnitPrice = ValidateUnitPrice()
          intQuantity = ValidateQuantity()
          #write fields to file
          basket_file.write(str(intBasketID) + "\n")
          basket_file.write(strDescription + "\n")
          basket_file.write(str(fltUnitPrice) + "\n")
          basket_file.write(str(intQuantity) + "\n")
          #increment counter
          intRecordCount += 1
          #read next basket id or negative
          intBasketID = ValidateBasketID()
     #end while
#Close file
print(f"baskets.txt has been created with {intRecordCount} record(s)")