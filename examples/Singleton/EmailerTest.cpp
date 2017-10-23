#include "TestFramework.h"

#include <string>

MOCK_INCLUDE("Singleton.h",
	class Singleton {
	public:
		static Singleton INSTANCE;
	
		std::string getToAddress() const {
			return "some.body@main.address";
		}
	};
	
	Singleton Singleton::INSTANCE;
);

#include "Emailer.h"

class EmailerTest {
public:
	void setUp() {
		// Some set up code.
	}
	
	void tearDown() {
		// Some tear down code.
	}
	
    void testSendEmailTo() {
    	Emailer emailer;
    	emailer.sendAnEmailTo("This is a test.",
    		                  "This email is sent by a test case.");
    }
};

TEST_ENTRY_POINT()