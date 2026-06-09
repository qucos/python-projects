#ReadFile6B
#csv file processing

with open("Names4.csv", "r") as filename: 
    #read record
    csvRecord = filename.readline()
    record_count=0
    #Heading
    print('       Student')
    print('ID    Name      Age')
    
    while csvRecord != "":
        csvRecord = csvRecord.rstrip("\n")
        DataList = csvRecord.split(",")
        ID = DataList[0]
        Name = DataList[1]
        Age = int(DataList[2])
        print(f'{ID:5} {Name:6} {Age:6}')
        record_count+=1
        csvRecord = filename.readline()

print(f'Names4.csv contains {record_count} record(s)')
