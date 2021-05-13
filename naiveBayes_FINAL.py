import readData
import getFeatures
import math
import statistics
import random
import time
import sys

class naiveBayes:
    
    def __init__(self):
        self.featurepd = []
        self.faceProb = 1
        self.featurepdDig = []
        self.digitProb = [1,1,1,1,1,1,1,1,1,1]
        self.k = 1.0

    def trainFace(self, dataFile, labelsFile, n, width, height, randomList):
        items = readData.loadDataFile(dataFile, n, width, height)
        labels = readData.loadLabelsFile(labelsFile, n)
        self.featurepd = []
        numberFaces = 0

        # featureTimes is a list of tuples where the first number is the number of times the feature occurs when the image is not a face
        # and the second number is the number of times the features occurs when the image is a face
        featureTimes = []
        numberFeatures = (math.ceil(height/getFeatures.DIM)) * math.ceil((width/getFeatures.DIM))
        for i in range(numberFeatures):
            featureTimes.append([0.0,0.0])

        for count in randomList:
            image = items[count]
            if labels[count] == 1:
                numberFaces += 1.0
            features = getFeatures.getFeatures(image.pixels, width, height)
            for i in range(len(features)):
                if features[i] > 0:
                    if labels[count] == 1:
                        featureTimes[i][1] += 1
                    else:
                        featureTimes[i][0] += 1

        for i in range(len(featureTimes)):
            self.featurepd.append([(featureTimes[i][0] + self.k)/(len(randomList)-numberFaces + self.k), (featureTimes[i][1] + self.k)/(numberFaces + self.k)])

        self.faceProb = numberFaces/len(randomList)
        

    def validateFace(self, dataFile, labelsFile, n, width, height, itemNo = -1):
        items = readData.loadDataFile(dataFile, n, width, height)
        labels = readData.loadLabelsFile(labelsFile, n)

        like = 0.0
        guess = 0
        correct = 0

        if itemNo != -1:
            image = items[itemNo]
            features = getFeatures.getFeatures(image.pixels, width, height)
            productTrue = pow(10,300.0)
            productFalse = pow(10,300.0)
            for j in range(len(self.featurepd)):
                if features[j] > 0:
                    productTrue *= self.featurepd[j][1]
                    productFalse *= self.featurepd[j][0]
                else:
                    productTrue *= (1 - self.featurepd[j][1])
                    productFalse *= (1 - self.featurepd[j][0])       
            
            like = (productTrue * self.faceProb)/(productFalse * (1-self.faceProb))
            
            if like >= 1:
                return 1
            else:
                return 0
        
        for i in range(len(items)):
            image = items[i]
            features = getFeatures.getFeatures(image.pixels, width, height)
            productTrue = pow(10,300.0)
            productFalse = pow(10,300.0)
            for j in range(len(self.featurepd)):
                if features[j] > 0:
                    productTrue *= self.featurepd[j][1]
                    productFalse *= self.featurepd[j][0]
                else:
                    productTrue *= (1 - self.featurepd[j][1])
                    productFalse *= (1 - self.featurepd[j][0])       
            
            like = (productTrue * self.faceProb)/(productFalse * (1-self.faceProb))
            
            if like >= 1:
                guess = 1
            else:
                guess = 0
            if guess == labels[i]:
                correct += 1
                
        return correct/n

    def trainDigit(self, dataFile, labelsFile, n, width, height, randomList):
        items = readData.loadDataFile(dataFile, n, width, height)
        labels = readData.loadLabelsFile(labelsFile, n)
        self.featurepdDig = []
        numberDigits = [0,0,0,0,0,0,0,0,0,0]

        # featureTimes is a list of tuples where the first number is the number of times the feature occurs when the image is not a face
        # and the second number if the number of times the features occurs when the image is a face
        featureTimes = []
        numberFeatures = height * width
        for i in range(numberFeatures):
            featureTimes.append([0,0,0,0,0,0,0,0,0,0])

        for count in randomList:
            image = items[count]
            numberDigits[labels[count]] += 1
            features = getFeatures.getFeaturesPixels(image.pixels, width, height)
            for i in range(len(features)):
                if features[i] > 0:
                    featureTimes[i][labels[count]] += 1

        pd = []
        totalF = 0
        for i in range(len(featureTimes)):
            for m in range(10):
                totalF += featureTimes[i][m]
            for j in range(10):
                pd.append([(featureTimes[i][j] + self.k)/(numberDigits[j] + self.k),
                           (totalF - featureTimes[i][j] + self.k)/(len(randomList) - numberDigits[j] + self.k)])
            self.featurepdDig.append(pd)
            pd = []
            totalF = 0

        for k in range(10):
            self.digitProb[k] = numberDigits[k]/len(randomList)


    def validateDigit(self, dataFile, labelsFile, n, width, height, itemNo = -1):
        items = readData.loadDataFile(dataFile, n, width, height)
        labels = readData.loadLabelsFile(labelsFile, n)

        like = [0,0,0,0,0,0,0,0,0,0]
        guess = 0
        correct = 0

        if itemNo != -1:
            image = items[itemNo]
            features = getFeatures.getFeaturesPixels(image.pixels, width, height)
            productTrue = 1
            productFalse = 1
            for k in range(10):
                
                for j in range(len(self.featurepdDig)):
                    if features[j] > 0:
                        productTrue *= self.featurepdDig[j][k][0]
                        productFalse *= self.featurepdDig[j][k][1]
                    else:
                        productTrue *= (1 - self.featurepdDig[j][k][0])
                        productFalse *= (1 - self.featurepdDig[j][k][1])
                
                like[k] = (productTrue * self.digitProb[k])/(productFalse * (1-self.digitProb[k]))
                productTrue = 1
                productFalse = 1
            guess = like.index(max(like))
            return guess
            
        for i in range(len(items)):
            image = items[i]
            features = getFeatures.getFeaturesPixels(image.pixels, width, height)
            productTrue = 1
            productFalse = 1
            for k in range(10):
                
                for j in range(len(self.featurepdDig)):
                    if features[j] > 0:
                        productTrue *= self.featurepdDig[j][k][0]
                        productFalse *= self.featurepdDig[j][k][1]
                    else:
                        productTrue *= (1 - self.featurepdDig[j][k][0])
                        productFalse *= (1 - self.featurepdDig[j][k][1])
                
                like[k] = (productTrue * self.digitProb[k])/(productFalse * (1-self.digitProb[k]))
                productTrue = 1
                productFalse = 1
            guess = like.index(max(like))
   
            if guess == labels[i]:
                correct += 1
        return correct/n

        
