import requests
import concurrent.futures
import os

# Form list of requests, for each zip code 

t1 = ['0' + str(i) for i in range(1000,8900, 100)]
t2 = [str(i) for i in range(10000,99400, 100)]

zip_ranges = ['01000', *t1, *t2]

folder = 'domestic_zones'

if not os.path.exists(folder):
    os.makedirs(folder)


form_data = [ {'zipcode' : code} for code in zip_ranges]

# Write url request  
url = 'https://www.ups.com/zonecharts/'

def send_post(form_data, file_name):
    response = session.post(url, data=form_data)
    if response.status_code == 200:
        save_excel_file(response, folder, file_name)

def save_excel_file(response, folder, filename):
    content_type = response.headers.get('Content-Type')
    print(filename)
    if 'application/vnd.ms-excel' in content_type:

        filepath = os.path.join(folder, filename)
        with open(filepath, 'wb') as f:
            f.write(response.content)


# Initialize session for asynchronous requests
session = requests.Session()
adapter = requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100)
session.mount('https://', adapter)

folder = 'domestic_zones'

if not os.path.exists(folder):
    os.makedirs(folder)

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    for pos, form_req in enumerate(form_data):
        file_name = str(pos + 1) + '.xlsx'
        executor.submit(send_post, form_req, file_name)
