import terrascript
import terrascript.provider
import terrascript.resource
import json
import terrascript.data
import ipaddress 
with open('./data/subnet-list.json') as data_subnet:
  json_subnet = json.load(data_subnet)

with open('./data/creds.json') as aws_creds:
  creds = json.load(aws_creds)   

with open('./data/data.json') as data_file:
  data = json.load(data_file)   
  
config = terrascript.Terrascript()





config += terrascript.resource.aws_security_group(
  "aws-adds-sg",
    name = "aws-adds-sg",
    vpc_id  = "${aws_vpc.littleobi-vpc.id}",
    tags={
        "Flag"          : "ConfigRequired",
        "Access"        : "Restriced",
        "Type"          : "Production",
        "Purpose"       : "AWS-ADDS",
        "ParentRes"     : "AWS-ADDS-INST",
        "Creator"       : "Tarak Patel",
        "CreationMethod": "terraform",
        "Name"          : "aws-adds-sg",
        }
)


config += terrascript.resource.aws_security_group(
  "aws-image-builder-sg",
    name = "aws-image-builder-sg",
    vpc_id  = "${aws_vpc.littleobi-vpc.id}",
    tags={
        "Flag"          : "ConfigRequired",
        "Access"        : "Private",
        "Type"          : "Production",
        "Purpose"       : "LittleOBI",
        "Creator"       : "Tarak Patel",
        "CreationMethod": "terraform",
        "Name"          : "aws-image-builder-sg",
        }
)



config += terrascript.resource.aws_security_group(
  "packer-windows-sg",
    name = "packer-windows-sg",
    vpc_id  = "${aws_vpc.littleobi-vpc.id}",
    tags={
        "Flag"          : "ConfigRequired",
        "Access"        : "Private",
        "Type"          : "Production",
        "Purpose"       : "LittleOBI",
        "Creator"       : "Tarak Patel",
        "CreationMethod": "terraform",
        "Name"          : "packer-windows-sg",
        }
)

with open('../output/secuirty_group.network.aws.tf.json', 'w', encoding='utf-8') as config_file_tf:
  json.dump(config,config_file_tf,ensure_ascii=False, indent=4)