if __name__ == '__main__':
    trial = naiveBayes()

# run with decimal form first argument and index of image second argument
# for accuracy run with index -1

    percentage = float(sys.argv[1])
    testimage = int(sys.argv[2])
    print("Percentage: ", int(percentage * 100))
    print("Image Index: ", testimage)
    randomList = random.sample(range(0,451), int(percentage * 451))
    trial.trainFace("data/facedata/facedatatrain", "data/facedata/facedatatrainlabels", 451, 60, 70, randomList)
    print("Face: ", trial.validateFace("data/facedata/facedatatest", "data/facedata/facedatatestlabels", 150, 60, 70, testimage))
    
    randomList = random.sample(range(0,5000), int(percentage * 5000))
    trial.trainDigit("data/digitdata/trainingimages", "data/digitdata/traininglabels", 5000, 28, 28, randomList)
    print("Digit: ", trial.validateDigit("data/digitdata/testimages", "data/digitdata/testlabels", 1000, 28, 28, testimage))

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
##    numbersD = [i for i in range(5000)]
##    print("Digit Classification")
##    print("Training...")
##    trial.trainDigit("data/digitdata/trainingimages", "data/digitdata/traininglabels", 5000, 28, 28, numbersD)
##    print("Training Complete!")
##    print("Testing...")
##    accD = trial.validateDigit("data/digitdata/testimages", "data/digitdata/testlabels", 1000, 28, 28)
##    print("Testing Complete! Accuracy: ", accD)



    
'''
The below code was what we used for collecting our statistics.

    f1 = open('naive_acc.txt','w')
    f2 = open('naive_std.txt', 'w')
    f3 = open('naive_time.txt','w')
    
    
    
    percent = [.1,.2,.3,.4,.5,.6,.7,.8,.9,1]
    
    f1.write("Naive Bayes Face*********\n")
    f2.write("Naive Bayes Face*********\n")
    f3.write("Naive Bayes Face*********\n")
    
    for i in percent:
        acc1 = []
        time1 = []
        n1 = int(450*i)
        
        print("At ", i)
       
        for j in range(20):
            randomList = random.sample(range(0,450),n1)
            trial = naiveBayes()
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
        
    f1.write("Naive Bayes Digit*********\n")
    f2.write("Naive Bayes Digit*********\n")
    f3.write("Naive Bayes Digit*********\n")
    
    for i2 in percent:
        acc2 = []
        time2 = []
        n2 = int(5000*i2)
        print("At", i2)
        for j2 in range(5):
            randomList2 = random.sample(range(0,5000),n2)
            trial2 = naiveBayes()
            t0a = time.time()
            trial2.trainDigit("data/digitdata/trainingimages", "data/digitdata/traininglabels", 5000, 28, 28, randomList2)
            t1a = time.time()
            a2 = trial2.validateDigit("data/digitdata/testimages", "data/digitdata/testlabels", 1000, 28, 28)
            acc2.append(a2)
            print(a2)
            time2.append(t1a-t0a)
            
        
        f1.write("{}\n".format(statistics.mean(acc2)))
        f2.write("{}\n".format(statistics.stdev(acc2)))
        f3.write("{}\n".format(statistics.mean(time2)))    
    
    f1.close()
    f2.close()
    f3.close()


'''









            
        
