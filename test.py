import warnings

warnings.filterwarnings("ignore")
import requests

a = requests.post("http://192.168.0.111:4567", data="Hi")
print(a.content)
