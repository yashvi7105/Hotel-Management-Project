from datetime import date # importing the date module
from datetime import datetime #importing the datetime module
import pandas as pd  # importing the pandas library
from pandas import DataFrame   # importing DataFrame module from pandas library

df = pd.read_csv('Occupancy.csv') #df variable to read the csv file 'Occupancy.csv'

#Creating a hotel class
class Hotel:

    def __init__(self): # init method
        self.rooms = {} # dictionary to store the data of the guest occupying the room
        self.avlbl_rooms = {'std':[101,102,103,104], 'deluxe':[201,202,203,204],'ps':[301,302,303,304]}  # dictionary of available rooms
        self.roomprice = {1:1000, 2:2000, 3:4000}  # dictionary to store the prices of the respective rooms where 1, 2 and 3 are 'standard', 'deluxe' and 'presedential suite' roomtypes respectively
        
        try:
            self.guest_df = pd.read_csv('guest_details.csv')
        except FileNotFoundError:    #to create the columns of guest details in 'guest_details.csv' file
            self.guest_df = pd.DataFrame(columns=['Name', 'Address', 'Phone', 'CheckInDate', 'Roomservice', 'RoomNo', 'RoomType'])
        
        self.load_rooms_from_csv()


    def load_rooms_from_csv(self):
            for index, row in self.guest_df.iterrows():
                room_no = row['RoomNo']
                self.rooms[room_no] = {
                    'name': row['Name'],
                    'address': row['Address'],
                    'phone': row['Phone'],
                    'check_in_date': row['CheckInDate'],
                    'roomservice': row['Roomservice'],
                    'roomtype': row['RoomType']
                }  #load method to extract all the guest details from the csv file and append it to the 'self.rooms' dictionary


    def check_in(self,name,address,phone):
        df = pd.read_csv('Occupancy.csv')

        print("Room Types: \n1. Standard\n2. Deluxe\n3. Presedential Suite\n")
        roomtype = int(input("Please select the desired type of room: "))

        if roomtype==1:
            for i in range(0,4):
                if df.loc[i, 'Occupancy'] == 0:
                    room_no = df.loc[i, 'Roomno']
                    df.loc[i, 'Occupancy'] = 1
                    df.to_csv('Occupancy.csv', index = False)
                    break
            else:
                print("Sorry, we are out of Standard rooms for now")
                return
        
        elif roomtype==2:
            for i in range(4,8):
                if df.loc[i, 'Occupancy'] == 0:
                    room_no = df.loc[i, 'Roomno']
                    df.loc[i, 'Occupancy'] = 1
                    df.to_csv('Occupancy.csv', index = False)
                    break
            else:
                print("Sorry, we are out of Deluxe rooms for now")
                return
            
        elif roomtype==3:
            for i in range(8,12):
                if df.loc[i, 'Occupancy'] == 0:
                    room_no = df.loc[i, 'Roomno']
                    df.loc[i, 'Occupancy'] = 1
                    df.to_csv('Occupancy.csv', index = False)
                    break
            else:
                print("Sorry, we are out of Suite rooms for now")
                return
            
        else:
            print("Please choose a valid room type")

        d,m,y = map(int,input("Enter check-in date in 'dd mm yyyy' format: ").split(' ')) #to split the date month and year into their specific variables
        check_in = date(y,m,d)
        self.rooms[room_no] = {
            'name': name,
            'address': address,
            'phone': phone,
            'check_in_date': check_in,
            'roomservice': 0,
            'roomtype': roomtype
        }
        print(f"\n{name} checked in to room {room_no} on {check_in}\n")

        guest_data = {
            'Name': name,
            'Address': address,
            'Phone': phone,
            'CheckInDate': check_in.strftime('%d %B %Y'),
            'Roomservice': 0,
            'RoomNo': room_no,
            'RoomType': roomtype
        }
        
        self.guest_df = pd.concat([self.guest_df, pd.DataFrame([guest_data])], ignore_index=True) #to concat(add) all the details of the guest in the csv file made to store the details
        self.guest_df.to_csv('guest_details.csv', index=False)

        
    def view_room_types(self):
        print("We have 3 room types available: \n")
        print("1. Standard")
        print("2. Deluxe")
        print("3. Presedential Suite")


    def room_serv(self,room_no):
        df = pd.read_csv('Occupancy.csv')
        row_index = df.index[df['Roomno'] == room_no].tolist()[0]
        if df.loc[row_index, 'Occupancy'] == 1:   #to check if the entered room number is currently occupied or no
            print("----------CAFE MENU----------\n")
            print("1. Tea\t\t\tRs.15")
            print("2. Coffee\t\tRs.30")
            print("3. Fruit Juices\t\tRs.45\n")
            print("4. Bread-Butter\t\tRs.40")
            print("5. Sandwich\t\tRs.60")
            print("6. French Fries\t\tRs.70")
            print("7. Noodles\t\tRs.40")
            print("8. Cheese Sticks\tRs.80")
            print("\nEnter 9 for exit")

            while True:   #loop to take input from user until not exited
                c = int(input("\nEnter your choice: "))
                if c == 9:
                    break

                quantity = int(input("Enter the quantity: "))
                item_price = 0

                if c == 1:
                    item_price = 15
                elif c == 2:
                    item_price = 30
                elif c == 3:
                    item_price = 45
                elif c == 4:
                    item_price = 40
                elif c == 5:
                    item_price = 60
                elif c == 6:
                    item_price = 70
                elif c == 7:
                    item_price = 40
                elif c == 8:
                    item_price = 80
                else:
                    print("Invalid Choice")
                    continue

                total_price = quantity * item_price
                self.rooms[room_no]['roomservice'] += total_price

                # Update charges in the Excel file
                self.guest_df.loc[self.guest_df['RoomNo'] == room_no, 'Roomservice'] = self.rooms[room_no]['roomservice']
                self.guest_df.to_csv('guest_details.csv', index=False)

                print(f"Roomservice price: Rs. {total_price}")

        else:
            print("Invalid Room Number")


    def display_occupied(self):
        occupied_rooms = []
        for i in range(0,12):
            if df.loc[i, 'Occupancy'] == 1:
                occupied_rooms.append(df.loc[i,'Roomno'])
        for roomnos in occupied_rooms:
            print(roomnos, '\n', end='')


    def check_out(self,room_number):
        df = pd.read_csv('Occupancy.csv')
        row_index = df.index[df['Roomno'] == room_number].tolist()[0]
        if df.loc[row_index, 'Occupancy'] == 1:
            check_out_date = date.today()   #the day the guest checks out
            check_in_date = datetime.strptime(self.rooms[room_number]['check_in_date'], '%d %B %Y').date()
            duration = (check_out_date - check_in_date).days   #to calculate the number of days the guest stayed in the hotel
            roomtype = self.rooms[room_number]['roomtype']

            if roomtype == 1:
                self.avlbl_rooms['std'].append(room_number)
            elif roomtype == 2:
                self.avlbl_rooms['deluxe'].append(room_number)
            elif roomtype == 1:
                self.avlbl_rooms['ps'].append(room_number)  #to append the alloted room number back to available rooms dictionary
            
            print('------------------------------')
            print("----------ON THE GO HOTEL RECEIPT----------")
            print(f"Name: {self.rooms[room_number]['name']}")
            print(f"Address: {self.rooms[room_number]['address']}")
            print(f"Phone number: {self.rooms[room_number]['phone']}")
            print(f"Roomnumber: {room_number}")
            print(f"Check-in date: {check_in_date.strftime('%d %B %Y')}")
            print(f"Check-out date: {check_out_date.strftime('%d %B %Y')}")
            print(f"No. of days: {duration}\t\tPrice per day: Rs.{self.roomprice[roomtype]}")

            roombill = duration*self.roomprice[roomtype]   #roomprice per day multiplied by the total number of days
            roomservice = self.rooms[room_number]['roomservice']  #roomservice charges

            print(f"Roombill: Rs.{roombill}")
            print(f"Room service bill: Rs.{roomservice}")
            print("Grand Total: Rs.", roombill + roomservice)

            self.guest_df.loc[self.guest_df['RoomNo'] == room_number, 'Roomservice'] = roomservice
            self.guest_df.to_csv('guest_details.csv', index=False)

            del self.rooms[room_number]

            row_num = df.index[df['Roomno'] == room_number].tolist()[0]
            df.loc[row_num, 'Occupancy'] = 0
            df.to_csv('Occupancy.csv')    #to update the occupancy of the room

        else:
            print(f"Room {room_number} is not occupied")

    def startApp(self):  # the method that contains the start menu
        while True:   # while loop to be run until the guest wants any kind of service provided by the hotel
            print("\n---------------Welcome to ON THE GO Hotel---------------\n")
            print("Main Menu\n")
            print("1. Check-in")
            print("2. View Room Types")
            print("3. Room Service")
            print("4. Display Occupied Rooms")
            print("5. Check out and Payment")
            print("6. Exit\n")

            choice = int(input("Enter your desired choice: "))
            print()

            if choice==1:
                name = input("Enter Guest Name: ")
                address = input("Enter Address: ")
                phone = input("Enter Contact No.: ")
                print()
                self.check_in(name,address,phone)

            elif choice==2:
                self.view_room_types()

            elif choice==3:
                room_no = int(input("Enter Room No.: "))
                self.room_serv(room_no)

            elif choice==4:
                self.display_occupied()

            elif choice==5:
                room_number = int(input("Enter Room No.: "))
                self.check_out(room_number)

            elif choice==6:
                break

            else:
                print("Invalid Choice! Please Try Again!")   # displaying the respective methods according to the choice of the guest

h = Hotel()
h.startApp()
