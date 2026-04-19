
""" Генерация мьютексов процесса """


class Mutex:
    """ Класс Mutex - описание одного мьютекса процесса """

    # Номера типовых мьютексов. При указании номера << typeMutexNum >>,
    # отличного от нуля, генерируется типовой мьютекс из списка

    mNumEndResetProcess = 1
    """ Генерируется мьютекс принудительного завершения процесса, например:
     /** Входящий ONEX - Остановка процесса по внешней команде */
     ISSA_RESET_PROCESS_END_inONEX = FLAG_1,  """

    mNumSlaveActivateSwitch = 2
    """ SWITCH флаг SLAVE процесс активирован. Пример:
     /** SWITCH - SLAVE процесс активирован */
     ISSA_SLAVE_ACTIVATE_SWITCH = FLAG_2,  """

    mTypeList = [
        ["", ""],
        ["RESET_PROCESS_END_inONEX", "Входящий ONEX - Остановка процесса по внешней команде"],
        ["SLAVE_ACTIVATE_SWITCH", "SWITCH - SLAVE процесс активирован"]
    ]
    """ Список тегов и дескрипторов типовых мьютексов. Имя мьютекса предваряется
     именем процесса, строка определения заканчивается именем флага и запятой """

    mDict = {}
    """ Словарь содержит мьютексы, сгенерированные при обращениях к классу
     КЛЮЧ - имя процесса 
     ЗНАЧЕНИЕ - список списков содержит списки из двух значений: 
                имя мьютекса и дескриптор"""

    def __init__(self,
                 nameProcess="",
                 nameMutex="",
                 descriptor="",
                 typeMutexNum=0,
                 ):

        self.tagMutex = f"{nameProcess.upper()}_"
        """ Полное имя мьютекса в ENUM структуре в верхнем регистре """

        self.descriptor = ""

        if typeMutexNum > 0:
            # номер не 0 - формируем мьютекс из списка типовых мьютексов
            if typeMutexNum <= len(Mutex.mTypeList):
                # если номер не выходит за границы списка
                self.tagMutex += Mutex.mTypeList[typeMutexNum][0]
                self.descriptor += Mutex.mTypeList[typeMutexNum][1]
        else:
            # если типовой мьютекс не задан, генерим из входных значений
            self.tagMutex += nameMutex
            self.descriptor += descriptor

        # Добавляем мьютекс в словарь - ищем в словаре имя процесса
        if nameProcess in Mutex.mDict:
            # имя процесса есть в словаре - добавляем мьютекс в список
            thisList = Mutex.mDict[nameProcess]  # список в словаре
            thisList.append([self.tagMutex, self.descriptor])
            Mutex.mDict[nameProcess] = thisList
        else:
            # имени процесса нет в словаре, добавляем запись в словарь
            Mutex.mDict[nameProcess] = [[self.tagMutex, self.descriptor]]

