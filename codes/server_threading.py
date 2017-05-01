import time
from threading import *
from socket import *
from datetime import datetime;
import re
now=time.time();
accept={0:['127.0.0.1','sravan','chandra',now,0]};
Blacklist=[]
# lock = Lock()
# def Check_DoS():
#     last_updated_time=time.time()
#     while True:
#         current_time=time.time()
#         if current_time-last_updated_time>10:
#             lock.acquire();
#             reset_count();
#             lock.release();
#             last_updated_time=current_time

class Server(Thread):
    def __init__(self,addr):
        Thread.__init__(self);
        self.addr=addr;
        self.server = socket(AF_INET, SOCK_STREAM);
        self.server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1);
        self.clients=[];
    def run(self):
        try :
            self.server.bind(self.addr);
            self.server.listen(1);
        except:
            print "Error in Server Hosting";
            exit(0);
        # DoS = Thread(target=Check_DoS);
        # DoS.start();
        while True:
            client,addr=self.server.accept();
            message=client.recv(4096);
            # x='';
            # while message:
            #     x=x+message;
            #     message=client.recv(1024);
            self.clients.append(Client(client,message));
            self.clients[-1].daemon=True;
            self.clients[-1].start();

    def close(self):
        for t in self.clients:
            try:
                t.client.shutdown(SHUT_RDWR)
                t.client.close();
            except:
                pass;
        self.server.shutdown(SHUT_RDWR);
        self.server.close();

def header_message(length,Cookie):
    now = datetime.now();
    header_message_info={
        'Date':now.strftime('%Y-%m-%d %H:%M'),
        'Content-Length':length,
        'Keep-Alive':'timeout=10,max=100',
        'Connection':'Keep-Alive',
        'Connect-Type':'text/html',
        #'Set-Cookie':'hello_google'
    };
    if Cookie!='':
        header_message_info['Set-Cookie']=Cookie;

    header_message_info='\r\n'.join("%s:%s" % (key,header_message_info[key]) for key in header_message_info);
    return header_message_info;

def Add_to_blacklist(Cookie):
    # print 'Added to Blacklist'+ Cookie
    Blacklist.append(accept[int(Cookie)][0])


def Check_Cookie(client_message):
    if 'Cookie' not in client_message:
        return ''
    elif 'Cookie' in client_message:
        lines=client_message.split('\n');
        for l in lines:
            # print l
            if 'Cookie:' in l:
                Cookie=l[7:].split()[0];
                # print "hello Cookie:"+Cookie
            if 'Host:' in l:
                Host=l[5:].split(':')[0].split()[0];
                # print Host
        try:
            if accept[int(Cookie)][0]==Host:
                # print accept
                # print accept[int(Cookie)][0],Host
                accept[int(Cookie)][4]+=1;
                now=time.time()
                if accept[int(Cookie)][4]==10:
                    if now-accept[int(Cookie)][3]<10:
                        Add_to_blacklist(Cookie);
                    else:
                        accept[int(Cookie)][4]=0;
                        accept[int(Cookie)][3]=now;
                return Cookie;
            else:
                return '';
        except:
            # print 'Cookie:%s Host:%s'%(Cookie,Host);
            return '';

def Check_Blacklist(client_message):
    Host=re.search('Host:.*\S',client_message).group(0)[5:].split(':')[0].split()[0];
    if Host in Blacklist:
        return True
    else:
        return False

def Post_File_info(client_message):
# print self.client_message
    client_message=client_message.split('\n');
    boundary='';
    posted_file=''
    flag=False;
    for l in client_message:
        if 'boundary=' in l:
            boundary=re.search('boundary=.*\S',l).group(0)[9:]
            print boundary
            continue
        if boundary in l and boundary!='':
            flag=True;
            continue
        if flag:
            if boundary in l:
                break
            posted_file=posted_file+l+'\n';
    return posted_file
