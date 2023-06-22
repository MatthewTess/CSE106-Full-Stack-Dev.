class Course:
    def __init__(self, department, number, name, credits, lecture_days, start_time, end_time, avg_grade):
        self.department = department
        self.number = number
        self.name = name
        self.credits = credits
        self.lecture_days = lecture_days
        self.start_time = start_time
        self.end_time = end_time
        self.avg_grade = avg_grade

    def __str__(self):
        return "{}{}: {}\nNumber of Credits: {}\nDays of Lectures: {}\nLecture Time: {} - {}\nStat: on average, students get {}% in this course\n\n\n".format(
            self.department, self.number, self.name, self.credits, self.lecture_days, self.start_time, self.end_time,
            self.avg_grade)


# Open file and read the contents
with open("classesinput.txt") as f:
    lines = f.readlines()
    num_courses = int(lines[0])
    courses = []
    for i in range(num_courses):
        # Get the details of each course from the file
        course_dept = lines[i * 8 + 1].strip()
        course_num = lines[i * 8 + 2].strip()
        course_name = lines[i * 8 + 3].strip()
        credits = lines[i * 8 + 4].strip()
        lecture_days = lines[i * 8 + 5].strip()
        start_time = lines[i * 8 + 6].strip()
        end_time = lines[i * 8 + 7].strip()
        avg_grade = lines[i * 8 + 8].strip()
        # Create a new course object using the details
        course = Course(course_dept, course_num, course_name, credits, lecture_days, start_time, end_time, avg_grade)
        courses.append(course)

# Print details
for i, course in enumerate(courses):
    print("COURSE " + str(i + 1) + ": ", end="")
    print(course)