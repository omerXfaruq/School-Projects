# Dev v20 all should be fixed, needs testing

from requests import get
from bs4 import BeautifulSoup
import csv
import sys
from unidecode import unidecode
from time import sleep



programs = ['MANAGEMENT', 'ASIAN+STUDIES', 'ASIAN+STUDIES+WITH+THESIS', 'ATATURK+INSTITUTE+FOR+MODERN+TURKISH+HISTORY', 'AUTOMOTIVE+ENGINEERING', 'MOLECULAR+BIOLOGY+%26+GENETICS', 'BUSINESS+INFORMATION+SYSTEMS', 'BIOMEDICAL+ENGINEERING', 'CRITICAL+AND+CULTURAL+STUDIES', 'CIVIL+ENGINEERING', 'CONSTRUCTION+ENGINEERING+AND+MANAGEMENT', 'COMPUTER+EDUCATION+%26+EDUCATIONAL+TECHNOLOGY', 'EDUCATIONAL+TECHNOLOGY', 'CHEMICAL+ENGINEERING', 'CHEMISTRY', 'COMPUTER+ENGINEERING', 'COGNITIVE+SCIENCE', 'COMPUTATIONAL+SCIENCE+%26+ENGINEERING', 'ECONOMICS', 'EDUCATIONAL+SCIENCES', 'ELECTRICAL+%26+ELECTRONICS+ENGINEERING', 'ECONOMICS+AND+FINANCE', 'ENVIRONMENTAL+SCIENCES', 'ENVIRONMENTAL+TECHNOLOGY', 'EARTHQUAKE+ENGINEERING', 'ENGINEERING+AND+TECHNOLOGY+MANAGEMENT', 'FINANCIAL+ENGINEERING', 'FOREIGN+LANGUAGE+EDUCATION', 'GEODESY', 'GEOPHYSICS', 'GUIDANCE+%26+PSYCHOLOGICAL+COUNSELING', 'HISTORY', 'HUMANITIES+COURSES+COORDINATOR', 'INDUSTRIAL+ENGINEERING', 'INTERNATIONAL+COMPETITION+AND+TRADE', 'CONFERENCE+INTERPRETING', 'INTERNATIONAL+TRADE', 'INTERNATIONAL+TRADE+MANAGEMENT', 'LINGUISTICS', 'WESTERN+LANGUAGES+%26+LITERATURES', 'LEARNING+SCIENCES', 'MATHEMATICS', 'MECHANICAL+ENGINEERING', 'MECHATRONICS+ENGINEERING', 'INTERNATIONAL+RELATIONS%3aTURKEY%2cEUROPE+AND+THE+MIDDLE+EAST', 'INTERNATIONAL+RELATIONS%3aTURKEY%2cEUROPE+AND+THE+MIDDLE+EAST+WITH+THESIS', 'MANAGEMENT+INFORMATION+SYSTEMS', 'FINE+ARTS', 'PHYSICAL+EDUCATION', 'PHILOSOPHY', 'PHYSICS', 'POLITICAL+SCIENCE%26INTERNATIONAL+RELATIONS', 'PRIMARY+EDUCATION', 'PSYCHOLOGY', 'MATHEMATICS+AND+SCIENCE+EDUCATION', 'SECONDARY+SCHOOL+SCIENCE+AND+MATHEMATICS+EDUCATION', 'SYSTEMS+%26+CONTROL+ENGINEERING', 'SOCIOLOGY', 'SOCIAL+POLICY+WITH+THESIS', 'SOFTWARE+ENGINEERING', 'SOFTWARE+ENGINEERING+WITH+THESIS', 'TURKISH+COURSES+COORDINATOR', 'TURKISH+LANGUAGE+%26+LITERATURE', 'TRANSLATION+AND+INTERPRETING+STUDIES', 'SUSTAINABLE+TOURISM+MANAGEMENT', 'TOURISM+ADMINISTRATION', 'TRANSLATION', 'EXECUTIVE+MBA', 'SCHOOL+OF+FOREIGN+LANGUAGES']
departments = ['AD', 'ASIA', 'ASIA', 'ATA', 'AUTO', 'BIO', 'BIS', 'BM', 'CCS', 'CE', 'CEM', 'CET', 'CET', 'CHE', 'CHEM', 'CMPE', 'COGS', 'CSE', 'EC', 'ED', 'EE', 'EF', 'ENV', 'ENVT', 'EQE', 'ETM', 'FE', 'FLED', 'GED', 'GPH', 'GUID', 'HIST', 'HUM', 'IE', 'INCT', 'INT', 'INTT', 'INTT', 'LING', 'LL', 'LS', 'MATH', 'ME', 'MECA', 'MIR', 'MIR', 'MIS', 'PA', 'PE', 'PHIL', 'PHYS', 'POLS', 'PRED', 'PSY', 'SCED', 'SCED', 'SCO', 'SOC', 'SPL', 'SWE', 'SWE', 'TK', 'TKL', 'TR', 'TRM', 'TRM', 'WTR', 'XMBA', 'YADYOK']
deps=[]
for i in range(0,len(programs)):
    deps.append(departments[i]+"&bolum="+programs[i])
    
    
