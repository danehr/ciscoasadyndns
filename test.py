import sys,re,base64,string,cookielib, urllib, urllib2,httplib
import xml.etree.ElementTree as ET
from socket import *
import thread
import logging

login = ''
password = ''
 
def handler(clientsocket, clientaddr):
    print "Accepted connection from: ", clientaddr
    a = 0
    logger.error('Accepted connection from:')
    logger.error(clientaddr[0])
    while 1:
        data = clientsocket.recv(2048)
        if not data:
            break
        else:
         try:
          print data
          logger.error(data)
          if len(data.split('\n')) > 10:
            logger.error(data)
            logger.error(a)
            print a
            tmp = 'a'
              
            data = data.split('\n')
            
            print '::',data[0],'::'
            if data[0] == 'POST / HTTP/1.0\r' or 'POST /hej HTTP/1.0\r' or data[0] == '<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>':             
             if data[5] == '<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>':
              print 'delar'
	      data = data[5:len(data)]
              tmp = data[0]
              data = '\n'.join(data)
             if data[0] == '<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>':
              tmp = data[0]
              data = '\n'.join(data)

            print data
            if tmp == '<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>':
             tree = ET.ElementTree(ET.fromstring(data))
             root = tree.getroot()
             for child in root:
         	print child.tag, child.attrib, child.text
                if child.tag == "HostName":
                          hosta = child.text
                if child.tag == "IPAddress":
                          ipa = child.text
             print hosta, ipa

	     updatehost = "members.dyndns.org"
	     fakeagent = "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)"
	     updatepage = "/nic/update"
	     updateprefix = updatepage + "?system=custom&hostname="
             updatesuffix = '.dyndns.org&myip=' + clientaddr[0]
 
	     h2 = httplib.HTTPS(updatehost)
	     h2.putrequest("GET", updateprefix + hosta + updatesuffix)
	     h2.putheader("HOST", updatehost)
	     h2.putheader("USER-AGENT", fakeagent)
	     authstring = base64.encodestring(login + ":" + password)
	     authstring = string.replace(authstring, "12", "")
	     h2.putheader("AUTHORIZATION", "Basic " + authstring)
	     h2.endheaders()
 
	     errcode, errmsg, headers = h2.getreply()
 
	    # try to get the html text
	     try:
	   	   fp = h2.getfile()
		   httpdata = fp.read()
		   fp.close()
	     except:
		   httpdata = "No output from http request."
		   fp.close()
		
	     print httpdata
                
             logger.error(httpdata)

          print 'borjar om'
          msg = "You sent me: %s" % data
          clientsocket.send(msg)
          a = a + 1
       
          print 'rstanger anslutning'
          logger.error('closing connection')
          clientsocket.close()
         except:
          clientsocket.close()
 
if __name__ == "__main__":
 


    logger = logging.getLogger('myapp')
    hdlr = logging.FileHandler('/var/log/asalogger')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr) 
    logger.setLevel(logging.WARNING)
    logger.error('Starting log')

    host = '10.20.20.107'
    port = 80
    buf = 1024
 
    addr = (host, port)
 
    serversocket = socket(AF_INET, SOCK_STREAM)
 
    serversocket.bind(addr)
 
    serversocket.listen(2)
 
    while 1:
        print "Server is listening for connections\n"
        logger.error('Server started and listening') 

        clientsocket, clientaddr = serversocket.accept()
        thread.start_new_thread(handler, (clientsocket, clientaddr))
    serversocket.close()
