import warnings

warnings.filterwarnings("ignore")
import requests

a = requests.post("http://localhost:5678/", data="Hi")
print(a.content)
