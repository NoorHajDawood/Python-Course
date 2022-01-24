# Noor Haj Dawood - 314997602
# Bader Daka - 208219212
import json
import csv


def validateFeature(columns, feature, isnumeric=False):
    """
    Input:\n
    \tcolums: dictionary of features\n
    \tfeature: a column in data\n
    \tisnumeric: True/False to valide if feature is numeric\n
    Validate if feature is valid.\n
    Validate that feature is number if isnumber equals True\n
    Throw exception if not valid
    """
    if not feature in columns:
        raise ValueError("ValueError: Feature doesn't exist")
    if isnumeric and columns[feature] == 'string':
        raise TypeError("TypeError: can't do sum on this feature")

def getFeatureList(data, feature, includeNone=True):
    """
    return a list of features from data list of dictionaries
    """
    return [dic[feature] for dic in data if (includeNone or dic[feature] is not None)]

class DataSummary:
    """
    Data Structure of Dataset
    """
    def __init__(self, datafile="", metafile=""):
        """
        intialise the object with dataset from a json and meta-info from a csv
        """
        self.data = []
        self.columns = {}

        # read from metafile
        try:
            with open(metafile, 'r') as theFile:
                reader = csv.DictReader(theFile)
                for row in reader:
                    self.columns = row
        except FileNotFoundError:
            raise ValueError("ValueError: metafile doesn't exist")

        #read from datafile
        try:
            jsonfile = open(datafile)
        except FileNotFoundError:
            raise ValueError("ValueError: datafile doesn't exist")
        tmpdata = json.load(jsonfile)
        for item in tmpdata["data"]:
            res = dict()
            self.data.append(res)
            for key, value in self.columns.items():
                if key in item:
                    if(value != 'string'):
                        res[key] = eval(value)(item[key])
                    else:
                        res[key] = item[key]
                else:
                    res[key] = None

    def __getitem__(self, item):
        """
        return the dictionary in index [item] if item is a number\n
        return a list of values of a certain feature
        """
        if(type(item) is int):
            if((-1*len(self.data)) > item or item >= len(self.data)):
                raise IndexError("IndexError: Index out of bounds")
            return self.data[item].copy()
        if not item in self.columns:
            raise KeyError("KeyError: No such key")
        return getFeatureList(self.data, item)

    def sum(self, feature):
        """
        sum of values of a feature not including categorial features
        """
        validateFeature(self.columns, feature, True)
        return sum(getFeatureList(self.data, feature, False))

    def count(self, feature):
        """
        return the count of a feature not including None values
        """
        validateFeature(self.columns, feature)
        return len(getFeatureList(self.data, feature, False))

    def mean(self, feature):
        """
        the average of a feature values not including categorial features         
        """
        validateFeature(self.columns, feature, True)
        data = getFeatureList(self.data, feature, False)
        _count = len(data)
        if(_count == 0):
            raise ZeroDivisionError("ZeroDivisionError: feature count is 0")
        return sum(data)/_count

    def min(self, feature):
        """
        return the min value of a feature not including categorial features
        """
        validateFeature(self.columns, feature, True)
        return min(getFeatureList(self.data, feature, False))

    def max(self, feature):
        """
        return the max value of a feature not including categorial features
        """
        validateFeature(self.columns, feature, True)
        return max(getFeatureList(self.data, feature, False))

    def unique(self, feature):
        """
        return a list of unique values of a feature
        """
        validateFeature(self.columns, feature)
        return sorted(set(getFeatureList(self.data, feature, False)))

    def mode(self, feature):
        """
        return a list of most frequent values of a feature
        """
        validateFeature(self.columns, feature)
        data = getFeatureList(self.data, feature, False)
        frequency = {}
        for value in data:
            frequency[value] = frequency.get(value, 0) + 1
        maxFreq = max(frequency.values())
        return [key for key, value in frequency.items() if value == maxFreq]

    def empty(self, feature):
        """
        return count of None values of a feature
        """
        validateFeature(self.columns, feature)
        return len(self.data) - len(getFeatureList(self.data, feature, False))

    def to_csv(self, filename, delimiter=','):
        """
        output the DataSummary to a csv file
        """
        if(not delimiter in ',.:|-;#* '):
            delimiter = ','
        with open(filename, "w", newline="") as csvfile:
            file_buffer = csv.writer(csvfile, delimiter = delimiter, lineterminator='\r\n', quoting=csv.QUOTE_ALL)
            file_buffer.writerow(self.columns.keys())
            for x in self.data:
                file_buffer.writerow(x.values())
