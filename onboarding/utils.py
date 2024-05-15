import boto3
import json
import os
from dotenv import load_dotenv


def extract_text_from_document(file_path):
    load_dotenv()
    client = boto3.client(
        'textract',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_DEFAULT_REGION')
    )
    with open(file_path, 'rb') as document:
        imageBytes = document.read()

    response = client.analyze_document(
        Document={'Bytes': imageBytes},
        FeatureTypes=["FORMS"]
    )
    # print(response, "EEEEEEEE")

    extracted_data = {}
    # Process response to extract necessary data
    line_count = 0  # Initialize a counter for 'LINE' blocks

    for block in response['Blocks']:
        if block['BlockType'] == 'LINE':
            line_count += 1  # Increment the counter for each 'LINE' block
            if line_count == 10:  # Check if it's the 10th 'LINE' block
                text = block['Text']
                # print(text, "RRRR")
                extracted_data['Name'] = text.split(':')[-1].strip()
                # print(extracted_data['Name'], "oooooo")
                break
           
    return extracted_data




# extract_text_from_document('C:/Users/hp/Downloads/pancard.jpg')


# def extract_text  _from_document(file_path):
#     textract = boto3.client('textract')

#     with open(file_path, 'rb') as document:
#         response = textract.analyze_document(
#             Document={'Bytes': document.read()},
#             FeatureTypes=['FORMS', 'TABLES']
#         )

#     extracted_data = {}
#     for block in response['Blocks']:
#         if block['BlockType'] == 'LINE':
#             extracted_data[block['Id']] = block['Text']

#     return json.dumps(extracted_data)
