import os
import re
from config import *
from testgenlib import *


# TODO: switch, enum, connect trees in func calling, add includes, stab registers

walk_dir = "input"

global_defines = {}
global_registers = {}
global_structs = {}
global_stabs = {}
global_used_struct_fields = {}
global_equals = {}

tree = Tree()


# Переводит комплексную строку в список из структур и полей
def disassemble_on_struct(elem_):
    last_elem = ""
    while last_elem != elem_:
        last_elem = elem_
        if ("." in elem_) or ("->" in elem_):
            if "." in elem_:
                div_ = "."
            else:
                div_ = "->"
            struct_ = elem_.split(div_)[0]
            field_ = elem_.split(div_)[1]
            if "[" in struct_:
                struct_ = struct_.split("[")[0]
            if "[" in field_:
                field_ = field_.split("[")[0]
            elem_ = f"{struct_} {field_}"
    return elem_.split(" ")


# Убирает лишние символы с начала и конца элемента списка
def beautify(words):
    for i_ in range(0, len(words)):
        if words[i_] == '':
            continue
        if words[i_][0] == "\t":
            words[i_] = words[i_][1:]
        if len(words[i_]) == 0:
            continue
        if words[i_][0] == "}":
            words[i_] = words[i_][1:]
        if len(words[i_]) == 0:
            continue
        if words[i_][-1] == "\n":
            words[i_] = words[i_][:-1]
        if len(words[i_]) == 0:
            continue
        if words[i_][-1] == ";":
            words[i_] = words[i_][:-1]
        if len(words[i_]) == 0:
            continue
        if words[i_][-1] == ")":
            words[i_] = words[i_][:-1]
    words = list(filter(None, words))
    return words


# Функция непосредственно парсит файлы
def parser_controller(filename_, lines):
    global global_defines
    global global_structs
    global global_registers
    global global_used_struct_fields
    global tree

    if filename_[-1] == "h":

        level = 0
        curr_struct = {}
        is_enum = False

        for line in lines:

            if "//" in line:
                s_line = str(line.split("//")[0])
                if len(s_line) == 0:
                    continue
                else:
                    line = s_line

            if "enum" in line:
                is_enum = True

            if "{" in line:
                level += 1
                curr_struct[level] = []

            if "}" in line:
                if not is_enum:
                    words = beautify([x for x in line.split(" ") if x != ''])
                    # print(words[-1])
                    struct_name = words[-1].split("[")[0]
                    global_structs[struct_name] = curr_struct[level]
                    curr_struct[level] = []
                else:
                    is_enum = False
                level -= 1

            if level != 0:
                words = [x for x in line.split(" ") if x != '']
                if 'uint' in words[0]:
                    words = beautify([words[0], words[1]])
                if 'struct' in words[0]:
                    words = beautify([words[0]])
                # print(words)
                if (words != ['{\n']) and (words != ['\n']):
                    words = beautify(words)
                    curr_struct[level].append(words)

            if "define" in line:
                if "*)0x" in line:
                    words = [x for x in line.split(" ") if x != '']
                    global_registers[words[1]] = re.search('\(\((.*) \*\)', line).group(1)
                    # print(words[1])
                else:
                    words = beautify([x for x in line.split(" ") if x != ''])
                    if len(words) > 2:
                        global_defines[words[1]] = words[2]

    if filename_[-1] == "c":

        level = -1  # not in function. 0 or more is in function
        previous_line = ''
        func_name = ''
        statement_stack = []

        for line in lines:

            if line[0] == "*":
                continue

            if "=" in line and "==" not in line:
                # TODO: concat this and next line if // on the end
                words = [x for x in line.split(" ") if x != '']
                if "/*" in line:
                    words = words[:words.index("/*")]
                if "//" in line:
                    words = words[:words.index("//")]
                words = beautify(words)
                if not words:
                    continue
                if func_name not in global_equals:
                    global_equals[func_name] = []
                if words[0] in ["uint32", "uint16", "char", "struct", "float"]:
                    continue
                global_equals[func_name].append(words)
                disassemble_on_struct(words[0])
                tree.curr.equals.append(words)
                # print(words)

            if "->" in line or "." in line:  # catch used fields
                words = [x for x in line.split(" ") if x != '']
                for word in words:
                    if "->" in word or "." in word:
                        if "->" in word:
                            divider = "->"
                        else:
                            divider = "."
                        if word[0] == "(":
                            word = word[1:]
                        data = beautify([x for x in word.split(divider)])
                        if len(data) < 2:
                            continue
                        if data[1] == 'h"':
                            continue
                        if data[0] not in global_used_struct_fields:
                            global_used_struct_fields[data[0]] = []
                        if data[1] not in global_used_struct_fields[data[0]]:
                            global_used_struct_fields[data[0]].append(data[1])

            if "{" in line:
                level += 1
                tree.new_branch()
                if level == 0:  # function declared
                    tree.heads_list.append(tree.curr)
                    f_name = [x for x in previous_line.split(" ") if x != ''][1].split("(")[0]
                    tree.curr.statement = f_name
                    func_name = previous_line[:-1]
                else:
                    words = [x for x in previous_line.split(" ") if x != '']
                    words[-1] = words[-1][:-1]
                    if words[0][0] == "\t":
                        words[0] = words[0][1:]
                    if words[0] == "if":
                        tree.curr.statement = words
                        statement_stack.append(words)
                    elif words[0] == "else":
                        statement = (statement_stack.pop()).copy()
                        statement[0] = statement[0] + " !"
                        tree.curr.statement = statement

            if "}" in line:
                level -= 1
                tree.parent()

            previous_line = line


