#ifndef Emailer_h
#define Emailer_h

#include <string>

class Emailer {
public:
    void sendAnEmailTo(const std::string& subject, const std::string& body);
    
private:
	void _implSendEmailTo(const std::string& to, const std::string& subject, const std::string& body);
};

#endif // Emailer_h