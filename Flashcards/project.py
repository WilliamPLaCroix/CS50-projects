import csv
from datetime import date, datetime, timedelta
import glob
import os
from random import shuffle
import re
import sys


def main():

    field_names = ["front", "back", "notes", "status", "interval", "ease", "deck"]
    options: list = ["review", "add card", "browse deck", "new deck", "delete deck"]
    deck_options: dict = {"daily reviews": 20, "daily new": 20}

    while True:
        try:
            if option := input(f"What would you like to do? Type: {', '.join(options)} - or press ctrl+d to exit\n"):
                if option not in options:
                    continue
        except EOFError:
            sys.exit("Goodbye!")

        if option == "review":
            review_deck = select_deck()
            deck: str = import_csv(review_deck)
            study: list = create_study(deck, deck_options)
            print("")
            review(study)
            print("Review finished!")
            continue

        if option == "add card":
            selected_deck = select_deck()
            while True:
                try:
                    add_card(selected_deck)
                    answer = input("Would you like to add another card? Y/N - or press ctrl+d to exit\n")
                    if answer == "y" or answer == "yes":
                        continue
                    if answer == "n" or answer == "no":
                        break
                except EOFError:
                    sys.exit("Goodbye!")

        if option == "browse deck":
            browse_deck = select_deck()
            browse(browse_deck)
            continue

        if option == "new deck":
            while True:
                try:
                    if new_deck := input("What would you like to call this new deck?: - or press ctrl+d to exit\n"):
                        build_deck(new_deck, field_names)
                        while True:
                            answer = input("Would you like to add a card? Y/N - or press ctrl+d to exit\n").lower()
                            if answer == "y" or answer == "yes":
                                add_card(new_deck)
                            if answer == "n" or answer == "no":
                                break
                    break
                except EOFError:
                    sys.exit("Goodbye!")
            continue

        if option == "delete deck":
            while True:
                delete_deck = select_deck()
                answer = input(f'Are you sure you want to delete deck "{delete_deck}"? Y/N - or press ctrl+d to exit\n').lower()
                if answer == "y" or answer == "yes":
                    os.remove(f"{delete_deck}.csv")
                    break
                if answer == "n" or answer == "no":
                    break
            continue
    ### suspend card, delete card


def add_card(deck_name: str) -> dict:

    card = {}

    while True:
        if new_front := input("what would you like the front to say? "):
            card['front'] = new_front
            break
    while True:
        if new_back := input("what would you like the back to say? "):
            card['back'] = new_back
            break
    if new_notes := input("would you like to add any notes to the card? "):
            card['notes'] = new_notes
    else:
        card['notes'] = None
    card['interval'] = 10
    card['ease'] = 1.30
    card['status'] = "new"
    card['deck'] = deck_name

    field_names = card.keys()

    try:
        with open(f"{deck_name}.csv", 'a', newline='') as deck:
            writer = csv.DictWriter(deck, field_names)
            return writer.writerow(card)
    except FileNotFoundError:
        return print(f"Could not find deck {deck_name}, something must have gone wrong...")


def backup_csv(deck_name, field_names) -> None:

    try:
        with open(f"{deck_name}_backup.csv", newline='') as backup:
            pass
    except FileNotFoundError:
        backup = open(f"{deck_name}_backup.csv", 'w', newline='')
        with open(f"{deck_name}.csv", newline='') as fin:
            reader = csv.DictReader(fin)
            writer = csv.DictWriter(backup, field_names)
            writer.writeheader()
            for row in reader:
                writer.writerow(row)
        backup.close()
    return


def browse(browse_deck: str) -> None:

    deck = []
    try:
        with open(f"{browse_deck}.csv", newline='') as fin:
            reader = csv.DictReader(fin)
            for row in reader:
                deck.append(row)
    except FileNotFoundError:
        sys.exit(f"Could not find {review_deck}, exiting...")

    for card in deck:
        print(f"front: {card['front']}\nback: {card['back']}\nnotes: {card['notes']}\n")
    return

def build_deck(deck_name: str, field_names: list) -> None:

    try:
        with open(f"{deck_name}.csv", 'x', newline='') as new_deck:
            writer = csv.DictWriter(new_deck, field_names)
            writer.writeheader()
            return print(f"New deck {deck_name}created.")
    except:
        print("hmm, something went wrong")


