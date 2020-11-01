




#Scheduling of meetings taking place for a day in the academic year of a college.
#This scheduling follows the given primary constraints :
#1. Same teacher has no overlapping timing of a class.
#2. Same course is not taught at the same time slot.
#3. Same meet is not used by multiple classes in a time slot.





import prettytable as prettytable
import random as rnd
POPULATION_SIZE = 9
NUMB_OF_ELITE_SCHEDULES = 1
TOURNAMENT_SELECTION_SIZE = 3
MUTATION_RATE = 0.1


class Data:
    MEETS = [["M501", 45],
             ["M502", 35],
             ["M503", 35]]

    MEETING_TIMES = [["MT1", "10:00 - 11:00"],
                     ["MT2", "11:00 - 12:00"],
                     ["MT3", "12:30 - 13:30"],
                     ["MT4", "13:30 - 14:30"]]

    TEACHERS = [["T1", "Teacher 1"],
               	["T2", "Teacher 2"],
            	["T3", "Teacher 3"],
                ["T4", "Teacher 4"]]


    def __init__(self):
        self._meets = []
        self._meetingTimes = []
        self._teachers = []
        for i in range(0, len(self.MEETS)):
            self._meets.append(Meet(self.MEETS[i][0], self.MEETS[i][1]))
        for i in range(0, len(self.MEETING_TIMES)):
            self._meetingTimes.append(MeetingTime(self.MEETING_TIMES[i][0], self.MEETING_TIMES[i][1]))
        for i in range(0, len(self.TEACHERS)):
            self._teachers.append(Teacher(self.TEACHERS[i][0], self.TEACHERS[i][1]))
        course1 = Course("C1", "CST-351", [self._teachers[0], self._teachers[1]], 25)
        course2 = Course("C2", "CST-352", [self._teachers[0], self._teachers[1], self._teachers[2]], 35)
        course3 = Course("C3", "CST-353", [self._teachers[0], self._teachers[1]], 25)
        course4 = Course("C4", "CST-354", [self._teachers[2], self._teachers[3]], 30)
        course5 = Course("C5", "CSP-351", [self._teachers[3]], 35)
        course6 = Course("C6", "CSP-352", [self._teachers[0], self._teachers[2]], 45)
        course7 = Course("C7", "CSP-353", [self._teachers[1], self._teachers[3]], 45)
        self._courses = [course1, course2, course3, course4, course5, course6, course7]
        dept1 = Department("D1", [course1, course3])
        dept2 = Department("D2", [course2, course4, course5])
        dept3 = Department("D3", [course6, course7])
        self._depts = [dept1, dept2, dept3]
        self._numberOfClasses = 0
        for i in range(0, len(self._depts)):
            self._numberOfClasses += len(self._depts[i].get_courses())

    def get_meets(self): return self._meets
    def get_teachers(self): return self._teachers
    def get_courses(self): return self._courses
    def get_depts(self): return self._depts
    def get_meetingTimes(self): return self._meetingTimes
    def get_numberOfClasses(self): return self._numberOfClasses


class Schedule:
    def __init__(self):
        self._data = data
        self._classes = []
        self._numbOfConflicts = 0
        self._fitness = -1
        self._classNumb = 0
        self._isFitnessChanged = True

    def get_classes(self):
        self._isFitnessChanged = True
        return self._classes

    def get_fitness(self):
        if(self._isFitnessChanged == True):
            self._fitness = self.calculate_fitness()
            self._isFitnessChanged = False
        return self._fitness

    def initialize(self):
        depts = self._data.get_depts()
        for i in range(0, len(depts)):
            courses = depts[i].get_courses()
            for j in range(0, len(courses)):
                newClass = Class(self._classNumb, depts[i], courses[j])
                self._classNumb += 1
                newClass.set_meetingTime(data.get_meetingTimes()[rnd.randrange(0, len(data.get_meetingTimes()))])
                newClass.set_meet(data.get_meets()[rnd.randrange(0, len(data.get_meets()))])
                newClass.set_teacher(courses[j].get_teachers()[rnd.randrange(0, len(courses[j].get_teachers()))])
                self._classes.append(newClass)
        return self

    def calculate_fitness(self):
        self._numbOfConflicts = 0
        classes = self.get_classes()
        for i in range(0, len(classes)):
            if(classes[i].get_meet().get_seatingCapacity() < classes[i].get_course().get_maxNumbOfStudents()):
                self._numbOfConflicts += 1
            for j in range(0, len(classes)):
                if(j > i):
                    if(classes[i].get_meetingTime() == classes[j].get_meetingTime() and classes[i].get_id() != classes[j].get_id()):
                        if(classes[i].get_meet() == classes[j].get_meet()):
                            self._numbOfConflicts += 1
                        if(classes[i].get_teacher() == classes[j].get_teacher()):
                            self._numbOfConflicts += 1
        return 1/((1.0*self._numbOfConflicts +1))

    def __str__(self):
        returnValue = ""
        for i in range(0, len(self._classes)-1):
            returnValue += str(self._classes[i]) + ", "
        returnValue += str(self._classes[len(self._classes)-1])
        return returnValue


class Population:
    def __init__(self, size):
        self._size = size
        self._data = data
        self._schedules = []
        for i in range(0, size):
            self._schedules.append(Schedule().initialize())

    def get_schedules(self):
        return self._schedules


