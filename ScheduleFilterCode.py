#Check if any two lists overlap by checking if any value falls between another list or if one of the values are equal
def isOverlapping(lst1, lst2):
    if (lst2[0] > lst1[0] and lst2[0] < lst1[-1]) or (lst1[0] > lst2[0] and lst1[0] < lst2[-1]):

        return True

    elif (lst1[0] == lst2[0] or lst1[-1] == lst2[-1]):

        return True

    return False

#Convert time to flaot, i.e., "12:30-14:00" --> [12.5,14.0]. This will be used with the overlapping function
def TimeToFloat(time):
    #Convert the string into a list
    time = time.split("-")

    #Loop through the list and divide the last 2 numbers by 60. Ex: if the time ends in 30, like 12:30, you'll get 12.5
    for index in range(len(time)):
        time[index] = float(time[index][:-3]) + float(time[index][-2:]) / 60

    return time

#Check if two courses can be registered together. This utilizes the overlapping and time to float conversion functions
def isEligible(firstCourse, secondCourse):
    #Loop through the timings of each course
    for firstCourseTiming in range(2, len(firstCourse), 2):
        for secondCourseTiming in range(2, len(secondCourse), 2):
            #Get the course time and the course day
            courseOneTime = TimeToFloat(firstCourse[firstCourseTiming])
            courseTwoTime = TimeToFloat(secondCourse[secondCourseTiming])

            courseOneDay = firstCourse[firstCourseTiming - 1]
            courseTwoDay = secondCourse[secondCourseTiming - 1]
            #If the course days are the same and their timings overlap, return false
            if courseOneDay == courseTwoDay and isOverlapping(courseOneTime, courseTwoTime):
                return False
    return True

#Check if a schedule is eligible by checking if every course in said schedule doesn't overlap with another course
def isEligibleSchedule(schedule):
    for firstCourse in range(len(schedule)):
        for consequentCourse in schedule[firstCourse+1:]:
            if isEligible(schedule[firstCourse],consequentCourse) == False:
                return False
    return True

#Display the course in a formal way.
#Ex: ['course1,'monday','12:00-15:00','wednesday','9:00-12:00'] --> course1: monday 12:00-15:00, wednesday 9:00-12:00
def displayCourse(course):
    #loop through the course information
    for info in range(len(course)):
        #if it's the first item (course name), add :
        if info == 0:
            print(course[info] + ": ", end='')
        #If not, check if it's the course day (odd numbers) and display it with the timing (the item next).
        elif info % 2 != 0:
            print(course[info], course[info + 1], end='')
        #Don't add a comma to the last item
            if info != len(course) - 2:
                print(",", end='')

#Display the schedule in a formal way.
#Loop through the courses and use the displayCourse function
def displaySchedule(schedule):

    print("Missing days: " + getMissingDays(schedule))
    print("Total hours of freetime: " + str(totalFreeTimePerSchedule(schedule)) + " hours")
    print("Average starting time: " + singleFloatToTime(averageStartTimePerSchedule(schedule)))
    print("Average finishing time: " + singleFloatToTime(averageFinishTimePerSchedule(schedule)))
    print()

    for course in schedule:
        displayCourse(course)
        print()

#Get any missing days in a specific schedule. This is a filter function to determine if any schedule can lack any day
def getMissingDays(schedule):
    allowedDays = {'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'}
    scheduledDays = set()

    for course in schedule:
        for day in range(1, len(course), 2):
            scheduledDays.add(course[day])

    missingDays = list(allowedDays - scheduledDays)

    if len(missingDays) == 0:
        return 'No missing days'

    elif len(missingDays) == 1:
        return missingDays[0]

    else:
        missingDaysDisplay = ','.join(missingDays[:-1]) + ' and ' + missingDays[-1]

    return missingDaysDisplay


#Get the course name from the file. Ex: Get the "Information Structures" from "Information Structures(BCS206Lec3)"
def courseName(string):
    return string[:string.find("(")]

#Convert the course, as a string, to a list.
def courseStringToCourseList(course):
    course = course.split(',')

    return course

#Get the class timings for each day
def timePerEachDay(schedule):
    timePerDay = {}

    for course in schedule:
        for day in range(1, len(course), 2):

            if course[day] not in timePerDay:
                timePerDay[course[day]] = []

    for course2 in schedule:
        for day2 in range(1, len(course2), 2):
            timePerDay[course2[day2]].append(TimeToFloat(course2[day2 + 1]))

    return timePerDay

