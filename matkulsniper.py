
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import pandas as pd
import mechanize
import re

print('Matkul Sniper by Gondok')

alamat = r'https://akademik.itb.ac.id/app/mahasiswa:18219024+2020-2/registerasi/103099/kelas/44023?fakultas=FSRD&prodi=179#44023'
req = Request(alamat, headers={'User-Agent': 'Mozilla/5.0'})
html = urlopen(req).read()
data = BeautifulSoup(html,'html.parser')


br = mechanize.Browser()
br.set_handle_robots(False)
br.open(alamat)

target_login_INA = r'/login/INA?returnTo=https://akademik.itb.ac.id/app/mahasiswa:18219024%2B2020-2/registerasi/103099/kelas/44023?fakultas%3DFSRD%26prodi%3D179'

print('Opening subject link...')

for link in br.links():
    if link.url == target_login_INA:
        break

br.follow_link(link)

br.select_form(id='fm1')

username = input('Enter INA Username: ')
password = input('Enter INA Account Password: ')

credentials = {
	'username' : username,
	'password' : password
}

br.form['username'] = credentials['username']
br.form['password'] = credentials['password']


res = br.submit()

print('Successfully logged in. \nReturning to KRS Menu...')

target_redirect_matkul = '/locale/en?returnTo=/app/mahasiswa:18219024%2B2020-2/registerasi/103099/kelas/44023?fakultas%3DFSRD%26prodi%3D179'

for link in br.links():
    if link.url == target_redirect_matkul:
        break

br.follow_link(link)

print('Subject retrieved. Fetching results...')

html=br.response().read()

soup = BeautifulSoup(html,'html.parser')

cols = soup.findAll('div', {"class" : 'list-group-item notice notice-info'})

Kuota = []

for j in cols[0]:
    test = soup.findAll('p', {"class" : 'small'})
    for x in test:
        Kuota.append(x.text)
    
subject = soup.find('a', {'class' : 'list-group-item list-group-item-info'})
print('Results for '+subject.text)

def divide_chunks(l, n): 
    for i in range(0, len(l), n):  
        yield l[i:i + n] 
x = list(divide_chunks(Kuota, 2))

for i in range (0,len(x)):
    print('K'+str(i+1)+':')
    print(x[i][0] + ' '+ x[i][1])
    if(int(x[i][0][-2:])-int(x[i][1][-2:])>0):
        print('\033[0;32mSpace available at K'+str(i+1)+'! GOGOGOGOGOGOO\033[0;37m')
