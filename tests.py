from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file

# #Tests for get_files_info
# print(get_files_info("calculator", "."))
# print(get_files_info("calculator", "pkg"))
# print(get_files_info("calculator", "/bin"))
# print(get_files_info("calculator", "../"))

##Tests for get_file_content
#print(get_file_content("calculator", "lorem.txt"))

# print(get_file_content("calculator", "main.py"))
# print(get_file_content("calculator", "pkg/calculator.py"))
# print(get_file_content("calculator", "/bin/cat"))

# #Tests for write_file
# print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
# print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
# print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))

#Test for run_python.py
print(run_python_file("calculator", "main.py"))
print(run_python_file("calculator", "tests.py"))
print(run_python_file("calculator", "../main.py")) #This should error
print(run_python_file("calculator", "nonexistent.py")) #This should error