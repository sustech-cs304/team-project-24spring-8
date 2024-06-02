import os

def generate_project_structure(directory):
    project_structure = ''
    indent = 0

    def traverse_directory(dir_path):
        nonlocal project_structure, indent
        files = os.listdir(dir_path)
        files.sort()

        for file in files:
            if file == 'node_modules' or file == '.git':
                continue
            file_path = os.path.join(dir_path, file)

            if os.path.isfile(file_path):
                project_structure += '  ' * indent + '- ' + file + '\n'
            elif os.path.isdir(file_path):
                project_structure += '  ' * indent + '- ' + file + '/' + '\n'
                if file == 'node_modules' or file == '.git':
                    continue
                indent += 1
                traverse_directory(file_path)
                indent -= 1

    traverse_directory(directory)
    return project_structure

# 使用示例
project_directory = '.'
project_structure = generate_project_structure(project_directory)
print(project_structure)