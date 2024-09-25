from datetime import date, datetime, timedelta
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import json


def tenorCheck(df: pd) -> bool:
    """
    tenorCheck: returns bool to show whehter the data is feasible
    tenorCheck(df): Pandas => bool

    requirement: df should be date sorted data
    """
    tempTenor: str = ""         # Store temporary tenor
    for t in df['tenor'].values:
        if tempTenor == "":     # the first element in the tenor array
            tempTenor = t
        elif tenorComparison(tempTenor,t):   # tenor array is sorted
            tempTenor = t
        else:           # tenor array isnt sorted
            return False
    return True

def tenorComparison(tenor1: str, tenor2: str) -> bool:
    """
    tenorComparison: compares the int part of tenor1 and tenor2, if tenor1 < tenor2 reutrn true,
    otherwise return false

    tenorComparison(tenor1, tenor2): Str, Str => Bool

    """
    t1 = int(tenor1[:-1])   # transform str to int
    t2 = int(tenor2[:-1])   # transform str to int
    return t1 < t2  # return Bool

def neighborNode(df: pd, tenor: str) -> list:
    """
    neighborNode: returns the 2 neighboring nodes of tenor on the yield curve, 
    if tenor is on the curve of df, return [tenor, tenor]
    neighbirNode(self, tenor): Pandas Str => List
    
    requirement:
        1d <= tenor <= 18263d
    """
    # requirement:
    assert 1 <= int(tenor[:-1]) <= 18263, "tenor should fit requiement: 1d <= tenor <= 18263d"

    result = [tenor,tenor]      # List for result
    for t in df['tenor'].values:        # for loop to check all tenor in the df
        if t == tenor:                  # find tenor in the curve
            result = [tenor,tenor]
            return result
        elif tenorComparison(t,tenor):  # t < tenor
            result[0] = t
        elif tenorComparison(tenor,t):  # t > tenor
            result[1] = t
            return result

def actDiscount(df: pd, tenor: str) -> float:
    """
    actDiscount: use linear interpolation to find yield value of tenor on the yield curve (df).
                    return the actual discount rate according to the yield value.
    actDiscount(self, tenor): Pandas Str => Float

    requirement:
        1d <= tenor <= 18263d
    """
    #requirement:
    assert 1 <= int(tenor[:-1]) <= 18263, "tenor should fit requiement: 1d <= tenor <= 18263d"

    result: float  = 0
    yieldValue: float = 0
    
    tenorPair = neighborNode(df, tenor)        # get neighbor nodes of tenor

    if tenorPair[0] == tenorPair[1]:            # if the tenor exactly appear on the curve
        yieldValue = df[df['tenor']  == tenorPair[0]]['yield'].values[0]      # yield value for tenor

    else:
        # prepare variables for Linear Interpolation below
        yieldValue1: float  = df[df['tenor']  == tenorPair[0]]['yield'].values[0]       # yield value for the first neigbor
        yieldValue2: float  = df[df['tenor']  == tenorPair[1]]['yield'].values[0]       # yield value for the second neigbor

        intTenor  = int(tenor[:-1])             # digital part of tenor
        intTenor1 = int(tenorPair[0][:-1])      # digital part of tenor1
        intTenor2 = int(tenorPair[1][:-1])      # digital part of tenor2

        # Linear Interpolation Fomular: y = y1 + (x - x1)*(y2 - y1)/(x2 - x1):
        yieldValue = yieldValue1 + (intTenor - intTenor1)*(yieldValue2 - yieldValue1)/(intTenor2 - intTenor1)   # yield value for tenor

    # calculate actual discount rate by fomular actual_discount_rate = [(1 + yield/365) ^ tenor]^-1
    result = ((1 + yieldValue/365) ** int(tenor[:-1])) ** -1

    return result

