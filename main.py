from decimal import Decimal
from random import randint


class Requirement:
    def __init__(self, room, teacher, _class):
        self.room = room
        self.teacher = teacher
        self._class = _class

    def __str__(self):
        return "( R" + str(self.room) + ", T" + str(self.teacher) + ", C" + str(self._class) + " )"


requirement_filename = 'hdtt4req.txt'
note_filename = 'hdtt4note.txt'
number_of_teachers = 0
number_of_rooms = 0
number_of_classes = 0
number_of_subjects = 0
number_of_requirements = 0
number_of_slots = 0

number_of_periods = 5
number_of_days_per_week = 6

teacher_conflict_weight = 1
room_conflict_weight = 1
class_conflict_weight = 1

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
    number_of_slots = number_of_rooms * number_of_periods * number_of_days_per_week
    print("number of slots : " + str(number_of_slots))


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
                print("some errors in extracting from file")
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


def create_empty_array(size):
    ret = []
    for i in range(size):
        ret.append(0)
    return ret


def update_conflict(a_list):
    var = 0
    for item in a_list:
        var += max(0, item - 1)
    return var


def calculate_heuristic_cost(now_list):
    teacher_conflict_count = 0
    room_conflict_count = 0
    class_conflict_count = 0

    for a_list in now_list:

        # initialize empty arrays
        number_of_teacher_conflict = create_empty_array(number_of_teachers)
        number_of_room_conflict = create_empty_array(number_of_rooms)
        number_of_class_conflict = create_empty_array(number_of_classes)

        # calculate conflicts for this period
        for item in a_list:
            number_of_teacher_conflict[item.teacher] += 1
            number_of_room_conflict[item.room] += 1
            number_of_class_conflict[item._class] += 1

            '''
            if len(a_list) > 1:
                print(item)
            '''

        '''
        if len(a_list) > 1:
            print(number_of_teacher_conflict)
            print(number_of_room_conflict)
            print(number_of_class_conflict)

        if len(a_list) > 1:
            print(str(teacher_conflict_count) + " " +
                  str(room_conflict_count) + " " +
                  str(class_conflict_count))
        '''

        # update conflicts to counter
        teacher_conflict_count += update_conflict(number_of_teacher_conflict)
        room_conflict_count += update_conflict(number_of_room_conflict)
        class_conflict_count += update_conflict(number_of_class_conflict)

        '''
        if len(a_list) > 1:
            print(str(teacher_conflict_count) + " " +
                  str(room_conflict_count) + " " +
                  str(class_conflict_count))
        '''

    return teacher_conflict_count * teacher_conflict_weight + room_conflict_count * room_conflict_weight + \
           class_conflict_count * class_conflict_weight


def print_arrangement(list_of_lists):
    for a_list in list_of_lists:
        for item in a_list:
            print(item)
        print('\n')


def find_optimal_arrangement():

    # create empty list of lists
    list_of_lists = []
    for x in range(number_of_slots):
        temp_list = []
        list_of_lists.append(temp_list)

    # initial assignment of random order
    for item in requirement:
        index = randint(0, number_of_slots - 1)
        list_of_lists[index].append(item)

    # shuffle a requirement and switch to that arrangement if heuristic cost is lower
    i = 0
    while i < 1000:

        # copy the list first
        temp_list_of_lists = list_of_lists[:]

        # find a requirement to shuffle
        for j in range(1000):
            index = randint(0, len(temp_list_of_lists) - 1)
            if len(temp_list_of_lists[index]) <= 1:
                is_found = False
                continue
            else:
                is_found = True

                index2 = randint(0, len(temp_list_of_lists[index]) - 1)
                req = temp_list_of_lists[index].pop(index2)

                index3 = randint(0, len(temp_list_of_lists) - 1)
                temp_list_of_lists[index3].append(req)
                break

        if not is_found:
            # that means everything is ok, we can return
            print("nothing to shuffle")
            print(calculate_heuristic_cost(list_of_lists))
            print_arrangement(list_of_lists)
            return

        if calculate_heuristic_cost(temp_list_of_lists) < calculate_heuristic_cost(list_of_lists):
            list_of_lists = temp_list_of_lists
            i = 0
        else:
            i += 1

    # now we have found the arrangement which is consistently lower in 1000 iterations
    print_arrangement(list_of_lists)
    print(calculate_heuristic_cost(list_of_lists))


def main():

    extract_note()
    # print_note()
    extract_requirements()
    find_optimal_arrangement()


if __name__ == '__main__':
    main()
