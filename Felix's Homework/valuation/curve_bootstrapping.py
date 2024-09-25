
def short_term_yield(day: int, traded_point: float) -> float:
    """
    short_term_yield(day, traded_point): returns short-term(1d,7d,30d,90d) yield value
    short_term_yield: int, float -> float
    """
    annulized_factor: float = 360/day       # Constants Variable to store factor for annulized
    effective_rate: float = (100 - traded_point) / traded_point     # Effective rate
    yield_value: float = annulized_factor * effective_rate
    return yield_value

def mid_term_yield(data: list) -> float:
    """
    short_term_yield(day, traded_point): returns mid-term(1d,7d,30d,90d) yield value by bootstrapping method
    short_term_yield: list -> float
    """
    rate: float = 1
    for x in data:
        rate = rate * (1 + x)
    rate = rate ** (1/len(data)) - 1
    return rate    



    # data.get("tenor").append(data[0][1])
    # self.data.get("yield_of_3month_IR_Future").append(short_term_yield((data[0][1]-data[0][0]), data[1]))
    # rate: float = 1.0
    # list = self.data.get("yield_of_3month_IR_Future")


    
    # rate = rate ** (1/len(list)) - 1
    # self.data.get("yield").append(rate)    
    return 0.01

def data_get() -> dict:
    """
    data_get(): ask user to input the trade price of futures, return a dictionary in {"tenor":[],"price":[]} format
    data_get: None -> dict
    """
    tenor_list: list = [1,7,30,90,180,270,360]   # a list stored dates we want to have in the yield curve
    price_list: list = []   # a list stored the traded price on each date
    for i in [1,7,30,90]:
        price: float = float(input(f"Enter the trade price on {i}d: "))        # ask to input price
        assert (price > 0), "You should input a price which is bigger than zero"     # doest accept input price <= 0
        price_list.append(price)    # add price data in the list
    for i in [180,270,360]:
        price: float = float(input(f"Enter the trade price of a 3-month IR Future on {i}d: "))        # ask to input price
        assert (price > 0), "You should input a price which is bigger than zero"     # doest accept input price <= 0
        price_list.append(price)    # add price data in the list

    for i in [450,540,630,720]:
        price: float = float(input(f"Enter the fixed-rate of a  year and 3 months IRS end on {i}d: "))        # ask to input price
        assert (price > 0), "You should input a price which is bigger than zero"     # doest accept input price <= 0
        price_list.append(price)    # add price data in the list

    print({"tenor":tenor_list, "price":price_list})
    return {"tenor":tenor_list, "price":price_list}






class CurveBootstrapping:
    """
    Class CurveBootstrapping is used to build a yield curve by observed market data. In this class, 
    financial concept of bootstrapping is applied.

    Attribute:
        self.yield_curve: a dictionary to store the yield curve
    """

    def __init__(self, data: dict = {"tenor":[],"price":[]}):
        """
        
        """
        if data == {"tenor":[],"price":[]}:
            data = data_get()

        assert (data.get("tenor") == [1,7,30,90,180,270,360,450,540,630,720]), "tenor list is not correct"
        assert (len(data.get("price")) == 11), "price list is not correct"
        for p in data.get("price"):
            assert (p > 0), f"price {p} is not bigger than zero"



        self.data: dict = {"tenor" : [1,7,30,90,180,270,360,450,540,630,720],
                           "yield" : []}
        
        # short term bootstrapping
        for t,p in zip(data.get("tenor")[0:4],data.get("price")[0:4]):
            self.data.get("yield").append(short_term_yield(t,p))

        yield_3month_IR: list = [self.data.get("yield")[-1]]



        mid_price_list: list = data.get("price")[4:7]    # price list

        # mid term bootstrapping
        for p in mid_price_list:
            yield_3month_IR.append(short_term_yield(90,p))
            rate: float = mid_term_yield(yield_3month_IR)
            self.data.get("yield").append(rate)

        print(yield_3month_IR)

        # long term bootstrapping
        long_price_list: list = data.get("price")[7:]
        #tmp_cnt: int = 0        # this is a temparay counter
        irs_pv: float = 0       # fix leg's present value

        dividend = 0
        divisor = 1

        for p in long_price_list:
            #tmp_cnt += 1
            for y in yield_3month_IR:
                dividend = (p - y)
                divisor = divisor*(1+y)
                # print("y: ", divisor)
                # print("x: ", dividend)
                irs_pv = irs_pv + dividend/divisor                
                
                # print("irs: ", irs_pv)
                # print("rate: ", rate )
            rate: float = (irs_pv*dividend + p)/(1-irs_pv*dividend)
            yield_3month_IR.append(rate)
            long_term_rate: float = mid_term_yield(yield_3month_IR)
            self.data.get("yield").append(long_term_rate)


        print (self.data)

        
        








