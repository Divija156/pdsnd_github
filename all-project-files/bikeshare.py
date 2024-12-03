import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
# STATIC DATA 
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']
DAYS = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    while True:
        city = input("Enter a city of your choice from Chicago, New york city, Washington:").lower().strip()
        if city in CITY_DATA.keys():
            break
        else:
            print("Invalid input for (city), try again")

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Enter a month from ({}) or all: ".format(", ".join(MONTHS))).lower().strip()
        if month in MONTHS or month == 'all':
            break
        else:
            print("Invalid input for (month) filter, try again")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Enter a day from ({}) or all: ".format(", ".join(DAYS))).lower().lstrip().rstrip()
        if day in DAYS or day == 'all':
            break
        else:
            print("Invalid input for (day) filter, try again")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # path = '/Users/divija/Desktop/Study-Dec-2024/Programming4DataSciencewithPython/03_python/all-project-files/'
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    # filter by month if applicable
    if month != 'all':
        month = MONTHS.index(month) + 1
        df = df[df['month'] == month]
    # filter by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'].str.lower() == day]  
    return df 

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    month = df['month'].value_counts().index[0]
    print("The most common month : ", MONTHS[month-1].capitalize())

    # display the most common day of week
    day_of_week = df['day_of_week'].value_counts().index[0]
    print("The most common day of week : ", day_of_week)

    # display the most common start hour
    hour = df['hour'].value_counts().index[0]
    print("The most common start hour : ", hour)

    print("\nThis took %s seconds." % round((time.time() - start_time), 6))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].value_counts().index[0]
    print("The most common start station : ", start_station)

    # display most commonly used end station
    end_station = df['End Station'].value_counts().index[0]
    print("The most common end station : ", end_station)

    # display most frequent combination of start station and end station trip
    grouped_df = df.groupby(['Start Station', 'End Station']).size().reset_index(name='count')
    max_count = grouped_df['count'].max()
    frequent_trip = grouped_df[grouped_df['count'] == max_count]
    print("The most frequent combination of start station and end station trip : \n", frequent_trip[['Start Station', 'End Station']])

    print("\nThis took %s seconds." % round((time.time() - start_time), 6))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f"Total travel time : {total_travel_time} seconds")

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print(f"Mean travel time : {round(mean_travel_time, 1)} seconds")    

    print("\nThis took %s seconds." % round((time.time() - start_time), 6))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Counts of user types : \n", user_types)


    # Display counts of gender
    if 'Gender' in df.columns:
        gender_count = df['Gender'].value_counts()
        print("Counts of gender : \n", gender_count)
    else:
        print("'Gender' is not available in data")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns: 
        min_yob = int(df['Birth Year'].min())
        max_yob = int(df['Birth Year'].max())
        common_yob = int(df['Birth Year'].mode()[0])
        print(f"earliest year of birth : {min_yob} \nmost recent year of birth : {max_yob} \nmost common year of birth : {common_yob}")
    else:
        print("'Birth Year' is not available in data")

    print("\nThis took %s seconds." % round((time.time() - start_time), 6))
    print('-'*40)

def display_raw_data(df, city):
    """ Displays 5 rows of raw data from city user selected"""
    i = 0
    # TO DO: convert the user input to lower case using lower() function
    raw = input(f"Would like to see raw data from ({city}) dataset. Enter 'yes' or 'no' :").lower().lstrip().rstrip() 
    pd.set_option('display.max_columns',200)
    while True:            
        if raw == 'no':
            break
        elif raw == 'yes':
            # TO DO: appropriately subset/slice your dataframe to display next five rows
            print(df[i:i+5]) 
            raw = input("Would like to see more records. Enter 'yes' or 'no':").lower().lstrip().rstrip() 
            i += 5
        else:
            raw = input("Your input is invalid. Enter 'yes' or 'no':").lower().lstrip().rstrip()
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        print(f"Loading data for {city} \n Applying month filter {month} \nAlong side day filter {day}")
        df = load_data(city, month, day)
        display_raw_data(df, city)
        print(f"Loading stats from {city} for months:{month}, days:{day}")
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()