#Get the difference between two timings, that is, the time between two classes
def timeDifference(timeList):
    timeList.sort()

    difference = 0

    for time in range(len(timeList) - 1):
        difference += timeList[time + 1][0] - timeList[time][1]

    return difference

#Get the total amount of free time between each class per schedule
def totalFreeTimePerSchedule(schedule):
    totalFreeTime = 0

    timePerDay = timePerEachDay(schedule)

    for day in timePerDay:
        timePerDay[day] = timeDifference(timePerDay[day])

    for freeTime in timePerDay.values():
        totalFreeTime += freeTime

    return totalFreeTime


#To store the schedules as a key in a dict
def TwoDimensionalListToTuple(lst):
    for index in range(len(lst)):
        lst[index] = tuple(lst[index])

    lst = tuple(lst)
    return lst

#Function to sort a dictionary. Will be used in sorting filters
def sortDict(Dict):
    #Create an empty dict that will contain our sorted keys & values
    newDict = {}
    #Create a sorted list of the dict values
    SortedDictValues = sorted(list(Dict.values()))
    #Loop through the sorted values and the keys of our dict, if they match, add them to the empty dict
    for sortedValue in SortedDictValues:
        for originalKey in Dict:
            if Dict[originalKey] == sortedValue:
                newDict[originalKey] = sortedValue

    return newDict
#Function to convert a given float to time. Ex: 16.5 --> 16:30
def singleFloatToTime(numTime):

    decimalValue = numTime - int(numTime)
    afterColon = str(int(decimalValue * 60))

    if len(afterColon) == 1:
        afterColon = "0" + afterColon

    TimeDisplay = str(int(numTime)) + ":" + afterColon

    return TimeDisplay

#Function to get the average time classes start on a schedule
def averageStartTimePerSchedule(schedule):
    #Use the previous timePerEachDay function to get the time per each day and sort it to get the first timings per day
    #Add them to a list, so we can calculate the average

    timings = []
    timeList = timePerEachDay(schedule)
    #Loop through the timings and sort them to get the first timing. After that, get the starting time of that timing.
    #Ex: Tuesday has 2 classes, 12:00-15:00 and 16:00-18:00. 12:00-15:00 would be the first timing and 12:00 would be the starting time
    for day in timeList:
        timeList[day] = sorted(timeList[day])
        timings.append(timeList[day][0][0])

    average = sum(timings)/len(timings)

    return average

#Function to get the average time classes finish on a schedule
def averageFinishTimePerSchedule(schedule):
    #Use the previous timePerEachDay function to get the time per each day and sort it to get the last timings per day
    #Add them to a list, so we can calculate the average

    timings = []
    timeList = timePerEachDay(schedule)
    #Loop through the timings and sort them to get the last timing. After that, get the finish time of that timing.
    #Ex: Tuesday has 2 classes, 12:00-15:00 and 16:00-18:00. 16:00-18:00 would be the last timing and 18:00 would be the finish time
    for day in timeList:
        timeList[day] = sorted(timeList[day])
        timings.append(timeList[day][-1][-1])

    average = sum(timings)/len(timings)

    return average


#Generate all possible schedules which will then be filtered to get only eligible schedules
allSchedules= []

def generateAllPossibleSchedules(courseList,holder=[]):
    if len(courseList) == 0:
        allSchedules.append(holder)
    else:
        for courseIndex in courseList[0]:
            generateAllPossibleSchedules(courseList[1:],holder+[courseIndex])

#Get the file path from the user and validate the input
while True:
    try:
        filePath = input("Enter courses file path: ")
        courseFile = open(filePath, 'r')
        break
    except FileNotFoundError:
        print("\nFile not found. Please try again\n")

#Remove any spaces incase they were added. Also, remove any \n at the end of the strings.
courseFileList = courseFile.readlines()
newCourseFileList = []

for course in courseFileList:
    if course != '\n':
        newCourseFileList.append(course)

for newCourse in range(len(newCourseFileList)):
    newCourseFileList[newCourse] = newCourseFileList[newCourse][:-1]

#Get the amount of lectures per each course. This helps in determining the number of courses as well
lecturesPerCourse = {}

#If the course name isn't in the dictionary, add it. If it exists, increment the counter by one
for lecture in newCourseFileList:

    if courseName(lecture) not in lecturesPerCourse:
        lecturesPerCourse[courseName(lecture)] = 1

    else:
        lecturesPerCourse[courseName(lecture)] += 1

#Number of courses will be the length of the lecturesPerCourse dictionary
numberOfCourses = len(lecturesPerCourse)


#Group the same courses together. This will be used for getting all possible schedules by looping later
courses = {}

