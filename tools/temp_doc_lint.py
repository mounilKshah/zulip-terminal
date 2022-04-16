import os
from typing import Dict, List, Tuple, cast
from os.path import isfile, join
from os import getcwd, listdir
import pathlib
import sys
import importlib
import argparse
import pprint

# txt = "| ---------------------- | ------------------- | ------------------------------------------------------------------------------------------------------ |"
# final_txt = txt.split("|")
# for x in final_txt:
#     print("Length of txt: ", len(x))
#     print(x)

INDEX = 7

parent_root = pathlib.Path(__file__).resolve().parent.parent
developer_doc = join(parent_root, "docs", "aa-doc-string.md")

LENGTH_TUPLE = (23, 20, 103)
SPACEBAR = " "
SCRIPTS = "zulipterminal/scripts"
SCRIPTS_DESC = "Scripts bundled with the application"
THEMES = "zulipterminal/themes"
THEMES_DESC = "Themes bundled with the application"

BLANK_LINE_TUPLE = (" ", " ", " ")
BLANK_LINE = f"| {23*SPACEBAR}| {20*SPACEBAR}| {103*SPACEBAR}|\n"


def text_with_spaces(text_tuple, length_tuple=LENGTH_TUPLE):
    folder_width, file_width, desc_width = length_tuple
    folder_text, file_text, desc_text = text_tuple
    folder_spaces = (folder_width - len(folder_text)) * SPACEBAR
    file_spaces = (file_width - len(file_text)) * SPACEBAR
    desc_spaces = (desc_width - len(desc_text)) * SPACEBAR
    folder_name = folder_text + folder_spaces
    file_name = file_text + file_spaces
    desc_name = desc_text + desc_spaces
    return (folder_name, file_name, desc_name)


def write_to_file(new_files_list, current_doc_data, location):
    current_doc_data[(location) : (location - 1)] = new_files_list
    temp_list = new_files_list
    location += len(new_files_list)
    location += 1
    updated_data = "".join(current_doc_data)
    with open(developer_doc, "w") as file:
        # print("Value of i: ", i)
        file.write(updated_data)
    return location

def generate_heirarchy_dict():
    rootdir = pathlib.Path(__file__).resolve().parent.parent
    print(rootdir)
    # Return a list of regular files only, not directories
    final_root = pathlib.Path(join(rootdir, 'zulipterminal'))
    # print(type(final_root))
    print(final_root)
    relative_path = final_root.relative_to(rootdir)
    print(relative_path)
    # mport os
    path = pathlib.Path(__file__).resolve().parent.parent
    # os.path.join(os.path.basename(os.path.dirname(p)), os.path.basename(p))
    # This works on python 3:

    # # str(p.relative_to(p.parent.parent))
    # get_docstrings()
    folder_paths_dictionary = {}

    # file_list = []
    
    for f in final_root.glob('**/*'):
        if f.is_dir(): # and f != '__init__.py':
            # append_name = f.relative_to(rootdir)
            relative_path = f.relative_to(rootdir)
            print(relative_path)

            folder_paths_dictionary[str(relative_path)] = f
    # file_list = [
    #         file
    #         for file in final_root.glob('**/*.py')
    #         if (isfile(join(path, file)) and file != "__init__.py")
    #         ]
    print("FILE DICTIONARY: ")
    pprint.pprint(folder_paths_dictionary)
    print("GET DOCSTRINGS PATHS: ")
    get_docstrings()
    # for x in file_list:
    #     print(x)



def get_docstrings() -> Tuple[Dict[str, str], Dict[str, List[str]]]:
    root = join(getcwd(), "zulipterminal")
    # print(root)
    print(parent_root)
    folder_paths = {
        "zulipterminal": join(parent_root, "zulipterminal"),
        "zulipterminal/cli": join(parent_root, "zulipterminal", "cli"),
        "zulipterminal/config": join(parent_root, "zulipterminal", "config"),
        "zulipterminal/ui_tools": join(parent_root, "zulipterminal", "ui_tools"),
    }
    print(folder_paths)
    total_files = {}
    for folder, path in folder_paths.items():
        # print("Folder name: ", folder, ", path: ", path)
        total_files[folder] = [
            file
            for file in listdir(path)
            if (isfile(join(path, file)) and file != "__init__.py")
        ]
    all_zt_files_dict = {}
    for folder, files in total_files.items():
        for file in files:
            # print("Name of the file: ", file)
            imported_file = importlib.import_module(
                f'{folder.replace("/",".")}.{file[:-3]}'
            )
            # print(imported_file)
            docstring = cast(str, imported_file.__doc__)
            # print(docstring)
            all_zt_files_dict[file] = docstring.strip().replace("\n", " ")
    # print("files dictionary: ")
    # pprint.pprint(all_zt_files_dict)
    print("Total files: ")
    pprint.pprint(total_files)
    return (all_zt_files_dict, total_files)


