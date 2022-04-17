#!/usr/bin/env python3
"""
| Folder                 | File                | Description                                                                                            |
| ---------------------- | ------------------- | ------------------------------------------------------------------------------------------------------ |
| zulipterminal/         | api_types.py        | Preliminary Zulip API types defined in python, to allow type checking                                  |
"""

import argparse
import importlib
import sys
from os import getcwd, listdir
from os.path import isfile, join
from typing import Dict, List, Tuple, cast


developer_doc = join(getcwd(), 'docs', 'aa-doc-string.md')

def get_docstrings() -> Tuple[Dict[str, str], Dict[str, List[str]]]:
    root = join(getcwd(), 'zulipterminal')
    folder_paths = {
        'zulipterminal': root,
        'zulipterminal/cli': join(root, 'cli'),
        'zulipterminal/config': join(root, 'config'),
        'zulipterminal/ui_tools': join(root, 'ui_tools')
    }
    total_files = {}
    for folder, path in folder_paths.items():
        total_files[folder] = [file for file in listdir(path)
                               if(isfile(join(path, file))
                               and file != '__init__.py')]
    all_zt_files_dict = {}
    for folder, files in total_files.items():
        for file in files:
            print("Name of the file: ", file)
            imported_file = importlib.import_module(
                            f'{folder.replace("/",".")}.{file[:-3]}')
            docstring = cast(str, imported_file.__doc__)
            print(docstring)
            all_zt_files_dict[file] = docstring.strip().replace('\n', ' ')
    return (all_zt_files_dict, total_files)


def get_file_overview_doc_docstrings() -> Dict[str, str]:
    with open(developer_doc, 'r') as file:
        doc_data = file.readlines()

    # table is present from line 6 to (length - 1)
    computed_doc_dict = {}
    for i in range(6, len(doc_data)):
        _, _, filename, docstring, _ = str(doc_data[i]).split('|')
        filename = filename.strip()
        if filename:
            computed_doc_dict[filename] = docstring.strip()
    return computed_doc_dict


def lint_files() -> None:
    all_zt_files_dict, _ = get_docstrings()
    computed_doc_dict = get_file_overview_doc_docstrings()
    try:
        for file in all_zt_files_dict:
            assert (all_zt_files_dict[file]
                    == computed_doc_dict[file])
    except AssertionError:
        print("Docstrings changed")
        print("Run './tools/docstring -fix' to fix")
        sys.exit(1)
    except KeyError:
        print("New File has been added")
        print("Run './tools/docstring -fix' to fix")
        sys.exit(1)
    print("Successful")


def update_file_overview_doc() -> None:
    all_zt_files_dict, total_files = get_docstrings()
    with open(developer_doc, 'r+') as file:
        doc_data = file.readlines()

    folder = None
    i = 6  # table starts from 6 to end
    while(i < len(doc_data)):
        line = doc_data[i].split('|')
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
                tabLength = '\t' * 6
                for new_file in total_files[str(folder)]:
                    new_line = f"|{tabLength} | {new_file}\t| {all_zt_files_dict[new_file]}\t|"
                    new_files_list.append(new_line)
                doc_data[(i - 1):(i - 1)] = new_files_list
                i += len(total_files[str(folder)])
                total_files.pop(str(folder))
        i += 1
    updated_data = ''.join(doc_data)
    with open(developer_doc, 'w') as file:
        file.write(updated_data)


def main(fix_file: bool=False) -> None:
    if fix_file:
        update_file_overview_doc()
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