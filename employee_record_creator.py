#FileCreate5Ev2
#   ID     999
#   Name   x(12)
#   Age    99   (15-80)

def ValidateID():
     bad_data = True    
     intID=0
     while bad_data == True:
          try:
               #read id
               intID = int(input("Enter ID or negative value to stop: "))
               bad_data = False     
               if intID >= 0:     
                    if intID not in range(100,1000) :  #check for 100-999
                         #display error message
                         print("ID must be between 100 and 999")
                         bad_data=True 
                    #end if
               #end if
          except:
               print ("non-numeric data entered")  
               bad_data = True   
     #end while
     return intID     

def ValidateName():
     bad_data = True
     while bad_data == True:
          strName = input("Enter name: ")
          if strName != "" and len(strName) <= 12:      #check for missing name ("")
               bad_data = False
          else:
               print('Invalid Name')
     return(strName)

def ValidateAge():
     bad_data = True
     intAge=0
     while bad_data == True:
          try:
               #read age
               intAge = int(input("Enter age: "))
               bad_data = False
               if intAge not in range(15,81) :  #check for 15-80
                    #display error message
                    print("ID must be between 15 and 80")
                    bad_data = True
               #end if
          except:
               print ("non-numeric data entered")  
               bad_data = True 
     #end while
     return intAge   

previousID=0
intRecordCount=0
#Open file
with open('Names3v6.txt', 'w') as emp_file:
     intID = 0
     strName=""
     intAge=0
     intID=ValidateID()
     while intID >0:
          strName = ValidateName()
          intAge=ValidateAge()
          previousID=intID
          #write fields to file
          emp_file.write(str(intID) + "\n")
          emp_file.write(strName + "\n")
          emp_file.write(str(intAge) + "\n")
          #increment counter
          intRecordCount+=1
          #read next ID or -1
          intID=ValidateID()
          #check order of IDs being entered
          while intID <= previousID and intID >= 0 :
               print("Invalid ID, must be greater than",previousID)
               intID=ValidateID()
#Close file
print(f"Names3v6.txt has been created with {intRecordCount} record(s)")
    