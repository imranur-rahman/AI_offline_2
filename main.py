from decimal import Decimal
from random import randint


class Requirement:
    def __init__(self, room, teacher, _class):
        self.room = room
        self.teacher = teacher
        self._class = _class

    def __str__(self):
        return "(" + str(self.room) + " " + str(self.teacher) + " " + str(self._class) + ")"


requirement_filename = 'hdtt4req.txt'
note_filename = 'hdtt4note.txt'
number_of_teachers = 0
number_of_rooms = 0
number_of_classes = 0
number_of_subjects = 0
number_of_requirements = 0
number_of_slots = 0

# a list containing all requirement instances
requirement = []

'''
this function returns the first integer from a string
if no integer is found it will return infinity
'''


def get_first_int_from_line(line):
    for token in line.split():
        try:
            ret = int(token)
        except ValueError:
            continue
        return ret
    return Decimal('Infinity')


def extract_note():
    file = open(note_filename, 'r')

    global number_of_teachers
    text = file.readline()
    number_of_teachers = get_first_int_from_line(text)

    global number_of_subjects
    text = file.readline()
    number_of_subjects = get_first_int_from_line(text)

    global number_of_classes
    text = file.readline()
    number_of_classes = get_first_int_from_line(text)

    global number_of_rooms
    text = file.readline()
    number_of_rooms = get_first_int_from_line(text)

    global number_of_requirements
    text = file.readline()
    number_of_requirements = get_first_int_from_line(text)

    file.close()

    global number_of_slots
    number_of_slots = number_of_rooms * number_of_classes * number_of_teachers
    print(number_of_slots)


def print_note():
    print(number_of_teachers)
    print(number_of_classes)
    print(number_of_rooms)


def extract_requirements():
    file = open(requirement_filename, 'r')

    for room in range(0, number_of_rooms):
        for _class in range(0, number_of_classes):

            text = file.readline()
            line = [int(s) for s in text.split()]

            if len(line) != number_of_teachers:
                pass

            # index -> which teacher, item -> periods per week
            for index, item in enumerate(line):
                for i in range(int(item)):
                    requirement.append(Requirement(room, index, _class))

    file.close()
    # print(len(requirement))

    '''
    for item in requirement:
        print(item)
    '''


def find_optimal_arrangement():

    # create empty list of lists
    list_of_lists = []
    for x in range(number_of_requirements):
        temp_list = []
        list_of_lists.append(temp_list)

    # initial assignment of random order
    for item in requirement:
        index = randint(0, number_of_requirements - 1)



def main():

    extract_note()
    # print_note()

    extract_requirements()


if __name__ == '__main__':
    main()
