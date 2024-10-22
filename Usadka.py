import numpy as np
import matplotlib.pyplot as plt
import serial
from drawnow import drawnow
import datetime
import time
import tkinter
import serial.tools.list_ports


# Создание интерфейса пользователя

# Глобальные переменные для хранения выбора COM порта и времени замера
selected_port = None
selected_time = None

# Получение списка активных портов
list1 = serial.tools.list_ports.comports() #  Переменная, которая принимает значения активных портов
connected = []  # Список, где будут находится названия активных портов

# Пробежка по полученному списку list1 и добавка активных портов в список connected
for element in list1:
    connected.append(element.device)  # В список connected добавляем все активные порты с помощью функции devise
print ("Connected COM ports: " + str(connected)) # Вывод списка активных портов в текстовом формате

# Создаём оконное приложение
window = tkinter.Tk()
window.title("Усадка и расширения цементного раствора")   # Название окно
window.geometry('410x300')  # Размер окно

# В оконное приложении создаём окошку (Listbox), куда поместим список активных COM портов
List1 = tkinter.Listbox(window, width = 7, height = 4, selectmode = 'SINGLE') # Из списка нам надо выбирать 1 элемент, поэтому параметр для selectmode выбираем 'SINGLE'
for i in range (len(connected)):   # Цикл пробежки по активным портом в списке connected
    List1.insert(tkinter.END, connected[i])  # Доваление элементов из списка connected
List1.grid(row=1,column=1)

def v1():     # Функция выбора СОМ порта
    global selected_port
    select1 = list(List1.curselection())
    selected_port = connected[int(select1[0])]
    print("Выбранный COM порт:", selected_port)

# Кнопка для выбора СОМ порта
B1 = tkinter.Button(window, text = 'Выбрать необходимый COM порт', width = 30, height = 2, command = v1)
B1.grid(row=2,column=1)


# Cписок времени замеров
measurement_time = ['1440', '4320', '10080','40320']  # Список времени замеров в минутах

# Создаём окошку (Listbox), куда поместим список времени замеров
List2 = tkinter.Listbox(window, width = 7, height = 4, selectmode = 'SINGLE') # Из списка нам надо выбирать 1 элемент, поэтому параметр для selectmode выбираем 'SINGLE'
for i in range (len(measurement_time)):   # Цикл пробежки по активным портом в списке connected
    List2.insert(tkinter.END, measurement_time[i])  # Доваление элементов из списка connected
List2.grid(row=3,column=1)

def v2():    # Функция выбора выбора необходимого времени замера
    global selected_time
    select2 = list(List2.curselection())
    selected_time = measurement_time[int(select2[0])]
    print("Выбранное время замера:", selected_time)

# Кнопка для выбора времени замера
B2 = tkinter.Button(window, text = 'Выбрать необходимого времени замера', width = 35, height = 2, command = v2)
B2.grid(row=4,column=1)


def v3():    # Функция закрытия оконного приложения
    window.destroy()  # Закрыть окно

# Кнопка для закрытия окно выбора
B3 = tkinter.Button(window, text = 'Закрыть окно', width = 20, height = 2, command = v3)
B3.grid(row=5,column=1)

window.mainloop()


# Установка шрифта, поддерживающего кириллицу
plt.rcParams['font.family'] = 'DejaVu Sans'

#вывод выборки в графическое окно
def cur_graf():
    plt.title("График усадки и расширения цементного раствора")
    plt.ylim( -7.1, 7.1 )
    plt.plot(nw, lw1, "r.-")    #  выбор цвета
    plt.ylabel(r'результат измерения мм')
    plt.xlabel(r'номер измерения')
    plt.grid(True)

#вывод всех списков в графическое окно
def all_graf():
    plt.close()
    plt.figure()
    plt.title("График усадки и расширения цементного раствора\n" +
              "Дата проведение эксперимента " +
              "(" + now.strftime("%d-%m-%Y %H:%M") + ")")
    plt.plot( n, l1,  "r-")      #  выбор цвета
    plt.ylabel(r'Линейное изменение раствора,  мм')
    plt.xlabel(r'количество измерения' +
               '; (период опроса датчика: {:.6f}, c)'.format(Ts))
    plt.grid(True)
    plt.show()

#определяем количество измерений
# общее количество измерений
# str_m   = input("введите количество измерений: ")
m = int(selected_time)  # Используем выбранное время замера

# количество элементов выборки
mw  = 16

#настроить параметры последовательного порта
ser = serial.Serial()
ser.baudrate = 9600
# port_num = input("введите номер последовательного порта: ")
ser.port = selected_port  # Используем выбранный COM порт
ser

#открыть последовательный порт
try:
    ser.open()
    ser.is_open
    print("соединились с: " + ser.portstr)
except serial.SerialException:
    print("нет соединения с портом: " + ser.portstr)
    raise SystemExit(1)

#определяем списки
l1  = [] # для значений линейного изменения раствора
t1  = []
lw1 = [] # для значений выборки линейного изменения раствора
n   = [] # для значений моментов времени
nw  = [] # для значений выборки моментов времени

#подготовить файлы на диске для записи
filename = 'count.txt'
in_file = open(filename,"r")
count = in_file.read()
in_file.close()
in_file = open(filename,"w")
in_file.write(count)
in_file.close()
filename = count + '_' + filename
out_file = open(filename,"w")

#вывод информации для оператора на консоль
print("\n Параметры:\n")
print("№ - номер измерения;")
print("Линейное изменения раствора - мм;")
print("\n измеряемые значения усадки и расширения\n")
print('{0}{1}\n'.format('№'.rjust(4),'мм'.rjust(10)))

#считывание данных из последовательного порта
#накопление списков
#формирование текущей выборки
#вывод значений текущей выборки в графическое окно
i = 0
while i < m:
    n.append(i)
    nw.append(n[i])
    if i >= mw:
        nw.pop(0)
    line1 = ser.readline().decode('utf-8')[:-2]
    t1.append(time.time())
    if line1:
        l1.append(eval(line1))
        lw1.append(l1[i])
        if i >= mw:
            lw1.pop(0)
    print('{0:4d} {1:10.2f}'.format(n[i],l1[i]))
    drawnow(cur_graf)
    i += 1

#закрыть последовательный порт
ser.close()
ser.is_open
#time_tm -= time_t0
time_tm = t1[m - 1] - t1[0]
print("\n продолжительность времени измерений: {0:.3f}, c".format(time_tm))
Ts = time_tm / (m - 1)
print("\n период опроса датчика: {0:.6f}, c".format(Ts))

#запись таблицы в файл
print("\n таблица находится в файле {}\n".format(filename))
for i in np.arange(0,len(n),1):
    count = str(n[i]) + "\t" + str(l1[i]) + "\n"
    out_file.write(count)

#закрыть файл с таблицей
out_file.close()
out_file.closed

#получить дату и время
now = datetime.datetime.now()

#вывести график в графическое окно
all_graf()
end = input("\n нажмите Ctrl-C, чтобы выйти ")
