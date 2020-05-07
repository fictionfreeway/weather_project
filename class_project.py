import requests

# api key and base url from openweathermap.org
api_key = "b2efd09c6e9fb57ba98c6b4c33bff0fc"
owm_url = "http://api.openweathermap.org/data/2.5/weather?"


# function to find city from zip code or city/state
def find_city(user_loc):
    try:
        int(user_loc)
        response = requests.get(owm_url + "zip=" + user_loc + "&units=imperial" + "&appid=" + api_key)
        return response.json()
    except ValueError:
        user_state = input("Please enter state:  ")
        response = requests.get(owm_url + "q=" + user_loc + "," + user_state + ",u&units=imperial" + "&appid=" + api_key)
        return response.json()
    # Connection error exception will occur if no connection to openweathermap.org
    except requests.exceptions.ConnectionError:
        return "not connected"


# convert wind speed into representative word
def wind_speed(speed):
    if speed < 5:
        return "Calm"
    elif 5 <= speed < 15:
        return "Breezy"
    else:
        return "Windy"


# convert visibility percentage to representative cloudiness word
def cloudiness(clouds):
    if clouds < 15:
        return "Clear"
    elif 15 <= clouds < 60:
        return "Partly Cloudy"
    else:
        return "Cloudy"


# formats response from find_city() to user friendly readable format
def format_weather(response):
    weather = "Today's Weather in " + response["name"] + ":"
    temp = "Temperature: " + str(response["main"]["temp"]) + " Degrees Fahrenheit"
    high_low = "Today's High/Low: " + str(response["main"]["temp_max"]) + "/" + str(response["main"]["temp_min"]) + \
               " Degrees Fahrenheit "
    wind = "Wind: " + wind_speed(response["wind"]["speed"])
    clouds = "Clouds: " + cloudiness(response["clouds"]["all"])
    return weather + "\n" + temp + "\n" + high_low + "\n" + wind + "\n" + clouds


# asks if user wishes to check another location, verifies response and returns True of False
def go_again():
    while True:
        check_another = input("Would you like to check another location? Y/N: ").upper()
        if check_another == "Y":
            return True
        elif check_another == "N":
            return False
        else:
            print("Enter 'Y' or 'N'")
            continue


def main():
    print("Welcome to the weather center")
    while True:
        # get user location to be passed to find_city()
        user_loc = input("Please type city name or zip code to view current weather:  ")
        response = find_city(user_loc)
        if response == "not connected":
            print("connection error")
        # 400 and 404 are error codes openweathermap.org returns if location isn't found
        elif response["cod"] == "400" or response["cod"] == "404":
            print("Location not found, please try another")
        else:
            formatted_weather = format_weather(response)
            print(formatted_weather)
        # asks if user would like to check another location
        try_another = go_again()
        if try_another:
            continue
        elif not try_another:
            print("Thanks for using the weather center, goodbye.")
            break


main()