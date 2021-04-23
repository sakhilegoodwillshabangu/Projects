from wsgiref.util import setup_testing_defaults, request_uri
from wsgiref.simple_server import make_server
import urllib
import random
import time
import db
class User(db.Model):
    user_name = str
    user_surname = str
    user_email = str
    transaction_path_node = dict
class UserProfilePicture(db.Model):
    user = str
    image_file_content = str
class Wallet(db.Model):
    user = str
    available_amount = float
    currency = str
    wallet_pin = str
class Transaction(db.Model):
    prev_hash = str
    next_hash = str
    sender_key = str
    reciever_key = str
    amount = float
    currency = str
    time = str
class TransactionBlock(db.Model):
    root_hash = str
    height = int
    root_amount = float
    currency = str
    time = str
    current_amount = float
    transactions = list
    block_starter = str
class EndPoint(db.Model):
    block_starter = str
    amount = float
    currency = str
    root_hash = str
    time = str
class Peers(db.Model):
    user = str
    peers_list = list
def generateHashKey():
    key_string = ""
    digit_list = range(256)
    random.shuffle(digit_list)
    length = len(digit_list)
    digit_list = digit_list[:length/2]
    for item in digit_list:
        key_string += hex(item)[2:]
    key_string = key_string.upper()
    return key_string
class paramRequest:
    def __init__(self, environ):
        self.router, self.table = getRoute(environ)
    def get(self, param_key):
        if self.table != None:
            try:
                return self.table[param_key]
            except:
                return None
        else:
            return None
class ResponseHandler:
    def __init__(self, environ):
        self.response_message = ""
    def redirect(self, response_string = ""):
        self.response_message = response_string
    def write(self, response_string = ""):
        self.response_message = response_string
class RequestHandler:
    def __init__(self, environ):
        self.response = ResponseHandler(environ)
        self.request = paramRequest(environ)
        if environ["REQUEST_METHOD"] == "GET":
            self.get()
        elif environ["REQUEST_METHOD"] == "POST":
            self.post()
        elif environ["REQUEST_METHOD"] == "PUT":
            self.put()
    def get(self):
        pass
    def post(self):
        pass
    def put(self):
        pass
class LoginHandler(RequestHandler):
    def post(self):
        user_email_address = urllib.unquote(self.request.get("email_address"))
        print("my email is = " + user_email_address)
        wallet_pin = self.request.get("wallet_pin")
        print("my wallet in = " + wallet_pin)
        query = db.Query(User)
        query = query.filterData("user_email", user_email_address)
        results = query.fetchData(1)
        if len(results) > 0:
            user_key = results[0]
            wallet_query = db.Query(Wallet)
            wallet_query = wallet_query.filterData("user", user_key)
            wallet_query = wallet_query.filterData("wallet_pin", wallet_pin)
            print(wallet_pin)
            second_results = wallet_query.fetchData(1)
            print(second_results)
            print(len(second_results))
            if len(second_results) > 0:
                print("You are logged in")
        else:
            self.response.write("False")
class SignUpHandler(RequestHandler):
    def post(self):
        user_name = self.request.get("user_name")
        user_surname = self.request.get("user_surname")
        user_email = urllib.unquote(self.request.get("email_address"))
        wallet_pin = self.request.get("wallet_pin")
        print(user_name)
        print(user_surname)
        print(user_email)
        print(wallet_pin)
        query = db.Query(User)
        query = query.filterData("user_email", user_email)
        results = query.fetchData(1)
        if len(results) > 0:
            object_instance = query._object()
            key = query.query_table[object_instance.generateModelKey()].keys()[0]
            query = db.Query(Wallet)
            query.filterData("user", key)
            self.response.write("False")
        else:
            print("Registering new user")
            user = User(user_name = user_name, user_surname = user_surname, user_email = user_email, transaction_path_node = dict())
            user_key = user.save()
            wallets = Wallet(user = user_key, available_amount = 0.00, currency = "R", wallet_pin = wallet_pin)
            wallets.save()
            peers = Peers(user = user_key, peers_list = [])
            print(user_key)
            self.response.write(str(user_key))
            peers.save()
            print("New user Registerd")
            
