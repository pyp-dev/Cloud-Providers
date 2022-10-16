import requests
import json
import pandas as pd

url = 'https://aws.amazon.com/api/dirs/items/search?item.directoryId=aws-products&sort_by=item.additionalFields.productNameLowercase&sort_order=asc&size=350&item.locale=en_US&tags.id=!aws-products#type#feature&tags.id=!aws-products#type#variant&page=0'

response = requests.get(url)

response_json = json.loads(response.text)

rows = []

for i in range(1, len(response_json['items'])):
    item = response_json['items'][i]['item']
    row = {}
    row['id'] = item['name']

    if 'additionalFields' in item:
        row['name'] = item['additionalFields'].get('productName', None)
        row['description'] = item['additionalFields'].get('productSummary', None)
        row['category'] = item['additionalFields'].get('productCategory', None)
        row['launchDate'] = item['additionalFields'].get('launchDate', None)
        row['freeTier'] = item['additionalFields'].get('freeTierAvailability', None)
    
    if row['freeTier'] and '<' in row['freeTier']:
        row['freeTier'] = None
    if row['description'] and '<' in row['description']:
        row['description'] = row['description'][row['description'].find('>')+1:row['description'][1:].find('<')]
    
    rows.append(row)

pd.DataFrame.from_dict(rows).to_csv('aws-products.csv', index=False)