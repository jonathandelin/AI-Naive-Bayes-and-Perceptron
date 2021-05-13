import readData

# Sets the size of the square features.
DIM = 3

# Method for getting features where each feature is the number of pixels in
# each square of size DIM x DIM. Contains additional loops for if the size of
# the image is not divisible by the DIM. Used for face classification
def getFeatures(data, width, height):
    height = len(data)
    width = len(data[0])
    count = 0
    features = []
    for i in range(int(height/DIM)):
        for j in range(int(width/DIM)):
            for k in range(DIM):
                for l in range(DIM):
                    if data[i*DIM + k][j*DIM + l] != 0:
                        count += 1

            features.append(count)
            count = 0

    if width % DIM != 0:
        for i in range(int(height/DIM)):
            for k in range(DIM):
                for l in range(width % DIM):
                        if data[i*DIM + k][width - (width % DIM) + l] != 0:
                            count += 1

            features.append(count)
            count = 0

    if height % DIM != 0:
        for j in range(int(width/DIM)):
            for k in range(height % DIM):
                for l in range (DIM):
                    if data[height - (height % DIM) + k][j*DIM + l] != 0:
                        count += 1

            features.append(count)
            count = 0

    if width % DIM != 0 and height % DIM != 0:
        for k in range(height % DIM):
            for l in range(width % DIM):
                if data[height - (height % DIM) + k][width - (width % DIM) + l] != 0:
                    count += 1

        features.append(count)            
        count = 0

    return features

# Method for getting features where each feature is a whether or not a pixel
# is marked or not. Used for digit classification.

def getFeaturesPixels(data, width, height):
    height = len(data)
    width = len(data[0])
    features = []
    for i in range(height):
        for j in range(width):
            if data[i][j] > 0: features.append(1)
            else: features.append(0)

    return features

# Main used for testing.

##if __name__ == '__main__':
##    items = readData.loadDataFile("data/facedata/facedatatrain", 2, 60, 70)
##    labels = readData.loadLabelsFile("data/facedata/facedatatrainlabels", 2)
##    features = getFeatures(items[0].pixels, 60, 70)
##    print(features)
