#ifndef CalendarPrinter_h
#define CalendarPrinter_h

class CalendarPrinter {
public:
    void printCalendar(int year, int month) const;

private:
    bool isLeapYear(int) const;
    int firstDayOfNewYearMonth(int) const;
    int numOfDaysInMonth(int, bool) const;
    void printHeader(int) const;
    void printMonth(int, int&) const;
    void stepOverMonth(int, int&) const;
    void skip(int) const;
    void skipToDay(int) const;
};

/*#include <iostream>
#include <cstdlib>
#include <iomanip>

using namespace std;

int main ()
{
    system ("color f1 ");
    int year, firstDayInCurrentMonth;
    int currentMonth = 1;
    int numDays;
    bool leap;
    cout << "What year do you want a calendar for? ";
    cin >>year;
    cout<<endl;
    firstDayInCurrentMonth=firstDayofnewyearMonth(year);
    leap = isLeapYear(year);
    skip(9);
    cout << year << endl;
    while (currentMonth <= 12)
    {
    numDays = numOfDaysInMonth(currentMonth, leap);
    printHeader(currentMonth);
    printMonth(numDays, firstDayInCurrentMonth);
    cout << endl << endl << endl;
    currentMonth = currentMonth + 1;
    }
    cout << endl;
}*/

#endif
