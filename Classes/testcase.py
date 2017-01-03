#!/usr/bin/env python3

import json


"""
# Loads card information from json files.
#
#
"""
def loadCRS():
    try:
        with open('cardSuits.json') as ranksData:
            try:
                typ = json.load(ranksData)
            except ValueError as exc:
                print (exc)
                return False
            print (typ)
    except (IOError, OSError) as exc:
        print (exc)
        return False


loadCRS()
