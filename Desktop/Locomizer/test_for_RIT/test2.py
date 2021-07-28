#-*- coding: utf-8 -*-
from datetime import date
from numpy.lib.function_base import average
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.core.frame import DataFrame
from pandas.core.series import Series
import os

def main():

    print('Тестовое задание\n')
    print('Пожалуйста введите адрес файлов "Приложение A", "Приложение B", "Приложение C":')
    path = 'string'

    while path == 'string':    
        path = input()             
        try:
            os.chdir(path)   
        except:
            print('В', path, 'файлы не найдены, повторите попытку')
            path = 'string'

    data_date = pd.read_csv('Приложение A', delimiter= '\t')
    data_price = pd.read_csv('Приложение C', delimiter= '\t')
    data_time = pd.read_csv('Приложение B',delimiter= '\t')    

    data_date.columns = ['Date', 'Performer', 'Task', 'Time']
    data_price.columns = ['Performer', 'Rate']
    data_time.columns = ['Task', 'Estimate']



    ##################################### Functions ##################################

    # Average hours per day by worker
    def average_hours_per_day(worker):         
        amount_days = len(data_date[data_date['Performer'] == worker].groupby(data_date['Date']))
        average_time = work_time[work_time.index == worker] / amount_days
        average_time[0] = "%.1f" % average_time[0]
        return average_time[0]


    # Average task time by worker
    def average_hours_for_task(worker):         
        amount_tasks = len(data_date[data_date['Performer'] == worker].groupby(data_date['Task']))
        average_time = work_time[work_time.index == worker] / amount_tasks
        average_time[0] = "%.1f" % average_time[0]
        return average_time[0]




    # Absence days for worker
    def absence_days(worker):
        worker_dates = workers_dates[worker]
        worker_dates = pd.unique(worker_dates.dropna())
        worker_dates.sort()
        result = list(set(dates) - set(worker_dates) - set(['08.05.2021', '09.05.2021']))
        return result



    # mean deviation time for worker
    def mean_deviation_time(worker):            
        worker = (data_date.loc[data_date['Performer'] == worker])
        worker_tasks = worker.loc[ :, ['Task'][0]]
        worker_tasks = pd.unique(worker_tasks)
        deviation = delta_time[worker_tasks].sum() / len(delta_time[worker_tasks])
        deviation = "%.2f" % deviation
        return deviation



    ################################################################################################################

    # work time for each worker
    work_time = data_date['Time'].groupby(data_date['Performer']).sum()                                         

    # time for each task
    tasks_time = data_date['Time'].groupby(data_date['Task']).sum()                                           
    tasks_time = tasks_time.iloc[tasks_time.index.str.extract('(\d+)', expand=False).astype(int).argsort()]
    tasks_time.index = np.arange(0, len(tasks_time))

    # mean deviation time for each task
    delta_time = data_time.loc[:,'Estimate'] - tasks_time
    delta_time.index = data_time['Task']


    # Project time
    project_time = int(data_date.loc[ :, ['Time'] ].sum())

    # Average task time
    average_time_task = tasks_time.sum()/len(tasks_time)                         

    # Median task time
    median_time_task = tasks_time.median(axis = 0)  


    # workers dates
    workers_dates = data_date['Date'].groupby(data_date['Performer']).apply(pd.DataFrame)


    # all dates
    dates = data_date['Date']
    dates = pd.unique(dates)
    dates.sort()



    # Project profitability
    # profitability = profit * 100 / income
    # profit = income - costs
    income = 24000
    # costs = worker_time * price

    costs = 0
    for i in range(len(data_price['Performer'])):
        costs += work_time[i] * data_price.loc[i]['Rate']
    profit = income - costs
    profitability = (profit * 100) / income







    d = {'average_hours_per_day':   [average_hours_per_day(x)   for x in data_price['Performer']],
        'average_hours_for_task':  [average_hours_for_task(x)  for x in data_price['Performer']],
        'mean_deviation_time':     [mean_deviation_time(x)     for x in data_price['Performer']],
        'absence_days':            [absence_days(x)            for x in data_price['Performer']]}


    data_output = pd.DataFrame(data=d)
    data_output.columns = ['Среднее время работы в день', 'Среднее время решения задачи', 'Среднее отклонение', 'Прогулы']
    data_output.index = data_price['Performer']

    print(data_output)   
    print('\nТрудозатраты на проект в часах:', project_time)
    print('Среднее время, затраченное на решение задач в часах:', "%.1f" % average_time_task)
    print('Медианное время, затраченное на решение задач в часах:', median_time_task)


    print('\nРентабельность:', profitability, '\n')




    x = np.arange(1, len(data_time)+1)
    y = data_time['Estimate']
    yy = tasks_time
    plt.rcParams['figure.figsize'] = (15.0, 8.0)
    plt.title('Оценка трудозатрад')
    plt.bar(x,y, label='Ожидаемые трудозатраты')
    plt.bar(x-0.2,yy, width= 0.4, label='Фактические трудозатраты')
    plt.legend()  
    plt.xticks(np.arange(1, len(data_time)+1))
    plt.xlabel('задачи, №')
    plt.ylabel('время, час')


    plt.savefig(path + '\\Оценка трудозатрат.png', dpi=200)


if __name__ == '__main__':
    main()


