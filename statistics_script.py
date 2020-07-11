import tkinter
from tkinter.filedialog import askopenfilename
import tabula


def chooseFile():
    print("Choose a PDF file..")
    # Open FileChooser
    tkinter.Tk().withdraw()
    filename = askopenfilename()

    # Path
    if filename == '':
        path = None
        print("..")
    else:
        path = filename
        print("Done!\n")

    return path


def readFile(path):
    # Read PDF
    df = tabula.read_pdf(path, pages='all', encoding='utf-8', multiple_tables=False)

    for i in df:
        return i


def chooseField(file):
    print('Choose which column contains the grades..')
    i = 0
    for col in file.columns:
        i = i + 1
        print(str(i) + ". " + col)

    grade_to_calculate = input('> ')
    try:
        grade_col = int(grade_to_calculate)
    except:
        grade_col = 0

    while grade_col <= 0 or grade_col > i:
        print("Wrong input..Choose between the columns above!")
        grade_to_calculate = input('> ')
        try:
            grade_col = int(grade_to_calculate)
        except:
            grade_col = 0

    i = 0
    for col in file.columns:
        i = i + 1
        if i == grade_col:
            return col


def calculateStatistics(df, grades):
    passed = 0
    failed = 0
    error = 0
    for i in df[grades]:
        try:
            if type(i) is str:
                format_grade = i.replace(",", ".")
                grade = float(format_grade)
            else:
                grade = i

            if (5 <= grade <= 10) or (50 <= grade <= 100):
                passed = passed + 1
            else:
                failed = failed + 1
        except:
            error = error + 1

    ratio = passed / len(df[grades].index)

    print()
    print("---- STATISTICS ----")
    print("Total Students: ", passed + failed)
    print("Passed: ", passed)
    print("Failed: ", failed)
    print(str("{:.2f}".format(ratio * 100)) + '% passed!')
    print()
    print(error, "Error(s)")
    print()
    analytics = input("Calculate analytics? [y/n]")
    if analytics.lower() == 'y':
        calculateAnalytics(df, grades)


def sortGrades(grade_analytics):
    try:
        sorted_grades = {}
        while len(grade_analytics) > 0:
            min = 1000
            for grade in grade_analytics:
                if grade < min:
                    min = grade
            sorted_grades[min] = grade_analytics[min]
            del grade_analytics[min]
        return sorted_grades
    except:
        print("Something went wrong :(")
        return None


def calculateAnalytics(df, grades):
    grade_analytics = {}
    error = 0
    for i in df[grades]:
        try:
            if type(i) is str:
                format_grade = i.replace(",", ".")
                grade = float(format_grade)
            else:
                grade = i

            if grade in grade_analytics:
                grade_analytics[grade] = grade_analytics[grade] + 1
            else:
                grade_analytics[grade] = 1
        except:
            error = error + 1

    all_grades = len(df) - error
    total_grades = len(grade_analytics)
    final_grades = sortGrades(grade_analytics)
    if final_grades is not None:
        print()
        print("---- ANALYTICS ----")
        print("Total Grades: ", total_grades)
        for grade in final_grades:
            print(str(grade) + "  " + str("{:.2f}".format((final_grades[grade] / all_grades) * 100)) + "%")


# Convert to CSV
# tabula.convert_into(file_path, "inputCSV.csv", encoding='utf-8', output_format="csv")

# Info to Dataframe
# grades = pd.read_csv("inputCSV.csv", encoding='utf-8')

# --------------------- MAIN ---------------------

file_path = chooseFile()

if file_path is not None:
    file = readFile(file_path)

    column = chooseField(file)

    calculateStatistics(file, column)
