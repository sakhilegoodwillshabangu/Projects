import pickle
import random
import os
object_fields = {}
def saveData(db_file_name, data_table):
    file_object = open(db_file_name, "wb")
    pickle.dump(data_table, file_object)
    file_object.close()
def loadData(db_file_name):
    try:
        file_object = open(db_file_name, "rb")
        db_table = pickle.load(file_object)
    except:
        file_object = open(db_file_name, "wb")
        pickle.dump(dict(), file_object)
        file_object.close()
        return dict()
    file_object.close()
    return db_table
class Query:
    def __init__(self, _object):
        self._object = _object
        self.query_table = dict()
        print("pre query_table="+str(self.query_table))
    def fetchData(self, object_limit):
        object_instance = self._object()
        table_len = len(self.query_table)
        print("table_len="+str(table_len))
        try:
            keys_list = self.query_table[object_instance.generateModelKey()].keys()
        except:
            return []
        if object_limit >= table_len:
            return keys_list
        else:
            return keys_list[:object_limit]
    def filterData(self, field, _input):
        object_instance = self._object()
        db_table = loadData("dbFile")
        try:
            sub_table = db_table[object_instance.generateModelKey()]
        except:
            return self
        if getattr(object_instance, field) == type(_input):
            keys_list = sub_table.keys()
            for key in keys_list:
                for key_field in sub_table[key]:
                    if key_field == field:
                        if sub_table[key][key_field] == _input:
                            x=dict()
                            x[key] = sub_table[key]
                            self.query_table[object_instance.generateModelKey()] = x
                            return self
        else:
            print("Wrong type")
            print(field)
        return self
    def fetchField(self, object_key, model_key, field_string):
        table = loadData("dbFile")
        print(table[model_key][object_key])
        field = table[model_key][object_key][field_string]
        return field
    def deleteObject(self, object_key):
        object_instance = self._object()
        db_table = loadData("dbFile")
        del db_table[object_instance.generateModelKey()][object_key]
        del self.query_table[object_instance.generateModelKey()][object_key]
        saveData("dbFile", db_table)
class Model:
    _locals = locals()
    def __init__(self, **arg):
        self.collectInitKeywordArg(**arg)
    def generateModelKey(self):
        hexa_string = ""
        item_list = []
        for item in dir(self):
            if item not in self._locals:
                item_list.append(item)
        hexa_string = self.collectVars(item_list)
        return hexa_string
    def collectInitKeywordArg(self, **arg):
        
        l=locals()
        arguments = l["arg"]
        for key, arg_key in zip(arguments, arg):
            if key in dir(self):
                
                if getattr(self, arg_key) == type(arguments[key]):
                    global object_fields
                    object_fields[key] = arguments[key]
                else:
                    print("Wrong type")
            else:
                print("Wrong Attr!")
        print(object_fields)
    def convertAlphaToDigit(self, alpha_string):
        output_string = ""
        for alpha in alpha_string:
            integer = ord(alpha)
            hexadecimal = hex(integer)
            output_string = output_string + hexadecimal[2:].upper()
        return output_string
    def collectVars(self, attr_keys):
        hexa_string = ""
        counter = 0
        for key in attr_keys:
            if key in dir(self):
                output_string = self.convertAlphaToDigit(key)
                hexa_string = hexa_string + output_string
            counter += 1
        _object_locals = locals()
        _object_string = str(_object_locals["self"])
        _object_name_start = _object_string.index(".") + 1
        _object_name_end = _object_string.index(" ")
        _object_name = _object_string[_object_name_start:_object_name_end]
        output_string = self.convertAlphaToDigit(_object_name)
        return (output_string + hexa_string)
    def generateObjectKey(self):
        key_string = ""
        digit_list = range(256)
        random.shuffle(digit_list)
        for item in digit_list:
            key_string += hex(item)[2:]
        key_string = key_string.upper()
        return key_string
    def __setattr__(self, attr, value):
        global object_fields
        local_table = locals()
        key = local_table["attr"]
        if key in dir(self):
            if getattr(self, key) == type(local_table["value"]):
                object_fields[key] = local_table["value"]
            else:
                print("Wrong Attr!")
        elif (key != "model_key"):
            print("Wrong Attr!")
    def __get__(self, attr, aa):
        print(self, attr, aa)
    def update(self, update_struct, object_key, model_key):
        table = loadData("dbFile")
        for key in update_struct:
            table[model_key][object_key][key] = update_struct[key]
        saveData("dbFile", table)
    def save(self):
        global object_fields
        print(object_fields)
        _object_key = self.generateObjectKey()
        model_key = self.generateModelKey()
        table = loadData("dbFile")
        db_table = table
        try:
            _object_table = table[model_key]
        except:
            _object_table = dict()
        _object_table[_object_key] = object_fields
        db_table[model_key] = _object_table
        saveData("dbFile", db_table)
        object_fields = dict()
        return _object_key