def walletAmountAlt(amount_alt, object_key):
    query = db.Query(Wallet)
    query = query.filterData("user", object_key)
    results = query.fetchData(1)
    wallet = Wallet()
    field = int(query.fetchField(results[0], wallet.generateModelKey(), "available_amount"))
    amount_struct = {"available_amount":field + amount_alt}
    wallet.update(amount_struct, results[0], wallet.generateModelKey())
def checkWalletAvailableBalance(object_key):
    wallet = Wallet()
    query = db.Query(Wallet)
    query = query.filterData("user", object_key)
    results = query.fetchData(1)
    available_amount = query.fetchField(results[0], wallet.generateModelKey(), "available_amount")
    currency = query.fetchField(results[0], wallet.generateModelKey(), "currency")
    return available_amount, currency
def checkAmountQualification(field_amount, amount):
    if int(field_amount) > int(amount):
        return True
    else:
        return False
class FormBlockHandler(RequestHandler):
    def post(self):
        user_key = self.request.get("key")
        amount = self.request.get("amount")
        current_time = time.ctime()
        new_hash = generateHashKey()
        self.makeTransactionBlock(new_hash, float(amount), current_time, user_key)
        self.makeEndPoint(user_key, current_time, amount, user_key)
        self.formTransactionNode(user_key, new_hash)
        walletAmountAlt(float(amount), user_key)
    def makeTransactionBlock(self, hash_key, amount, time, object_key, currency = "R"):
        transaction_block = TransactionBlock(root_hash = hash_key, height = 0,
                                              root_amount = amount, current_amount = amount,
                                              block_starter = object_key, time = time, transactions = list(), currency = currency)
        transaction_block.save()
    def makeEndPoint(self, hash_key, time, amount, object_key, currency = "R"):
        end_point = EndPoint(root_hash = hash_key, time = time, amount = amount, block_starter = object_key, currency = currency)
        end_point.save()
    def formTransactionNode(self, object_key, hash_key):
        user = User()
        query = db.Query(User)
        node_struct = query.fetchField(object_key, user.generateModelKey(), "transaction_path_node")
        sub_struct = {"prev":hash_key, "next":generateHashKey()}
        node_struct[hash_key] = sub_struct
        user.update({"transaction_path_node":node_struct}, object_key, user.generateModelKey())
