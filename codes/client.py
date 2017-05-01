from socket import *
from socket import *
from datetime import datetime;
from sys import argv

if len(argv)!=3:
    print argv
    print "Error in giving arguments"
    exit(0);

try:
    addr=(argv[1],int(argv[2]));
except:
    print "Error in giving arguments"
    exit(0);

while True:
    command=raw_input('prompt>')
    if len(command.split())!=2:
        continue;
    response='';
    try:
        client=socket();
        client.connect(addr);
        header={
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language':'en-us',
            'Host':argv[1]+':'+argv[2],
            'Cookie':'0'
        };
        header_message_info='\r\n'.join('%s:%s'%(key,header[key]) for key in header);
        if command.split()[0]=='GET':
            file_name=command.split()[1];
            client.send('\r\nGET /'+file_name+' HTTP/1.1'+ header_message_info+'\r\n\r\n');
        if command.split()[0]=='POST' or command.split()[0]=='PUT':
            file_name=command.split()[1];
            f=open(file_name)
            file_info=f.read()
            header_message_info+='\r\nboundary=----------------------1234567890'
            client.send(''+command.split()[0]+' /'+file_name+' HTTP/1.1\r\n'+ header_message_info+'\r\n\r\n');
            header_message_info='\r\n----------------------1234567890+\r\n'
            header_message_info=header_message_info+'\r\nContent-Disposition: form-data; filename=\"'+str(file_name)+'\"';
            header_message_info=header_message_info+'\r\nContent-Type: text/x-csrc\r\n';
            client.send(header_message_info+file_info+'\r\n\r\n\r\n')


    except ValueError:
        client.close()
        exit(0)

    info=client.recv(1024)
    while info:
        response =response+info;
        info=client.recv(1024);

    client.close()
    print response;
