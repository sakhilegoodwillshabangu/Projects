from socket import *
import thread
from db_manager import *
import time
class Client:
    def __init__(self, ip_address = "localhost", port = 50007):
        self.server_address = ip_address
        self.server_port = port
    def makeRequest(self, message, server_address = "localhost", server_port = 50007):
        try:
            socket_object = socket(AF_INET, SOCK_STREAM)
            socket_object.connect((server_address, server_port))
            socket_object.send(message)
            received_data = socket_object.recv(10240)
            socket_object.close()
            return received_data
        except:
            return ""
    def requestSignUp(self, user_name, password):
        param = {"name":user_name, "password":password}
        message_request = b"SignUp:" + str(param)
        received_data = self.makeRequest(message_request)
        if received_data == "":
            return "(0, '')"
        return received_data
    def requestLogin(self, user_name, password):
        param = {"name":user_name, "password":password}
        message_request = b"Login:" + str(param)
        received_data = self.makeRequest(message_request)
        if received_data == "":
            return "(0, '')"
        return received_data
    def requestFriendsList(self, key):
        param = {"key":key}
        print("Friends request param:"+str(param))
        message_request = b"FriendsList:" + str(param)
        received_data = self.makeRequest(message_request)
        print("Received Data from server:"+received_data)
        return received_data
    def sendMessageToServer(self, user_key_one, user_key_two, message):
        param = {"from":user_key_one, "to":user_key_two, "message":message}
        message_request = b"SendMessage:" + str(param)
        received_data = self.makeRequest(message_request)
        return received_data
    def sendMessageToClient(self, _to, _from, message):
        param = {"key":_to}
        message_request = b"Address:" + str(param)
        received_data = self.makeRequest(message_request)
        data = eval(received_data)
        message_request = str((_to, message, _from))
        request_output = self.makeRequest(message_request, server_address = data[1][0], server_port = 40007)
        return request_output
    def fetchUnseenMessages(self, key):
        param = {"key":key}
        message_request = b"UnseenMessages:" + str(param)
        received_data = self.makeRequest(message_request)
        return received_data
    def messageReceiver(self, key, ui_object = None):
        host_address = ""
        port_address = 40007
        socket_object = socket(AF_INET, SOCK_STREAM)
        socket_object.bind((host_address, port_address))
        socket_object.listen(5)
        print("message server now listening...")
        while True:
            connection, address = socket_object.accept()
            while True:
                data = connection.recv(10240)
                if not data:
                    break
                list_data = eval(data)
                if list_data[0] == key:
                    self.messageDisplayer(list_data[1], list_data[2], list_data[0], ui_object)
                    connection.send(b"Echo=>" + str(1))
                else:
                    connection.send(b"Echo=>" + str(0))
            connection.close()
    def formMessageTable(self, message, key):
        message_table = dict()
        message_table["message"] = message
        message_table["key"] = key
        message_table["time"] = time.asctime()
        return message_table
    def storeReceivedMessagesLocally(self, _from, _to, message, message_view = 0):
        messages_key = _to + _from
        print("store message line:1")
        db_manager_object = DatabaseManager()
        print("store message line:2")
        local_db_table = db_manager_object.loadData("dbl.dat")
        print("store message line:3")
        chats_sub_table = dict()
        print("store message line:4")
        chats_sub_table["sender_key"] = _from
        print("store message line:5")
        chats_sub_table["message"] = message
        print("store message line:6")
        chats_sub_table["time"] = time.asctime()
        print("store message line:7")
        chats_sub_table["view"] = message_view
        print("store message line:8")
        try:
            print("store message line:9")
            chats_list = local_db_table["chats"][messages_key]
            print("store message line:10")
        except:
            chats_list = []
        print("store message line:11")
        chats_list.append(chats_sub_table)
        print("store message line:12")
        print("store message line:13")
        try:
            chats_table = local_db_table["chats"]
        except:
            local_db_table["chats"] = dict()
            chats_table = local_db_table["chats"]
        print("local_db_table:" + str(local_db_table))
        chats_table[messages_key] = chats_list
        local_db_table["chats"] = chats_table
        print("local_db_table again:" + str(local_db_table))
        print("store message line:14")
        db_manager_object.saveData("D:\Work\Projects\Project Two\App\dbl.dat", local_db_table)
        print("store message line:15")
    def messageDisplayer(self, message, _from, _to, ui_object = None):
        message_table = self.formMessageTable(message, _from)
        self.storeReceivedMessagesLocally(_from, _to, message)
        print("Message Table:"+str(message_table))
        ui_object.new_chats.append(message_table)
        print("New Chats:"+str(ui_object.new_chats))
        try:
            chat_space_box = ui_object.children
            child = ui_object.children
            screen_child = child[0]
            chat_space_box = screen_child.children[0]
            chat_box = chat_space_box.chat_box_object()
            chat_box.chat_box_object.text = message
            chat_space_box.chats_list_object.add_widget(chat_box)
            self.storeReceivedMessagesLocally(_from, _to, message, message_view = 1)
        except:
            print("Failure")
    
