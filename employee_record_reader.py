#ReadFile5Ev2

def main():
    with open('Names3v6.txt', 'r') as filename:
        #read first id
        strID = filename.readline()
        
        #initialize counter
        intRecordCount=0
        #print headings
        #print('ID    Name      Age')
        print(f"{'ID':6}{'Name':14}{'Age':3}")
        
        #read records until EOF
        while strID != "":
            #prepare dat for printint
            strID = strID.rstrip("\n")
            strName = filename.readline()
            strName = strName.rstrip("\n")
            strAge = filename.readline()
            strAge = strAge.rstrip("\n")
            
            #print fields
            print(f'{strID:6}{strName:13}{int(strAge):4}')
            
            #increment counter
            intRecordCount+=1
            
            #read next record
            strID = filename.readline()
            
        print()
        #display number of records read
        print(f"Names3v6.txt has {intRecordCount} records")    
        
# Call the main function.
if __name__ == '__main__':
    main()