class GeneticAlgorithm:
    def evolve(self, population):
        return self._mutate_population(self._crossover_population(population))

    def _crossover_population(self, pop):
        crossover_pop = Population(0)
        for i in range(NUMB_OF_ELITE_SCHEDULES):
            crossover_pop.get_schedules().append(pop.get_schedules()[i])
        i = NUMB_OF_ELITE_SCHEDULES
        while i < POPULATION_SIZE:
            schedule1 = self._select_tournament_population(pop).get_schedules()[0]
            schedule2 = self._select_tournament_population(pop).get_schedules()[0]
            crossover_pop.get_schedules().append(self._crossover_schedule(schedule1, schedule2))
            i += 1
        return crossover_pop

    def _mutate_population(self, population):
        for i in range(NUMB_OF_ELITE_SCHEDULES, POPULATION_SIZE):
            self._mutate_schedule(population.get_schedules()[i])
        return population

    def _crossover_schedule(self, schedule1, schedule2):
        crossoverSchedule = Schedule().initialize()
        for i in range(0, len(crossoverSchedule.get_classes())):
            if(rnd.random() > 0.5):
                crossoverSchedule.get_classes()[i] = schedule1.get_classes()[i]
            else:
                crossoverSchedule.get_classes()[i] = schedule2.get_classes()[i]
        return crossoverSchedule

    def _mutate_schedule(self, mutateSchedule):
        schedule = Schedule().initialize()
        for i in range(0, len(mutateSchedule.get_classes())):
            if(MUTATION_RATE > rnd.random()):
                mutateSchedule.get_classes()[i] = schedule.get_classes()[i]
        return mutateSchedule

    def _select_tournament_population(self, pop):
        tournament_pop = Population(0)
        i = 0
        while i < TOURNAMENT_SELECTION_SIZE:
            tournament_pop.get_schedules().append(pop.get_schedules()[rnd.randrange(0, POPULATION_SIZE)])
            i += 1
        tournament_pop.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
        return tournament_pop


class Course:
    def __init__(self, number, name, teachers, maxNumbOfStudents):
        self._number = number
        self._name = name
        self._teachers = teachers
        self._maxNumbOfStudents = maxNumbOfStudents

    def get_number(self): return self._number

    def get_name(self): return self._name

    def get_teachers(self): return self._teachers

    def get_maxNumbOfStudents(self): return self._maxNumbOfStudents

    def __str__(self): return self._name


class Teacher:
    def __init__(self, id, name):
        self._id = id
        self._name = name

    def get_id(self): return self._id

    def get_name(self): return self._name

    def __str__(self): return self._name


class Meet:
    def __init__(self, number, seatingCapacity):
        self._number = number
        self._seatingCapacity = seatingCapacity

    def get_number(self): return self._number
    def get_seatingCapacity(self): return self._seatingCapacity


class MeetingTime:
    def __init__(self, id, time):
        self._id = id
        self._time = time

    def get_id(self): return self._id
    def get_time(self): return self._time


class Department:
    def __init__(self, name, courses):
        self._name = name
        self._courses = courses

    def get_name(self): return self._name

    def get_courses(self): return self._courses


class Class:
    def __init__(self, id, dept, course):
        self._id = id
        self._dept = dept
        self._course = course
        self._teacher = None
        self._meetingTime = None

    def get_id(self): return self._id

    def get_dept(self): return self._dept

    def get_course(self): return self._course

    def get_teacher(self): return self._teacher

    def get_meetingTime(self): return self._meetingTime
    def get_meet(self): return self._meet
    def set_teacher(self, teacher):  self._teacher = teacher
    def set_meetingTime(self, meetingTime): self._meetingTime = meetingTime
    def set_meet(self, meet): self._meet = meet

    def __str__(self):
        return str(self._dept.get_name()) + "," + str(self._course.get_number()) + "," + \
            str(self._meet.get_number()) + "," + str(self._teacher.get_id()
                                                     ) + "," + str(self._meetingTime.get_id())


class DisplayMgr:
    def print_available_data(self):
        print("> All Available Data")
        self.print_dept()
        self.print_course()
        self.print_meet()
        self.print_teacher()
        self.print_meeting_times()

    def print_schedule_as_table(self, schedule):
        classes = schedule.get_classes()
        table = prettytable.PrettyTable((['Subject (No. of students)', 'Meet Code (Capacity)', 'Teacher (Teacher code)', 'Meet Time (Slot Code)']))
        for i in range(0, len(classes)):
            table.add_row([classes[i].get_course().get_name() + " (" + str(classes[i].get_course().get_maxNumbOfStudents()) + ")",
                            classes[i].get_meet().get_number() + " (" + str(classes[i].get_meet().get_seatingCapacity()) + ")",
                            classes[i].get_teacher().get_name() + " (" + str(classes[i].get_teacher().get_id()) + ")",
                            classes[i].get_meetingTime().get_time() + " (" + str(classes[i].get_meetingTime().get_id()) + ")"])
        print(table)


data = Data()
displayMgr = DisplayMgr()
generationNumber = 0
population = Population(POPULATION_SIZE)
population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
geneticAlgorithm = GeneticAlgorithm()
print("\n> Generation # 0")
displayMgr.print_schedule_as_table(population.get_schedules()[0])
i=0
while(population.get_schedules()[i].get_fitness != 1.0 and i<POPULATION_SIZE-1):
    generationNumber += 1
    print("\n> Generation # " + str(generationNumber))
    population = geneticAlgorithm.evolve(population)
    population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
    displayMgr.print_schedule_as_table(population.get_schedules()[0])
    i=i+1
