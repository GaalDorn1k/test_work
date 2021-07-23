from numpy.core.fromnumeric import size
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



##################################### Data download ###############################

print('Тестовое задание\n')
print('Пожалуйста введите адрес файлов A, B, C:')
path = 'string'

while path == 'string':
    
    path = input()

    try:
        data_time = pd.read_csv(path + '\\A', delimiter = '\t')
        data_price = pd.read_csv(path + '\\C', delimiter = '\t')
        data_mark = pd.read_csv(path + '\\B', delimiter = '\t')
    
    except:
        print('В', path, 'файлы не найдены, повторите попытку')
        path  = 'string'
    
data_mark['Время'] = 0
    
data_price['Время'] = 0
data_price['Среднее время работы в день'] = 0
data_price['Количество задач'] = 0
data_price['Среднее время выполнения задачи'] = 0



##################################### Average hours per day by each worker ##################################

for col in range(len(data_time['Задача'])):
  index = data_mark[data_mark['Задача'] == data_time.iloc[col]['Задача']].index
  data_mark.at[index[0], 'Время'] += data_time.iloc[col]['Часы']  




workers_list = [0] * len(data_price) 
workers_list = list(map(float, workers_list))


for col in range(len(data_time['Исполнитель'])):
  index = data_price[data_price['Исполнитель'] == data_time.iloc[col]['Исполнитель']].index  
  workers_list[index[0]] += 1  
  data_price.at[index[0], 'Время'] += data_time.iloc[col]['Часы']


data_price['Среднее время работы в день'] = list(map(float, data_price['Среднее время работы в день']))
for i in range(len(data_price['Исполнитель'])):
    data_price.at[i, 'Среднее время работы в день'] = "%.1f" %  (data_price.loc[i, 'Время'] / workers_list[i])






##################################### Average task time by each worker ######################################

def average_worker_task(name, n):
    worker = (data_time.loc[data_time['Исполнитель'] == name])
    worker_tasks = worker.loc[ :, ['Задача'][0]]
    worker_tasks = pd.unique(worker_tasks)
    data_price.at[n, 'Количество задач'] = len(worker_tasks)
    data_price['Среднее время выполнения задачи'] = list(map(float, data_price['Среднее время выполнения задачи']))
    data_price.at[n, 'Среднее время выполнения задачи'] = "%.1f" % (data_price.loc[n, 'Время'] / data_price.loc[n, 'Количество задач'])
    return worker_tasks


workers_tasks_list = []

for i in range(len(data_price['Исполнитель'])):
    workers_tasks_list.append(average_worker_task(data_price.loc[i, 'Исполнитель'], i))









##################################### Absence days for each worker ##########################################

def absence_days(name):
    worker = (data_time.loc[data_time['Исполнитель'] == name])
    worker = worker.loc[ :, ['Дата'][0]]
    worker.index = np.arange(0, len(worker))                            # reindex table
    for i in range(len(worker)):
        worker.at[i] = worker.loc[i][0] + worker.loc[i][1]              # data number
    worker_abs = worker.values.tolist()
    worker_abs = list(map(int, worker_abs))
    b = [x for x in range(worker_abs[0], worker_abs[-1] + 1)]
    worker_abs = set(worker_abs)
    worker_abs = (list(worker_abs ^ set(b)))
    if 8 in worker_abs:
        worker_abs.remove(8)
    if 9 in worker_abs:    
        worker_abs.remove(9)
    return worker_abs

may_absence = []
for i in range(len(data_price['Исполнитель'])):
    may_absence.append(absence_days(data_price.loc[i, 'Исполнитель']))







##################################### Project profitability #################################################

# profitability = profit * 100 / income
# profit = income - costs
income = 24000
# costs = worker_time * price

costs = 0
for i in range(len(data_price['Исполнитель'])):
  costs += data_price.loc[i]['Время'] * data_price.loc[i]['Ставка']
profit = income - costs
profitability = (profit * 100) / income








##################################### Mean deviation time for each worker #####################################


deviation_list = []
for i in range(len(data_price)):
    deviation = 0
    for j in range(len(workers_tasks_list[i])):       
        delta = data_mark.loc[data_mark['Задача'] == workers_tasks_list[i][j]]['Время'] - data_mark.loc[data_mark['Задача'] == workers_tasks_list[i][j]]['Оценка'] 
        deviation += int(delta)
        
    deviation_list.append("%.2f" % (deviation / len(workers_tasks_list[i])))


data_price['Средний вылет из оценки'] = deviation_list







##################################### Total labor costs for the project in hours ###########################

project_time = int(data_time.loc[ :, ['Часы'] ].sum())

average_time_task = "%.1f" % (float((project_time) / (len(data_mark))))                         # Average task's time

median_time_task = int(data_mark.loc[ :, ['Время']].median(axis = 0))                           # Median task's time









##################################### Data output ##############################################################

print('\n\n', data_price[['Исполнитель', 'Среднее время работы в день', 'Среднее время выполнения задачи', 'Средний вылет из оценки']], '\n')
 

print('\nТрудозатраты на проект в часах:', project_time)
print('Среднее время, затраченное на решение задач в часах:', average_time_task)
print('Медианное время, затраченное на решение задач в часах:', median_time_task)


print('\nПрибыльность:', profitability, '\n')

for i in range(len(data_price)):
    print('Прогулы', data_price.loc[i, 'Исполнитель'], 'в мае:', may_absence[i])

print('\n\nГрафик сохранен в', path, '\n\n')




##################################### Graph ###################################################################

x = np.arange(1, len(data_mark)+1)
y = data_mark['Оценка']
yy = data_mark['Время']
plt.rcParams['figure.figsize'] = (15.0, 8.0)
plt.title('Оценка трудозатрад')
plt.bar(x,y, label='Ожидаемые трудозатраты')
plt.bar(x-0.2,yy, width= 0.4, label='Фактические трудозатраты')
plt.legend()  
plt.xticks(np.arange(1, len(data_mark)+1))
plt.xlabel('задачи, №')
plt.ylabel('время, час')


plt.savefig(path + '\\Оценка трудозатрат.png', dpi=200)