class YieldCurve:
    """

    A Class to represent a yield curve

    Attributes:
        yieldData(pandas): dataframe of the yield curve


    """
    def __init__(self, file: str):
        """
        Initializes a new yield curve

        __init__(self, file): Str, Str => None

        requirement: parameter file is the file name of the yield curve in string format
                    the file should in json format
        """
        # process file
        with open(file,"r") as f:
            data = json.load(f)
        curve = data["zeroCurve"]["points"]
        date_diff = datetime.today() - datetime.strptime(data["curveDate"],"%Y-%m-%d")
        for p in curve:
            p["date"] = (datetime.strptime(p["date"],"%Y-%m-%d") + 
                         timedelta(date_diff.days)).strftime("%Y-%m-%d")
            
        df = pd.DataFrame(curve)        # dataframe to store data of curves
        df.sort_values(by=['date'], inplace=True)       # sort the data frame by date
        assert tenorCheck(df), "Tenor data is incorrect"     # to check whether the data is feasible, if data and tenor should both be ascending

        self.yieldData = df


    def showYieldCurve(self) -> None:   # plot yield curve
        """
        showYieldCurve: print yield curve
        showYieldCurve(self): None => None

        effect: print a graph
        """
        sns.scatterplot(x='tenor', y='yield', data=self.yieldData)
        plt.xticks(rotation=90)
        plt.title('Yield Curve')
        plt.show()


    def showData(self, rowNum: int = 5) -> pd:  #print first rowNum row of data
        """
        showData: print first rowNum rows of yield curve data
        showData(self, rowNum): Int => Pandas

        effect: print table in the screen
        """
        df: pd = self.yieldData.head(rowNum)
        print(df)
        return df


    def csvCreate(self) -> None:    # stores data in a csv file
        """
        csvCreate(self): create a csv file for the yield curve data
        requirement: self.yield is not empty

        Effect:
            if the csv is created sucessfully, print msg
            created a csv file with current date in its name
        """
        try:      
            pd.DataFrame(self.yieldData).to_csv(f"cad_ois_{date.today().strftime('%Y-%m-%d')}.csv",index=False)
            print(f"cad_ois_{date.today().strftime('%Y-%m-%d')}.csv", " Created")
        except:
            print("Cant save data as CSV")


    def present_value(self, cashflow: float, tenor: str) -> float:     # return the present value of cashflow
        """
        present_value: calculated present value of the cashflow by use the yield data in self.yieldData
        present_value(self, cashflow, tenor): Float, Str => Float

        requirement:
            0 < cashflow
            1d <= tenor <= 18263d
        """
        #requirement:
        assert 1 <= int(tenor[:-1]) <= 18263, "tenor should fit requiement: 1d <= tenor <= 18263d"
        assert 0 < cashflow, "cashflow should greater than 0"

        presentValue: float = 0
        adf: float = actDiscount(self.yieldData, tenor)        # actual discount factor
        presentValue = cashflow * adf               # calculate present value
        return presentValue
    
    def insight(self, cashflow: float) -> None:     # shows insight of the bond, such as profit, profit per day, present value
        """
        insight: prints a table and two grapgh to show the insight of the bond in the yield curve.
                output table countains columns: date, tenor, yield, actual discount rate, cash flow, present values, profit, profit per day
                graph 1: show the profit per day of each tenor
                graph 2: show the profit of each tenor

        requirement:
            0 <= cashflow
        """
        assert 0 <= cashflow, "cashflow should greater than 0"

        df = self.yieldData[["date","tenor","yield"]].copy()
        df["actual discount rate"] = df["tenor"].apply(lambda t: actDiscount(self.yieldData, t))

        df["cash flow"] = cashflow

        df["present values"] = df["tenor"].apply(lambda t: self.present_value(cashflow, t))

        df["profit"] = df["cash flow"] - df["present values"]

        df["profit per day"] = df.apply(lambda row: row["profit"] / int(row["tenor"][:-1]), axis=1)

        sns.scatterplot(x='tenor', y='profit per day', data=df)
        plt.xticks(rotation=90)
        plt.title('daily profit curve')
        plt.show()

        sns.scatterplot(x='tenor', y='profit', data=df)
        plt.xticks(rotation=90)
        plt.title('profit curve')
        plt.show()

        print(df)