print('walk_dir = ' + walk_dir)

# If your current working directory may change during script execution, it's recommended to
# immediately convert program arguments to an absolute path. Then the variable root below will
# be an absolute path as well. Example:
# walk_dir = os.path.abspath(walk_dir)
print('walk_dir (absolute) = ' + os.path.abspath(walk_dir))

for root, subdirs, files in os.walk(walk_dir):
    print('--\nroot = ' + root)

    for subdir in subdirs:
        print('\t- subdirectory ' + subdir)

    for filename in files:
        file_path = os.path.join(root, filename)

        print('\t- file %s (full path: %s)' % (filename, file_path))

        with open(file_path, 'r', encoding="cp1251") as f:
            parser_controller(filename, f.readlines())


# Afterword on recieved data

# This thing here concats ["struct"] and it's name
for key in global_structs:
    i = len(global_structs[key])-1
    while i != -1:
        if global_structs[key][i][0] == 'struct':
            global_structs[key][i] = ["struct", global_structs[key][i + 1][0]]
            global_structs[key][i + 1].pop()
        i -= 1
    global_structs[key] = list(filter(None, global_structs[key]))

# Getting arrays
for key in global_structs:
    for elem in global_structs[key]:
        if "[" in elem[1]:
            name = elem[1].split("[")[0]
            index = elem[1].split("[")[1].split("]")[0][:-1]
            elem[1] = name
            elem.append(index)

# disassembling complex fields into simple structs and fields
temp_struct = {}
while global_used_struct_fields != temp_struct:
    temp_struct = global_used_struct_fields
    for key in list(global_used_struct_fields):
        for elem in global_used_struct_fields[key]:
            if ("." in elem) or ("->" in elem):
                if "." in elem:
                    div = "."
                else:
                    div = "->"
                struct = elem.split(div)[0]
                field = elem.split(div)[1]
                if "[" in struct:
                    struct = struct.split("[")[0]
                if "[" in field:
                    field = field.split("[")[0]
                if struct not in global_used_struct_fields:
                    global_used_struct_fields[struct] = []
                global_used_struct_fields[struct].append(field)
            if "[" in elem:
                name = elem.split("[")[0]
                global_used_struct_fields[key][global_used_struct_fields[key].index(elem)] = elem.split("[")[0]
        global_used_struct_fields[key] = [i for j, i in enumerate(global_used_struct_fields[key]) if
                                          i not in global_used_struct_fields[key][:j]]

# equaling registers to structs
for key in global_registers:
    if global_registers[key] in global_structs:
        global_structs[key] = global_structs[global_registers[key]]
        del global_structs[global_registers[key]]

print("\nИспользованные структуры и поля")
for key in global_used_struct_fields:
    print(f'\t{key}', global_used_struct_fields[key])
print("\nОбъявленные структуры")
for key in global_structs:
    print(f'\t{key}', global_structs[key])
print("\nРегистры с адресом")
for key in global_registers:
    print(f'\t{key}', global_registers[key])
print("\nДефайны значений")
for key in global_defines:
    print(f'\t{key}', global_defines[key])
print("\nСтруктуры и поля для объявления в заготовках")
for key in list(global_used_struct_fields).__reversed__():
    if key in global_structs:
        print(f'\t{key}', global_used_struct_fields[key])

print("\nПриравнивания в функциях")
for key in global_equals:
    print(f'\t{key}', global_equals[key])


