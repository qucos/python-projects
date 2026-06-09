#BasketPlusList

def main():
     with open('baskets.txt', 'r') as basket_file:
          #read first basket id
          strBasketID = basket_file.readline()

          #initialize counter and records list
          intRecordCount = 0
          lstRecords = []

          #read all records into list
          while strBasketID != "":
               #prepare data for storage
               strBasketID = strBasketID.rstrip("\n")
               strDescription = basket_file.readline()
               strDescription = strDescription.rstrip("\n")
               strUnitPrice = basket_file.readline()
               strUnitPrice = strUnitPrice.rstrip("\n")
               strQuantity = basket_file.readline()
               strQuantity = strQuantity.rstrip("\n")

               #store record as tuple
               lstRecords.append((int(strBasketID), strDescription,
                                   float(strUnitPrice), int(strQuantity)))

               #increment counter
               intRecordCount += 1

               #read next basket id
               strBasketID = basket_file.readline()
          #end while

     #sort records by Basket ID
     lstRecords.sort(key=lambda record: record[0])

     #print headings
     print(f"{'Basket Plus':^75}")
     print(f"{'Product Master List':^75}")
     print()

     #print stacked column headers
     print(f"{'':12}{'Product':<26}{'Unit':>12}{'':>10}{'Inventory':>15}")
     print(f"{'Basket ID':<12}{'Description':<26}{'Price':>12}{'Quantity':>10}{'Value':>15}")
     print("-" * 75)

     #initialize total
     fltTotalInventory = 0.0

     #print each record
     for record in lstRecords:
          intBasketID    = record[0]
          strDescription = record[1]
          fltUnitPrice   = record[2]
          intQuantity    = record[3]
          fltInvValue    = fltUnitPrice * intQuantity
          fltTotalInventory += fltInvValue
          print(f"{intBasketID:<12}{strDescription:<26}{fltUnitPrice:>12.2f}{intQuantity:>10}{fltInvValue:>15.2f}")
     #end for

     print("-" * 75)
     print(f"{'Total Inventory Value:':>48}{fltTotalInventory:>15.2f}")
     print()
     print(f"baskets.txt has {intRecordCount} record(s)")

# Call the main function
if __name__ == '__main__':
     main()
