import utils
import vars
import os
from sys import platform
import time
import warnings

def Main():

# File and script path for windows platform
    if platform == "win64" or platform == "win32":
        script_dir = os.path.dirname(__file__) # get script execution path
        inPath = f'{script_dir}\\resources\\SARS-CoV-2 Dataset.csv' # create absolute file path for input
        outPath = f'{script_dir}\\resources\\SARS-CoV-2 Dataset-Preprocessed.csv' # create absolute file path for output
        ttestPathAllData = f'{script_dir}\\resources\\t-test\\paired sample t-test - All Data.txt'
        ttestPathCountries = f'{script_dir}\\resources\\t-test\\paired sample t-test - countries.txt'
        ttestPathContinents = f'{script_dir}\\resources\\t-test\\paired sample t-test - continents.txt'
        gchartPathCountry = f'{script_dir}\\resources\\growth-charts\\countries\\'
        gchartPathContinent = f'{script_dir}\\resources\\growth-charts\\continents\\'
        rchartPathCountry = f'{script_dir}\\resources\\relation-charts\\countries\\'
        rchartPathContinent = f'{script_dir}\\resources\\relation-charts\\continents\\'


# File and script path for GNU/Linux palatform
    if platform == "linux" or platform == "linux2": # check for platform
        script_dir = os.getcwd() # get script execution path
        inPath = f'{script_dir}/resources/SARS-CoV-2 Dataset.csv' # create absolute file path for input
        outPath = f'{script_dir}/resources/SARS-CoV-2 Dataset-Preprocessed.csv' # create absolute file path for output
        ttestPathAllData = f'{script_dir}/resources/t-test/paired sample t-test - All Data.txt'
        ttestPathCountries = f'{script_dir}/resources/t-test/paired sample t-test - countries.txt'
        ttestPathContinents = f'{script_dir}/resources/t-test/paired sample t-test - continents.txt'
        gchartPathCountry = f'{script_dir}/resources/growth-charts/countries/'
        gchartPathContinent = f'{script_dir}/resources/growth-charts/continents/'
        rchartPathCountry = f'{script_dir}/resources/relation-charts/countries/'
        rchartPathContinent = f'{script_dir}/resources/relation-charts/continents/'

# Create dataset
    dataset = [] # create an empty list for input dataset
                 # note that dataset is stored as a list of dictionaries


# Remove null and zero
    utils.readCsv(dataset, inPath) # read the dataset from specified csv file
    utils.removeNull(dataset) # replace all the null cells with zero
    utils.removeZero(dataset) # replace all the unnecessary zeros with appropriate values


# Population statistics
    utils.addPopulationStatistics(dataset) # calculate and add population statistics to dataset


# Paired sample t-test
    warnings.filterwarnings('ignore')
    
    sPaires = [
        ('people_fully_vaccinated_per_population','total_cases_per_population'),
        ('people_fully_vaccinated_per_population','total_deaths_per_population'),
        ('people_fully_vaccinated','total_cases'), 
        ('people_fully_vaccinated','total_deaths')
    ]
    
    utils.pairedSampleTTestStrings2File(dataset,sPaires,ttestPathAllData)
    
    locations = vars.countryList
    utils.pairedSampleTTestStringsLocation2File(dataset,sPaires,locations,ttestPathCountries)
    
    locations = vars.continentList
    utils.pairedSampleTTestStringsLocation2File(dataset,sPaires,locations,ttestPathContinents)
    
    warnings.resetwarnings()


# Plot growth chart
    
    gPairs = [
        ('total_deaths_per_population', 'people_fully_vaccinated_per_population', 'total_cases_per_population'),
        ('total_deaths', 'people_fully_vaccinated', 'total_cases'),
        ('total_vaccinations', 'people_vaccinated', 'people_fully_vaccinated'),
    ] 
    
    locations = vars.countryList
    utils.plotGrowthChart(dataset, gPairs, locations, gchartPathCountry)
    
    locations = vars.continentList
    utils.plotGrowthChart(dataset, gPairs, locations, gchartPathContinent)


# Plot relation chart

    rPaires = [
        ('people_fully_vaccinated', 'total_cases'),
        ('people_fully_vaccinated', 'total_deaths'),
        ('total_vaccinations', 'total_cases'),
        ('total_vaccinations', 'total_deaths'),
        ('total_vaccinations', 'people_fully_vaccinated'),
        ('total_deaths', 'total_cases')
        ] 
    
    locations = vars.countryList
    utils.plotRelationChart(dataset, rPaires, locations, rchartPathCountry)
    
    locations = vars.continentList
    utils.plotRelationChart(dataset, rPaires, locations, rchartPathContinent)


# write dataset to a csv file
    utils.writeCsv(dataset, outPath) # save dataset to csv file


if __name__ == "__main__":
    stime = time.time()
    Main()
    print("\nscript execution time: {0}\n".format(time.time() - stime) )
