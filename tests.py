from functions.get_files_info import get_files_info
from functions.get_file_contents import get_file_contents

# print(get_files_info("calculator", "."))
# print(get_files_info("calculator", "pkg"))
# print(get_files_info("calculator", "/bin"))
# print(get_files_info("calculator", "../"))

# print(get_file_contents("calculator", "lorem.txt"))
print(get_file_contents("calculator", "main.py"))
print(get_file_contents("calculator", "pkg/calculator.py"))
print(get_file_contents("calculator", "/bin/cat"))
