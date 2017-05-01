from socket import *
from datetime import datetime;
server = socket(AF_INET, SOCK_STREAM);
host='';
port=54321;
try :
    server.bind((host,port));
    server.setsockopt(SOL_SOCKET,SO_REUSEADDR, 1);
except:
    print "Error in Server Hosting";
    exit(0);

now = datetime.now();
server.listen(1);
if __name__=="__main__":
    while True:
        client,addr=server.accept();
        client_message=client.recv(1024);
        print client_message
        if not client_message:
            continue;
        file_name=client_message.split()[1][1:];
        print file_name
        try:
            f=open(file_name);
        except:
            client.send("HTTP/1.1 404 Not Found\r\n\r\n");
            client.send('<html><head></head><body><h3>404 Not Found</h3></body></html>');
            client.close();
            continue;
        file_info=f.read();
        length=len(file_info);
        header_message_info={
            'Date':now.strftime('%Y-%m-%d %H:%M'),
            'Content-Length':length,
            'Keep-Alive':'timeout=10,max=100',
            'Connection':'Keep-Alive',
            'Connect-Type':'text/html'
        };
        header_message_info='\r\n'.join("%s:%s" % (key,header_message_info[key]) for key in header_message_info);
        client.send('HTTP/1.1 200 OK\r\n'+str(header_message_info)+'\r\n\r\n');
        for i in range(0,length):
            client.send(file_info[i]);
        client.close();	
