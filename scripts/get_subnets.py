import terrascript
import terrascript.provider
import terrascript.resource
import json
import terrascript.data
import ipaddress 
import get_data

with open('./data/subnet-list.json') as data_subnet:
  json_subnet = json.load(data_subnet)

with open('./data/creds.json') as aws_creds:
  creds = json.load(aws_creds)   

with open('./data/data.json') as data_file:
  data = json.load(data_file)   

public_subnets = []
private_subnets = []
secured_subnets = []
config = terrascript.Terrascript()

def get_public_subnets(subnets,xconfig):
    for i in range(32):
        if (json_subnet['subnets'][i]["Access"] == "pub"):
            subnets.append("${data.aws_subnet.littleobi-subnet-pub-list-"+str(i)+".id}")
            xconfig += terrascript.data.aws_subnet(
                "littleobi-subnet-pub-list-"+str(i),
                filter = {
                    "name"   : "tag:No",
                    "values" : [str(i+1)],
                    }
            )
        



def get_private_subnets(subnets,xconfig):
    for i in range(32):
        if (json_subnet['subnets'][i]["Access"] == "priv"):
           subnets.append("${data.aws_subnet.littleobi-subnet-priv-list-"+str(i)+".id}")
           xconfig += terrascript.data.aws_subnet(
                "littleobi-subnet-priv-list-"+str(i),
                filter = {
                    "name"   : "tag:No",
                    "values" : [str(i+1)],
                    }
            )
        



def get_secured_subnets(subnets,xconfig):
    for i in range(32):
          if (json_subnet['subnets'][i]["Access"] == "secured"):
              subnets.append("${data.aws_subnet.littleobi-subnet-sec-list-"+str(i)+".id}")
              xconfig += terrascript.data.aws_subnet(
              "littleobi-subnet-sec-list-"+str(i),
              filter = {
                "name"   : "tag:No",
                "values" : [str(i+1)],
                }
    )
        
  
    