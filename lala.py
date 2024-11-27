import pandas as pd



if __name__ == '__main__':
    muscles = pd.read_csv("muscles.csv")

    for m in muscles:
        print(m)