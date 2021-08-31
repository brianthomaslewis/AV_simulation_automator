import pandas as pd

list_of_paths = ["C:/Users/blewi156/Desktop/big_sim/MiamiStandardRides_20190321.csv",
                 "C:/Users/blewi156/Desktop/big_sim/MiamiStandardRides_20190321_2per.csv",
                 "C:/Users/blewi156/Desktop/big_sim/MiamiStandardRides_20190321_3per.csv"]


def multiply_times(filepath):
    df = pd.read_csv(filepath, header=None)
    df.iloc[:, [5]] = df.iloc[:, [5]] * 1000
    df.iloc[:, [6]] = df.iloc[:, [6]] * 1000
    df.to_csv(filepath, index=False, header=False)


if __name__ == '__main__':
    for path in list_of_paths:
        multiply_times(path)