class TransferMoneyHandler(RequestHandler):
    def post(self):
        print("am in transfer money handler class")
        sender_user_key = self.request.get("sender_key")
        print("s_key === " + sender_user_key)
        reciever_user_key = self.request.get("reciever_key")
        print("r_user_key == " + reciever_user_key)
        amount = self.request.get("amount")
        print(amount)
        self.transferMoney(sender_user_key, reciever_user_key, amount, time.ctime())
    def getTransactionBlockCurrentAmount(self, object_key):
        transaction_block = TransactionBlock()
        query = db.Query(TransactionBlock)
        query = query.filterData("block_starter", object_key)
        results = query.fetchData(1)
        if len(results) > 0:
            current_amount = query.fetchField(results[0], transaction_block.generateModelKey(), "current_amount")
            return current_amount
        else:
            return -1
    def getNodes(self, object_key):
        user = User()
        query = db.Query(User)
        nodes = query.fetchField(object_key, user.generateModelKey(), "transaction_path_node")
        return nodes
    def makeNodesTable(self, hash_key, amount, node_table, nodes):
        item_tuple = (hash_key, nodes[hash_key]["prev"], nodes[hash_key]["next"], amount)
        node_table.append(item_tuple)
        return node_table
    def getContributingNodes(self, nodes, amount, object_key):
        total = 0
        nodes_table = []
        for item in nodes:
            current_amount = int(self.getTransactionBlockCurrentAmount(object_key))
            amount = int(amount)
            if current_amount >= amount:
                nodes_table = self.makeNodesTable(item, amount, nodes_table, nodes)
                return nodes_table
            elif (current_amount < amount) and (amount > (current_amount + total)):
                total = total + current_amount
                nodes_table = self.makeNodesTable(item, current_amount, nodes_table, nodes)
            elif (current_amount < amount) and ((current_amount + amount) > amount):
                contributing_amount = amount - current_amount
                nodes_table = self.makeNodesTable(item, contributing_amount, nodes_table, nodes)
                return nodes_table
        return []
    def recordTransactionBlock(self, sub_nodes_list, sender_object_key, transaction_object_key, amount):
        transaction_block = TransactionBlock()
        for node in sub_nodes_list:
            query = db.Query(TransactionBlock)
            query = query.filterData("root_hash", node[0])
            results = query.fetchData(1)
            if len(results) > 0:
                transaction_block_current_amount = query.fetchField(results[0], transaction_block.generateModelKey(), "current_amount")
                transaction_list = query.fetchField(results[0], transaction_block.generateModelKey(), "transactions")
                height = query.fetchField(results[0], transaction_block.generateModelKey(), "height")
                new_height = height + 1
                transaction_block_current_amount = transaction_block_current_amount - node[3]
                transaction_list.append(transaction_object_key)
                update_struct = {"root_hash":node[0],
                                 "height":new_height,
                                 "transactions":transaction_list,
                                 "current_amount":transaction_block_current_amount}
                transaction_block.update(update_struct, results[0], transaction_block.generateModelKey())
    def updateSenderNode(self, contributing_block_node_list, object_key):
        user = User()
        query = db.Query(User)
        nodes_struct = query.fetchField(object_key, user.generateModelKey(), "transaction_path_node")
        for node in contributing_block_node_list:
            sub_struct = {"prev":node[1], "next":generateHashKey()}
            nodes_struct[node[0]] = sub_struct
        user.update({"transaction_path_node":nodes_struct}, object_key, user.generateModelKey())
    def updateRecieverNode(self, contributing_block_node_list, object_key):
        user = User()
        query = db.Query(User)
        nodes_struct = query.fetchField(object_key, user.generateModelKey(), "transaction_path_node")
        for node in contributing_block_node_list:
            sub_struct = {"prev":node[2], "next":generateHashKey()}
            nodes_struct[node[0]] = sub_struct
        user.update({"transaction_path_node":nodes_struct}, object_key, user.generateModelKey())
    def transferMoney(self, sender_object_key, reciever_object_key, amount, time):
        field_amount, currency = checkWalletAvailableBalance(sender_object_key)
        print(currency + str(field_amount))
        out_put = checkAmountQualification(field_amount, amount)
        print(out_put)
        if out_put:
            nodes = self.getNodes(sender_object_key)
            print("sender nodes == " + str(nodes))
            contributing_block_node = self.getContributingNodes(nodes, amount, sender_object_key)
            print("Contributing Nodes == " + str(contributing_block_node))
            for node in contributing_block_node:
                transaction = Transaction()
                transaction.prev_hash = node[1]
                transaction.next_hash = node[2]
                transaction.sender_key = sender_object_key
                transaction.reciever_key = reciever_object_key
                transaction.amount = node[3]
                transaction.currency = "R"
                transaction.time = time
                transaction_key = transaction.save()
            self.recordTransactionBlock(contributing_block_node, sender_object_key, transaction_key, amount)
            self.updateSenderNode(contributing_block_node, sender_object_key)
            self.updateRecieverNode(contributing_block_node, reciever_object_key)
            walletAmountAlt(-int(amount), sender_object_key)
            walletAmountAlt(int(amount), reciever_object_key)
class WalletHandler(RequestHandler):
    def post(self):
        user_key = self.request.get("key")
        available_amount, currency = checkWalletAvailableBalance(user_key)
        self.response.write(currency + str(available_amount))
class AddPeerHandler(RequestHandler):
    def post(self):
        user_key = self.request.get("key")
        peer_email = urllib.unquote(self.request.get("user_email_address"))
        self.addPeer(peer_email, user_key)
    def addPeer(self, peer_email, current_user_key):
        query = db.Query(User)
        query = query.filterData("user_email", peer_email)
        print("my peer email is = " + str(peer_email))
        results = query.fetchData(1)
        if len(results) > 0:
            peers = Peers()
            query = db.Query(Peers)
            print("am in add peer")
            query = query.filterData("user", current_user_key)
            peer_key_results = query.fetchData(1)
            peers_list = query.fetchField(peer_key_results[0], peers.generateModelKey(), "peers_list")
            peers_list.append(results[0])
            pre_update_struct = {"peers_list":peers_list}
            peers.update(pre_update_struct, peer_key_results[0], peers.generateModelKey())
            print(peers_list)
            self.response.write("True")
        else:
            self.response.write("False")
