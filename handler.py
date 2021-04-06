import json
import requests
import json
import pandas as pd
import os
from twilio.rest import Client


def lambda_handler(event, context):

    # Find these values at https://twilio.com/user/account
    # To set up environmental variables, see http://twil.io/secure
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']

    client = Client(account_sid, auth_token)

    URL = 'https://www.cvs.com/immunizations/covid-19-vaccine/immunizations/covid-19-vaccine.vaccine-status.TX.json?vaccineinfo'
    page = requests.get(URL)
    table = json.loads(page.content.decode('utf8').replace("'", '"'))

    l = table['responsePayloadData']['data']['TX']
    df = pd.DataFrame(l)
    cities = ['FRISCO', 'GRAPEVINE', 'PLANO', 'DENTON',
              'MCKINNEY', 'The Colony', 'LEWISVILLE',
              'Decatur', 'Dallas', 'Fort Worth']

    df = df[df['city'].str.lower().isin([c.lower() for c in cities])]

    df = df[df["status"] == "Available"]

    client.api.account.messages.create(
        to="+1530xxxxxxx",
        from_="+120xxxxxx",
        body=f"Vaccinations available at {df.city.to_list()}")

    return {
        'statusCode': 200,
        'body': json.dumps(f"Vaccinations available at {df.city.to_list()}")
    }
