#include "CalendarPrinter.h"

#include <iostream>
#include <iomanip>

using namespace std;

void disaster()
{
    cout << "Disaster! Exiting ..." << endl;
    exit(-1);
}

void CalendarPrinter::printCalendar(int year, int month) const
{
    int currentMonth = 1;
    int firstDayInCurrentMonth = firstDayOfNewYearMonth(year);
    bool leap = isLeapYear(year);
    skip(9);
    cout << year << endl;
    while (currentMonth <= 12)
    {
        int numDays = numOfDaysInMonth(currentMonth, leap);
        if (currentMonth == month)
        {
            printHeader(currentMonth);
            printMonth(numDays, firstDayInCurrentMonth);
            cout << std::endl << std::endl << std::endl;
        }
        else
        {
            stepOverMonth(numDays, firstDayInCurrentMonth);
        }
        currentMonth = currentMonth + 1;
    }
    std::cout << std::endl;
}

bool CalendarPrinter::isLeapYear (int year) const
{
    return ((year % 4 == 0) && (year % 100 != 0)) || (year % 400 == 0);
}

int CalendarPrinter::firstDayOfNewYearMonth(int year) const
{
    int x1 = (year - 1) / 4;
    int x2 = (year - 1) / 100;
    int x3 = (year - 1) / 400;
    int day_start = (year + x1 - x2 + x3) % 7;
    return day_start;
}

int CalendarPrinter::numOfDaysInMonth(int m, bool leap) const
{
    if (m == 1) {
        return(31);
    } else if (m == 2) {
        if (leap) { return(29); }
        return(28);
    } else if (m == 3) {
        return(31);
    } else if (m == 4) {
        return(30);
    } else if (m == 5) {
        return(31);
    } else if (m == 6) {
        return(30);
    } else if (m == 7) {
        return(31);
    } else if (m == 8) {
        return(31);
    } else if (m == 9) {
        return(30);
    } else if (m == 10) {
        return(31);
    } else if (m == 11) {
        return(30);
    } else if (m == 12) {
        return(31);
    } else {
        disaster();
    }
}

void CalendarPrinter::printHeader(int m) const
{
    if (m == 1) {
        skip(7);
        cout << "January" << endl;
    } else if (m == 2) {
        skip(7);
        cout << "February" << endl;
    } else if (m == 3) {
        skip(7);
        cout << "March" << endl;
    } else if (m == 4) {
        skip(7);
        cout << "April" << endl;
    } else if (m == 5) {
        skip(7);
        cout << "May" << endl;
    } else if (m == 6) {
        skip(7);
        cout << "June" << endl;
    } else if (m == 7) { skip(7); cout << "July" << endl; }
    else if (m == 8) { skip(7); cout << "August" << endl; }
    else if (m == 9) { skip(7); cout << "September" << endl; }
    else if (m == 10) { skip(7); cout << "October" << endl; }
    else if (m == 11) { skip(7); cout << "November" << endl; }
    else if (m == 12) { skip(7); cout << "December" << endl; }
    else {
        disaster();
    }

    cout << " S  M  T  W  T  F  S" << endl;
    cout << "____________________" << endl;
}

void CalendarPrinter::skip(int i) const {
    while (i > 0) {
        cout << " ";
        i = i - 1;
    }
}

void CalendarPrinter::printMonth(int numDays, int &weekDay) const
{
    int day = 1;
    skipToDay(weekDay);
    while (day <= numDays) {
        cout << setw(2) << day << " ";
        if (weekDay == 6) {
            cout << endl;
            weekDay = 0;
        } else {
            weekDay = weekDay + 1;
        }
        day = day + 1;
    }
}

void CalendarPrinter::stepOverMonth(int numDays, int &weekDay) const
{
    int day = 1;
    while (day <= numDays) {
        if (weekDay == 6) {
            weekDay = 0;
        } else {
            weekDay = weekDay + 1;
        }
        day = day + 1;
    }
}

void CalendarPrinter::skipToDay(int d) const {
    skip(3 * d);
}