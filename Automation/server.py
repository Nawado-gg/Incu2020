from ncclient import manager
import xml.dom.minidom
import socket

node = "127.0.0.1"

def hello():
    device_connection = connect(node)
    return "Avalible commands: show hostname, show version, set hostname + name"

def connect(node):
    try:
        device_connection = manager.connect(host = node, port = '2222', username = 'admin', password = 'cisco!123', hostkey_verify = False, device_params={'name':'nexus'})
        return device_connection
    except:
        print("Unable to connect " + node)

def getHostname(node):
    device_connection = connect(node)
    try:
        hostname = """
                   <show xmlns="http://www.cisco.com/nxos:1.0">
                       <hostname>
                       </hostname>
                   </show>
                   """
        netconf_output = device_connection.get(('subtree', hostname))
        xml_doc = xml.dom.minidom.parseString(netconf_output.xml)
        print(xml_doc)
        hostname = xml_doc.getElementsByTagName("mod:hostname")
        return "Hostname: " + str(hostname[0].firstChild.nodeValue)
    except:
        return 'Can not get hostname'

def getVersion(node):
    device_connection = connect(node)
    try:
        version = """
                   <show xmlns="http://www.cisco.com/nxos:1.0">
                       <version>
                       </version>
                   </show>
                   """
        netconf_output = device_connection.get(('subtree', version))
        xml_doc = xml.dom.minidom.parseString(netconf_output.xml)
        version = xml_doc.getElementsByTagName("mod:nxos_ver_str") #also need to check bios_ver_str, loader_ver_str
        return f"Version: {str(version[0].firstChild.nodeValue)}"
    except:
        return "Unable to get this node version"
    
def setHostname(node, new_hostname):
    device_connection = connect(node)
    host_name = '''
                <config>
                    <configure xmlns="http://www.cisco.com/nxos:1.0">
                        <__XML__MODE__exec_configure>
                            <hostname>
                                <name>%s</name>
                            </hostname>
                        </__XML__MODE__exec_configure>
                    </configure>
                </config>    
                '''
    config_ = host_name % (new_hostname.split()[-1])
    try:
        device_connection.edit_config(target = 'running', config = config_)
        return (f"New hostname is {new_hostname.split()[-1]}")
    except:
        return 'Unable to change the hostname' + \
                '\nIf you want to change a hostname you need paste "set hostname" + new_hostname as one word'
    
def Main():
    host = "127.0.0.1"
    port = 5000

    mySocket = socket.socket()
    mySocket.bind((host, port))

    mySocket.listen(2)
    conn, addr = mySocket.accept()
    
    #hello_user = hello()
    #conn.send(hello_user.encode())
    
    print ("Connection from: " + str(addr))
    while True:
        message = conn.recv(1024).decode()
        if message == "show hostname":
            message = getHostname(node)
        elif message == 'show version':
            message = getVersion(node)
        elif 'set hostname' in message:
            message = setHostname(node, message)
        else:
            message = "I do not understand"
        conn.send(message.encode())
    conn.close()

if __name__ == '__main__':
        Main()
