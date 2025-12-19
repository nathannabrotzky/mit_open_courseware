import pylab
import re

CITIES = [
    'BOSTON','SEATTLE','SAN DIEGO','PHILADELPHIA','PHOENIX','LAS VEGAS','CHARLOTTE',
    'DALLAS','BALTIMORE','SAN JUAN','LOS ANGELES','MIAMI','NEW ORLEANS','ALBUQUERQUE',
    'PORTLAND','SAN FRANCISCO','TAMPA','NEW YORK','DETROIT','ST LOUIS','CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2010)
TESTING_INTERVAL = range(2010, 2016)

class Climate(object):
    def __init__(self:Climate, filename:str) -> None:
        self.rawdata = {}
        with open(filename, 'r') as f:
            header:list[str] = f.readline().strip().split(',')
            for line in f:
                items:list[str] = line.strip().split(',')
                date = re.match(r'(\d{4})(\d{2})(\d{2})', items[header.index('DATE')])
                year:int = int(date.group(1))
                month:int = int(date.group(2))
                day:int = int(date.group(3))
                city:str = items[header.index('CITY')]
                temperature:float = float(items[header.index('TEMP')])
                if city not in self.rawdata:
                    self.rawdata[city] = {}
                if year not in self.rawdata[city]:
                    self.rawdata[city][year] = {}
                if month not in self.rawdata[city][year]:
                    self.rawdata[city][year][month] = {}
                self.rawdata[city][year][month][day] = temperature

    def get_yearly_temp(self:Climate, city:str, year:int) -> pylab.array:
        temperatures:list = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return pylab.array(temperatures)

    def get_daily_temp(self:Climate, city:str, month:int, day:int, year:int) -> float:
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

def se_over_slope(x:pylab.array, y:pylab.array, estimated:pylab.array, model:pylab.array) -> float:
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = pylab.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]

def generate_models(x:pylab.array, y:pylab.array, degs:list[int]) -> list[pylab.array]:
    coefficients_list = []
    for degree in degs:
        coeff = pylab.polyfit(x, y, degree)
        coefficients_list.append(coeff)
    return coefficients_list

def r_squared(y:pylab.array, estimated:pylab.array) -> float:
    mean:float = pylab.mean(y)
    r_squared:float = 1 - (pylab.sum((y - estimated) ** 2) / pylab.sum((y - mean) ** 2))
    return r_squared

def evaluate_models_on_training(x:pylab.array, y:pylab.array, models:list[pylab.array]) -> None:
    for model in models:
        estimated = pylab.polyval(model, x)
        r2 = r_squared(y, estimated)
        degree = len(model) - 1
        title = f'Degree: {degree}, R^2: {r2:.4f}'
        if degree == 1:
            se_slope = se_over_slope(x, y, estimated, model)
            title += f', SE/Slope: {se_slope:.4f}'
        pylab.figure()
        pylab.plot(x, y, 'bo', label='Data Points')
        pylab.plot(x, estimated, 'r-', label='Best Fit Curve')
        pylab.xlabel('X-axis')
        pylab.ylabel('Y-axis')
        pylab.title(title)
        pylab.legend()
        pylab.show()

def gen_cities_avg(climate:Climate, multi_cities:list[str], years:list[int]) -> pylab.array:
    data:list[float] = []
    for year in years:
        cities_data:list[float] = []
        for city in multi_cities:
            year_data = (climate.get_yearly_temp(city, year))
            cities_data.append(pylab.mean(year_data))
        data.append(pylab.mean(cities_data))
    data:pylab.array = pylab.array(data)
    return data

def moving_average(y:pylab.array, window_length:int) -> pylab.array:
    result:pylab.array = pylab.zeros(len(y))
    for i in range(len(y)):
        if i < window_length:
            window = y[0:i+1]
        else:
            window = y[i-window_length+1:i+1]
        result[i] = pylab.mean(window)
    return result

def rmse(y:pylab.array, estimated:pylab.array) -> float:
    return pylab.sqrt(pylab.mean((y - estimated) ** 2)/len(y))

