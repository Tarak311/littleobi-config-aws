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
security_config = terrascript.Terrascript()
config += terrascript.provider.aws(region=creds["region"],access_key=creds["access_key"],secret_key=creds["secret_key"])
config += terrascript.resource.aws_vpc(
    "littleobi-vpc",
    enable_dns_support=True,
    assign_generated_ipv6_cidr_block=True,
    enable_dns_hostnames=True,
    cidr_block="10.2.0.0/16",
    tags={
        "Flag"          : "Compliant",
        "Access"        : "Multivalue",
        "Type"          : "Production",
        "Purpose"       : "LittleOBI",
        "Creator"       : "Tarak Patel",
        "CreationMethod": "terraform",
        "Name"          : "littleobi-vpc",
        }
    )

config += terrascript.resource.aws_internet_gateway(
  "littleobi-igw",
  vpc_id = "${aws_vpc.littleobi-vpc.id}",
  tags={
        "Flag"          : "Compliant",
        "Access"        : "Multivalue",
        "Type"          : "Production",
        "Name"          : "littleobi-igw",
        }
)



config += terrascript.resource.aws_default_network_acl(
  "default-acl",
  default_network_acl_id = "${aws_vpc.littleobi-vpc.default_network_acl_id}",
  ingress = {
    "rule_no"    : "200",
    "protocol"       : "tcp",
    "action"    : "deny",
    "cidr_block"     : "0.0.0.0/0",
    "from_port"      : "22",
    "to_port"        : "22",
  },
  tags={
        "Flag"          : "Compliant",
        "Access"        : "Multivalue",
        "Type"          : "Production",
        "Name"          : "default-littleobi-acl",
        
        }
  )






config += terrascript.resource.aws_default_route_table(
   "default-rt",
  default_route_table_id = "${aws_vpc.littleobi-vpc.default_route_table_id}",
  tags={
        "Flag"          : "Compliant",
        "Access"        : "Multivalue",
        "Type"          : "Production",
        "Name"          : "default-littleobi-rt",
        
        }
)

config += terrascript.resource.aws_default_security_group(
   "default-littleobi-sg",
  vpc_id = "${aws_vpc.littleobi-vpc.id}",
  tags={
        "Flag"          : "Compliant",
        "Access"        : "Multivalue",
        "Type"          : "Production",
        "Name"          : "default-littleobi-sg",
        
        }
)

config += terrascript.data.aws_vpc(
  "littleobi-vpc-d",
  id =  "${aws_vpc.littleobi-vpc.id}"
)
for i in range(32):
  if ((json_subnet['subnets'][i]["Access"] == "pub") | (json_subnet['subnets'][i]["Access"] == "open")):
    config += terrascript.resource.aws_subnet(
      str(json_subnet['subnets'][i]["full_name"]),
      vpc_id               = "${aws_vpc.littleobi-vpc.id}",
      cidr_block           = str(json_subnet['subnets'][i]['ip_cidr'])+"/"+str(json_subnet['subnets'][i]['NetworkBits']),
      ipv6_cidr_block      = '${cidrsubnet("${data.aws_vpc.littleobi-vpc-d.ipv6_cidr_block}", 8,' + str(json_subnet['subnets'][i]['3-Oct']) + ')}',
      availability_zone_id = data["AvailabilityZones"][json_subnet["subnets"][i]["AZ"]]["ZoneId"],
      tags={
          "No"            : json_subnet['subnets'][i]["No"],
          "Flag"          : json_subnet['subnets'][i]["Flag"],
         "Environment"   : json_subnet['subnets'][i]["Environment"],
         "Access"        : json_subnet['subnets'][i]["Access"],
         "Type"          : "Production",
         "Purpose"       : json_subnet['subnets'][i]["Purpose"],
         "Creator"       : "Tarak Patel",
         "CreationMethod": "terraform",
         "Name"          : json_subnet['subnets'][i]["full_name"],
        }
    )

  else: 
    config += terrascript.resource.aws_subnet(
      str(json_subnet['subnets'][i]["full_name"]),
      vpc_id               = "${aws_vpc.littleobi-vpc.id}",
      cidr_block           = str(json_subnet['subnets'][i]['ip_cidr'])+"/"+str(json_subnet['subnets'][i]['NetworkBits']),
      availability_zone_id = data["AvailabilityZones"][json_subnet["subnets"][i]["AZ"]]["ZoneId"],
      tags={
        "Flag"          : json_subnet['subnets'][i]["Flag"],
        "No"            : json_subnet['subnets'][i]["No"],
        "Environment"   : json_subnet['subnets'][i]["Environment"],
        "Access"        : json_subnet['subnets'][i]["Access"],
        "Type"          : "Production",
        "Purpose"       : json_subnet['subnets'][i]["Purpose"],
        "Creator"       : "Tarak Patel",
        "CreationMethod": "terraform",
        "Name"          : json_subnet['subnets'][i]["full_name"],
      }
    
    )
  
with open('../output/vpc_subnet.network.aws.tf.json', 'w', encoding='utf-8') as config_file_tf:
  json.dump(config,config_file_tf,ensure_ascii=False, indent=4)