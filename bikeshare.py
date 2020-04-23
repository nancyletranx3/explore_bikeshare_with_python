import time
import pandas as pd
import numpy as np
import calendar

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
# Asking for the city -- 
    city = input("Would you like to see the data for Chicago, New York City, or Washington?: ").lower()
    cities = ['chicago', 'new york city', 'washington']
    while (city not in cities):
        print("That's an invalid city. Please try again.")
        city = input("Would you like to see the data for Chicago, New York City, or Washington?: ").lower()
    
    if (city == "chicago"):
        pd.read_csv("chicago.csv")
    elif (city == "washington"):
        pd.read_csv("washington.csv")
    else:
        pd.read_csv("new_york_city.csv")
        
#Asking for month, day, or none --         
    time = input('Would you like to filter the data by month, day, or not at all? Type "none" for no time filter: ').lower()
    times = ['month', 'day', 'none']
    
#To avoid unbound local variable error --
    month = 'all'
    day = 'all'
    
    while (time not in times):
        print("That's an invalid choice. Please try again.")
        time = input('Would you like to filter the data by month, day, or not at all? Type "none" for no time filter: ').lower()

    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name   
   
#If user chosen month, which month? --
    if (time == 'month'):
        month = input("Which month - January, February, March, April, May, or June?: ").lower()
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        while (month not in months):
            print("That's an invalid month. Please try again.")
            month = input("Which month - January, February, March, April, May, or June?: ").lower()


#If user chosen day, which day? --     
    elif (time == 'day'):
        day = input("Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?: ").lower()
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        while (day not in days):
            print("That's an invalid day. Please try again.")
            day = input("Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?: ").lower()
          
#If user chosen none, then no time filter --            
    elif (time == 'none'):
        month = 'all'
        day = 'all'
    
    
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

#Load data file into a data frame -- 
    df = pd.read_csv(CITY_DATA[city])
    
#Convert Start Time to datetime, then extract the month and day to its own columns --
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    if (month != 'all'):
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        
        df = df[df['month'] == month]
        
    if (day != 'all'):
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

#Display the most common month --
    popular_month = df['month'].mode()[0]
    print("The most popular month is: {}.".format(calendar.month_name[popular_month]))

#Display the most common day of week --
    popular_day = df['day_of_week'].mode()[0]
    print("The most popular day is: {}.".format(popular_day))


#Display the most common start hour -- 
    popular_hour = df['hour'].mode()[0]
    
    if (popular_hour > 12):
        popular_hour -= 12
        print("The most popular hour is: {} PM.".format(popular_hour))
    else:
        print("The most popular hour is: {}.".format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

#Display most commonly used start station --
    popular_start_st = df['Start Station'].mode()[0]
    print("The most popular start station is:\n{}.\n".format(popular_start_st))

#Display most commonly used end station -- 
    popular_end_st = df['End Station'].mode()[0]
    print("The most popular end station is:\n{}.\n".format(popular_end_st))


#Display most frequent combination of start station and end station trip -- 
    popular_combo_st = df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    print("The most frequent combination of start station and end station is:\n\n{}.".format(popular_combo_st))
   


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

#Display total travel time --
    total_trip_dur = df['Trip Duration'].sum()
    print("The total trip duration is: {:,} seconds.".format(total_trip_dur))


#Display mean travel time --
    avg_trip_dur = df['Trip Duration'].mean()
    print("The mean-average trip duration is: {:.1f} seconds.".format(avg_trip_dur))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

#Display counts of user types --
    user_type = df['User Type'].value_counts()
    print("The total number of people from each user type is:\n\n{}.\n".format(user_type))


#Display counts of gender --
    if ('Gender' in df):
        gender = df['Gender'].value_counts()
        print("The total number of people from each gender is:\n\n{}.\n".format(gender))
    else:
        print("There is no information on gender at this location.")


#Display earliest, most recent, and most common year of birth -- 
    if ('Birth Year' in df):
        earliest = min(df['Birth Year'])
        most_recent = max(df['Birth Year'])
        most_common = df['Birth Year'].mode()[0]
    
        print("The earliest birth year is: {:.0f}.".format(earliest))
        print("The most recent birth year is: {:.0f}.".format(most_recent))
        print("The most common birth year from this data is: {:.0f}.".format(most_common))
    else:
        print("There is no information on birth year at this location.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
