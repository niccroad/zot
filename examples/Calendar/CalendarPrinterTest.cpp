#include "TestFramework.h"
#include "CalendarPrinter.h"

MOCK_INCLUDE(<iostream>,
#include <sstream>
    std::stringstream cout;
);

class CalendarPrinterTest {
public:
    void setUp() {
        ::cout.str("");
    }

    void test_when_print_calendar_is_called_the_calendar_is_printed_to_stdout() {
        CalendarPrinter printer;
        printer.printCalendar(2017, 12);
        EXPECT_EQ("         2017\n"
                  "       December\n"
                  " S  M  T  W  T  F  S\n"
                  "____________________\n"
                  "                1  2 \n"
                  " 3  4  5  6  7  8  9 \n"
                  "10 11 12 13 14 15 16 \n"
                  "17 18 19 20 21 22 23 \n"
                  "24 25 26 27 28 29 30 \n"
                  "31 \n\n\n"
                  , ::cout.str());
    }

    void test_when_print_calendar_is_called_for_april_the_calendar_is_printed_to_stdout() {
        CalendarPrinter printer;
        printer.printCalendar(2017, 4);
        EXPECT_EQ("         2017\n"
                  "       April\n"
                  " S  M  T  W  T  F  S\n"
                  "____________________\n"
                  "                   1 \n"
                  " 2  3  4  5  6  7  8 \n"
                  " 9 10 11 12 13 14 15 \n"
                  "16 17 18 19 20 21 22 \n"
                  "23 24 25 26 27 28 29 \n"
                  "30 \n\n\n"
                  , ::cout.str());
    }
};

TEST_ENTRY_POINT()