import readData
import getFeatures
import math
import statistics
import time
import random
import sys

class perceptron:

    def __init__(self):
        self.weightsFace = []
        self.weightsDigit = []

    def importWeightsFace(self, filename, width, height):
        f = open(filename, "r")
        flines = f.readlines()
        numberFeatures = (math.ceil(height/getFeatures.DIM)) * math.ceil((width/getFeatures.DIM))
        for i in range(numberFeatures + 1):
            self.weightsFace.append(int(flines.pop(0)))
        f.close()

    def trainFace(self, dataFile, labelsFile, n, width, height, rList):
        items = readData.loadDataFile(dataFile, n, width, height)
        old_labels = readData.loadLabelsFile(labelsFile, n)
        self.weightsFace = []
        
        numberFeatures = (math.ceil(height/getFeatures.DIM)) * math.ceil((width/getFeatures.DIM))
        for i in range(numberFeatures + 1):
            self.weightsFace.append(0)
            
        labels = []
        for r in rList:
            labels.append(old_labels[r])
            
        # this array contains the features for every image
        features = []
        for i in rList:
            features.append(getFeatures.getFeatures(items[i].pixels, width, height))
        loop = 0
        index = 0
        # traverses all the items and updates the weights accordingly
        # stops when a full loop is completed without updates
        iterations = 0
        while loop < len(rList) and iterations <  10 *len(rList):
            iterations +=1
            function = 0
            for i in range(numberFeatures):
                function += self.weightsFace[i] * features[index][i]
            function += self.weightsFace[numberFeatures]
            if (function >= 0 and labels[index] == 1) or (function < 0 and labels[index] == 0):
                loop += 1
            elif function < 0 and labels[index] == 1:
                for i in range(numberFeatures):
                    self.weightsFace[i] += features[index][i]
                self.weightsFace[numberFeatures] += 1
                loop = 0
            else:
                for i in range(numberFeatures):
                    self.weightsFace[i] -= features[index][i]
                self.weightsFace[numberFeatures] -= 1
                loop = 0
            if index == len(rList)-1: index = 0
            else: index += 1

    def recordWeightsFace(self, filename):
        f = open(filename,'w')
        for i in range(len(self.weightsFace)):
            f.write(str(self.weightsFace[i]) + "\n")

    def validateFace(self, dataFile, labelsFile, n, width, height, itemNo = -1):
        items = readData.loadDataFile(dataFile, n, width, height)
        labels = readData.loadLabelsFile(labelsFile, n)

        function = 0
        guess = 0
        correct = 0

        if itemNo != -1:
            image = items[itemNo]
            features = getFeatures.getFeatures(image.pixels, width, height)
            for j in range(len(features)):
                function += (self.weightsFace[j] * features[j])
            function += self.weightsFace[len(features)]
            if function >= 0: return 1
            else: return 0

        for i in range(len(items)):
            image = items[i]
            features = getFeatures.getFeatures(image.pixels, width, height)
            for j in range(len(features)):
                function += (self.weightsFace[j] * features[j])
            function += self.weightsFace[len(features)]
            if function >= 0: guess = 1
            else: guess = 0
            if guess == labels[i]: correct += 1
            function = 0
            
        return correct/n

    def importWeightsDigit(self, filename, height, width):
        f = open(filename, "r")
        flines = f.readlines()
        numberFeatures = height * width
        for i in range(numberFeatures + 1):
            self.weightsDigit.append([])
            for j in range(10):
                self.weightsDigit[i].append(int(flines.pop(0)))
        f.close()

    def trainDigit(self, dataFile, labelsFile, n, width, height, rList):
        items = readData.loadDataFile(dataFile, n, width, height)
        old_labels = readData.loadLabelsFile(labelsFile, n)
        self.weightsDigit = []
        
        numberFeatures = height * width
        for i in range(numberFeatures + 1):
            self.weightsDigit.append([0,0,0,0,0,0,0,0,0,0])

        # this array contains the features for every image
        features = []
        labels = []
        for i in rList:
            features.append(getFeatures.getFeaturesPixels(items[i].pixels, width, height))
            labels.append(old_labels[i])
        loop = 0
        index = 0
        # traverses all the items and updates the weights accordingly
        # stops when a full loop is completed without updates

        guess = 0
        iterations = 0
        while loop < len(rList) and iterations <  10 * len(rList):
            function = [0,0,0,0,0,0,0,0,0,0]
            iterations += 1
            for k in range(10):
                for i in range(numberFeatures):
                    function[k] += self.weightsDigit[i][k] * features[index][i]
                function[k] += self.weightsDigit[numberFeatures][k]
            guess = function.index(max(function))
            if guess == labels[index]:
                loop += 1
            else:
                for i in range(numberFeatures):
                    self.weightsDigit[i][labels[index]] += features[index][i]
                self.weightsDigit[numberFeatures][labels[index]] += 1
                for i in range(numberFeatures):
                    self.weightsDigit[i][guess] -= features[index][i]
                self.weightsDigit[numberFeatures][guess] -= 1
                loop = 0
            if index == len(rList)-1: index = 0
            else: index += 1

    def recordWeightsDigit(self, filename):
        f = open(filename,'w')
        for i in range(len(self.weightsDigit)):
            for j in range(10):
                f.write(str(self.weightsDigit[i][j]) + "\n")

    def validateDigit(self, dataFile, labelsFile, n, width, height, itemNo = -1):
        items = readData.loadDataFile(dataFile, n, width, height)
        labels = readData.loadLabelsFile(labelsFile, n)

        function = [0,0,0,0,0,0,0,0,0,0]
        guess = 0
        correct = 0

        if itemNo != -1:
            for k in range(10):
                image = items[itemNo]
                features = getFeatures.getFeaturesPixels(image.pixels, width, height)
                for j in range(len(features)):
                    function[k] += (self.weightsDigit[j][k] * features[j])
                function[k] += self.weightsDigit[len(features)][k]

            return function.index(max(function))

        for i in range(len(items)):
            for k in range(10):
                image = items[i]
                features = getFeatures.getFeaturesPixels(image.pixels, width, height)
                for j in range(len(features)):
                    function[k] += (self.weightsDigit[j][k] * features[j])
                function[k] += self.weightsDigit[len(features)][k]

            guess = function.index(max(function))
            if guess == labels[i]: correct += 1
            function = [0,0,0,0,0,0,0,0,0,0]
        return correct/n

    
