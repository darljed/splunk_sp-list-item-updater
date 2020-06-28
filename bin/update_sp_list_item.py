import os
import sys
import time
import datetime
import json
import splunk.Intersplunk
import settings
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from office365.runtime.client_request import ClientRequest
from office365.runtime.utilities.http_method import HttpMethod
from office365.runtime.utilities.request_options import RequestOptions


# print sys.argv
configEntry=None
list_title=None
field2update=None 
updateValue=None 
itemID=None
goFlag=False
try:
    configEntry=sys.argv[1]

    list_title= settings.settings[configEntry]["list_title"]
    field2update= sys.argv[3]
    updateValue=sys.argv[4]
    itemID=sys.argv[2]
    goFlag=True
except Exception as inst:
    print("Result")
    print("Error: Incomplete Argument provided or entry mismatch- {0}".format(inst))
# field2update= "type"
# updateValue="Sample Test Value"
# itemID=2


def update_list_item2(context, list_title, item_id):
    """Update list item example"""
    request = ClientRequest(context)
    options = RequestOptions(
        settings.settings[configEntry]['url']+"/_api/web/lists/getbyTitle('{0}')/items({1})".format(list_title, item_id))
    options.set_header('Accept', 'application/json; odata=nometadata')  # JSON Light nometadata mode!
    options.set_header('IF-MATCH', '*')
    options.set_header('X-HTTP-Method', 'MERGE')
    options.data = {field2update: updateValue}
    options.method = HttpMethod.Post
    data = request.execute_request_direct(options)
    try:
        print(data["odata.error"])
        # s = json.loads(data.content);
    except:
        print("Result")
        print("Success")

if __name__ == '__main__':
    if(goFlag):
        ctx_auth = AuthenticationContext(url=settings.settings[configEntry]['url'])
        # if ctx_auth.acquire_token_for_user(username=settings.settings['user_credentials']['username'], password=settings.settings['user_credentials']['password']): #used for user based login
        if ctx_auth.acquire_token_for_app(client_id=settings.settings[configEntry]['client_credentials']['client_id'], client_secret=settings.settings[configEntry]['client_credentials']['client_secret']): #used for app based login
            ctx = ClientContext(settings.settings[configEntry]['url'], ctx_auth)


            update_list_item2(ctx,list_title,itemID)
        else:
            print (ctx_auth.get_last_error())