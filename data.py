

def input(filename):
    with open(filename, "r") as file:
        data = file.read()
        header, *rows = data.split("\n")
        return header, rows

def write(filename, header, data):
    with open(filename, "w") as file:
        file.write(header + "\n")
        file.write(data)