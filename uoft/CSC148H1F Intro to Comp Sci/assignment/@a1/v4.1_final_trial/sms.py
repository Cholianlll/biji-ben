# Assignment 1 - Managing students!## CSC148 Fall 2014, University of Toronto# Instructor: David Liu# ---------------------------------------------# STUDENT INFORMATION## List your group members below, one per line, in format# Su Young Lee, leesu9# Rui Qiu, qiurui2### ---------------------------------------------'''Interactive console for assignment.This module contains the code necessary for running the interactive console.As provided, the console does nothing interesting: it is your job to buildon it to fulfill all the given specifications.run: Run the main interactive loop.'''from student import *def run():    ''' (NoneType) -> NoneType    Run the main interactive loop.    '''    UOFT = School('University of Toronto')    while True:        command = input('')        clist = command.split()        if len(clist) == 3:            if clist[0:2] == ['create', 'student']:                student_name = clist[2]                try:                    UOFT.student_create(student_name)                except StudentAlreadyExistsError:                    print ('ERROR: Student {0} already exists.'.format(                        student_name))            elif clist[0] == 'enrol':                student_name, course_name = clist[1], clist[2]                try:                    UOFT.enrol_student(student_name, course_name)                except StudentNotExistError:                    print ('ERROR: Student {0} does not exist.'.format(                        student_name))                except FullCourseError:                    print ('ERROR: Course {0} is full.'.format(course_name))            elif clist[0] == 'drop':                student_name, course_name = clist[1], clist[2]                try:                    UOFT.course_drop(student_name, course_name)                except StudentNotExistError:                    print ('ERROR: Student {0} does not exist.'.                           format(student_name))            elif clist[0] == 'common-courses':                name1, name2 = clist[1], clist[2]                try:                    UOFT.common_check(name1, name2)                except BothStudentsNotExistError:                    print ('ERROR: Student {0} does not exist.'.format(name1))                    print ('ERROR: Student {0} does not exist.'.format(name2))                except StudentNotExistError:                    print ('ERROR: Student {0} does not exist.'.format(name1))                except Student2NotExistError:                    print ('ERROR: Student {0} does not exist.'.format(name2))            else:                print('Unrecognized command!')                UOFT.undo_stack.push(1)        elif len(clist) == 2:            if clist[0] == 'list-courses':                student_name = clist[1]                try:                    UOFT.list_courses(student_name)                except StudentNotExistError:                    print ('ERROR: Student {0} does not exist.'.                           format(student_name))            elif clist[0] == 'class-list':                course_name = clist[1]                UOFT.class_list(course_name)            elif clist[0] == 'undo':                repeat_number = clist[1]                try:                    UOFT.undo_repeat(repeat_number)                except NoCommandsUndoError:                    print ('ERROR: No commands to undo.')                except NotNaturalNumberUndoError:                    print ('ERROR: {0} is not a positive natural number.'.                           format(repeat_number))            else:                print('Unrecognized command!')                UOFT.undo_stack.push(1)        elif len(clist) == 1:            if clist[0] == 'undo':                try:                    UOFT.undo_once()                except NoCommandsUndoError:                    print ('ERROR: No commands to undo.')            elif clist[0] == 'exit':                break            else:                print('Unrecognized command!')                UOFT.undo_stack.push(1)        else:            print('Unrecognized command!')            UOFT.undo_stack.push(1)
if __name__ == '__main__':    run()