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

config = terrascript.Terrascript()

config += terrascript.resource.aws_route_table(
    "littleobi-pub-rt",
     vpc_id  = "${aws_vpc.littleobi-vpc.id}",
    tags={
        "Flag"          : "Compliant",
        "Access"        : "Public",
        "Type"          : "Production",
        "Purpose"       : "LittleOBI",
        "Creator"       : "Tarak Patel",
        "CreationMethod": "terraform",
        "Name"          : "littleobi-pub-rt",
        }
)

config += terrascript.resource.aws_route_table(
    "littleobi-priv-rt",
    vpc_id  = "${aws_vpc.littleobi-vpc.id}",
    tags={
        "Flag"          : "Compliant",
        "Access"        : "Private",
        "Type"          : "Production",
        "Purpose"       : "LittleOBI",
        "Creator"       : "Tarak Patel",
        "CreationMethod": "terraform",
        "Name"          : "littleobi-priv-rt",
        }
)

config += terrascript.resource.aws_route_table(
    "littleobi-sec-rt",
    vpc_id  = "${aws_vpc.littleobi-vpc.id}",
    tags={
        "Flag"          : "Compliant",
        "Access"        : "Secured",
        "Type"          : "Production",
        "Purpose"       : "LittleOBI",
        "Creator"       : "Tarak Patel",
        "CreationMethod": "terraform",
        "Name"          : "littleobi-sec-rt",
        }
)


with open('../output/route_table.network.aws.tf.json', 'w', encoding='utf-8') as config_file_tf:
  json.dump(config,config_file_tf,ensure_ascii=False, indent=4)