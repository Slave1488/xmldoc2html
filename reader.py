def get_line_reader(file):
    line = file.readline()
    while line:
        yield line
        line = file.readline()
