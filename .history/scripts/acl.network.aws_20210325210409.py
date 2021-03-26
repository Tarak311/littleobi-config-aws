import terrascript
import terrascript.provider
import terrascript.resource
import json
import terrascript.data
import ipaddress 
import get_subnets
with open('./data/subnet-list.json') as data_subnet:
  json_subnet = json.load(data_subnet)

with open('./data/creds.json') as aws_creds:
  creds = json.load(aws_creds)   

with open('./data/data.json') as data_file:
  data = json.load(data_file)   


config = terrascript.Terrascript()

public_subnets = []
private_subnets = []
secured_subnets = []


get_subnets.get_public_subnets(public_subnets,config)

get_subnets.get_private_subnets(private_subnets,config)

get_subnets.get_secured_subnets(secured_subnets,config)


    
config += terrascript.resource.aws_network_acl(
  "littleobi-pub-acl",
  subnet_ids = public_subnets,
  vpc_id = "${aws_vpc.littleobi-vpc.id}",
  tags={
        "Flag"          : "Compliant",
        "Access"        : "Public",
        "Type"          : "Production",
        "Purpose"       : "LittleOBI",
        "Creator"       : "Tarak Patel",
        "CreationMethod": "terraform",
        "Name"          : "littleobi-pub-acl",
        }
)

config += terrascript.resource.aws_network_acl(
  "littleobi-priv-acl",
  subnet_ids = private_subnets,
  vpc_id = "${aws_vpc.littleobi-vpc.id}",
  tags={
        "Flag"          : "Compliant",
        "Access"        : "Private",
        "Type"          : "Production",
        "Purpose"       : "LittleOBI",
        "Creator"       : "Tarak Patel",
        "CreationMethod": "terraform",
        "Name"          : "littleobi-priv-acl",
        }
)


config += terrascript.resource.aws_network_acl(
  "littleobi-open-acl",
  vpc_id = "${aws_vpc.littleobi-vpc.id}",
  tags={
        "Flag"          : "Compliant",
        "Access"        : "Open",
        "Type"          : "Production",
        "Purpose"       : "LittleOBI",
        "Creator"       : "Tarak Patel",
        "CreationMethod": "terraform",
        "Name"          : "littleobi-open-acl",
        }
)

config += terrascript.resource.aws_network_acl(
  "littleobi-sec-acl",
  subnet_ids = secured_subnets,
  vpc_id = "${aws_vpc.littleobi-vpc.id}",
  tags={
        "Flag"          : "Compliant",
        "Access"        : "Secured",
        "Type"          : "Production",
        "Purpose"       : "LittleOBI",
        "Creator"       : "Tarak Patel",
        "CreationMethod": "terraform",
        "Name"          : "littleobi-sec-acl",
        }
)

with open('../output/acl.network.aws.tf.json', 'w', encoding='utf-8') as config_file_tf:
  json.dump(config,config_file_tf,ensure_ascii=False, indent=4)