

def input():
    with open("input.csv", "r") as file:
        data = file.read()
        header, *rows = data.split("\n")
        return header, rows

def write(header, data):
    with open("output.csv", "w") as file:
        file.write(header + "\n")
        file.write(data)