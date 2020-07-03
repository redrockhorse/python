with open('/Users/hongyanma/Desktop/Report_SingleCar-1.csv','r') as infile:
    line = infile.readline()
    while line:
        print(line)
        line = infile.readline()