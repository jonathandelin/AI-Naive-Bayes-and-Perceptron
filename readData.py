# This class stores the 2D array containing the data and creates a blank image
# the data is unclear.

class Data:

    def __init__(self, data, width, height):

        self.height = height
        self.width = width
        if data == None:
            data = [[' ' for i in range(width)] for j in range(height)]
        for i in range(width):
            for j in range(height):
                if data[j][i] == ' ':
                    data[j][i] = 0
                elif data[j][i] == '#':
                    data[j][i] = 1
                elif data[j][i] == '+':
                    data[j][i] = 2
        self.pixels = data

# Loads file containing images and parses it into n 2D arrays
# of size width x height

def loadDataFile(filename, n, width, height):
    f = open(filename, "r")
    flines = f.readlines()
    items = []
    for i in range(n):
        data = []
        for j in range(height):
            data.append(list(flines.pop(0)))
            data[j].pop()
        if(len(data[0]) < width - 1):
            print("Truncating at %d examples (maximum)" % i)
            break
        items.append(Data(data, width, height))
    return items

# Loads file containing labels and parses it into an array of size n

def loadLabelsFile(filename , n):
    f = open(filename, "r")
    flines = f.readlines()
    labels = []
    for i in flines[:min(n, len(flines))]:
        if i == '':
            break
        labels.append(int(i))
    return labels

##if __name__ == '__main__':
##    
##    items = loadDataFile("data/facedata/facedatatrain", 2, 60, 70)
##    labels = loadLabelsFile("data/facedata/facedatatrainlabels", 2)
##    print(items)
##    print(labels)