def gen_std_devs(climate:Climate, multi_cities:list[str], years:list[int]) -> pylab.array:
    data:list[float] = []
    for year in years:
        cities_data:list[float] = []
        for city in multi_cities:
            year_data = (climate.get_yearly_temp(city, year))
            cities_data.append(pylab.std(year_data))
        data.append(pylab.mean(cities_data))
    data:pylab.array = pylab.array(data)
    return data

def evaluate_models_on_testing(x:pylab.array, y:pylab.array, models:list[pylab.array]) -> None:
    for model in models:
        estimated = pylab.polyval(model, x)
        degree = len(model) - 1

        rmse_value = rmse(y, estimated)
        title = f'Degree: {degree}, RMSE: {rmse_value:.4f}'
        model_x = pylab.array([*list(x), *TESTING_INTERVAL])
        model_y = pylab.polyval(model, model_x)

        pylab.figure()
        pylab.plot(x, y, 'bo', label='Data Points')
        pylab.plot(model_x, model_y, 'r-', label='Best Fit Curve')
        pylab.xlabel('X-axis')
        pylab.ylabel('Y-axis')
        pylab.title(title)
        pylab.legend()
        pylab.show()

if __name__ == '__main__':
    climate:Climate = Climate('ps5\\data.csv')

    # Regression for daily temperature in NY on Jan 10th
    data:list[float] = []
    for year in TRAINING_INTERVAL:
        data.append(climate.get_daily_temp('NEW YORK', 1, 10, year))
    data:pylab.array = pylab.array(data)
    x:pylab.array = pylab.array(range(len(data)))
    coefficients:list[pylab.array] = generate_models(x, data, [1])
    evaluate_models_on_training(x, data, coefficients)

    # Regression for annual average temperature in NY
    data:list[float] = []
    for year in TRAINING_INTERVAL:
        year_data = (climate.get_yearly_temp('NEW YORK', year))
        data.append(pylab.mean(year_data))
    data:pylab.array = pylab.array(data)
    x:pylab.array = pylab.array(range(len(data)))
    coefficients:list[pylab.array] = generate_models(x, data, [1])
    evaluate_models_on_training(x, data, coefficients)

    # Regression for annual average temperature over all cities
    data:pylab.array = gen_cities_avg(climate, CITIES, TRAINING_INTERVAL)
    x:pylab.array = pylab.array(range(len(data)))
    coefficients:list[pylab.array] = generate_models(x, data, [1])
    evaluate_models_on_training(x, data, coefficients)

    # Regression for moving average of annual average temperature over all cities
    data:pylab.array = gen_cities_avg(climate, CITIES, TRAINING_INTERVAL)
    data:pylab.array = moving_average(data, 5)
    x:pylab.array = pylab.array(range(len(data)))
    coefficients:list[pylab.array] = generate_models(x, data, [1])
    evaluate_models_on_training(x, data, coefficients)

    # Predictive regression for future daily temperature in NY on Jan 10th
    data:list[float] = []
    for year in TRAINING_INTERVAL:
        data.append(climate.get_daily_temp('NEW YORK', 1, 10, year))
    data:pylab.array = pylab.array(data)
    x:pylab.array = pylab.array(TRAINING_INTERVAL)
    coefficients:list[pylab.array] = generate_models(x, data, [1])
    evaluate_models_on_testing(x, data, coefficients)

    # Predictive regression for moving average of annual average temperature over all cities
    data:pylab.array = gen_cities_avg(climate, CITIES, TRAINING_INTERVAL)
    data:pylab.array = moving_average(data, 5)
    x:pylab.array = pylab.array(range(len(data)))
    coefficients:list[pylab.array] = generate_models(x, data, [1,2,20])
    evaluate_models_on_testing(x, data, coefficients)

    # Regression for moving average of annual std dev over all cities
    data:pylab.array = gen_std_devs(climate, CITIES, TRAINING_INTERVAL)
    data:pylab.array = moving_average(data, 5)
    x:pylab.array = pylab.array(range(len(data)))
    coefficients:list[pylab.array] = generate_models(x, data, [1])
    evaluate_models_on_training(x, data, coefficients)
