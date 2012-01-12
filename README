Introduction
============
Datautils is used for caching the data as persistent. It's used in situations when we want to 
store the data locally instead of burden the data-server too much. It provides functionality 
for saving data as persistent into the given "tool". Tool is a persistent "dataobject" which 
contains peristent data-structure like BTree. ToolHandler converts all the dicts and lists 
inside of OOBTree into a PersistentDict or PersistentList and sideways when we want to read 
the data from it.

Usage
-----

First we must create the tool and inside of it a data-structure that acts like dict-type. This 
product is tested with OOBTree only, but it should work with every dict-like BTree. Here we
create a tool that installs itself during product installation::
   
    from BTrees.OOBTree import OOBTree
    from OFS.SimpleItem import SimpleItem
    from Globals import InitializeClass
    from Products.CMFCore.utils import UniqueObject

    class MyTool(UniqueObject, SimpleItem):
        id = 'my_tool'
        description = 'tool for handling my data'

        def __init__(self):
            UniqueObject.__init__(self)
            SimpleItem.__init__(self)

            # Create a map data-structure for data
            self.query = OOBTree()

        # This is needed when you need to register the tool
        # during installation of the product
        plone_tool = 1

    # Init class during product installation
    InitializeClass(MyTool)

If we want the installation of the tool work, we need to add this to profiles/default/toolset.xml::

    <?xml version="1.0" encoding="UTF-8"?>
      <required tool_id="my_tool"
           class="my.product.mymodule.MyTool"/>

After creating a tool, we need to make an interface for our product which uses the ToolHandler correctly. In querydata.py
module we have a base class 'BaseHandler' for that so we don't have to create it from scratch. In our handler class we should
inherit it from BaseHandler and override methods "get_tool_data()" and "update()"::

    from jyu.datautils.querydata import BaseHandler
    from my.product.utility import get_data

    class MyToolHandler(BaseHandler):

    # Return our data-structure from the tool
    def get_tool_data(self):
        portal_url = getToolByName(self.context, 'portal_url')
        self.root = portal_url.getPortalObject()
        return self.root.my_tool.query

    # create data usin save() or update() method
    # Parameters:
    # query = dict which contains the parameters from our query
    # save() -method saves the query as a new reference to match the given result
    # update() -method updates the data without acting like a new reference
    def update(self, query):
        # Get results 
        result = get_data(query)
        # Save the key with result
        self.save(query, result)
        #self.update(query, result)





 
