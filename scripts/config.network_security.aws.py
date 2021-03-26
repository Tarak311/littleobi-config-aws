import terrascript
import terrascript.provider
import terrascript.resource
import json
import terrascript.data
import ipaddress 
import get_subnets
import get_data
with open('./data/subnet-list.json') as data_subnet:
  json_subnet = json.load(data_subnet)

with open('./data/creds.json') as aws_creds:
  creds = json.load(aws_creds)   

with open('./data/data.json') as data_file:
  data = json.load(data_file)   
  
config = terrascript.Terrascript()
dconfig = terrascript.Terrascript()
public_subnets = []
private_subnets = []
secured_subnets = []


get_subnets.get_public_subnets(public_subnets,dconfig)

get_subnets.get_private_subnets(private_subnets,dconfig)

get_subnets.get_secured_subnets(secured_subnets,dconfig)


get_data.get_main_route_table("Public",config)
get_data.get_main_route_table("Private",config)
get_data.get_main_route_table("Secured",config)

for x in range(len(public_subnets)):
  config += terrascript.resource.aws_route_table_association(
  "public-rt-asso"+str(x),
  subnet_id = public_subnets[x],
  route_table_id = "${data.aws_route_table.littleobi-rt-Public.id}"
)

for x in range(len(private_subnets)):
  config += terrascript.resource.aws_route_table_association(
  "private-rt-asso"+str(x),
  subnet_id = private_subnets[x],
  route_table_id = "${data.aws_route_table.littleobi-rt-Private.id}"
)

for x in range(len(secured_subnets)):
  config += terrascript.resource.aws_route_table_association(
  "secured-rt-asso"+str(x),
  subnet_id = secured_subnets[x],
  route_table_id = "${data.aws_route_table.littleobi-rt-Secured.id}"
)





print(config)
with open('../output/postcore/config.network.aws.tf.json', 'w', encoding='utf-8') as config_file_tf:
  json.dump(config,config_file_tf,ensure_ascii=False, indent=4)