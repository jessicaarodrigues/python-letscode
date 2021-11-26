#!/usr/bin/env python
# coding: utf-8

# In[3]:


get_ipython().system('pip install requests')


# In[5]:


import requests as r


# In[12]:


url = 'https://api.covid19api.com/dayone/country/brazil'
resp = r.get(url)


# In[10]:


resp.status_code


# In[13]:


raw_data = resp.json()


# In[14]:


raw_data [0]


# In[3]:


final_data = []
for obs in raw_data:
    final_data.append([obs['Confirmed'], obs['Deaths'], obs['Recovered'], obs['Active'], obs['Date']])


# In[1]:


final_data.insert(0, ['confirmados', 'óbitos', 'recuperados', 'ativos', 'data'])


# In[2]:


final_data


# In[4]:


CONFIRMADOS = 0
OBITOS = 1
RECUPERADOS = 2
ATIVOS = 3
DATA = 4


# In[5]:


for i in range(1, len(final_data)):
    final_data[1][DATA] = final_data[i][DATA][:10]


# In[6]:


final_data


# In[7]:


import datetime as dt


# In[8]:


import csv


# In[9]:


with open('brasil-covid.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerows(final_data)


# In[10]:


for i in range(1, len(final_data)):
    final_data[i][DATA] = dt.datetime.strptime(final_data[i][DATA], '%Y-%m-%d')


# In[12]:


def get_datasets(y, labels):
    if type(y[0]) == list:
        datasets  = []
        for i in range(len(y)):
            datasets.append({
                'label' : labels[i],
                'data' :y[i]
            })
        return datasets
    else:
        return [
            {
                'label' : labels[0],
                'data' : y
            }
        ]


# In[13]:


def set_title(title=''):
    if title != '':
        display = 'true'
    else:
        diplay = 'false'
    return {
        'title' : title,
        'display' : display
    }


# In[14]:


def create_chart(x, y, labels, kind='bar', title=''):
    
    datasets = get_datasets(y, labels)
    options = set_title(title)
    
    chart = {
        'type' : kind,
        'data' : {
            'labels' :x,
            'datasets' : datasets
        },
        'options' : options
    }
    
    return chart


# In[15]:


def get_api_chart(chart):
    url_base = 'https://quickchart.io/chart'
    resp = r.get(f'{url_base}?c={str(chart)}')
    return resp.content


# In[16]:


def save_image(path, content):
    with open(path, 'wb') as image:
        image.write(content)


# In[18]:


from PIL import Image
from IPython.display import display


# In[20]:


def display_image(path):
    img_pil = Image.open(path)
    display(img_pil)


# In[21]:


y_data_1 = []
for obs in final_data[1::10]:
    y_data_1.append(obs[CONFIRMADOS])

y_data_2 = []
for obs in final_data[1::10]:
    y_data_2.append(obs[RECUPERADOS])
    
labels = ['Confirmados', 'Recuperados']

x = []
for obs in final_data[1::10]:
    x.append(obs[DATA].strftime('%d/%m/%Y'))
    
chart = create_chart(x, [y_data_1, y_data_2], labels, title='Gráfico confirmados vs recuperados')
chart_content = get_api_chart(chart)
save_image('meu-primeiro-grafico.png', chart_content)
display_image('meu-primeiro-grafico.png')


# In[22]:


from urllib.parse import quote


# In[23]:


def get_api_qrcode(link):
    text = quote(link) # parsing do link para url
    url_base = 'https://quikchart.io/qr'
    resp = r.get(f'{url_base}?text={text}')
    return resp.content


# In[24]:


url_base = 'https://quickchart.io/chart'
link = f'{url_base}?c={str(chart)}'
save_image('qr-code.png', get_api_qrcode(link))
display_image('qr-code.png')


# In[ ]:




