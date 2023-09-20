# Import the csv and os
import csv
import os
import sys
from collections import defaultdict

columns = defaultdict(list) # each value in each column is appended to a list
aircraftTypes = ['Medium narrow body', 'Large narrow body', 'Medium wide body']
medNarBody = {'Running cost per seat per 100 km': '8', 'Maximum flight range (km)': '2650', 'Capacity if all seats are standard-class': '180', 'Minimum number of first-class seats': '8'}
larNarBody = {'Running cost per seat per 100 km': '7', 'Maximum flight range (km)': '5600', 'Capacity if all seats are standard-class': '220', 'Minimum number of first-class seats': '10'}
medWidBody = {'Running cost per seat per 100 km': '5', 'Maximum flight range (km)': '4050', 'Capacity if all seats are standard-class': '406', 'Minimum number of first-class seats': '14'}
# Read Airports.csv
with open('Airports.csv', 'r') as csvfile:
    csvdictreader = csv.DictReader(csvfile)
    # csvreader = csv.reader(csvfile)
    # data = list(csvreader)
    for row in csvdictreader:
        for (k,v) in row.items():
            columns[k].append(v)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# Airport details
def airportDetails():
        global ukAirport
        global abrAirport
        global columnIndex
        global abrAirportName
        ukAirport = input('Enter the 3 letter code for the UK airport. \n')
        if(ukAirport == 'LPL' or ukAirport == 'BOH'):
            abrAirport = input('Enter the three letter code for the overseas airport. \n')
            if abrAirport in columns['Overseas airport code']:
                columnIndex = columns['Overseas airport code'].index(abrAirport)
                abrAirportName = columns['Overseas airport name'][columnIndex]
                clear()
                print('You have selected: ' + abrAirportName)
                mainMenu()
            else:
                clear()
                print('Invalid airport code, returning to main menu')
                mainMenu()

# FLight details
def flightDetails():
        global selectedAircraftType
        global firstClassSeats
        global standardSeats
        global bodyType
        
        clear()
        selectedAircraftType = input('Enter aircraft type\n').upper()
        if(selectedAircraftType == 'MEDIUM NARROW BODY'):
            bodyType = medNarBody
        elif(selectedAircraftType == 'LARGE NARROW BODY'):
            bodyType = larNarBody
        elif(selectedAircraftType == 'MEDIUM NARROW BODY'):
            bodyType = medWidBody
        else:
            clear()
            print('Invalid aircraft type, returning to main menu')
            mainMenu()
        
        print('Running cost per seat per 100 km: ' + bodyType['Running cost per seat per 100 km'] + '\nMaximum flight range (km): ' + medNarBody['Maximum flight range (km)'] + '\nCapacity if all seats are standard-class: ' + medNarBody['Capacity if all seats are standard-class'] + '\nMinimum number of first-class seats: ' + medNarBody['Minimum number of first-class seats'])
        firstClassSeats = int(input('Enter amount of first class seats\n'))
        if(firstClassSeats > 0):
            if(firstClassSeats < int(bodyType['Minimum number of first-class seats'])):
                clear()
                print('First class seats less than minimum, returning to main menu.')
                mainMenu()
            if(firstClassSeats > int(bodyType['Capacity if all seats are standard-class'])):
                clear()
                print('First class seats greater then capacity, returning to main menu.')
                mainMenu()
            standardSeats = int(bodyType['Capacity if all seats are standard-class']) - firstClassSeats*2
            clear()
            print('Flight details verified, returning to main menu.')
            mainMenu()

def distCalc(bodyType):
    if(ukAirport == 'LPL'):
        if(bodyType['Maximum flight range (km)'] >= columns['Distance from Liverpool John Lennon (km)'][columnIndex]):
            clear()
            print('Max flight range is bigger than distance to airport, returning to main menu')
            mainMenu()
    else:
        if(bodyType['Maximum flight range (km)'] >= columns['Distance from Bournemouth International (km)'][columnIndex]):
            clear()
            print('Max flight range is bigger than distance to airport, returning to main menu')
            mainMenu()

def costPerSeat(bodyType):
    global flightCostPS
    if(ukAirport == 'LPL'):
        flightCostPS = int(bodyType['Running cost per seat per 100 km'])*int(columns['Distance from Liverpool John Lennon (km)'][columnIndex])/100
    elif(ukAirport == 'BOH'):
        flightCostPS = int(bodyType['Running cost per seat per 100 km'])*int(columns['Distance from Bournemouth International (km)'][columnIndex])/100

def mainMenu():
    print('''
=========================================
Welcome to the airline profit calculator
=========================================
(1) Enter airport details
(2) Enter flight details
(3) Enter price plan and calculate profit
(4) Clear data
(Q) Quit
=========================================
    ''')
    menuSelection = input()
    clear()
    # Enter airport details
    if(menuSelection == '1'):
        airportDetails()
    # Enter flight details
    if(menuSelection == '2'):
        flightDetails()
    # Calculate profit
    if(menuSelection == '3'):
        if(ukAirport == None or abrAirport == None):
            clear()
            print('Airport hasnt been selected, returning to main menu')
            mainMenu()
        elif(selectedAircraftType == None):
            clear()
            print('Aircraft type has not been selected, returning to main menu')
            mainMenu()
        elif(firstClassSeats == None):
            clear()
            print('First class seats havent been entered, returning to main menu')
            mainMenu()
        distCalc(bodyType)
        stdSeatPrice = float(input('Enter the price of a standard seat\n£'))
        clear()
        fcSeatPrice = float(input('Enter the price of a first class seat\n£'))
        clear()
        # Calculate flight cost per seat
        costPerSeat(bodyType)
        flightCost = flightCostPS*(firstClassSeats+standardSeats)
        flightIncome = firstClassSeats*fcSeatPrice+standardSeats*stdSeatPrice
        flightProfit = flightIncome-flightCost
        clear()
        print("=========================================\n\n" + "Flight cost per seat: £" + str(flightCostPS) + "\nFlight cost: £" + str(flightCost) + "\nFlight income: £" + str(flightCost) + "\nFlight profit: £" + str(flightProfit))
        mainMenu()
    # Clear all data
    if(menuSelection == '4'):
        restartPrompt = input('Are you sure you want to clear all data? Y/N\n')
        if(restartPrompt == 'Y' or restartPrompt == 'y'):
            os.execl(sys.executable, '"{}"'.format(sys.executable), *sys.argv)
        if(restartPrompt == 'N' or restartPrompt == 'n'):
            mainMenu()
        else:
            clear()
            print('Invalid input, returning to main menu')
            mainMenu()

    # Quit
    if(menuSelection == 'q' or menuSelection == '5'):
        print('You have exited the program')
        # Exits with code 0
        sys.exit(0)
clear()
mainMenu()