start = sys.argv[1]  # Beginning Term
end = sys.argv[2]  # Ending Term
# Converting Terms To website type
startSTerm = start[5:]
endSTerm = end[5:]

startYear1 = int(start[0:4])            #Converting startYear1 string to integer
endYear1 = int(end[0:4])                #Converting endYear1 string to integer

if startSTerm == 'Fall':                #Convert given input proper url suited form
    startTerm = 1
    startYear2 = startYear1 + 1
elif startSTerm == 'Spring':
    startTerm = 2
    startYear1 = startYear1 - 1
    startYear2 = startYear1 + 1
else:
    startTerm = 3
    startYear1 = startYear1 - 1
    startYear2 = startYear1 + 1

if endSTerm == 'Fall':
    endTerm = 1
    endYear2 = endYear1 + 1
elif endSTerm == 'Spring':
    endTerm = 2
    endYear1 = endYear1 - 1
    endYear2 = endYear1 + 1
else:
    endTerm = 3
    endYear1 = endYear1 - 1
    endYear2 = endYear1 + 1

currentYear1 = startYear1
currentYear2 = startYear2
currentTerm = startTerm

years = []

while True:  # Adding years to years[] while traversing all terms iintermediate of the given input
    year = str(currentYear1) + '/' + str(currentYear2) + '-' + str(currentTerm)
    years.append(year)

    if ((currentYear1 == endYear1) and (currentYear2 == endYear2) and (currentTerm == endTerm)):
        break

    currentTerm += 1

    if (currentTerm == 4):
        currentTerm = 1
        currentYear1 += 1
        currentYear2 += 1


def ConvertYear(year):  # Converting StartYear/EndYear-Term to StartYear-(Spring or Fall or Summer)

    if (year[10:] == "1"):
        return (year[:4] + "-" + "Fall")
    elif (year[10:] == "2"):
        return (year[5:9] + "-" + "Spring")
    else:
        return (year[5:9] + "-" + "Summer")


def IsGrad(courseCode):                                         # Returns true if course is graduate, else false
    for i in range(0, len(courseCode)):
        if ord(courseCode[i]) < 65 and ord(courseCode[i])>40 :  # Reaching the number part in code like in ASIA503 5 is the number that I am looking for
            codeNumber = courseCode[i]
            if ord(codeNumber) > 52:                            # If greater than integer 4 (in ascii 52) then grad
                return True
            else:
                return False


				
				
				
def ChangeComa(myString):		            #Changes , s to ; since it corrupts csv format
	newString=""
	for i in range(0,len(myString)):
		if(myString[i]==","):
			newString+=";"
		else:
			newString+=myString[i]
	return newString		
	
def GetCourseCode(myString):			   #Returns ASIA503 from ASIA503.01
	return myString[:myString.find(".")]
		
		
def GetDepartmentName(myString):		   #Returns departmentName from url
	myString=ChangeComa(myString)
	index=myString.find("&")
	shortName=myString[:index]
	longName=myString[(index+7):]
	longName=longName.replace("%26","&")
	longName=longName.replace("+"," ")
	return shortName+"("+longName+")"
	

