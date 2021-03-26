import json

def get_data(creds,json_subnet,data):
    with open('./data/data.json') as data_file:
        data = json.load(data_file)   

    with open('./data/creds.json') as aws_creds:
        creds = json.load(aws_creds)   

    with open('./data/subnet-list.json') as data_subnet:
        json_subnet = json.load(data_subnet)