if __name__ == '__main__':
    trial = perceptron()
# run with decimal form first argument and index of image second argument
# for accuracy run with index -1

    percentage = int(float(sys.argv[1]) * 100)
    testimage = int(sys.argv[2])
    print("Percentage: ", percentage)
    print("Image Index: ", testimage)

    trial.importWeightsFace("data/weights/faceWeights_" + str(percentage), 60, 70)
    print("Face: ", trial.validateFace("data/facedata/facedatatest", "data/facedata/facedatatestlabels", 150, 60, 70, testimage))

    trial.importWeightsDigit("data/weights/digitWeights_" + str(percentage), 28, 28)
    print("Digit: ", trial.validateDigit("data/digitdata/testimages", "data/digitdata/testlabels", 1000, 28, 28, testimage))

# The below code was used to generate the weight files.

##    for i in [80]:
##        randomList = random.sample(range(0,451), int(i*4.51))
##        trial.trainFace("data/facedata/facedatatrain", "data/facedata/facedatatrainlabels", 451, 60, 70, randomList)
##        trial.recordWeightsFace("data/weights/faceWeights_" + str(i))
##        print("face ", i)
##        print(trial.validateFace("data/facedata/facedatatest", "data/facedata/facedatatestlabels", 150, 60, 70))
##        randomList = random.sample(range(0,5000), int(i * 50))
##        trial.trainDigit("data/digitdata/trainingimages", "data/digitdata/traininglabels", 5000, 28, 28, randomList)
##        trial.recordWeightsDigit("data/weights/digitWeights_" + str(i))
##        print("digit ", i)
##        print(trial.validateDigit("data/digitdata/testimages", "data/digitdata/testlabels", 1000, 28, 28))

# The below code is for testing the accuracy at 100%

##    numbersF = [i for i in range(451)]
##    print("Face Recognition")
##    print("Training...")
##    trial.trainFace("data/facedata/facedatatrain", "data/facedata/facedatatrainlabels", 451, 60, 70, numbersF)
##    print("Training Complete!")
##    print("Testing...")
##    accF = trial.validateFace("data/facedata/facedatatest", "data/facedata/facedatatestlabels", 150, 60, 70)
##    print("Testing Complete! Accuracy: ", accF)
##
##    numbersD = random.sample(range(0,5000),5000)
##    print("Digit Classification")
##    print("Training...")
##    trial.trainDigit("data/digitdata/trainingimages", "data/digitdata/traininglabels", 5000, 28, 28, numbersD)
##    print("Training Complete!")
##    print("Testing...")
##    accD = trial.validateDigit("data/digitdata/testimages", "data/digitdata/testlabels", 1000, 28, 28)
##    print("Testing Complete! Accuracy: ", accD)


'''
The below code was what we used for collecting our statistics

    f1 = open('perceptron_acc.txt','w')
    f2 = open('perceptron_std.txt', 'w')
    f3 = open('perceptron_time.txt','w')
    
    
    
    percent = [.05,.1, 0.2, .3,.4,.5,.6,.7,.8,.9,1]
    
    f1.write("Perceptron Face*********\n")
    f2.write("Perceptron Face*********\n")
    f3.write("Perceptron Face*********\n")
    
    for i in percent:
        acc1 = []
        time1 = []
        n1 = int(450*i)
        
        print("At ", i)
       
        for j in range(10):
            randomList = random.sample(range(0,450),n1)
            trial = perceptron()
            t0 = time.time()
            trial.trainFace("data/facedata/facedatatrain", "data/facedata/facedatatrainlabels", 450, 60, 70, randomList)
            t1 = time.time()
            a1 = trial.validateFace("data/facedata/facedatatest", "data/facedata/facedatatestlabels", 150, 60, 70)
            print(a1)
            acc1.append(a1)
            time1.append(t1-t0)
            
        
        f1.write("{}\n".format(statistics.mean(acc1)))
        f2.write("{}\n".format(statistics.stdev(acc1)))
        f3.write("{}\n".format(statistics.mean(time1)))
        
    f1.write("Perceptron Digit*********\n")
    f2.write("Perceptron Digit*********\n")
    f3.write("Perceptron Digit*********\n")
    
    for i2 in percent:
        acc2 = []
        time2 = []
        n2 = int(5000*i2)

        print("At ", i2)
      
        for j2 in range(5):
            randomList2 = random.sample(range(0,5000),n2)
            trial2 = perceptron()
            t0a = time.time()
            trial2.trainDigit("data/digitdata/trainingimages", "data/digitdata/traininglabels", 5000, 28, 28, randomList2)
            t1a = time.time()
            a2 = trial2.validateDigit("data/digitdata/testimages", "data/digitdata/testlabels", 1000, 28, 28)
            print(a2)
            acc2.append(a2)
            time2.append(t1a-t0a)
            
        
        f1.write("{}\n".format(statistics.mean(acc2)))
        f2.write("{}\n".format(statistics.stdev(acc2)))
        f3.write("{}\n".format(statistics.mean(time2)))
    
    
    f1.close()
    f2.close()
    f3.close()
'''





            
                                                          
