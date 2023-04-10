#--------------------------------------------------------

# Date: 4/7/23
# Python Version: 3.10.10

#--------------------------------------------------------

import json
import sys
from subprocess import call
from datetime import datetime
import random

#--------------------------------------------------------

data_file = "test_data.json"
exit_terms = [
    "q",
    "quit",
    "exit",
    "bye"
]

#--------------------------------------------------------

def load_data():
    return json.load(open(data_file,"r"))


def save_data(new_data):
    with open(data_file, "w") as file:
        file.write(json.dumps(new_data,indent=4))

#--------------------------------------------------------

def clear():
    call('clear')


def todays_date():
    now = datetime.now()
    return now.strftime("%m/%d/%y")

#--------------------------------------------------------
#? Manage Courses

# Add new dict to the "courses" dict in json
def create_course():
    clear()
    print("[~] Creating new course\n")
    # Get course info from user
    title = input("[?] Title: ")
    code = input("[?] Code (eg: ISTM183A): ")
    term = input("[?] Term (eg: SP23): ")
    instructor = input("[?] Instructor: ")
    start = input("[?] Start date (MM/DD/YY): ")
    end = input("[?] End date (MM/DD/YY): ")
    print()
    # Confirm save loop
    conf = input("[?] Save course (Y/N): ")
    while conf.lower() != 'y' and conf.lower() != 'n':
        conf = input("[?] Save course (Y/N): ")
    # Exit if no
    if conf.lower() == 'n':
        print("\n[!] Returning to menu")
        input("[~] Press enter to continue. ")
        return 
    elif conf.lower() == 'y':
    # Generate course dictionary
        course = {
            "title":title,
            "code":code,
            "term":term,
            "instructor":instructor,
            "start_date":start,
            "end_date":end,
            "created_date":todays_date(),
            "cards":[]
        }
    # Save course to json
        data = load_data()
        data["courses"].append(course)
        save_data(data)
        print("\n[!] Course saved!")
        input("[~] Press enter to continue. ")
        return
    

def select_course():
    clear()
    data = load_data()
    courses = data["courses"]
    # Return the course if there's only one
    if len(courses) == 1:
        return courses[0]
    print("[~] Select a course: \n")
    for course in courses:
        c_index = courses.index(course)
        print(f"[{str(c_index + 1)}]. {course['title']}")
    print()
    while True:
        select = input("[?] ")
        try:
            return courses[int(select) - 1]
        except IndexError:
            print("[X] Enter a valid number from the list.")
        except ValueError:
            print("[X] Enter a valid number from the list.")

# Reload data from JSON for the provided course. Used to
# refresh values mid-loop. 
def update_course(course):
    data = load_data()
    for c in data["courses"]:
        if course["title"] == c["title"]:
            return c


# Rewrites the course. Used for updating card views
# or rewritting course information
def save_course(course):
    data = load_data()
    for c in data["courses"]:
        if course["title"] == c["title"]:
            target = data['courses'].index(c)
            data['courses'][target] = course
            break
    save_data(data)


# Check if data in "courses" list, if not, create_course()
def verify_course_list():
    data = load_data()
    if not data['courses']:
        create_course()


#--------------------------------------------------------
#? Manage Cards

# Update course w/ new card
def save_card(course,card):
    data = load_data()
    for c in data["courses"]:
        if c["title"] == course["title"]:
            c["cards"].append(card)        
            break
    save_data(data)

# Take user input for new card
def add_card(course):
    clear()
    print("[~] Creating card for " + course['title'])
    print("[~] Enter \"quit\" to exit.")
    while True:
        print()
        question = input("[?] Question: ")
        if question.lower() in exit_terms: 
            return
        answer = input("[?] Answer: ")
        if answer.lower() in exit_terms:
            return
        card = {
            "question":question,
            "answer": answer,
            "course":course['title'],
            "date_added":todays_date(),
            "times_viewed":0
        }
        save_card(course, card)
        print("[!] Card saved. ")


def flash(course):
    clear()
    deck = course['cards']
    while True:
        card = random.choice(deck)
        card['times_viewed'] += 1
        clear()
        print("[~] Shuffling cards for " + course['title'])
        print("[~] Enter \"quit\" to exit flash.\n\n")
        print("[Q].", card['question'])
        in1 = input("[~] Press enter to see the answer. ")
        if in1 in exit_terms:
            break
        print("\n[A].", card['answer'])
        in2 = input("[?] Press enter to continue ")
        if in2 in exit_terms:
            break
    save_course(course)
    return


def search_cards(course):
    found = []
    clear()
    print(f"[~] Searching cards in {course['title']}\n")
    term = input("[?] Search term: ")
    if term in exit_terms:
        return
    for card in course['cards']:
        if term.upper() in card['question'].upper():
            found.append(card)
            card["times_viewed"] += 1
            continue
        if term.upper() in card['answer'].upper():
            found.append(card)
            card['times_viewed'] += 1
    save_course(course)
    clear()
    if not found:
        print("[X] No cards found with that string.")
        input("[~] Press enter to continue. ")
        return
    for card in found: 
        print()
        print('[~] Q:', card['question'])
        print('[~] A:', card['answer']) 
    print(f"\n[~] Cards found: {str(len(found))}")
    input("[~] Press enter to continue. ")
    return


#--------------------------------------------------------


def start_menu():
    while True:
        clear()
        print("\t/  Estupyous  /\n")
        print("[1]. Start")
        print("[2]. Add courses")
        print("[3]. Settings")
        print("[Q]. Quit")
        select = input("\n[?] ")
        if select.lower() == 'q':
            return
        elif select == '1':
            main()
        elif select == '2':
            create_course()
        elif select == '3':
            pass


def main():
    clear()
    verify_course_list()
    course = select_course() # Dict of course data
    while True:
        course = update_course(course)
        clear()
        print(f"[~] {course['title']} - {course['code']}")
        print(f"[~] Instructor: {course['instructor']}")
        print(f"[~] Number of cards: {str(len(course['cards']))}")
        print()
        print("[1]. Flash cards")
        print("[2]. Search cards")
        print("[3]. Add cards")
        print("[Q]. Exit")
        select = input("\n[?] ")
        if select.lower() == 'q':
            return
        elif select == '1':
            flash(course)
        elif select == '2':
            search_cards(course)
        elif select == '3':
            add_card(course)



#--------------------------------------------------------


start_menu()