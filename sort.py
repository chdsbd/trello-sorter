#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import print_function

import argparse

import requests
import trello


def main():
    parser = argparse.ArgumentParser(
        description='Interactive command line utility for sorting Trello lists')
    parser.add_argument('apikey', help='Trello API Key from https://trello.com/app-key')
    args = parser.parse_args()

    APIKEY = args.apikey
    trello_api = trello.TrelloApi(APIKEY)

    token_url = trello_api.get_token_url('Trello Sorter', expires='30days', write_access=True)
    print(u'Provide the app token from this url:', token_url)
    TOKEN = raw_input('App token: ')

    selected_list = find_list(APIKEY, TOKEN)
    sort_list(selected_list, APIKEY, TOKEN)


def find_list(APIKEY, TOKEN):
    print('Enter your username ("@johnsmith" would be "johnsmith")')
    user = raw_input('Username: ')

    member = trello.Members(APIKEY, token=TOKEN)
    print("Choose your board")
    boards = member.get_board(user)
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
    trello_board = trello.Boards(APIKEY, token=TOKEN)
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

    return trello.Lists(APIKEY, token=TOKEN).get_card(list_id)


def sort_list(selected_list, APIKEY, TOKEN):
    for card in sorted(selected_list, key=lambda card: card['due']):
        print(card['name'])
        url = "https://api.trello.com/1/cards/{}/pos?key={}&token={}".format(
            card['id'], APIKEY, TOKEN)
        r = requests.put(url, data={'value': 'bottom'})
        if r.status_code != 200:
            print(u"ERRORS for card with NAME: {}, ID: {}".format(card['name'],
                                                                  card['id']))


if __name__ == '__main__':
    main()