# Our main method. Takes depname as parameter from deps array and fill the url part
# and begins crawling into urls. First parses <tr> field with class ‘schtd2’ as gray zone 
# and <tr> field with class ‘schtd2’ as white zone. Appends each row of the page into bodyArray 
# then from bodyArray to bodiesTemp. From bodiesTemp to bodies as pages. From bodies to allBodies 
# as a whole department with given intermediate from input.
def DepMethod(depName):  # Does all the main job for given departmentName, and prints the needed output about that department
    pages = []
    for i in years:
        url = 'https://registration.boun.edu.tr/scripts/sch.asp?donem=' + i + '&kisaadi=' + depName
        pages.append(url)

    bodies = []
    bodies2 = []
    allBodies = []
    allBodies2 = []

    allCourses = []         # All courses array initialized

    whichTerm = 0
    for url in pages:		#Process the url in pages
        bodies = []
        b = True
        r=''
        while r == '':
            try:
                r = get(url)
                break
            except:         # Waits a while for other url to parse the page
                time.sleep(1)
                continue
        
        response = r
        html_soup = BeautifulSoup(response.text, 'html.parser') # Using BeautifulSoup as scraping tool
        type(html_soup)

        title = html_soup.find_all('tr', class_='schtd2')       # Finds <tr> field with class ‘schtd2’ as white zone
        if title is None:
            continue
        for bodiesTitle in title:
            body = bodiesTitle.find_all('td')                   # Finds all <td> fields as 13 fields
            bodyArray = []                                      # Initialize bodyarray to fill it with fields
            i = 0
            for tds in body:
                tds = unidecode(tds.text)                       # Using unicode library to smooth the UTF-8 format as Turkish characters appears
                bodyArray.append(tds)                           # Appends each row of the page into bodyArray
                i += 1

            bodiesTemp = []
            if(len(bodyArray[0])<4):
                continue
            bodiesTemp.append(bodyArray[0])                     # CodeSegment
            bodiesTemp.append(bodyArray[2])                     # Course name
            bodiesTemp.append(bodyArray[5])                     # Instructor name
            bodiesTemp.append(whichTerm)                        # Which term
            bodies.append(bodiesTemp)                           # Appends bodiestemp to bodies array
            allCourses.append(bodiesTemp)                       # Appends bodiestemp to allcourses to use it to retrieve all courses

        allBodies.append(bodies)                                # Appends all bodies(pages/terms) to allBodies

        title2 = html_soup.find_all('tr', class_='schtd')       # Same as above just schtd instead schtd2
        if title2 is None:
            continue
        for bodiesTitle in title2:
            body = bodiesTitle.find_all('td')
            bodyArray = []
            i = 0
            for tds in body:
                tds = unidecode(tds.text)
                bodyArray.append(tds)
                i += 1
            bodiesTemp = []
            if(len(bodyArray[0])<4):
                continue
            bodiesTemp.append(bodyArray[0])  # CourseCode
            bodiesTemp.append(bodyArray[2])  # CourseName
            bodiesTemp.append(bodyArray[5])  # CourseInstructor
            bodiesTemp.append(whichTerm)     # CourseTermNumber
            bodies2.append(bodiesTemp)
            allCourses.append(bodiesTemp)
        allBodies2.append(bodies2)

        whichTerm += 1

    if (len(allCourses) == 0):
        return

    sortedCourses = sorted(allCourses)  # Sort courses according to coursecode

    # Write a Row for each course

    departmentTable = ""  # Will be printed for department

    currentCourse = sortedCourses[0]

    if (IsGrad(currentCourse[0])):  
        graduate = 1
        undergraduate = 0
    else:
        graduate = 0
        undergraduate = 1

    instructorInTotalOfferings = []      # I number in Total Offerings
    instructorPerCourse = []             # Number in #/#
    xList = [0] * len(years)             # Will Marks  Xs with 1
    for i in sortedCourses:
        if (GetCourseCode(i[0]) != GetCourseCode(currentCourse[0])):  # Changing course code , ie cmpe150 to cmpe160
            if (IsGrad(i[0])):
                graduate += 1
            else:
                undergraduate += 1
            # Draw the last course row  
            row = "," + GetCourseCode(currentCourse[0])+ "," + ChangeComa(currentCourse[1]) + ","  # Course code and course name
            for j in xList:              # Look to xList, for drawing x
                if (j == 1):
                    row += "x"
                row += ","
            row += str(CalculateCourseGivenInTermsNumber(xList)) + "/"  # write   #/# part
            instructors = list(set(instructorPerCourse))
            numOfInstructor = len(instructors)
            row += str(numOfInstructor)
            row += "\n"                  # Finish the row
            departmentTable += row

            xList = [0] * len(years)     # Reset course variables
            currentCourse = i
            instructorPerCourse = []
        
        instructorName = i[2]

        if (instructorName != "STAFF"):
            instructorInTotalOfferings.append(i[2])
            instructorPerCourse.append(i[2])

        xList[i[3]] = 1                  # mark X the term as 1

		
	# Draw the last course row
    row = "," + GetCourseCode(currentCourse[0])+ "," + ChangeComa(currentCourse[1]) + ","  # Course code and course name
    for j in xList:                      # Look to xList, for drawing x
        if (j == 1):
            row += "x"
        row += ","
    row += str(CalculateCourseGivenInTermsNumber(xList)) + "/"  # write   #/# part
    instructors = list(set(instructorPerCourse))
    numOfInstructor = len(instructors)
    row += str(numOfInstructor)
    row += "\n"                          # Finish the row
    departmentTable += row
    begginingRow = ""
    begginingRow += GetDepartmentName(depName)+","			            #First Row of the department, Name etc
    begginingRow += ",U" + str(undergraduate) + " G" + str(graduate)	#UG under Course Code column
    begginingRow += ", "

    begginingRow += CountUGI(allBodies, allBodies2)

    instructors = list(set(instructorInTotalOfferings))
    numOfInstructor = len(instructors)

    begginingRow += " I" + str(numOfInstructor)

    departmentTable = begginingRow + "\n" + departmentTable
    print(departmentTable)


