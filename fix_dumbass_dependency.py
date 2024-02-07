import sys
import os

broken_file_name = 'plotting.py'
broken_style_name = 'seaborn-deep'
actual_style_name = 'seaborn-v0_8-deep'  # gotten from matplotlib.style.available


def fix_dumbass_dependency():
    global broken_file_name, broken_style_name, actual_style_name

    python_version = f"python{sys.version_info.major}.{sys.version_info.minor}"
    lib_path = os.path.join(os.getcwd(), '.venv', 'lib', python_version, 'site-packages', 'pypfopt')
    files_in_pypfopt = os.listdir(lib_path)

    if broken_file_name not in files_in_pypfopt:
        print(f"{broken_file_name} not found in: {lib_path}")
        exit(1)

    broken_ass_file_lines = []  # higher-scope var to store fixed lines
    # Yes, I'm storing all the files from the broken-ass file in this list
    # No, I don't care. It's not that much, and it gets the job done
    with open(os.path.join(lib_path, broken_file_name), "r") as broken_ass_code_file:
        lines = broken_ass_code_file.readlines()
        broken_line: int = -1

        for line_number, line in enumerate(lines):
            if actual_style_name in line:
                print("Seems like the broken file has been fixed. Moving on...")
                return

            if broken_style_name in line:
                broken_line = line_number
                break

        if broken_line == -1:
            print("ERROR: Did not find broken line, for some reason")
            exit(1)

        lines[broken_line] = lines[broken_line].replace(broken_style_name, actual_style_name)
        broken_ass_file_lines = lines

    with open(os.path.join(lib_path, broken_file_name), "w+") as broken_ass_code_file:
        broken_ass_code_file.writelines(broken_ass_file_lines)
