import pandas as pd

def load_data(path, sep=',', decimal=','):
    df = pd.read_csv(path, sep=sep, decimal=decimal, skiprows=[1])
    df = df.drop(columns=['Komentarze'], errors='ignore')
    return df

if __name__ == "__main__":
    path = 'cw2/dane/pkt4.csv'
    df = load_data(path)
    print(f"pkt4: {df.shape} wczytane.")