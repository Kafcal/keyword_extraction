import pandas as pd

data_path = 'data/video_data.csv'
data = pd.read_csv(data_path)

ids, titles, contents = list(data["id"]), list(data["title"]), list(data["content"])
print(ids)