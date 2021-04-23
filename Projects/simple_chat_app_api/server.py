from socket import *
from db_manager import *
import time
class Server:
    def __init__(self, ip_address = "localhost", port = 50007):
        self.host_address = ip_address
        self.port_address = port
        self.socket_object = socket(AF_INET, SOCK_STREAM)
        self.socket_object.bind((self.host_address, self.port_address))
        self.socket_object.listen(5)
        self.handler_routes = {"SignUp": self.requestSignUpHandler,
                               "Login": self.requestLoginHanlder,
                               "FriendsList":self.requestFriendsListHandler,
                               "SendMessage":self.requestChatHandler,
                               "Address":self.requestAddressHandler,
                               "UnseenMessages":self.requestUnseenMessagesHandler}
    def routeRequest(self, data_received, address):
        print(data_received)
        try:
            print("routeRequest function Line:1")
            router = data_received[0:data_received.index(":")]
            print("routeRequest function Line:2")
            param_table = eval(data_received[data_received.index(":") + 1:])
            print("routeRequest function Line:3")
            print(param_table)
            if router in ["SignUp", "Login"]:
                print("routeRequest function Line:4")
                handler_output = self.handler_routes[router](param_table, address)
                print("routeRequest function Line:5")
            else:
                print("routeRequest function Line:6")
                handler_output = self.handler_routes[router](param_table)
                print("routeRequest function Line:7")
            return handler_output
        except:
            print("request received")
            return ""
    def receiveRequest(self, connection, address):
        while True:
            data = connection.recv(10240)
            print(data)
            if not data:
                break
            handler_return = self.routeRequest(data, address)
            if handler_return:
                print("handler:--------"+str(handler_return) + "---------")
                connection.send(b"(1, " + str(handler_return) +")")
            else:
                connection.send(b"(1, '')")
    def requestAddressHandler(self, param):
        print("am on request address handler function")
        key = param["key"]
        db_manager = DatabaseManager()
        db_table = db_manager.loadData("db.dat")
        sub_table = db_table[key]
        address = sub_table["client_address"]
        return address
    def sigUpParamQuery(self, db_object, name):
        table = db_object.loadData("db.dat")
        for key in table:
            if table[key]["name"] == name:
                return 1
            else:
                return 0
    def requestSignUpHandler(self, param, address):
        print("Am on Sign up")
        db_manager_object = DatabaseManager()
        user_name = param["name"]
        user_password = param["password"]
        query_output = self.sigUpParamQuery(db_manager_object, user_name)
        if query_output == 0:
            db_table = db_manager_object.loadData("db.dat")
            key = db_manager_object.generateObjectKey()
            sub_table = dict()
            sub_table["name"] = user_name
            sub_table["password"] = user_password
            sub_table["chat"] = dict()
            sub_table["new_messages"] = 0
            sub_table["client_address"] = address
            db_table[key] = sub_table
            db_manager_object.saveData("db.dat", db_table)
            return "'"+key+"'"
        else:
            return ""
    def loginParamQuery(self, db_object, name, password, address):
        table = db_object.loadData("db.dat")
        for key in table:
            print("Login crede=="+name + "  " + password)
            if (table[key]["name"] == name) and (table[key]["password"] == password):
                print(str(table[key]["name"]) +":"+ name)
                print(str(table[key]["password"]) +":"+ password)
                sub_table = table[key]
                sub_table["client_address"] = address
                table[key] = sub_table
                db_object.saveData("db.dat", table)
                print(key)
                return "'"+key+"'"
        return ""
    def requestLoginHanlder(self, param, address):
        print("Am on Login")
        db_manager_object = DatabaseManager()
        print("Login Line:"+str(2))
        user_name = param["name"]
        print("Login Line:"+str(3))
        user_password = param["password"]
        print("Login Line:"+str(4))
        query_output = self.loginParamQuery(db_manager_object, user_name, user_password, address)
        print("Login Line:"+str(5))
        return query_output
    def queryFriendsList(self, db_object, key):
        table = db_object.loadData("db.dat")
        friends_list = []
        for _key in table:
            if _key == key:
                print("Keys are Equal")
                print(_key)
                print("_______________________________________________________")
                print(key)
            elif _key != key:
                print("Keys Not Equal")
                friends_list.append([_key, table[_key]["name"]])
        return friends_list
    def requestFriendsListHandler(self, param):
        print("Am on friends list")
        db_manager_object = DatabaseManager()
        user_key = param["key"]
        query_output = self.queryFriendsList(db_manager_object, user_key)
        return query_output
    def storeChatData(self, db_object, _from, _to, message):
        table = db_object.loadData("db.dat")
        _sending_user_name = table[_from]["name"]
        messages_info = table[_to]["chat"]
        user_chat_data = {"name":_sending_user_name, "key":_from, "message":message, "time":time.ctime()}
        messages_info.append(user_chat_data)
        table[_to]["chat"] = messages_info
        number_of_new_messages = table[_to]["new_messages"]
        table[_to]["new_messages"] = int(number_of_new_messages) + 1
        db_object.saveData("db.dat", table)
        return 1
    def requestChatHandler(self, param):
        message_from = param["from"]
        message_to = param["to"]
        message = param["message"]
        db_manager_object = DatabaseManager()
        received_data = self.storeChatData(db_manager_object, message_from, message_to, message)
        return received_data
    def requestUnseenMessagesHandler(self, param):
        print("Unseen Messages Line:"+str(1))
        key = param["key"]
        print("Unseen Messages Line:"+str(2))
        db_manager_object = DatabaseManager()
        print("Unseen Messages Line:"+str(3))
        table = db_manager_object.loadData("db.dat")
        print("Unseen Messages Line:"+str(4))
        chats_list = table[key]["chat"]
        table[key]["chat"] = []
        table[key]["new_messages"] = 0
        print("Unseen Messages Line:"+str(5))
        db_manager_object.saveData("db.dat", table)
        print("Number of new messages:"+str(len(chats_list)))
        return chats_list
if __name__ == "__main__":
    server_object = Server()
    while True:
        connection, address = server_object.socket_object.accept()
        server_object.receiveRequest(connection, address)
        connection.close()