def create_file_old() -> None:
    all_zt_files_dict, total_files = get_docstrings()
    with open(developer_doc, "r+") as file:
        doc_data = file.readlines()

    folder = None
    i = 6  # table starts from 6 to end
    while i < len(doc_data):
        line = doc_data[i].split("|")
        filename = line[2].strip()

        # folder name is not present in every row
        if line[1].strip():
            folder = (line[1].strip())[:-1]
        line[3] = line[3].strip()  # docstring
        if filename and line[3]:
            line[3] = f" {all_zt_files_dict[filename]}\t"
            doc_data[i] = f'{"|".join(line)}'
            total_files[str(folder)].remove(filename)
        else:
            # adding new files
            if total_files[str(folder)]:
                new_files_list = []
                tabLength = "\t" * 6
                for new_file in total_files[str(folder)]:
                    new_line = (
                        f"|{tabLength} | {new_file}\t| {all_zt_files_dict[new_file]}\t|"
                    )
                    new_files_list.append(new_line)
                doc_data[(i - 1) : (i - 1)] = new_files_list
                i += len(total_files[str(folder)])
                total_files.pop(str(folder))
        i += 1
    updated_data = "".join(doc_data)
    with open(developer_doc, "w") as file:
        file.write(updated_data)


def create_file():
    all_zt_files_dict, total_files = get_docstrings()
    with open(developer_doc, "r+") as file:
        doc_data = file.readlines()

    write_location = INDEX
    print("Enters the function")
    print("Length: ", len(doc_data))
    temp_var = 0
    for folder in total_files:
        folder_printed = False
        list_of_files = total_files[str(folder)]
        final_files_list = []

        folder_text = str(folder)
        for new_file in sorted(list_of_files, key=lambda s: s.lower()):
            if folder_printed is True:
                folder_text = " "
            text_tuple = (folder_text, str(new_file), all_zt_files_dict[new_file])
            folder_name, file_name, desc = text_with_spaces(text_tuple, LENGTH_TUPLE)
            new_line = f"| {folder_name}| {file_name}| {desc}|\n"
            final_files_list.append(new_line)
            folder_printed = True

        folder_name, file_name, desc = text_with_spaces(BLANK_LINE_TUPLE, LENGTH_TUPLE)
        blank_line = f"| {folder_name}| {file_name}| {desc}|\n"
        final_files_list.append(BLANK_LINE)
        write_location = write_to_file(final_files_list, doc_data, write_location)

    SCRIPTS_TUPLE = (SCRIPTS, " ", SCRIPTS_DESC)
    folder_name, file_name, desc = text_with_spaces(SCRIPTS_TUPLE, LENGTH_TUPLE)
    scripts_line = f"| {folder_name}| {file_name}| {desc}|\n"
    folder_name, file_name, desc = text_with_spaces(BLANK_LINE_TUPLE, LENGTH_TUPLE)
    final_files_list.append(scripts_line)
    final_files_list.append(BLANK_LINE)
    # temp_var = temp_var +1

    THEMES_TUPLE = (THEMES, " ", THEMES_DESC)
    folder_name, file_name, desc = text_with_spaces(THEMES_TUPLE, LENGTH_TUPLE)
    themes_line = f"| {folder_name}| {file_name}| {desc}|\n"

    final_files_list.append(themes_line)
    write_to_file(final_files_list, doc_data, write_location)
    # doc_data[(i):(i - 1)] = final_files_list
    # temp_list = list_of_files
    # i = i + len(list_of_files) + 1
    # # i += 1
    # updated_data = ''.join(doc_data)
    # with open(developer_doc, 'w') as file:
    #     # print("Value of i: ", i)
    #     file.write(updated_data)
    print(INDEX)


# create_file()

# temp_var = 1
# print("======= OUTSIDE Temporary variable: ", temp_var, " =============")
# get_docstrings()
# rootdir = pathlib.Path(__file__).resolve().parent.parent
# print(rootdir)
# # Return a list of regular files only, not directories
# final_root = pathlib.Path(join(rootdir, 'zulipterminal'))
# # print(type(final_root))
# print(final_root)
# relative_path = final_root.relative_to(rootdir)
# print(relative_path)
# mport os
# path = pathlib.Path(__file__).resolve().parent.parent
# os.path.join(os.path.basename(os.path.dirname(p)), os.path.basename(p))
# # This works on python 3:

# str(p.relative_to(p.parent.parent))
# get_docstrings()

# file_list = []
# for f in final_root.glob('**/*'):
#     if f.is_dir(): # and f != '__init__.py':
#         # append_name = f.relative_to(rootdir)
#         file_list.append(f)
# # file_list = [f for f in final_root.glob('**/*.py') if f.is_file()]
# print("Initial file list: ")
# for x in file_list:
#     print(x)

# print(file_list)
# For absolute paths instead of relative the current dir
# file_list = [f for f in rootdir.resolve().glob('**/*') if f.is_file()]
# print("NEW file list: ")
# for x in file_list:
#     print(x)


def main(fix_file: bool=False) -> None:
    # if fix_file:
    # create_file()
    generate_heirarchy_dict()
    # else:
    #     lint_files()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Lint and fix docstrings"
                                                 "in all ZulipTerminal files")
    parser.add_argument('-fix', action='store_true',
                        help="""Update developer-file-overview with
                        docstrings of all files""")
    args = parser.parse_args()
    main(args.fix)
