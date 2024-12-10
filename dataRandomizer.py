

#this is where the data that we will use for our presentation
import random


#randomize time and date
from datetime import datetime, timedelta

#class SouthAmericaBoudary:
#    def __init__(self):
#        self.min_latitude = -56.0  # Southern boundary (Cape Horn)
#        self.max_latitude = 12.0  # Northern boundary (Colombia/Venezuela border)
#        self.min_longitude = -81.3  # Western boundary (Chile)
#        self.max_longitude = -34.8  # Eastern boundary (Brazil)
    


class AustraliaBoundary:
    def __init__(self):
        self.min_latitude = -43.6 # Southern boundary (South East Cape, Tasmania)
        self.max_latitude = -10.5  # Northern boundary (Cape York, Queensland)
        self.min_longitude = 113.3  # Western boundary (Steep Point, Western Australia)
        self.max_longitude = 153.6  # Eastern boundary (Cape Buron, New South Wales)
    def random_Aus_latitude():
        return random.uniform(-43.6, -10.5)
    # Generate a random latitude
    latitude = random_Aus_latitude()
    #print(f"Random Latitude: {latitude}")

    #randomize Longitude
    def random_Aus_longitude():
        return random.uniform(113.3, 153.6)

    # Generate a random longitude
    longitude = random_Aus_longitude()


def random_datetime(start_year=2022):
    # Define the start and end dates
    start_date = datetime(start_year, 1, 1)
    end_date = datetime.now()  # You can also set a specific end date

    # Calculate the difference between the start and end dates
    delta = end_date - start_date

    # Generate a random number of days to add to the start date
    random_days = random.randint(0, delta.days)
    
    # Calculate the random date
    random_date = start_date + timedelta(days=random_days)

    # Generate random time
    random_hour = random.randint(0, 23)
    random_minute = random.randint(0, 59)
    random_second = random.randint(0, 59)

    # Combine date and time
    random_datetime = random_date.replace(hour=random_hour, minute=random_minute, second=random_second)
    return random_datetime.strftime("%Y-%m-%d %H:%M:%S")



#Set Boundaries

#NAmLoc= NorthAmericaBoundary()
#SAmLoc= SouthAmericaBoudary()
#EurLoc= EuropeBoundary()
#AsLoc= AsiaBoundary()
#AusLoc= AustraliaBoundary()
#AntLoc= AntarcticaBoundary()



#print("Random North American Latitude and Longitude: ", NAmLoc.random_latitude(), ", ", NAmLoc.random_longitude())

def random_NAm_latitude():
        return random.uniform(14.5, 71.5)

    # Generate a random latitude
latitude = random_NAm_latitude()
    #print(f"Random Latitude: {latitude}")

    #randomize Longitude
def random_NAm_longitude():
    return random.uniform(-179.1, 14.5)

    # Generate a random longitude
longitude = random_NAm_longitude()
def random_SAm_latitude():
    return random.uniform(-56.0, 12.0)

    # Generate a random latitude
latitude = random_SAm_latitude()
    #print(f"Random Latitude: {latitude}")

    #randomize Longitude
def random_SAm_longitude():
    return random.uniform(-81.3, -34.8)

    # Generate a random longitude
longitude = random_SAm_longitude()
#randomize Latitude

    

def random_Eur_latitude():
    return random.uniform(71.5, 34.5)

    # Generate a random latitude
latitude = random_Eur_latitude()
#print(f"Random Latitude: {latitude}")

    #randomize Longitude
def random_Eur_longitude():
    return random.uniform(59.3, 31.3)

   # Generate a random longitude
longitude = random_Eur_longitude()

def random_As_latitude():
    return random.uniform(81.0, -6.4)

    # Generate a random latitude
latitude = random_As_latitude()
#print(f"Random Latitude: {latitude}")

    #randomize Longitude
def random_As_longitude():
    return random.uniform(26.0, 169.0)

    # Generate a random longitude
longitude = random_As_longitude()

def random_Aus_latitude():
    return random.uniform(-43.6, -10.5)
    # Generate a random latitude
latitude = random_Aus_latitude()
#print(f"Random Latitude: {latitude}")

    #randomize Longitude
def random_Aus_longitude():
    return random.uniform(113.3, 153.6)

    # Generate a random longitude
longitude = random_Aus_longitude()

def random_Ant_latitude():
    return random.uniform(-90, -60)
    # Generate a random latitude
latitude = random_Ant_latitude()
    #print(f"Random Latitude: {latitude}")

    #randomize Longitude
def random_Ant_longitude():
    return random.uniform(180, -180)

    # Generate a random longitude
longitude = random_Ant_longitude()

#print/run methods
if __name__ == "__main__":
    print("Random Date and Time:", random_datetime())
    #print("Random North American Latitude and Longitude: ", random_NAm_latitude(), ", ", random_NAm_longitude()) #working
    print("Random South American Latitude and Longitude: ", random_SAm_latitude(), ", ", random_SAm_longitude()) #kinda working
    print("Random European Latitude and Longitude: ", random_Eur_latitude(), ", ", random_Eur_longitude()) #working
    print("Random Asian Latitude and Longitude: ", random_As_latitude(), ", ", random_As_longitude()) #working
    print("Random Australian Latitude and Longitude: ", random_Aus_latitude(), ", ", random_Aus_longitude()) #kinda working
    #print("Random Antarctica Latitude and Longitude: ", random_Ant_latitude(), ", ", random_Ant_longitude()) #working