# TODO: autogenerate name of file
with open("output/test_.py", "w+", encoding="UTF-8") as py_file:
    index = 0
    py_file.write(header)
    branch_list = tree.get_branches()
    for branch in branch_list:
        if branch[5]:
            index += 1
            if index < 10:
                s_index = f"0{index}"
            else:
                s_index = f"{index}"
            py_file.write(f"# test_{s_index}: ")
            branch.append(s_index)
            if not branch[2]:
                py_file.write(f"{branch[4]} ")
            else:
                py_file.write(f"{branch[2][0]} {' '.join(branch[4])} ")
            py_file.write(f"\n#\n")
    py_file.write(header_2)
    for key in global_structs:
        if key in global_used_struct_fields:
            py_file.write(f'class {key}(Structure):\n    _fields_ = [')
            for field in global_structs[key]:
                if field[1] in global_used_struct_fields[key]:
                    if field[0] != 'struct':
                        if len(field) == 2:
                            py_file.write(f'("{field[1]}", c_{field[0]}),\n        ')
                        else:
                            py_file.write(f'("{field[1]}", c_{field[0]} * {field[2]}),\n        ')
                    else:
                        if len(field) == 2:
                            py_file.write(f'({field[0]}),\n        ')
                        else:
                            py_file.write(f'({field[1]} * {field[2]}),\n        ')
            py_file.write("]\n\n\n")

    py_file.write('# Номер теста (технический)\ntest_number = c_uint32(1)\n\n')
    py_file.write('# Входные данные\n')

    for key in global_structs:
        if key in global_used_struct_fields:
            py_file.write(f"{key}_in = {key}()\n")
            py_file.write("# Поставить значения отличные от всех остальных!\n")
            for field in global_used_struct_fields[key]:
                py_file.write(f"{key}_in.{field} = 0  # Поменять значение!\n")
            py_file.write("\n")

    py_file.write('\n# Данные для проверки\n')

    variable_test_dict = {}
    for branch in branch_list:
        if branch[5]:
            used_structs = {}
            for elem in branch[5]:
                parsed_elements = disassemble_on_struct(elem[0])
                if parsed_elements[0] not in global_structs:
                    continue
                else:
                    previous_elem = ""
                    for parsed_elem in parsed_elements:
                        if parsed_elem in global_structs:
                            if parsed_elem not in used_structs:
                                used_structs[parsed_elem] = []
                            if previous_elem != "":
                                used_structs[previous_elem].append(parsed_elem)
                        else:
                            used_structs[previous_elem].append(parsed_elem)
                        previous_elem = parsed_elem
            for key in used_structs:
                used_structs[key] = [i for j, i in enumerate(used_structs[key]) if i not in used_structs[key][:j]]
                variable_test_dict[f"test_{branch[6]}_{key}_out"] = [key, used_structs[key], branch[6], branch]

    for key in variable_test_dict:
        py_file.write(f"{key} = {variable_test_dict[key][0]}\n")
        for field in variable_test_dict[key][1]:
            py_file.write(f"{key}.{field} = 0  # Поменять значение!\n")
        py_file.write("\n")

    py_file.write('data_common_in = {\n    "test_number": test_number,\n')
    for key in global_structs:
        if key in global_used_struct_fields:
            py_file.write(f'    "{key}_in": {key}_in,\n')
    py_file.write("}\n")
    py_file.write("\n")
    py_file.write('data_common_out = {\n')
    for key in variable_test_dict:
        py_file.write(f'    "{key}": {key},\n')
    py_file.write("}\n")
    py_file.write("\n")
    py_file.write(header_reglist)
    py_file.write(header_testcase_1)
    py_file.write(f'input_data = [')
    for key in global_structs:
        if key in global_used_struct_fields:
            py_file.write(f'in_data["{key}_in"], ')
    py_file.write(f']\n\n')
    py_file.write(header_testcase_2)

    tree_test_index = {}
    test_in_out_data = {}
    for key in variable_test_dict:
        if variable_test_dict[key][2] not in test_in_out_data:
            test_in_out_data[variable_test_dict[key][2]] = []
            tree_test_index[variable_test_dict[key][2]] = []
        test_in_out_data[variable_test_dict[key][2]].append([variable_test_dict[key][0], variable_test_dict[key][1]])
        tree_test_index[variable_test_dict[key][2]].append(variable_test_dict[key][3])

    for key in test_in_out_data:
        py_file.write(f"\n{comment_line}#\n")
        py_file.write(f"# Тесткейс test_{key}\n#\n")
        py_file.write(f"# 1. Проверяемые требования: BUKSUPK_SW.#####\n")
        py_file.write(f"#    тесткейс проверки работоспособности ")
        if not tree_test_index[key][0][2]:
            py_file.write(f"{tree_test_index[key][0][4]} ")
        else:
            py_file.write(f"{tree_test_index[key][0][2][0]} {' '.join(tree_test_index[key][0][4])} \n")
        py_file.write(f"\n#\n# 2. Входные данные:\n#    ")
        for pair in test_in_out_data[key]:
            py_file.write(f"{pair[0]} | ")
        py_file.write(f"\n#    ")
        for pair in test_in_out_data[key]:
            for elem in pair[1]:
                py_file.write(f"{elem} ")
            py_file.write(f"| ")
        py_file.write(f"\n#\n# 2. Выходные данные:\n#    ")
        for pair in test_in_out_data[key]:
            py_file.write(f"{pair[0]} | ")
        py_file.write(f"\n#    ")
        for pair in test_in_out_data[key]:
            for elem in pair[1]:
                py_file.write(f"{elem} ")
            py_file.write(f"| ")
        py_file.write(f"\n#    ")
        py_file.write(f"\n{comment_line}\n")
        py_file.write(f"def test_{key}():\n")
        py_file.write(f"    in_data = copy.deepcopy(data_common_in)\n")
        if key[0] == '0':
            num = key[1]
        else:
            num = key
        py_file.write(f'    in_data["test_number"].value = {num}\n')
        py_file.write(f'    verify_data = copy.deepcopy(data_common_out)\n')
        py_file.write(f'    out_data = copy.deepcopy(data_common_out)\n')
        py_file.write(f'    REGlist = {test_in_out_data[key]}\n')
        py_file.write(f'    execute_testcase(in_data, verify_data, out_data, REGlist)\n\n')

