import csv
from scipy import stats
import matplotlib.pyplot as plt
import datetime as dt


def removeNull(dataset):
    print("Removing null characters from dataset: ", end='')
    keys = ['total_cases', 'total_deaths', 'total_vaccinations', 'people_vaccinated', 'people_fully_vaccinated', 'population']
    for record in dataset:
        for key in keys:
            if record[key] == '':
                record[key] = '0'
    print("Done")


def readCsv(dataset, filePath):
    print("Reading dataset from file: ", end='')
    with open(filePath, newline='') as inputFile:
        csvReader = csv.DictReader(inputFile)
        for record in csvReader:
            if record['location'] != '':
                dataset.append(record)  
        inputFile.close()
    print("Done")


def writeCsv(dataset, path):
    print("Writing dataset to file: ", end='')
    with open(path, 'w', newline='') as outputFile:
        writer = csv.DictWriter(outputFile, dataset[0].keys())
        writer.writeheader()
        for dict in dataset:
            writer.writerow(dict)
        outputFile.close()
    print("Done")


def removeZero(dataset):
    print("Removing and replacing unnecessery zeros from dataset: ", end='')
    lastValue = {'total_cases':'0', 'total_deaths':'0', 'total_vaccinations':'0', 'people_fully_vaccinated':'0'}
    lastLocation = dataset[0]['location']
    for record in dataset:
        if record['location'] != lastLocation:
            lastLocation = record['location']
            lastValue = {'total_cases':'0', 'total_deaths':'0', 'total_vaccinations':'0', 'people_fully_vaccinated':'0'}
        for key in lastValue:
            if record[key] == '0':
                record[key] = lastValue[key]
            else:
                lastValue[key] = record[key]
    print("Done")


def addPopulationStatistics(dataset):
    print("Adding population statistics to dataset: ", end='')
    for record in dataset:
        tc_per_pop = int(record['total_cases']) * 100 / int(record['population'])
        td_per_pop = int(record['total_deaths']) * 100 / int(record['population'])
        pfv_per_pop = int(record['people_fully_vaccinated']) * 100 / int(record['population'])
        record.update([ ('total_cases_per_population', str("{:.3f}".format(tc_per_pop))), ('total_deaths_per_population', str("{:.3f}".format(td_per_pop))), ('people_fully_vaccinated_per_population', str("{:.3f}".format(pfv_per_pop)))])
    print("Done")


def pairedSampleTTestStrings2File(dataset, paires, path):
    print("Paired sample t-test on (All Data): ", end='')
    outputString = []
    for pair in paires:
        a = []
        b = []
        for record in dataset:
            a.append(float(record[pair[0]]))
            b.append(float(record[pair[1]]))
        tStat, pValue = stats.ttest_rel(a, b)
        output = "All Data and pair ({0}, {1}): P-Value:{2} T-Statistic:{3}".format(pair[0], pair[1], pValue, tStat)
        outputString.append(output)
    print("Done")  
    print("Writing result to file: ", end='')
    with open(path, 'w') as file:
        for string in outputString:
            file.write(string)
            file.write('\n')
        file.close()
    print("Done")


def pairedSampleTTestStringsLocation2File(dataset, paires, locations, path):
    outputString = []
    for location in locations:
        print(f'Paired sample t-test on ({location}): ', end='')
        for pair in paires:
            a = []
            b = []
            for record in dataset:
                if (record['location'] == location):
                    a.append(float(record[pair[0]]))
                    b.append(float(record[pair[1]]))
            tStat, pValue = stats.ttest_rel(a, b)
            output = "{4}: pair ({0}, {1}): P-Value:{2} T-Statistic:{3}".format(pair[0], pair[1], pValue, tStat, location)
            outputString.append(output)
        print("Done")
    print("Writing result to file: ", end='')
    with open(path, 'w') as file:
        for string in outputString:
            file.write(string)
            file.write('\n')
        file.close()
    print("Done")


def plotGrowthChart(dataset, attributes, locations, path):

    for location in locations:
        i = 1
        for attribute in attributes:
            dates = []
            att0 = []
            att1 = []
            att2 = []
            for record in dataset:
                if(record['location'] == location):
                    dates.append(str(record['date']))
                    att0.append(float(record[attribute[0]]))
                    att1.append(float(record[attribute[1]]))
                    att2.append(float(record[attribute[2]]))
                    
            formattedDates = [dt.datetime.strptime(d, '%m/%d/%Y').date() for d in dates]
            
            fig = plt.Figure(figsize=(10.8,7.2))
            fig.clf()

            ax = fig.add_subplot(111)
            ax.plot(formattedDates, att0, label=attribute[0].replace('_', ' '))
            ax.plot(formattedDates, att1, label=attribute[1].replace('_', ' '))
            ax.plot(formattedDates, att2, label=attribute[2].replace('_', ' '))
            ax.ticklabel_format(style='plain', axis='y')
            ax.legend([attribute[0].replace('_',' '), attribute[1].replace('_', ' '), attribute[2].replace('_', ' ')])
            ax.set_title(f'{location} {i}')
            ax.set_xlabel('date')
            ax.grid(True)
            if attribute == attributes[0]:
                ax.set_ylabel('percentage')
            else:
                ax.set_ylabel('number of')

            pltPath = f'{path}{location}-{i}.png'
            fig.savefig(pltPath)
            print(f'Created growth chart: {location}-{i}.png')

            i += 1
            plt.close(fig)
            

def plotRelationChart(dataset, attributes, locations, path):

    for location in locations:
        i = 1
        for attribute in attributes:
            dates = []
            att0 = []
            att1 = []
            for record in dataset:
                if(record['location'] == location):
                    dates.append(str(record['date']))
                    att0.append(float(record[attribute[0]]))
                    att1.append(float(record[attribute[1]]))
                    
            formattedDates = [dt.datetime.strptime(d, '%m/%d/%Y').date() for d in dates]
            
            fig = plt.Figure(figsize=(10.8,7.2))
            fig.clf()

            ax = fig.add_subplot(111)
            ax.scatter(att0, att1, s=2.5)
            ax.ticklabel_format(style='plain', axis='both')
            ax.set_title(f'{location} {i}')
            ax.set_xlabel(attribute[0].replace('_', ' '))
            ax.set_ylabel(attribute[1].replace('_', ' '))
            ax.grid(True)

            pltPath = f'{path}{location}-{i}.png'
            fig.savefig(pltPath)
            print(f'Created relation chart: {location}-{i}.png')

            i += 1
            plt.close(fig)