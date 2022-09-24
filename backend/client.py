import requests
url = 'http://localhost:8080/generate'
json_en_sentence = {'prompt': 'Hell', 'id': 1001}
x = requests.post(url, json = json_en_sentence)
print(x.text)