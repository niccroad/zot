#include "Emailer.h"

#include "Singleton.h"

void Emailer::sendAnEmailTo(const std::string& subject, const std::string& body) {
	_implSendEmailTo(Singleton::INSTANCE.getToAddress(), subject, body);
}

void Emailer::_implSendEmailTo(const std::string& to, const std::string& subject, const std::string& body) {
	// Implementation of sending email goes here.
}
