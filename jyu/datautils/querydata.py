# -*- coding: utf-8 -*-

from jyu.datautils.persist import to_normal, to_persistent
import hashlib
import DateTime

class KeyGenerator():
    ''' Converts key from datastructure that contains lists and dicts 
        using hashlib sha1'''
    def __init__(self, query):
        self.keyhash = hashlib.sha1()
        self.query = query

    def to_safe_str(self, st):
        try:
            # The input should be unicode object.
            # So lets encode it to string
            return st.encode('utf8')
        except UnicodeError:
            # Oh, shit! It was probably just a normal string. We have to decode
            # it to unicode. Lets guess that it is latin1.
            unicode_ob = st.decode("latin1")
            return unicode_ob.encode("utf8")

    def to_list(self, data):
        try:
            return data.values()
        except AttributeError:
            return data

    def to_id(self, data):
        if type(data) in (str, unicode):
            # if it's a string or unicode update hash
            self.keyhash.update(self.to_safe_str(data))
            return

        try:
            for item in sorted(self.to_list(data)):
                self.to_id(item)
        except TypeError:
            self.to_id(str(data))

    def get_key(self):
        return self.keyhash.hexdigest()

    def generate(self):
        self.to_id(self.query)
        return self.get_key()

class ToolHandler:
    '''
    Handler which takes a tool, for example TutkaTool
    or KorppiTool and handles the data inside of these
    tools. Every tool has it own interface which
    uses this handler.
    '''
    def __init__(self, tool_data):
        self.tool_data = tool_data
    

    def add_query(self, query, result_query, new = None):
        # store as string the changes made
        result = ""

        # Generate _list for query and result. New-attribute
        # is for refcounter update. We need to know 
        # if the call was from edit
        result_key = KeyGenerator(result_query).generate()
        query_key = KeyGenerator(query).generate()
        # convert dicts to persistent 
        query = to_persistent(query)
        result_query = to_persistent(result_query)
        # If we already have the same query
        if self.tool_data.has_key(query_key):
            # Check if the result has changed
            result = str(DateTime.DateTime()) + " NO CHANGES for key '" + query_key + "'"
            if new != None:
                # new reference
                self.tool_data[query_key]['refcounter'] += 1
                result = str(DateTime.DateTime()) + " Created new reference in key '" + query_key + "'"
            elif self.tool_data[query_key]['result_key'] != result_key:
                self.tool_data[query_key]['result_key'] = result_key
                self.tool_data[query_key]['result_query'] = result_query
                result = str(DateTime.DateTime()) + " RESULTS UPDATED for key '" + query_key + "'"
        else:
            # If there isn't any query linked we create a new one
            _dict = {'result_key': result_key, 'result_query': result_query, 'query': query, 'refcounter': 1 }
            self.tool_data[query_key] = to_persistent(_dict)
        return result

        



    def remove_reference(self, query_key):
        # remove one reference, if there are
        # no references, delete key
        try:
            self.tool_data[query_key]['refcounter'] -= 1

            if self.tool_data[query_key]['refcounter'] == 0:
                self.tool_data.pop(query_key)
        except KeyError:
            pass
    def get_query(self, query):
        query_key = KeyGenerator(query).generate()
        return self.tool_data[query_key]

    def has_query(self,query):
        query_key = KeyGenerator(query).generate()
        return self.tool_data.has_key(query_key)

    def get_result(self, query):
        # make key fro mquery
        query_key = KeyGenerator(query).generate()
        try:
            # Return query as normal list and dict
            return to_normal(self.tool_data[query_key]['result_query'])

        except KeyError:
            return []
        except AttributeError:
            return []

class BaseHandler():
    ''' Base class for toolhandler. Overwrite these methods:
    get_tool :: return the tool we're using
    update :: get the data and save it using save method

    Provides basic operations for the handler which offers
    the interface for ToolHandling
    '''
    def __init__(self, context):
        self.context = context

    def add_obj(self, query):
        self.save(query, {})

    def get_tool_data(self):
        raise NotImplementedError("Method get_tool_data is not implemented")
            
    def handle(self, query):
        raise NotImplementedError("Method update is not implemented")

    def save(self, query, query_result):
        # Save persistent data to root
        ToolHandler(self.get_tool_data()).add_query(query, query_result, new=True)

    def update(self,query, query_result):
        return ToolHandler(self.get_tool_data()).add_query(query, query_result,new=None)

    def has_query(self, query):
        return ToolHandler(self.get_tool_data()).has_query(query)

    def get_result(self, query):
        return ToolHandler(self.get_tool_data()).get_result(query) 

    def get_query(self, query):
        return ToolHandler(self.get_tool_data()).get_query(query)

    def remove_reference(self, query):
        ToolHandler(self.get_tool_data()).remove_reference(query)