def create_study(deck: list, deck_options: dict) -> list:

    study: list = []
    new_cards: int = 0
    review_cards: int = 0

    today = datetime.now()

    for card in deck:
        last = re.search("([0-9]{4})-([0-9]{2})-([0-9]{2}) ([0-9]{2}):([0-9]{2}):.*", card['last review'])
        match = datetime(int(last[1]), int(last[2]), int(last[3]), int(last[4]), int(last[5]))
        difference = today - match
        hours, minutes, seconds = str(difference).split(":")
        minutes = int(hours) * 60 + int(minutes)
        #print(f"difference: {minutes}, interval: {card['interval']}")
        if card['status'] == "new" and new_cards < deck_options['daily new'] and minutes > int(card['interval']):
            study.append(card)
            new_cards += 1
        if card['status'] == "old" and review_cards < deck_options["daily reviews"] and minutes > int(card['interval']):
            study.append(card)
            review_cards += 1
        if new_cards == deck_options['daily new'] and review_cards < deck_options["daily reviews"]:
            return study
    return study

def edit_card(card: dict) -> dict:

    if new_front := input("what would you like to chang the front to? "):
        card['front'] = new_front
    if new_back := input("what would you like to chang the back to? "):
        card['back'] = new_back
    if new_notes := input("what would you like to chang the notes to? "):
        card['notes'] = new_notes
    print("")

    return card

def export_csv(studied_deck: list, unstudied_deck: list, deck_name: str) -> None:


    field_names: list = []

    try:
        with open(f"{deck_name}.csv", newline='') as fin:
            reader = csv.reader(fin)
            field_names = reader.__next__()
    except FileNotFoundError:
        sys.exit(f"Could not find {deck_name}, exiting...")

    backup_csv(deck_name, field_names)

    try:
        with open(f"{deck_name}.csv", 'w', newline='') as fout:
            writer = csv.DictWriter(fout, field_names)
            writer.writeheader()
            for card in studied_deck:
                writer.writerow(card)
            for card in unstudied_deck:
                writer.writerow(card)
    except FileNotFoundError:
        sys.exit(f"Could not find {deck_name}, exiting...")


def import_csv(review_deck: str) -> list:

    deck = []
    try:
        with open(f"{review_deck}.csv", newline='') as fin:
            reader = csv.DictReader(fin)
            for row in reader:
                deck.append(row)
    except FileNotFoundError:
        sys.exit(f"Could not find {review_deck}, exiting...")

    return deck


def review(study: list) -> list:

    studied: list = []

    while True:
        try:
            shuffle(study)
            if not study:
                if len(studied) != 0:
                    return export_csv(studied, study, card['deck'])
                else:
                    return print("No cards to study today!")

            for card in study:
                prompt = input(card["front"])
                feedback = input(f"{card['back']}\n{card['notes']}\n")
                if not feedback:
                    card['interval'] = int(float(card['interval']) * float(card['ease']))
                    card['status'] = "old"
                    card['last review'] = datetime.now()
                    studied.append(card)
                    study.remove(card)
                elif feedback == "edit":
                    card = edit_card(card)
                elif feedback == "delete":
                    answer = input(f"Are you sure you want to delete card {card['front']}? Y/N - or press ctrl+d to exit\n").lower()
                    if answer == "y" or answer == "yes":
                        study.remove(card)
                    if answer == "n" or answer == "no":
                        pass
                elif feedback == "suspend":
                    answer = input(f"Are you sure you want to suspend card {card['front']}? Y/N - or press ctrl+d to exit\n").lower()
                    if answer == "y" or answer == "yes":
                        card['status'] = "suspended"
                        studied.append(card)
                        study.remove(card)
                    if answer == "n" or answer == "no":
                        pass
                else:
                    card['interval'] = int(float(card['interval']) * 0.6)
        except EOFError:
            return export_csv(studied, study, card['deck'])


def select_deck() -> str:

    paths: list = glob.glob("/workspaces/94390768/cs50p/final/*.csv")
    filenames: list = []
    for path in paths:
        if filename := re.search(".*/([^/]*)\.csv$", path):
            if not filename[1].endswith("backup"):
                filenames.append(filename[1])
    while True:
        try:
            deck = input(f"To select a deck, type: {', '.join(filenames)} - or press ctrl+d to exit\n")
        except EOFError:
            sys.exit("Exiting...")
        if deck not in filenames:
            print(f"Could not find {deck}...")
            continue
        return deck


if __name__ == "__main__":
    main()