# Parse xList to count Courses in terms
def CalculateCourseGivenInTermsNumber(xList):		#Calculates 1 s in the array, ie how many terms this course is given
    number = 0
    for i in xList:
        if i == 1:
            number += 1

    return number

# Traverse allBodies(gray zones) and allBodies2(white zones) and 
# concatenate findings about Undergraduate(U),  Graduate(G) and Instructor(I). 
# Return numbers of U, G, I to show in table. 
# At the end sum all findings and calculate Total
def CountUGI(allBodies, allBodies2):		        #Returns the UGI string in the department name row,
    numOfUndergrad = 0
    numOfGrad = 0
    numOfInstructor = 0
    instructors = []
    returnTheString = ""
    totalU = 0
    totalG = 0
    for i in range(0, len(allBodies)):
        courses=[]
        numOfUndergrad = 0
        numOfGrad = 0
        numOfInstructor = 0
        instructors = []
        for j in range(0, len(allBodies[i])):
            code = allBodies[i][j][0]               # CourseCode like ASIA503.1
            instructor = allBodies[i][j][2]
            instructors.append(instructor) 
            courses.append(GetCourseCode(code))     # Fills the couses array
            
        for j in range(0, len(allBodies2[i])):
            code = allBodies2[i][j][0]              # CourseCode like ASIA503.1
            instructor = allBodies2[i][j][2]
            instructors.append(instructor)
            courses.append(GetCourseCode(code))     # Fills the courses array

        instructors = list(set(instructors))        # To make instructor list unique eliminate repetitions
        numOfInstructor = len(instructors)
        
        
        courses=list(set(courses))
        numOfCourses=len(courses)
        
        
        for i in courses:       #Look for dinstict courses
            if IsGrad(i):
                numOfGrad+=1
            else:
                numOfUndergrad+=1
        
        returnTheString += 'U' + str(numOfUndergrad) + ' G' + str(numOfGrad) + ' I' + str(numOfInstructor) + ',' #UGI for each term
        totalU += numOfUndergrad
        totalG += numOfGrad

    returnTheString += 'U' + str(totalU) + ' G' + str(totalG)  #UG for Total Offerings

    return returnTheString


# First Row Of The Output

s = ""

for i in years:  # Need To Make a convertion to years, like 2017/2018-2 -> 2018 Spring
    s = s + "," + ConvertYear(i)

print("Dept./Prog.(Name),Course Code, Course Name" + s + ",Total Offerings")
for dep in deps:		#Work the retrieving and printing for all the departments
    DepMethod(dep)
    