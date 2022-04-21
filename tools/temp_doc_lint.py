#!/usr/bin/env python3

from csv import field_size_limit
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
BLANK_LINE = f"| {LENGTH_TUPLE[0]*SPACEBAR}| {LENGTH_TUPLE[1]*SPACEBAR}| {LENGTH_TUPLE[2]*SPACEBAR}|\n"


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
        file.write(updated_data)
    return location


def generate_heirarchy_dict():
    rootdir = pathlib.Path(__file__).resolve().parent.parent
    print(rootdir)
    final_root = pathlib.Path(join(rootdir, "zulipterminal"))
    print(final_root)
    relative_path = final_root.relative_to(rootdir)
    print(relative_path)
    path = pathlib.Path(__file__).resolve().parent.parent

    folder_paths_dictionary = {}

    # file_list = []

    for f in final_root.glob("**/*"):
        if f.is_dir():  # and f != '__init__.py':
            # append_name = f.relative_to(rootdir)
            relative_path = f.relative_to(rootdir)
            print(relative_path)

            folder_paths_dictionary[str(relative_path)] = f

    print("FILE DICTIONARY: ")
    pprint.pprint(folder_paths_dictionary)
    print("GET DOCSTRINGS PATHS: ")
    get_docstrings()
    # for x in file_list:
    #     print(x)

def split_string(long_string):
    first_part = long_string[:104]
    first_line = first_part.rsplit(' ', 1)
    # print(first_line)
    second_line = long_string.replace(first_line[0], '')
    print("first_line: ", first_line[0])
    print("second_line: ", second_line)
    return (first_line[0], second_line)


def extract_folder_structure():
    folder_paths = {
        "zulipterminal": join(parent_root, "zulipterminal"),
        "zulipterminal/cli": join(parent_root, "zulipterminal", "cli"),
        "zulipterminal/config": join(parent_root, "zulipterminal", "config"),
        "zulipterminal/ui_tools": join(parent_root, "zulipterminal", "ui_tools"),
    }
    # print(folder_paths)
    folders_and_files = {}
    for folder, path in folder_paths.items():
        # print("Folder name: ", folder, ", path: ", path)
        folders_and_files[folder] = [
            file
            for file in listdir(path)
            if (isfile(join(path, file)) and file != "__init__.py")
        ]
    return folders_and_files

def get_docstrings() -> Tuple[Dict[str, str], Dict[str, List[str]]]:
    # root = join(getcwd(), "zulipterminal")
    total_files = extract_folder_structure()
    file_doc_string = {}
    all_zt_files_dict = {}
    for folder, files in total_files.items():
        file_doc_string[str(folder)] = {}
        for file in files:
            imported_file = importlib.import_module(
                f'{folder.replace("/",".")}.{file[:-3]}'
            )
            docstring = cast(str, imported_file.__doc__)
            file_doc_string[str(folder)][file] = docstring.strip().replace("\n", " ")
            all_zt_files_dict[file] = docstring.strip().replace("\n", " ")
    # print("files dictionary: ")
    # pprint.pprint(all_zt_files_dict)
    # print("Total files: ")
    # pprint.pprint(total_files)
    # pprint.pprint(file_doc_string)
    # return (all_zt_files_dict, total_files, file_doc_string)
    return file_doc_string


