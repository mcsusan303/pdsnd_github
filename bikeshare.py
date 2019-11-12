import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Enter the name of one of the following cities to get its data (Chicago, New York City, or Washington):").lower()
        if city in (CITY_DATA):
            break
        else:
            print("That city does not have data.  Please enter a valid city:  ")
            continue

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = input("Enter name of month to use.  Valid months are January, February, March, April, May, or June.  If you want all months, enter keyword all:  ").lower()
        if month in ('january','february','march','april','may','june','all'):
            break
        else:
            print("That month does not have data available.  Please enter a valid month (January - June):  ")
            continue

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Enter day of week to use.  If you would like all days of the week, enter keyword all:  ").lower()
        if day in ('sunday','monday','tuesday','wednesday','thursday','friday','saturday','all'):
            break
        else:
            print("That is not a valid day of the week.  Please re-enter a valid day of the week:  ")
            continue

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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def raw_data(df):
    count = 0
    while True:
        response = input('\nWould you like to see raw data? Enter yes or no.\n').lower()
        if response != 'yes':
            break
        else:
            print(df.reset_index(drop=True).loc[count:count+4])
            count += 5


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    print('Most Common Month:  ', months[popular_month-1].title())

    # TO DO: display the most common day of week
    popular_dow = df['day_of_week'].mode()[0]
    print('Most Common Day of Week:  ', popular_dow)

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most Popular Start Station:', popular_start_station)

    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most Popular End Station:', popular_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    trips = df.groupby(['Start Station', 'End Station']).size().reset_index(name="Frequency").sort_values(by='Frequency',ascending=False).head(1)
    trips_start = trips['Start Station'].to_string(index=False)
    trips_end = trips['End Station'].to_string(index=False)
    print("The most frequent combination of Start Station and End Station is from {} to {}.". format(trips_start, trips_end))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    df['Travel Time'] = df['End Time'] - df['Start Time']
    total_travel_time = df['Travel Time'].sum()
    print("Total travel time is:  ", total_travel_time)

    # TO DO: display mean travel time
    mean_travel_time = df['Travel Time'].mean()
    print("Mean travel time is:  ", mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print('User Type Distribution:\n\n', user_types)

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        df['Gender'] = df['Gender'].fillna('Missing data')
        genders = df['Gender'].value_counts()
        print('\nGender Distribution:\n\n', genders)
    else:
        print('\n\nGender information is not available in the data you have selected.\n')

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_birth_yr = df['Birth Year'].min()
        most_recent_birth_yr = df['Birth Year'].max()
        most_common_birth_yr = df['Birth Year'].mode()[0]
        print('\n\nThe earliest birth year is:  ', earliest_birth_yr)
        print('\nThe most recent birth year is:  ', most_recent_birth_yr)
        print('\nThe most common birth year is:  ', most_common_birth_yr)
    else:
        print('\nBirth year information is not available in the data you have selected.\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
