import trello
import requests
import argparse

apikey = '<API-KEY>'

# trello_api = trello.TrelloApi(apikey)
# print "Please paste open this url and return here to input the token"
# print trello_api.get_token_url('My App', expires='30days', write_access=True)
#
# token = raw_input('token: ') #  ''
# print token
token = '<TOKEN>'


assignments_id = '55f76693290af1a98f38f9ad'
inbox_list_id = '55f766a1f4e5dbef3d198ea5'
this_week = '55fae3b7794dc049847e1a80'
to_do_today = '55f766aad87e214b31d62850'
completed = '55f766adc4935aa365e7e652'
list_id = inbox_list_id

# parser = argparse.ArgumentParser(description='Sort Trello lists')
# parser.add_argument('apikey', help='api key')
# parser.add_argument('token', help='user token')
# parser.add_argument('--gentoken', help='Generate token')
# args = parser.parse_args()
# apikey = args.apikey
# token = args.token


list = trello.Lists(apikey, token=token)
card_array = list.get_card(list_id)

for card in sorted(card_array, key=lambda card: card['due']):
    print card['due'], card['name'], card['pos'], card['id']
    url = "https://api.trello.com/1/cards/{}/pos?key={}&token={}".format(card['id'], apikey, token)
    r = requests.put(url, data={'value': 'bottom'})
    if r.status_code != 200:
        print u"ERRORS for card with NAME: {}, ID: {}".format(card['name'], card['id'])
