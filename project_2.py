from tqdm import tqdm
import csv
import matplotlib.pyplot as plt
import math
import numpy as np

def loadCSV(file_path):
    full_array = []
    full_file_path = file_path + '.csv'
    flag = True
    while(flag):
        try:
            with open(full_file_path, 'r') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',')
                # wrap te quiero demasiado around spamreader
                for row in tqdm(spamreader):
                    full_array.append(row)
                flag = False
        except FileNotFoundError:
            full_file_path = str(input('File Not Found, re-select the file name: ')) + '.csv'
    return full_array

def adjustData(dataset):
    # adjust the array to not include the column names
    dataset.pop(0)

def filterData(dataset):
    # remove any rides that lasted longer than 24 hours
    orig_length = len(dataset)
    for row in tqdm(dataset, desc='Progress: '):
        if int(row[1]) > 86400:
            dataset.remove(row)
    print('\nNUMBER OF REMOVED ENTRIES: ' + str(orig_length - len(dataset)))
    print('NUMBER OF TOTAL ENTRIES: ' + str(len(dataset)) + '\n')

def sampleAvg(dataset):
    sum_length = 0
    for duration in dataset:
        sum_length += int(duration[1])
    print('SAMPLE AVERAGE LENGTH: ' + str(sum_length/len(dataset)))
    return (sum_length/len(dataset))

def sampleVar(dataset, mean):
    sum_var = 0
    for element in dataset:
        sum_var += ((int(element[1]) - mean) ** 2)
    sample_var = sum_var / (len(dataset) - 1)
    print('SAMPLE VAR: ' + str(sample_var))
    print('SAMPLE SD: ' + str(math.sqrt(sample_var)))
    return sample_var

def stationProportion(dataset):
    count_stations = 0
    for station in dataset:
        if (str(station[5]) == "Queen Mary's, Mile End") or (str(station[8]) == "Queen Mary's, Mile End"):
            count_stations += 1
    print('NUMBER OF STATIONS (START/END INCLUSIVE): ' + str(count_stations))
    print('PROPORTION: ' + str(count_stations/len(dataset) * 100) + ' %')
    return (count_stations/len(dataset))

def generator(mu, var, n):
    sigma = math.sqrt(var)
    s = np.random.normal(mu, sigma, n)
    s_mean = np.mean(s)
    z_score = (s_mean - 1800) / (sigma / math.sqrt(n))
    return z_score

def simulateZScores(sample_mean, sample_var, n, trials):
    print('\n' + ' GENERATING Z SCORES FROM SIMULATED NORMALLY DISTRIBUTED POPULATIONS '.center(120, '=') + '\n')
    z_array = []
    x = 0
    pbar = tqdm(total=int(10**trials), desc='Progress: ')
    while(x < int(10**trials)):
        x += 1
        pbar.update(1)
        z_array.append(generator(sample_mean, sample_var, n))
    pbar.close()

    # plot it
    count, bins, ignored = plt.hist(z_array, 30, normed=True)
    plt.plot(bins, 1/(math.sqrt(sample_var) * np.sqrt(2 * np.pi)) * np.exp( - (bins - sample_mean)**2 / (2 * math.sqrt(sample_var)**2) ), linewidth=2, color='r')
    plt.show()

def proportionZScore(proportion, n):
    z_score = ((proportion) - 0.002) / math.sqrt(0.002*(1-0.002)/n)
    print('PROPORTION ZSCORE: ' + str(z_score))

def smeanZScore(sample_mean, sample_var, n):
    z_score = (sample_mean - 1800) / (math.sqrt(sample_var) / math.sqrt(n))
    print('SAMPLE MEAN ZSCORE: ' + str(z_score))

def avgConfidenceInterval(sample_mean, sample_var, n):
    lower_bound = sample_mean - (1.96*math.sqrt(sample_var)/math.sqrt(n))
    upper_bound = sample_mean + (1.96*math.sqrt(sample_var)/math.sqrt(n))
    print('AVG Lower Bound CI: ' + str(lower_bound) + ' || ' + 'AVG Upper Bound CI: ' + str(upper_bound))

def propConfidenceInterval(proportion, n):
    lower_bound = proportion - (1.96*math.sqrt(proportion*(1-proportion)/n))
    upper_bound = proportion + (1.96*math.sqrt(proportion*(1-proportion)/n))
    print('PROP Lower Bound CI: ' + str(lower_bound) + ' || ' + 'PROP Upper Bound CI: ' + str(upper_bound))


if __name__ == '__main__':
    # load the dataset first
    dataset = loadCSV(input('Select a file name: '))
    n_dataset = len(dataset)
    print('\n' + ' FILTERING DATASET '.center(120, '=') + '\n')
    # do calculations
    adjustData(dataset)
    filterData(dataset)
    print('\n' + ' PROCESSING DATASET '.center(120, '=') + '\n')
    sample_mean = sampleAvg(dataset)
    sample_var = sampleVar(dataset, sample_mean)
    proportion = stationProportion(dataset)
    smeanZScore(sample_mean, sample_var, n_dataset)
    proportionZScore(proportion, n_dataset)
    avgConfidenceInterval(sample_mean, sample_var, n_dataset)
    propConfidenceInterval(proportion, n_dataset)

    #Simulate Z Values
    while(True):
        ans = input('\nDo you want to run a Z Score Simulation? (Y/N): ')
        if ans.upper() not in ['Y', 'N']:
            print("Invalid answer, please select 'Y' or 'N'")
        elif(ans.upper() == 'Y'):
            simulateZScores(sample_mean, sample_var, n_dataset, int(input('Enter the number of trials 10^[x]: x = ')))
            break
        else:
            print('Good bye!')
            break
    