#!/usr/bin/env python2
 # -*- coding: utf-8 -*-
from __future__ import print_function

import os

import requests
import trello


# NOTE: This code is shit. But it's a script so that's okay
# NOTE: Python 2 *must* be used to run this code.

APP_NAME = 'Trello Sorter'
API_KEY = '<API-KEY>'
TOKEN = '<TOKEN>'

#TODO: Make it so it doesn't sort list if all set
#TODO: Add option to select all lists or multiple
#TODO: Add way to save credentials


def main():
    try:
        apikey = os.environ['TRELLO_API']
    except KeyError:
        print("Get your Trello API key here (https://trello.com/app-key)")
        apikey = raw_input('API Key: ')
        os.environ['TRELLO_API'] = apikey
    # Prompt user to get Trello app token
    trello_api = trello.TrelloApi(apikey)
    token_url = trello_api.get_token_url(
        APP_NAME, expires='30days', write_access=True)
    print(u'Provide the app token from this url:', token_url)
    token = raw_input('App token: ')

    # Get boards for user
    print('Enter your username ("@johnsmith" would be "johnsmith")')
    user = raw_input('Username: ')
    print("Choose your board")
    member = trello.Members(apikey, token=token)
    boards = member.get_board(user)

    # Select board to sort
    for board in boards:
        print(u"({index}) {name} ({id})".format(
            index=boards.index(board), name=board['name'], id=board['id']))
    print('Choose board number. e.g. For "(3) my_board" write 3')
    board_index = raw_input('board number: ')
    board = boards.pop(int(board_index))
    board_id = board['id']
    print(u"Selected" + board['name'])
    # Choose list on specified board to sort
    print("Choose list to sort")
    trello_board = trello.Boards(apikey, token=token)
    lists = trello_board.get_list(board_id)
    for select_list in lists:
        print(u"({index}) {name} ({id})".format(
            index=lists.index(select_list),
            name=select_list['name'],
            id=select_list['id']))
    print('Choose list number. e.g. For "(7) my_list" write 7')
    list_number = raw_input("list number: ")
    list_to_sort = lists.pop(int(list_number))
    list_id = list_to_sort['id']
    # sort list
    selected_list = trello.Lists(apikey, token=token)
    print("Sorting list")
    sort(apikey, token, selected_list.get_card(list_id))
    print("Labeling list")
    label(apikey, token, selected_list.get_card(list_id))


def sort(apikey, token, card_array):
    for card in sorted(card_array, key=lambda card: card['due']):
        print(card['due'], card['name'], card['pos'], card['id'])
        url = "https://api.trello.com/1/cards/{}/pos?key={}&token={}".format(
            card['id'], apikey, token)
        r = requests.put(url, data={'value': 'bottom'})
        if r.status_code != 200:
            print(u"ERRORS for card with NAME: {}, ID: {}".format(card['name'],
                                                                  card['id']))


def label(apikey, token, card_array):
    # blue, green, orange, purple, red, yellow
    cards = trello.Cards(apikey, token=token)
    for card in card_array:
        for card_label in card['labels']:
            cards.delete_label_color(card_label['color'], card['id'])
            print(u"Cleaned:", card['name'])
        if "ECE 242:" in card['name']:
            cards.new_label(card['id'], "green")
            print(card['name'])
        elif "ECE 221:" in card['name']:
            cards.new_label(card['id'], "red")
            print(card['name'])
        elif "Math 331:" in card['name']:
            cards.new_label(card['id'], "blue")
            print(card['name'])
        elif "ECE 211:" in card['name']:
            cards.new_label(card['id'], "orange")
            print(card['name'])
        elif "MUSIC 103:" in card['name']:
            cards.delete(card['id'])
            print(u'❎ DELETED CARD:', card['name'])
        else:
            cards.new_label(card['id'], "pink")
            print(u"Card doesn't match filter:", card['name'])


if __name__ == '__main__':
    main()
