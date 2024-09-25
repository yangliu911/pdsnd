import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_DATA = {1: 'Jan',
              2: 'Feb',
              3: 'Mar',
              4: 'Apl',
              5: 'May',
              6: 'Jun',
              7: 'Jul',
              8: 'Aug',
              9: 'Sep',
              10: 'Oct',
              11: 'Nov',
              12: 'Dec'}

DAY_DATA = {1: 'Mon',
              2: 'Tue',
              3: 'Wed',
              4: 'Thu',
              5: 'Fri',
              6: 'Sat',
              7: 'Sun'}
#refactoring get_filters
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
    city = input("Chicago, New York, or Washington?\n").lower()
    month = input("Which month? (1,2,3,4,5,6,7,8,9,10,11,12)\n").lower()
    day = input("Which day? Please type your response as an integer (e.g., 1=Monday,2=Tuesday... 7=Sunday)\n").lower()
    
    print('-'*40)
    return city, month, day

#refactoring load_data
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
    df_t = pd.read_csv(CITY_DATA[city])

    #format datetime
    df_t['Start Time'] = pd.to_datetime(df_t['Start Time'])
    df_t['End Time'] = pd.to_datetime(df_t['End Time'])
    df_t['month'] = df_t['Start Time'].dt.month
    df_t['weekday'] = df_t['Start Time'].dt.weekday
    df_t['hour'] = df_t['Start Time'].dt.hour
    df_t['start_to_end_station'] = df_t['Start Station'] + ' --> ' + df_t['End Station']

    #filter by month and weekday
    if month != "none":
        if day != "none":
            df = df_t[(df_t['month'] == int(month)) & (df_t['weekday'] == int(day))]
        else:
            df = df_t[(df_t['month'] == int(month))]
    else:
        if day != "none":
            df = df_t[(df_t['weekday'] == int(day))]
        else:
            df = df_t

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("The most common month is: " + MONTH_DATA[df['month'].mode()[0]])

    # display the most common day of week
    print("The most common day is: " + df['Start Time'].dt.weekday_name.mode()[0])


    # display the most common start hour
    print("The most common start hour is: " + str(df['hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The most common start station is: " + df['Start Station'].mode()[0])

    # display most commonly used end station
    print("The most common end station is: " + df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    print("The most common trip is: " + df['start_to_end_station'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("The total travel time is: " + str(df['Trip Duration'].sum()))

    # display mean travel time
    print("The mean travel time is: " + str(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Counts of user types:")
    print(df['User Type'].value_counts())
    print("")

    if city != 'washington':
        # Display counts of gender
        print("The counts of gender :\n", df['Gender'].value_counts())
        print("")

        # Display earliest, most recent, and most common year of birth
        print("The earliest year of birth: " + str(int(df['Birth Year'].min())))
        print("The most Recent year of birth: " + str(int(df['Birth Year'].max())))
        print("The most common year of birth: " + str(int(df['Birth Year'].mode()[0])))
    else:
        print("There is no \'gender\' and \'birth year\' data for Washington!!!")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


#refactoring display_data
def display_data(df):
    pd.set_option('display.max_columns', None)# configuration to show all columns
    start_index = 0
    feedback = input("Do you want to see  the first 5 rows of data? Enter yes or no.\n")
    if feedback == "yes":
        print('-' * 40)
        print(df.iloc[start_index:(start_index + 5)])
        print('-' * 40)
        start_index += 5
        feedback = input("Do you want to see  the next 5 rows of data? Enter yes or no.\n")         
    if feedback == "NO":
        print("\nThere is no data ")
        
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        if df.shape[0] > 0:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df, city)
            display_data(df)
        else:
            print("\nThere is no data ")



        restart = input('\nDo you want to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
