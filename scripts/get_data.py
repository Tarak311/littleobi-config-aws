import json
import terrascript
import terrascript.provider
import terrascript.resource
import terrascript.data
import ipaddress 

def get_data(creds,json_subnet,data):
    with open('./data/data.json') as data_file:
        data = json.load(data_file)   

    with open('./data/creds.json') as aws_creds:
        creds = json.load(aws_creds)   

    with open('./data/subnet-list.json') as data_subnet:
        json_subnet = json.load(data_subnet)


def get_main_route_table(route_table_type,xconfig):
    xconfig += terrascript.data.aws_route_table(
                "littleobi-rt-"+ route_table_type,
                filter = {
                    "name"   : "tag:Access",
                    "values" : [route_table_type],
                    }
            )
        
def get_route_table(route_table_type,xconfig,name):
    xconfig += terrascript.data.aws_route_table(
                "littleobi-rt-"+ route_table_type,
                filter = {
                    "name"   : "tag:Name",
                    "values" : [name],
                    }
            )