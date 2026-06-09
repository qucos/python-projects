#FileCreate6
#CSV files

def InputValidateID():
     id=0
     bad_data = True
     while bad_data == True:
          try:
               #read id
               id = int(input("Enter ID or negative value to stop: "))
               bad_data = False     
               if id >= 0:     
                    if id not in range(100,1000) :  #check for 100-999
                         #display error message
                         print("ID must be between 100 and 999")
                         bad_data=True 
                    #end if
               #end if
          except ValueError:
               print ("non-numeric data entered")  
               bad_data = True   
     #end while
     return(id)

def InputValidateName():
     bad_data = True
     while bad_data == True:
          name = input("Enter name: ")
          if name != "":
               bad_data = False
     return(name)

def InputValidateAge():
     age=0
     bad_data = True
     while bad_data == True:
          try:
               #read age
               age = int(input("Enter age: "))
               bad_data = False
               if age not in range(15,81) :  #check for 15-80
                    #display error message
                    print("ID must be between 15 and 80")
                    bad_data = True
               #end if
          except ValueError:
               print ("non-numeric data entered")  
               bad_data = True 
     #end while
     return(age)

def main():
     #Open file
     filename = open("Names4.csv", "w")
    
     #build records
     record_count = 0
     id=InputValidateID()

     while id >= 0:
          name = InputValidateName()
          age = InputValidateAge()
        
          #write name to file
          csvRecord = str(id) + "," + name + "," + str(age) + "\n"
          filename.write(csvRecord)
          record_count += 1
          id = InputValidateID()
    
     #Close file
     filename.close
     print(f"Filename Names4.csv has been created with {record_count} record(s)")
    
if __name__ == "__main__":
    main()