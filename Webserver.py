#author: Honna Gowri Manjuanth honna.manjunath@colorado.edu
#name:
#purpose:
#date
#version

import socket
import threading
import sys
import os
import time
import logging

class Server():
    def __init__(self):
        '''
        Initializing the class and allowing the server to listen on a port only if the port is greater than 1024. Additionally to check if the configuration file exisit or not.
         '''
        try:
            log_format= "%(asctime)s %(levelname)s %(thread)d %(threadName)s - %(message)s"
            logging.basicConfig(filename='Logging_File', level= logging.DEBUG, format = log_format, filemode='w')
            self.logger=logging.getLogger()
            check1=os.path.isfile("ws.conf")
            #print(check1)
            self.logger.info("Checking if the configuration file is present or not")
            if(check1==True):
                self.logger.info("The required configuration file is present")
                file=open("ws.conf",'r')
                a=file.readlines()
                self.dict={}
                for lines in a:
                    (key,value)=lines.split()
                    self.dict[key]=value       
            else:
                #print("Conf file is not present")
                self.logger.error("The required configuration file is not present")
                exit() 
            if (int(self.dict['ListenPort'])) > 1024:
                self.port =int(self.dict['ListenPort'])
            else:
                #print("Port number is less than 1024 hence exiting the program")
                self.logger.error("Port number is less than 1024 hence exiting the program")
                exit()
            self.host = ''
            self.create_socket()
            #self.threads=[]
        except KeyboardInterrupt:
            self.logger.error("Keyboard interrupt was triggered")
            sys.exit()
       
    
    def create_socket(self):
        '''
        To create a socket
        '''
        try:
            sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)#create an INET, STREAMing socket
            sock.bind((self.host,self.port))#bind the socket to a host, and a port
            sock.listen(5)#queue up as many as 5 connect requests
            print ('Serving HTTP on port %s ...' % self.port)
            self.logger.info('Serving HTTP on port %s ...' %self.port)
            self.sock=sock
            self.accept_req() #call accept_req()
        except socket.error as message: 
            if sock: 
                sock.close() 
            print ("Could not open socket: " + str(message) )
            self.logger.error("Could not open socket: " + str(message))
            #sys.exit(1) 
        except KeyboardInterrupt:
            self.logger.error("Keyboard interrupt was triggered")
            sys.exit()
    
    def accept_req(self):
        '''
        Accepting a request and starting threads.
        '''
        try:
            thread_list=[]
            i=1
            while 1:
                self.conn,addr=self.sock.accept()#accept Request
                if self.conn:
                    self.start=time.time()
                    #for i in range():
                    T=threading.Thread(name='thread{}'.format(i),target=self.function_g(self.conn,i))
        
                    thread_list.append(T)
                    self.logger.info(T)
                    T.start()
                    i=i+1
                    for t in thread_list:
                        t.join()
                    self.end=time.time()
                    #print('time_taken:{}',format(self.end-self.start))
                    #self.logger.info(format(self.end-self.start))
                else:
                    print("Nothing in TCP connection")
                    self.logger.info("Nothing sent across in TCP connection")
        except KeyboardInterrupt:
            self.logger.error("Keyboard interrupt was triggered")
            sys.exit()
        
            
                                             
    def function_g(self,conn,i):
        self.conn.settimeout(int(self.dict['KeepaliveTime']))
        self.logger.info("Keepalive time set thread" + str(i))
        try:
            while(1):
                request=''
                self.logger.info("Thread has entered the target function")
                request=self.conn.recv(65535)
                if request:
                    print("In the target function")
                    self.logger.info("The thread is inside the target function")
                    request = request.decode()
                    print ("Printing the request"+request)
                    self.logger.info("Printing the request"+request)
                    data=request.split()
                    version = data[2]
                    print("Printing version" + version)
                    self.logger.info("Printing version" + version)
                    version = version[5:]
                    #if 'Connection' in data:
                        #print('Connection time out is present') 
                    #print(version)
                    '''
                    To check if the supported protocols are requested and to enter the if loop. 
                    If the default page is requested load the default page else check for the concerned request and go about   
                    '''
                    if (data[0] in ("GET", "PUT","HEAD","DELETE","POST","OPTIONS","TRACE","CONNECT") and data[2] in ("HTTP/1.1","HTTP/1.0","HTTP/2.0")):
                        print("All parameters good")
                        self.logger.info("The basic check is cleared")
                        if (data[0]=="GET"): #HONNA PUT THE CONTENT CHECK ALSO IN AND CONDITION 
                            print("Entered GET function")
                            self.logger.info("Entered the GET function")
                            if(version=="1.1") or (version=="1.0") or (version=="2.0"):
                                print("Version cleared")
                                self.logger.info("Supporting the requested version for GET")
                                #self.function_g(data[1])
                                try:
                                    filename = data[1]
                                    if (filename=='/'):
                                        print("Entered Dpage loop")
                                        self.logger.info("Entered the Default page loop")
                                        filename = filename[1:]
                                        DMSG=("HTTP/"+version+" 200 OK\r\n"+"Content-Type: "+ self.dict['html']+ "\r\nContent-Length: "+ str(os.path.getsize("DPage.html"))+"\r\n"+"Keep-Alive: "+self.dict['KeepaliveTime']+", max=200\r\n"+"Connection: Keep-Alive\r\n")
                                        #ADD KEEP ALIVE INFORMATION IN THE HEADER
                                        print("Im printing this header\n"+ str(DMSG))
                                        self.logger.info("Printing header\n"+ DMSG)
                                        self.conn.send(DMSG.encode())
                                        self.conn.send("\r\n".encode())
                                        file_open=open("DPage.html",'rb')
                                        BytesSent=0
                                        while BytesSent <= os.path.getsize("DPage.html"):
                                            data1=file_open.read(1024)
                                            self.conn.send(data1)
                                            BytesSent=BytesSent+1024
                                        file_open.close()
                                    else:
                                        print("Entered non Dpage")
                                        self.logger.info("Entered the Non-Default page loop")
                                        (First,Second)=filename.split(".")
                                        print("Im printing"+First,Second)
                                        filename = filename[1:]
                                        print("Im printing filename "+str(filename))
                                        self.logger.info("Printing filename "+str(filename))
                                        check=filename.split(".")
                                        print("Im printing check"+str(check))
                                        self.logger.info("Printing check"+str(check))
                                        print(check[1])
                                        if check[1] in self.dict.keys():
                                            folderpath = self.dict[check[1]].split('/')
                                            subpath = folderpath[0]
                                            print("CHECKKKKKKKKKKKKKKKKK"+subpath)
                                            my_file = self.dict["DocumentRoot"]+"\\"+subpath+ "\\"
                                            print("Im print path " + str(my_file))
                                            #self.logger.info("Printing the path of the file " + str(my_file))
                                            checkPath= my_file+ filename
                                            print("iM PRINTING CHECKPATH " + checkPath)
                                            self.logger.info("PRINTING THE COMPLETE PATH TO THE FILE " + checkPath)
                                            check1 = os.path.isfile(checkPath)
                                            print(check1)
                                            if(check1==True):
                                                print("I ENTERED")
                                                self.logger.info("Requested file is present")
                                                MSG=("HTTP/"+version+" 200 OK\r\n"+"Content-Type: "+ self.dict[check[1]]+ "\r\n"+"Content-Length: "+ str(os.path.getsize(checkPath))+"\r\n"+"Keep-Alive: "+self.dict['KeepaliveTime']+", max=200\r\n"+"Connection: Keep-Alive\r\n")
                                                print("Im printitng message " + MSG)
                                                self.logger.info("Printing the header message " + MSG)
                                                self.conn.send(MSG.encode())
                                                self.conn.send("\r\n".encode())
                                                print("Path is")
                                                print(checkPath)
                                                file_open=open(checkPath,'rb')
                                                SendBytes=0
                                                while SendBytes<os.path.getsize(checkPath):
                                                    data1=file_open.read(1024)
                                                    self.conn.send(data1)
                                                    SendBytes=SendBytes+1024
                                                file_open.close()
                                            else:
                                                '''
                                                If requested page is not there throw 404 error.
                                                '''
                                                print("I entered else")
                                                self.logger.error("The requested file is not present")
                                                ERRMSG=("HTTP/"+version+" 404 Not Found\r\n Content-Type: "+self.dict['html']+"\r\nContent-Length: "+ str(os.path.getsize("404.html"))+"\r\n"+"Keep-Alive: "+self.dict['KeepaliveTime']+", max=200\r\n"+"Connection: Keep-Alive\r\n")
                                                print(ERRMSG)
                                                self.logger.info("Printing the error message " + ERRMSG)
                                                self.conn.send(ERRMSG.encode())
                                                self.conn.send("\r\n".encode())
                                                file_open=open('404.html','rb')
                                                SendBytes=0
                                                while SendBytes <os.path.getsize("404.html"):
                                                    data1=file_open.read(1024)
                                                    self.conn.send(data1)
                                                    SendBytes=SendBytes+1024
                                                file_open.close()
                                            
                                            #self.conn.close()
                                        else:  
                                            '''
                                            If extensions are not implemented throw 501 error.
                                            ''' 
                                            OMSG=("HTTP/"+version+" 501 Not Implemented\n Content-Type: "+self.dict['html']+"\r\nContent-Length: "+ str(os.path.getsize("501.html"))+"\r\n"+"Keep-Alive: "+self.dict['KeepaliveTime']+", max=200\r\n"+"Connection: Keep-Alive\r\n")
                                            self.conn.send(OMSG.encode())
                                            self.conn.send("\r\n".encode())
                                            file_open=open("501.html",'rb')
                                            SendBytes=0
                                            while SendBytes<os.path.getsize("501.html"):
                                                data1=file_open.read(1024)
                                                self.conn.send(data1)
                                                SendBytes=SendBytes+1024
                                            file_open.close()
                                except ValueError:
                                    print("File extension not provided")
                                    self.logger.info("File extension is not provided by the user")
                                    OMSG=("HTTP/"+version+" 400 Bad Request\r\nContent-Type: "+self.dict['html']+"\r\n"+"Content-Length: "+ str(os.path.getsize("400.html"))+"\r\nKeep-Alive: "+self.dict['KeepaliveTime']+", max=200\r\n"+"Connection: Keep-Alive\r\n")
                                    print("pRINTTING THE "+OMSG)
                                    self.logger.info("Printing the 404 error message header\n"+ OMSG)
                                    self.conn.send(OMSG.encode())
                                    self.conn.send("\r\n".encode())
                                    file_open=open("400.html",'rb')
                                    SendBytes=0
                                    while SendBytes<os.path.getsize("400.html"):
                                        data1=file_open.read(1024)
                                        self.conn.send(data1)
                                        SendBytes=SendBytes+1024
                                    file_open.close()      
                        else:
                            '''
                            Check for various conditions and throw appropriate errors.
                            '''
                            if (version=="1.0") and ((data[0]=="PUT") or (data[0]=="HEAD")):
                                print("Entered unhandled functions")
                                OMSG=("HTTP/"+version+"501 Not Implemented\r\n Content-Type: "+self.dict['html']+"\r\n"+"\r\nContent-Length: "+ str(os.path.getsize("501.html"))+"Keep-Alive: "+self.dict['KeepaliveTime']+", max=200\r\n"+"Connection: Keep-Alive\r\n")
                                print(OMSG)
                                self.logger.info("Printing the 501 error message header\n"+ OMSG)
                                self.conn.send(OMSG.encode())
                                self.conn.send("\r\n".encode())
                                file_open=open("501.html",'rb')
                                SendBytes=0
                                while SendBytes<os.path.getsize("501.html"):
                                    data1=file_open.read(1024)
                                    self.conn.send(data1)
                                    SendBytes=SendBytes+1024
                                file_open.close()
                            
                            elif (version in ("1.0","1.1")) and (data[0]=="POST"):
                                MSG=("HTTP/"+version+" 200 OK\r\n"+"Content-Type: "+ self.dict['html']+ "\r\n"+"Content-Length: "+ str(os.path.getsize('post.html'))+"\r\n"+"Keep-Alive: "+self.dict['KeepaliveTime']+", max=200\r\n"+"Connection: Keep-Alive\r\n")
                                print("Inside the POST " + MSG)
                                self.logger.info("Printing the POST message header\n"+ MSG)
                                self.conn.send(MSG.encode())
                                self.conn.send("\r\n".encode())
                                #print("Path is")
                                #print(checkPath)
                                file_open=open('post.html','rb')
                                SendBytes=0
                                while SendBytes<os.path.getsize('post.html'):
                                    data1=file_open.read(1024)
                                    self.conn.send(data1)
                                    SendBytes=SendBytes+1024
                                file_open.close()
                            
                            elif version=="1.1":
                                print("Entered unhandled functions")
                                OMSG=("HTTP/"+version+" 501 Not Implemented"+"\r\n"+"Content-Type: "+self.dict['html']+"\r\n"+"Content-Length: "+ str(os.path.getsize("501.html"))+"\r\n"+"Keep-Alive: "+self.dict['KeepaliveTime']+", max=200\r\n"+"Connection: Keep-Alive\r\n")
                                self.logger.info("Printing the 501 error message header\n"+ OMSG)
                                self.conn.send(OMSG.encode())
                                self.conn.send("\r\n".encode())
                                file_open=open("501.html",'rb')
                                SendBytes=0
                                while SendBytes<os.path.getsize("501.html"):
                                    data1=file_open.read(1024)
                                    self.conn.send(data1)
                                    SendBytes=SendBytes+1024
                                file_open.close()
                                
                            else:
                                print("1.0 is requesting 1.1's protocol not supported")
                                self.logger.error("1.0 is requesting 1.1's protocol not supported")
                                OMSG=("HTTP/"+version+" 400 Bad Request\r\nContent-Type: "+self.dict['html']+"\r\n"+"Content-Length: "+ str(os.path.getsize("400.html"))+"\r\nKeep-Alive: "+self.dict['KeepaliveTime']+", max=200\r\n"+"Connection: Keep-Alive\r\n")
                                print("pRINTTING THE "+OMSG)
                                self.logger.info("Printing the 400 error message header\n"+ OMSG)
                                self.conn.send(OMSG.encode())
                                self.conn.send("\r\n".encode())
                                file_open=open("400.html",'rb')
                                SendBytes=0
                                while SendBytes<os.path.getsize("400.html"):
                                    data1=file_open.read(1024)
                                    self.conn.send(data1)
                                    SendBytes=SendBytes+1024
                                file_open.close()
                                               
                    else:
                        '''
                        Anything other than 1.1/1.0/2.0 is requested throw an error.
                        '''
                        print("Version not supported")
                        self.logger.info("Requested version is not supported")
                        OMSG=("HTTP/"+version+" 400 Bad Request\r\nContent-Type: "+self.dict['html']+"\r\n"+"Content-Length: "+ str(os.path.getsize("400.html"))+"Keep-Alive: "+self.dict['KeepaliveTime']+", max=200\r\n"+"Connection: Keep-Alive\r\n")
                        print("Version not supported error"+OMSG)
                        self.logger.info("Printing the 400 error message header\n"+ OMSG)
                        self.conn.send(OMSG.encode())
                        self.conn.send("\r\n".encode())
                        file_open=open("400.html",'rb')
                        SendBytes=0
                        while SendBytes<os.path.getsize("400.html"):
                            data1=file_open.read(1024)
                            self.conn.send(data1)
                            SendBytes=SendBytes+1024
                        file_open.close()
                        
                #self.conn.close()
        except KeyboardInterrupt:
            self.logger.error("Keyboard interrupt was triggered")
            sys.exit()
        except socket.timeout:
            #self.conn.close()
            self.logger.info("Timeout done for thread" + str(i))

        
                                        
if __name__ == '__main__':
    server=Server()