class Client(Thread):
    def __init__(self,client,message):
        Thread.__init__(self);
        self.client_message=message;
        self.client=client;

    def run(self):
        # print re.search('Cookie',self.client_message).group(0);
        if not self.client_message:
             return;
        if Check_Blacklist(self.client_message):
            self.client.shutdown(SHUT_RDWR);
            self.client.close();
            return
        Cookie=Check_Cookie(self.client_message)
        try:
            # print accept
            # print "sravan"
            # print self.client_message
            # print Cookie
            # x=1;
            # receive_message=self.client.recv(1024);
            # print "post"+receive_message;
            # x=0

            # if self.client_message.split()[0]=='POST':
            #     print Post_File_info(self.client_message)
            # if self.client_message.split()[0]=='PUT':
            #     file_info=Post_File_info(self.client_message)
            #     file_name=re.search('filename=.*\S',file_info.split('\n')[0]).group(0)[9:].split('\"')[1]
            #     with open(file_name, 'wb') as f:
            #         file_info=file_info.split('\n')
            #         for i in range(3,len(file_info)-3):
            #             f.write(file_info[i]+'\n')
            #     f.close()
                # print self.client_message
            # print file_name
            # if file_name=='index.html':
            #     print "svn"
            #     time.sleep(5)
            #     print "sfasfdgsfgfsggfsggs"
            file_info='';
            if Cookie=='':
                verify=re.search('email=.*&password=.*\S',self.client_message);
                if verify:
                    verify=verify.group(0);
                    verify=verify.split('&')
                    email=verify[0][6:]
                    password=verify[1][9:]
                    Cookie=len(accept);
                    Host=re.search('Host:.*\S',self.client_message).group(0)[5:];
                    Host=Host.split(':')[0].split()[0];
                    now=time.time()
                    accept[int(Cookie)]=[Host,email,password,now,1];
                    file_name=self.client_message.split()[1][1:].split('?')[0];
                    f=open(file_name);
                    file_info=f.read();
                    # file_info='<html><head></head><body><h3>You are Authenicated</h3></body></html>'
                else:
                    f=open('authentication.html');
                    file_info=f.read();
                # header_message_info=header_message(len(file_info),'hell')
                # self.client.send('HTTP/1.1 200 OK\r\n'+str(header_message_info)+'\r\n\r\n');
                # self.client.send(file_info);

            elif self.client_message.split()[0]=='GET':
                Cookie=''
                file_name=self.client_message.split()[1][1:].split('?')[0];
                # if file_name=='hello.html':
                #     time.sleep(10);
                f=open(file_name);
                file_info=f.read();
            elif self.client_message.split()[0]=='POST':
                print Post_File_info(self.client_message)
                Cookie=''
                file_info='<html><head></head><body><h3>Posted Successfully</h3></body></html>'
            elif self.client_message.split()[0]=='PUT':
                file_info=Post_File_info(self.client_message)
                file_name=re.search('filename=.*\S',file_info.split('\n')[0]).group(0)[9:].split('\"')[1]
                with open(file_name, 'wb') as f:
                    file_info=file_info.split('\n')
                    for i in range(3,len(file_info)-3):
                        f.write(file_info[i]+'\n')
                f.close()
                Cookie=''
                file_info='<html><head></head><body><h3>Posted Successfully</h3></body></html>'

            length=len(file_info);

            # print length
            header_message_info=header_message(length,Cookie)
            self.client.send('HTTP/1.1 200 OK\r\n'+str(header_message_info)+'\r\n\r\n');
            for i in range(0,length):
                    self.client.send(file_info[i]);
            # client.close()
        except:
            # print 'Value Error is ' +ValueError
            file_info='<html><head></head><body><h3>404 Not Found</h3></body></html>';
            header_message_info=header_message(len(file_info),'')
            self.client.send('HTTP/1.1 404 Not Found\r\n'+str(header_message_info)+'\r\n\r\n');
            self.client.send(file_info);
            #client.close();
            # return;
        finally:
            self.client.shutdown(SHUT_RDWR);
            self.client.close();

#     print "sleeping 5 sec from thread %d" % i
#     time.sleep(5)
#     print "finished sleeping from thread %d" % i
#
# for i in range(10):
#     t = Thread(target=myfunc, args=(i,))
#     t.start()
# def reset_count():
#     print "resent Count"
#     n=len(accept);
#     for i in range(0,n):
#         accept[i][3]=0;

if __name__=='__main__':
    host='';
    port=54321;
    addr=(host,port);
    server=Server(addr);
    server.daemon=True;
    server.start()
    end =raw_input("press enter to stop server");
    server.close()
