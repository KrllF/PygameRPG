from csv import reader

def read_csv(path):
    lay_map = []
    with open(path, newline='') as file:
        lay = reader(file, delimiter=',')
        lay_map = [list(row) for row in lay]
    return lay_map