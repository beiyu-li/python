"""
e7_ont_telnet
Author :ywu
Date : 10/18/2023:08:45
project : pycharm
"""

"""
telnetlib_t2_20231010
Author :ywu
Date : 10/10/2023:09:29
project : pycharm
"""

import telnetlib
from telnetlib import Telnet
import time
import re


class E7telnet(Telnet):
    def __init__(self, host, port):
        super(E7telnet, self).__init__(host, port)
        print("self", self)

    def telnetE7(self, host, port, username=None, password=None, type=None):
        self.Tel = E7telnet(host, port)
        self.Tel.set_debuglevel(5)
        self.Tel.read_until(b'login:')
        self.Tel.write(username + b'\n')
        self.Tel.read_until(b'Password:')
        self.Tel.write(password + b'\n')
        res = self.Tel.read_until(b": " or b"# " or b"~ " or b">", 3)
        return self.Tel

    def telnetEXA(self, host, port, username=None, password=None, type=None):
        self.Tel = E7telnet(host, port)
        self.Tel.set_debuglevel(5)
        self.Tel.read_until(b'Username: ')
        self.Tel.write(username + b'\n')
        self.Tel.read_until(b'Password:')
        self.Tel.write(password + b'\n')
        res = self.Tel.read_until(b": " or b"# " or b"~ " or b">", 3)
        return self.Tel


    def cli(self, cmd):
        self.cmd = cmd
        self.Tel.write(cmd.encode() + b'\n')
        time.sleep(3)
        output = self.Tel.read_very_eager().decode()
        print(f'very eager output is {output}')
        return output

    def exa_cli(self, cmd):
        self.cmd = cmd
        self.Tel.write(cmd.encode() + b'\n')
        time.sleep(3)
        output = self.Tel.read_until(b"E7-YUAN-1>").decode()
        print(f'very eager output is {output}')
        return output



    def shutdown_ontport(self, port):
        self.port = port
        self.cli('config')
        self.cli('interface ont-ethernet ' + port)
        self.cli('shutdown')
        time.sleep(1)
        self.cli('no shutdown')
        time.sleep(1)
        self.cli('end')
        output = self.Tel.read_very_eager().decode()
        print(f'very eager output is {output}')
        return output

    def check_ont_exist(self, ont_id):
        self.ont_id = ont_id
        retry_time = 1
        ont_exist = 1
        for retry_time in range(1, 4):
            res1 = self.cli('show discovered-onts ')
            print(f'res1 is {res1}')
            if ont_id in res1:
                break
            else:
                retry_time = retry_time + 1
                time.sleep(5)
                if retry_time == 3:
                    ont_exist = 0
                    raise Exception(f'ont {ont_id} is missing, please check')
        # if ont_exist==0:
        #     raise Exception(f'ont {ont_id} is missing, please check')
        # else:
        #     print(f'ont {ont_id} is discovered')



    def check_axos_file(self,content,text):
        '''this method is used to check files in techlog'''
        self.cli('paginate false')
        res = self.cli(f'show file contents {content} ')
        time.sleep(3)
        print(f'{content} show result is {res}')
        file = text+r"[a-zA-Z0-9_\.\-]+"
        # file = r"techlog-.*?"  ####this patten can match file file size and time
        tech_file_list = re.findall(file,res)
        print(tech_file_list)
        return tech_file_list


class OntTelnet(E7telnet):
    def __init__(self, host, port):
        super(E7telnet, self).__init__(host, port)


    def ont_telnet(self, host, port, username=None, password=None):
        self.Tel = OntTelnet(host, port)
        self.read_until(b'#',3)
        output = self.Tel.read_very_eager().decode()
        print(output)




# username = b'test'
# password = b'test123'

username = b'sysadmin'
password = b'sysadmin'


def shutdown_ponport(ponport, ont_id, times):
    host1 = '10.245.37.191'
    xg1601 = E7telnet(host1, 23)
    xg1601.telnetE7(host1, 23, user1, pass1)
    xg1601.cli(''' paginate false''')
    xg1601.cli('''idle-timeout 0''')
    i = 1

    for i in range(1, times):
        xg1601.cli('config')
        xg1601.cli('interface pon ' + ponport)
        xg1601.cli('shutdown')
        time.sleep(5)
        xg1601.cli('no shutdown')
        time.sleep(5)
        xg1601.cli('end')
        res = xg1601.cli('show discovered-onts ')
        retry_time = 1
        for retry_time in range(1, 4):
            res1 = xg1601.cli('show discovered-onts ')
            if ont_id in res:
                break
            else:
                retry_time = retry_time + 1
                time.sleep(5)
        if retry_time == 3 and ont_id not in res1:
            break
        else:
            pass
        i = i + 1


def shutdown_ontport(host,ont_id):
    # host1 = '10.245.37.191'
    xg1601 = E7telnet(host, 23)
    xg1601.telnetE7(host, 23, user1, pass1)
    xg1601.cli(''' paginate false''')
    xg1601.cli('''idle-timeout 0''')
    i = 1
    for i in range(1, 10001):
        print(f'this is the {i} time to shutdown')

        i = i + 1
        xg1601.cli('''\r\n''')
        xg1601.shutdown_ontport(f'{ont_id}/x1')

        xg1601.shutdown_ontport(f'{ont_id}/g1')

        xg1601.shutdown_ontport(f'{ont_id}/g2')

        xg1601.shutdown_ontport(f'{ont_id}/g3')

        xg1601.check_ont_exist(ont_id)

        # xg1601.check_ont_exist('ywu_4201')


def check_ont(host, ont_id):
    xg1601 = E7telnet(host, 23)
    xg1601.telnetE7(host, 23, user1, pass1)
    xg1601.cli(''' paginate false''')
    xg1601.cli('''idle-timeout 0''')
    for i in range(1, 4):
        print(f'this is the {i} time check')
        xg1601.check_ont_exist('ont_id')


def check_ont_file():
    host = '10.245.37.119'
    port = '10016'
    elvis = OntTelnet(host, port)
    elvis.ont_telnet(host,port)
    elvis.cli('\r\n')
    elvis.cli('ls /calix/panic')


# shutdown_ontport('10.245.37.197', 'elvis')

# check_ont('10.245.37.191', '4201x123')

# check_ont_file()

if __name__ == "__main__":
    cmd = ['show ver', 'show card', 'show info', 'show inventory']
    host = '10.245.37.197'
    gpon8r2 = E7telnet(host,23)
    gpon8r2.telnetE7(host,23,username,password)
    gpon8r2.cli(''' paginate false''')
    gpon8r2.cli('''idle-timeout 0''')
    # for item in cmd:
    #     gpon8r2.cli(item)
    # shutdown_ponport('1/2/xp16', 'elvis', 2)
    # check_ont('10.245.37.191', '4201x123')

    # shutdown_ontport('10.245.37.197', 'elvis')
    list = ['techlog-GPON-8R2-472205021271-2023_09_13T08_33_32-common.tar.gz', 'techlog-GPON-8R2-472205021271-2023_09_21T11_04_19-common.tar.gz', 'techlog-GPON-8R2-472205021271-2023_10_10T15_46_26-common.tar.gz', 'techlog-GPON-8R2-472205021271-2023_09_13T10_17_47-common.tar.gz', 'techlog-GPON-8R2-472205021271-2023_09_19T08_34_20-common.tar.gz']

    tech_file_list = gpon8r2.check_axos_file('core','core')
