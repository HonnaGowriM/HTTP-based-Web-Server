THE WEB SERVER 
* The libraries used in the program are socket,threading,sys,os,time,logging.
* When the main program is called the initializing checks if the port number is greater than 1024 and binds to the port. The port number is read via the configuration file.
* Post that a TCP connection is establish when a connection is requested.
* Threading has been implemented. When a request comes in from the browser a thread is initialized to the target function.
* The requests are handelled according to the required conditions given.
* In the command prompt run the web server program.
* From the browser(Firefox) request <host Ip><Port>/<required path>


NOTE
* Logging is implemented.
* Post protocol is implemented.
* Program is written using Classes.