class PeersHandler(RequestHandler):
    def post(self):
        user_key = self.request.get("key")
        list_out_put = self.listPeers(user_key)
        print("am in post peers handler")
        print(list_out_put)
    def listPeers(self, object_key):
        peers = Peers()
        query = db.Query(Peers)
        query = query.filterData("user", object_key)
        peer_key_results = query.fetchData(1)
        if len(peer_key_results) > 0:
            peer_list = query.fetchField(peer_key_results[0], peers.generateModelKey(), "peers_list")
            return peer_list
        else:
            []
class ImageRequestHandler(RequestHandler):
    def put(self):
        user_key = self.request.get("key")
        user_profile_picture = self.request.get("profile_picture")
        print("my user key is = " + user_key)
        print("my profile_picture = " + user_profile_picture)
        query = db.Query(UserProfilePicture)
        query = query.filterData("user", user_key)
        results = query.fetchData(1)
        if len(results) > 0:
            user_profile_picture_model = UserProfilePicture()
            table = {"image_file_content":user_profile_picture}
            user_profile_picture_model.update(table, results[0], user_profile_picture_model.generateModelKey())
        else:
            user_profile_picture_model = UserProfilePicture(image_file_content = user_profile_picture, user = user_key)
            user_profile_picture_model.save()
    def get(self):
        pass
class MainHandler(RequestHandler):
    def get(self):
        self.redirect("Hello world Sakhile")
    def post(self):
        return "Post Hello world"
def tablelise(data_string):
    d = dict()
    param_string = data_string
    while len(param_string) > 0:
        if "&" in param_string:
            d[param_string[:param_string.index("=")]] = param_string[param_string.index("=") + 1:param_string.index("&")]
            param_string = param_string[param_string.index("&") + 1:]
        else:
            d[param_string[:param_string.index("=")]] = param_string[param_string.index("=") + 1:]
            param_string  = ""
    return d
def getRoute(environ):
    request_address = request_uri(environ)
    print("request address = "+str(request_address))
    request_address = request_address.replace("http://", "")
    slash_index = request_address.index("/")
    data_string = request_address[slash_index:]
    print(data_string)
    try:
        param_string_index = data_string.index("?")
        router = request_address[slash_index + 1:request_address.index("?")]
        print(router)
        param_string = data_string.replace(data_string[:param_string_index + 1], "")
        table = tablelise(param_string)
    except:
        param_string_index = data_string.index("/")
        try:
            second_slash_index = data_string[param_string_index + 1:].index("/")
            router = data_string[:second_slash_index+1]
            return router, table
        except:
            router = data_string[param_string_index + 1:] + "/"
            print("on except" + router)
            return router, None
    return router, table
def routeHanlders(router, handler_routes, environ):
    table = dict(handler_routes)
    print("router is ="+str(router))
    if router in table:
        handler = table[router]
        print("rout:"+router+"is being handled")
        handler_object = handler(environ)
    else:
        print("Main is being called")
        handler_object = MainHandler(environ)
    return handler_object
def simple_app(environ, start_response, handler_routes = [("/", MainHandler),
                                                          ("login/", LoginHandler),
                                                          ("signUp/", SignUpHandler),
                                                          ("formBlock/", FormBlockHandler),
                                                          ("walletBalance/", WalletHandler),
                                                          ("addPeer/", AddPeerHandler),
                                                          ("peers/", PeersHandler),
                                                          ("ImageFile/", ImageRequestHandler),
                                                          ("transferMoney/", TransferMoneyHandler)]):
    setup_testing_defaults(environ)
    status = "200 OK"
    headers = [("Content-type", "text/plain")]
    start_response(status, headers)
    
    router, table = getRoute(environ)
    handler_object = routeHanlders(router, handler_routes, environ)
    ret = ["%s: %s\n" % (key, value)
           for key, value in environ.iteritems()]
    return handler_object.response.response_message
httpd = make_server("", 8000, simple_app)
print("Serving on port 8000...")
httpd.serve_forever()
