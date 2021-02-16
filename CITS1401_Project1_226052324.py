# Jhune Aguiba - 22605234
# CITS1401 - Project 1
import os

def rows_columns(filename): #normalises each column and returns a list of normalised rows from the data
    columns= [ ]
    column = [ ]
    index = 0
    for item in range(6):
        for row in filename:
            row  = row[:-1].split(",")[2:]
            if row[index] != "":
                column.append(float(row[index]))     #swaps the list of rows into list of columns
            else:
                column.append(None)
        index += 1
        columns.append(column)
        column = [ ]
    
    normList = [ ]
    maxN= 0
    minN = 0
    normColumn = [ ] 
    for column in columns:
        maxN = max(score for score in column if score != None)
        minN = min(score for score in column if score != None)    #normalises each score in the column
        norm_score = 0
        for score in column:
            if score != None:
                norm_score = (score - minN) / (maxN - minN) 
                normColumn.append(norm_score)
            else:
                normColumn.append(None)
        normList.append(normColumn)
        accumulator = len(normColumn)
        normColumn = [ ]

    normalised_row = [ ]
    normalised_data = [ ]
    score_index = 0
    for item in range(accumulator):
        for nCol in normList:
            normalised_row.append(nCol[score_index])   #returns list of columns into rows
        normalised_data.append(normalised_row)
        score_index += 1
        normalised_row = [ ]
    score_index = 0
    return normalised_data

def listOfCountries(filename):  #returns a list of the countries fom the data
    countryList = [ ]
    for row in filename:
        row = row[:-1].split(",")
        countryList.append(row[0])
    return countryList

def lifeLadder(filename):  #returns a list of the life ladder scores from the data
    lifeLadderScores = [ ]
    for row in filename:
        row = row[:-1].split(",")
        lifeLadderScores.append(float(row[1]))
    return lifeLadderScores

def listOfMins(rows):  #returns a list of min values of each row from the normalised data
    mins = 0.0
    minList = [ ]
    for row in rows:
        mins = min(score for score in row if score != None)
        minList.append(mins)
    return minList

def meanList(rows):  #returns a list of mean values of each row from the normalised data
    mean = 0.0
    total = 0.0
    means = [ ]
    sumList = [ ]
    for row in rows:
        for score in row:
            if score != None:
                sumList.append(score)
        mean  = (sum(sumList) / len(sumList))
        sumList = [ ]
        means.append(mean)
    return means

def medianList(rows): #returns a list of median values of each row from the normalised data
    medians = [ ]
    sortList= [ ]
    length = 0
    index = 0
    for row in rows:
        for score in row:
            if score != None:
                sortList.append(score)
        sortList = sorted(sortList)
        length = len(sortList)
        index = (length - 1) // 2
        if length % 2 != 0:
            medians.append(sortList[index])
        else:
            medians.append((sortList[index] +sortList[index + 1]) / 2.0)
        sortList = [ ]
    return medians

def harmonicMeans(rows): #returns a list of harmonic mean values of each row from the normalised data
    harmonicMeanList = [ ]
    toSum = [ ]
    harmonic_mean = 0.0
    total = 0.0
    for row in rows:
        for score in row:
            if score != None and score != 0.0:
                score = 1/score
                toSum.append(score)
        total  = sum(toSum)
        harmonic_mean = len(toSum) /total
        harmonicMeanList.append(harmonic_mean)
        toSum = [ ]
    return harmonicMeanList

def countryScoreList(metric, countries): #list of country,metric score pairs in descending order
    pair = [ ]
    pairs = [ ]
    index = 0
    for country in countries:
        pair.append(metric[index])
        pair.append(country)
        pairs.append(pair)
        pair = [ ]
        index += 1
    pairs = sorted(pairs)
    pairs = list(reversed(pairs))
    return pairs

def spearman_rank(metricList, lifeLadderList, metric_name): #computes the spearman's rank correlation coefficient between the country score list and Life Ladder list
    ranking = metricList
    seq = sorted(ranking)
    index = [seq.index(i) for i in ranking]
    
    lifeLadderSeq = sorted(lifeLadderList)
    lifeLadderList = [lifeLadderSeq.index(j) for j in lifeLadderList]
    
    indexD = 0
    difference = 0
    differences  = [ ]
    for i in range(len(index)):
        difference = abs(((lifeLadderList[indexD]))-((index[indexD])))
        differences.append(difference)
        difference = 0
        indexD += 1
        
    squared_differences = [ ]
    for difference in differences:
        squared_differences.append(difference*difference)
        
    sumDsquaredvalues = sum(squared_differences)
    correlation = round(1 -((6*sumDsquaredvalues)/(len(ranking)*((len(lifeLadderList)**2) - 1))), 4)
    print("The correlation coefficient between the study ranking and the ranking using the", metric_name, "metric is", correlation)
    
def main(): #gets the filename, metric and action from the user and calls the required functions
    filename = input("Enter filename containing the World Happiness computation data: ")
    if not os.path.isfile(filename) :
        return(None)
    filename = open(filename, "r").readlines()
    filename.pop(0)
    countries = listOfCountries(filename)
    normalisedRows = rows_columns(filename)
    lifeLadderscores = lifeLadder(filename)
    
    print()
    metric = input("Choose metric to be tested from: min, mean, median, harmonic_mean: \n ")
    metric_name = ""
    if metric == "mean":
        metric_name = metric
        metric = meanList(normalisedRows)
    elif metric == "min":
        metric_name = metric
        metric = listOfMins(normalisedRows)
    elif metric == "median":
        metric_name = metric
        metric = medianList(normalisedRows)       
    elif metric == "harmonic_mean":
        metric_name = metric
        metric = harmonicMeans(normalisedRows)
    else:
        return(None)
    print()
    action = input("Chose action to be performed on the data using the specified metric. Options are list, correlation: \n")
    print()
    if action == "list":
        pairs = countryScoreList(metric, countries)
        print("Ranked list of countries' happiness scores based on the", metric_name,"metric:\n")
        for country_score in pairs:
            print("{1:<30}{0:>5.4f}".format(country_score[0],country_score[1]))
    elif action == "correlation":
        spearman_rank(metric, lifeLadderscores, metric_name)
    else:
        return(None)

main()