#Add empty lists for each course
for courseLectureKey in lecturesPerCourse.keys():
    if courseLectureKey not in courses:
        courses[courseLectureKey] = []

#Fill the lists for the corresponding course
for courseItem in newCourseFileList:
    for courseKey in courses.keys():
        if courseName(courseItem) == courseKey:
            courses[courseKey].append(courseStringToCourseList(courseItem))

coursesValues = list(courses.values())
#Get all possible schedules, regardless if courses overlap
generateAllPossibleSchedules(coursesValues)
#Store all the eligible schedules
eligibleSchedules = []

#Loop through the schedules. If the schedule is valid, add it to the eligibleSchedules list
for schedule in allSchedules:
    if isEligibleSchedule(schedule):
        eligibleSchedules.append(schedule)

#Display necessary information about schedules
print("\nNumber of courses: " + str(numberOfCourses))
print("\nNumber of lectures per each course: \n")
for lectureKey in lecturesPerCourse:
    print(lectureKey + ": " + str(lecturesPerCourse[lectureKey]))
print("\nTotal number of possible schedules: " + str(len(allSchedules)))
print("\nTotal number of eligible schedules: " + str(len(eligibleSchedules)))

#Custom exception for menu input validation
class InvalidOption(ValueError):
    pass

#Menu function for filtering the schedules
def menu():
    print("\nFilter options\n")
    print("1. Display all eligible schedules")
    print("2. Display all eligible schedules with missing days")
    print("3. Sort schedule from the lowest free time between courses to highest")
    print("4. Sort schedule from start early to start late")
    print("5. Sort schedule from finish early to finish late")
    print("6. Exit")


    #Validate the input
    while True:
        try:
            option = int(input("\nChoose your option: \n"))
            if option not in range(1,7):
                raise InvalidOption()
            break
        except (ValueError,InvalidOption):
            print("\nPlease use a valid number\n")

    #Loop through the eligible schedules and display them using the display schedule function
    if option == 1:
        for schedules in eligibleSchedules:
            displaySchedule(schedules)
            print()

        menu()
    #Loop through the eligible schedules and check if there are any missing days. If so, display the missing day and the schedule
    elif option == 2:
        #Store the filtered lectures to display them and the amount of courses
        missingDaysLectures = []
        #Store the amount of lectures that lack specific days
        missingDaysCounter = {}
        #Loop through the schedules, if they have missing days, add them to the list and increment their respective counter if already added
        for schedules in eligibleSchedules:

            if getMissingDays(schedules) != 'No missing days':
                missingDaysLectures.append(schedules)

                if getMissingDays(schedules) not in missingDaysCounter:
                    missingDaysCounter[getMissingDays(schedules)] = 1
                else:
                    missingDaysCounter[getMissingDays(schedules)] += 1

        #Display the info
        for missingDayLecture in missingDaysLectures:
            displaySchedule(missingDayLecture)
            print()
        print("\nNumber of schedules: " + str(len(missingDaysLectures)))
        print()

        for days in missingDaysCounter:
            print(days + ": " + str(missingDaysCounter[days]))

        menu()

    elif option == 3:
        #Map each lectures with the amount of free time between courses it has
        scheduleFreeTimes = {}

        for schedules in eligibleSchedules:
            tupleSchedule = TwoDimensionalListToTuple(schedules)
            scheduleFreeTimes[tupleSchedule] = totalFreeTimePerSchedule(schedules)
        #Sort the dictionary
        scheduleFreeTimes = sortDict(scheduleFreeTimes)

        for sortedKeys in scheduleFreeTimes:
            displaySchedule(sortedKeys)
            print()

        menu()

    elif option == 4:

        scheduleStartTime = {}

        for schedules in eligibleSchedules:
            tupleSchedule = TwoDimensionalListToTuple(schedules)
            scheduleStartTime[tupleSchedule] = averageStartTimePerSchedule(schedules)

        scheduleStartTime = sortDict(scheduleStartTime)

        for sortedKeys in scheduleStartTime:

            displaySchedule(sortedKeys)
            print()

        menu()

    elif option == 5:

        scheduleFinishTime = {}

        for schedules in eligibleSchedules:
            tupleSchedule = TwoDimensionalListToTuple(schedules)
            scheduleFinishTime[tupleSchedule] = averageFinishTimePerSchedule(schedules)

        scheduleFinishTime = sortDict(scheduleFinishTime)

        for sortedKeys in scheduleFinishTime:

            displaySchedule(sortedKeys)
            print()

        menu()

    elif option == 6:
        print("\nEnd of program")

menu()