def create_file():
    string_and_folders = get_docstrings()
    with open(developer_doc, "r+") as file:
        doc_data = file.readlines()

    write_location = INDEX
    doc_to_write = doc_data[: INDEX - 1]
    print("Enters the function")
    print("Length: ", len(doc_to_write))

    final_files_list = []
    for folder in string_and_folders:
        folder_printed = False
        dictionary_of_files = string_and_folders[str(folder)]

        folder_text = str(folder)
        for file in sorted(dictionary_of_files):
            description_text = string_and_folders[folder][file]
            if folder_printed is True:
                folder_text = " "
            
            if len(description_text) > LENGTH_TUPLE[2]:
                first_line, second_line = split_string(description_text)
                text_tuple = (folder_text, file, first_line)
                folder_name, file_name, desc = text_with_spaces(text_tuple, LENGTH_TUPLE)
                new_line = f"| {folder_name}| {file_name}| {desc}|\n"
                final_files_list.append(new_line)
                text_tuple = (folder_text, file, second_line)
                folder_name, file_name, desc = text_with_spaces(text_tuple, LENGTH_TUPLE)
                new_line = f"|{LENGTH_TUPLE[0]*SPACEBAR} | {LENGTH_TUPLE[1]*SPACEBAR}|{desc} |\n"
                final_files_list.append(new_line)
                folder_printed = True
            else:
                text_tuple = (folder_text, file, description_text)
                folder_name, file_name, desc = text_with_spaces(text_tuple, LENGTH_TUPLE)
                new_line = f"| {folder_name}| {file_name}| {desc}|\n"
                final_files_list.append(new_line)
                folder_printed = True

        folder_name, file_name, desc = text_with_spaces(BLANK_LINE_TUPLE, LENGTH_TUPLE)
        blank_line = f"| {folder_name}| {file_name}| {desc}|\n"
        final_files_list.append(BLANK_LINE)
        # write_location = write_to_file(final_files_list, doc_to_write, write_location)

    SCRIPTS_TUPLE = (SCRIPTS, " ", SCRIPTS_DESC)
    folder_name, file_name, desc = text_with_spaces(SCRIPTS_TUPLE, LENGTH_TUPLE)
    scripts_line = f"| {folder_name}| {file_name}| {desc}|\n"
    folder_name, file_name, desc = text_with_spaces(BLANK_LINE_TUPLE, LENGTH_TUPLE)
    final_files_list.append(scripts_line)
    final_files_list.append(BLANK_LINE)

    THEMES_TUPLE = (THEMES, " ", THEMES_DESC)
    folder_name, file_name, desc = text_with_spaces(THEMES_TUPLE, LENGTH_TUPLE)
    themes_line = f"| {folder_name}| {file_name}| {desc}|\n"

    final_files_list.append(themes_line)
    write_to_file(final_files_list, doc_to_write, write_location)


def extract_docstrings_from_file_overview() -> Dict[str, str]:
    with open(developer_doc, "r") as file:
        doc_data = file.readlines()

    # table is present from line 6 to (length - 1)
    computed_doc_dict = {}
    file_size = len(doc_data)
    # print(file_size)
    # for folder in range(INDEX-1, len(doc_data)):
    #     if str(folder)
    # computed_doc_dict[str(folder)] = {}

    folder_name = ""
    file_name = ""
    for i in range(INDEX - 1, len(doc_data) - 4):
        _, folder, filename, docstring, _ = str(doc_data[i]).split("|")
        folder, filename = folder.strip(), filename.strip()
        # print("VALUE OF FOLDER: ", folder)
        if folder:
            folder_name = folder
            # print("FOLDER_NAME: ", folder_name)
            computed_doc_dict[str(folder_name)] = {}
        if docstring.strip():
            print(filename)
            if filename:
                file_name = filename
                computed_doc_dict[folder_name][file_name] = docstring.strip()
            else:
                computed_doc_dict[folder_name][file_name] = computed_doc_dict[folder_name][file_name] + SPACEBAR+ docstring.strip()
                
        #         print(f'{folder_file_docstring[folder][file]} is missing')
    # for i in range(6, len(doc_data)):
    #     _, _, filename, docstring, _ = str(doc_data[i]).split('|')
    #     filename = filename.strip()
    #     if filename:
    #         computed_doc_dict[filename] = docstring.strip()
    print(computed_doc_dict)
    return computed_doc_dict


def lint_files():
    folder_file_docstring = get_docstrings()
    computed_doc_dict = extract_docstrings_from_file_overview()
    missing_file = ""
    try:
        for folder in folder_file_docstring:
            for file in folder_file_docstring[folder]:
                missing_file = file
                assert computed_doc_dict[folder][file] == folder_file_docstring[folder][file]
    except AssertionError:
        # in case the docstrings do not match
        print("Docstrings changed")
        print("Run './tools/lint-docstring -fix' to fix")
        sys.exit(1)
    except KeyError:
        # in case a new file is added and its docstring is not present in the document
        print(f'{missing_file} has been added')
        # print(str(folder_file_docstring[folder]))
        print("Run './tools/lint-docstring -fix' to fix")
        sys.exit(1)
    print("Successful")



# linting_file()
# temp_str = "Contains color definitions or functions common across all themes. For further details on themefiles look at the theme contribution guide."
# split_string(temp_str)
# lint_files()
# create_file()
# extract_docstrings_from_file_overview()
# get_docstrings()
# generate_heirarchy_dict()

def main(fix_file: bool=False) -> None:
    if fix_file:
        create_file()
        # get_docstrings()
    # generate_heirarchy_dict()
    else:
        lint_files()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Lint and fix docstrings"
                                                 "in all ZulipTerminal files")
    parser.add_argument('-fix', action='store_true',
                        help="""Update developer-file-overview with
                        docstrings of all files""")
    args = parser.parse_args()
    main(args.fix)
