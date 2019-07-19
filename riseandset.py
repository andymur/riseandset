#!/usr/bin/python3.5
import sys
from enum import Enum
import time

# Here I'm trying to play with daylight time
# 
# 1. I want to understand whether daylight has equal decrease / increase value 
# 	 from day to day between equinoxes / solstices throughout the year or not.
# 
# 2. Do we have same (similar) scenario for the question above for different latitudes 
# 	 (also to show how different are daylight times for different latitudes)
#
# Currently data are taken from here (links are general and an example for Seattle WA, USA):
#   https://aa.usno.navy.mil/data/docs/RS_OneYear.php
# 	http://aa.usno.navy.mil/cgi-bin/aa_rstablew.pl?ID=AA&year=2018&task=0&state=WA&place=Seattlei

months = Enum('Month', 'Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec')


def days_in_month(month):
    if month == months.Feb:
        return 28
    elif month in [months.Jan, month.Mar, month.May, month.Jul, month.Aug, month.Oct, month.Dec]:
        return 31
    else:
        return 30


def each_month_day_rise_and_set(encoded_line):
    day_size = 2
    next_space_size = 2
    rise_and_set_time_size = 9

    month_in_year = len(months)
    encoded_line = encoded_line[day_size:]  # take out day number
    rise_and_set_for_days = []

    for month_index in range(0, month_in_year):
        encoded_line = encoded_line[next_space_size:]
        rise_set_times = encoded_line[:rise_and_set_time_size]
        encoded_line = encoded_line[rise_and_set_time_size:]
        rise_and_set_for_days.append(rise_set_times.strip())

    return rise_and_set_for_days

def calculate_daylight_time_in_hours(sunrise_time, sunset_time):
	#times are encoded like '%H%M' e.g. 0813 or 1952
	time_pattern = '%H%M'
	return (time.mktime(time.strptime(sunset_time, time_pattern)) - time.mktime(time.strptime(sunrise_time, time_pattern))) / (60 * 60)

def calculate_daylight_times_in_hours(month_rise_and_set):
	result = []
	for day_rise_and_set in month_rise_and_set:
		sunrise_time, sunset_time = day_rise_and_set.split(" ")
		result.append(calculate_daylight_time_in_hours(sunrise_time, sunset_time))
	return result

def calendar_lines(filename):
    linecounter = 0
    body_started = False
    calendar = []
    header_size = 6
    calendar_lines = 4 + header_size + 31
    
    with open(filename) as f:
        for line in f:
            if (not body_started) and ('<pre>' in line):
                body_started = True
            if body_started:
                linecounter += 1
                if linecounter > header_size and linecounter < calendar_lines:
                    calendar.append(line)
    
    # skip first three lines: month names line, rise-set line and h-m line
    return calendar[3:]

if __name__ == "__main__":

    #input_filename = "seattle.dat"  # sys.argv[1]
    input_filename = sys.argv[1]
    day_lines = []
    calendar = {month: [None] * days_in_month(month) for month in months}

    day_lines = calendar_lines(input_filename)
    
    day_number = 0
    for day_line in day_lines:
        months_day_rise_and_set = each_month_day_rise_and_set(day_line)
        for month in months:
            if months_day_rise_and_set[month.value - 1]:
                calendar[month][day_number] = months_day_rise_and_set[month.value - 1]
        day_number += 1

    for month in months:
    	print(str(month) + ": ")
    	print("="*80)
    	print(len(calendar[month]), calendar[month])
    	print("="*80)
    	daylights = calculate_daylight_times_in_hours(calendar[month])
    	print(daylights)
    	print("="*80)
    	daylight_delta_vector = [abs(j-i) for i, j in zip(daylights[:-1], daylights[1:])]
    	print(daylight_delta_vector)
    	print("="*80)
    	print("Average Delta: " + str(sum(daylight_delta_vector) / len(daylight_delta_vector)))
    	print("="*80)
    	
    #print(days_in_month(months.Apr))
    #print(len(calendar[months.Jun]), calendar[months.Jun])
    #print(calculate_daylight_times_in_hours(calendar[months.Feb]))