with open("output/main_low_test.c", "w+", encoding="cp1251") as c_file:
    c_file.write(main_low_header)
    for key in list(global_used_struct_fields).__reversed__():
        if key in global_structs:
            c_file.write(f"typedef static struct {key}_in_ {{\n")
            for elem in global_structs[key]:
                if elem[1] in global_used_struct_fields[key]:
                    if len(elem) == 2:
                        c_file.write(f"    {elem[0]} {elem[1]}")
                    else:
                        c_file.write(f"    {elem[0]} {elem[1]}[{elem[2]}]")
                    if elem[0] == "struct":
                        c_file.write("_in")
                    c_file.write(";\n")
            c_file.write(f"}} {key}_in;\n\n")
    c_file.write(main_low_header_2)
    c_file.write(f"void put_config_values\n{{\n")
    for key in list(global_used_struct_fields).__reversed__():
        if key in global_structs:
            for elem in global_structs[key]:
                if elem[1] in global_used_struct_fields[key]:
                    end = ""
                    if key in global_registers:
                        end = "_in"
                    if len(elem) == 2:
                        c_file.write(f"    {key}{end}.{elem[1]} = {key}->{elem[1]}")
                    else:
                        c_file.write(f"    {key}{end}.{elem[1]}[{elem[2]}] = {key}->{elem[1]}[{elem[2]}]")
                    if elem[0] == "struct":
                        c_file.write("_in")
                    c_file.write(";\n")
    c_file.write(f"}}\n\nvoid get_config_values\n{{\n")
    for key in list(global_used_struct_fields).__reversed__():
        if key in global_structs:
            for elem in global_structs[key]:
                if elem[1] in global_used_struct_fields[key]:
                    end = ""
                    if key in global_registers:
                        end = "_in"
                    if len(elem) == 2:
                        c_file.write(f"    {key}->{elem[1]} = {key}{end}.{elem[1]}")
                    else:
                        c_file.write(f"    {key}->{elem[1]}[{elem[2]}] = {key}{end}.{elem[1]}[{elem[2]}]")
                    c_file.write(";\n")
    c_file.write(f"}}\n")
    c_file.write(main_low_header_3)
    for key in tree_test_index:
        if key[0] == '0':
            num = key[1]
        else:
            num = key
        c_file.write(f"            case {num}: //")
        if not tree_test_index[key][0][2]:
            c_file.write(f"{tree_test_index[key][0][4]} ")
        else:
            c_file.write(f"{tree_test_index[key][0][2][0]} {' '.join(tree_test_index[key][0][4])} \n")
        c_file.write(f"\n")
        c_file.write(f"                {tree_test_index[key][0][4]}();\n")
        c_file.write(f"            break;\n")
    c_file.write(main_low_header_4)
