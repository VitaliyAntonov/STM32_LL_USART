
from Process import Process
from Gran import Gran
from Mutex import Mutex
from CCode import tab

from OneProcessCppGen import OneProcessCppGen
import os


class CustModBus:
    """ Класс представляет собой список процессов. - ПРИМЕР реализации
    Класс генерирует куст из процесса МАСТЕР и SLAVE процессов,
     реализующих обработку команд, полученных по интерфейсу связи(например UART),
     по заданному протоколу. Файлы процессов создаются в указанной директории. """

    filePath = "/home/vitaliy/SoftWork/Obsidian/Develop/AAA_Automatic_programming" \
               "/ap_tutorial_0/Core/Src/genTest"
    """ Папка для сохранения файлов процессов """

    pathFileMutex = "/home/vitaliy/SoftWork/Obsidian/Develop/AAA_Automatic_programming/" \
                    "ap_tutorial_0/Core/Src/process/mutex.h"
    """ Путь к файлу mutex.h проекта """

    tprc = Process(
        name="tprc",
        descriptor="Тестовый процесс для проверки генератора кода",
        fModeMaster=1,
        slaveListIfMaster=["hand", "issa", "trzk"],
        gGran=[
            Gran("idle", "Процесс неактивен"),
            Gran("preference_port", "Настройка тестового порта"),
            Gran("read_port_value", "Чтение состояния порта"),
            Gran("pack_read_result_transmit", "Передача прочитанного значения по UART", flagPauseNext=1),
            Gran("timeout_wait_end_cmd_wait",
                 "Ожидание таймаута, либо команды окончания процесса",
                 flagCheckPauseEnd=1,
                 flagCheckEndInOnex=0),
            Gran("end_process", "Окончание процесса")
        ],
        mutex=[
            Mutex(typeMutexNum=Mutex.mNumEndResetProcess),
        ]
    )

    hand = Process(
        name="hand",
        descriptor="SLAVE_0 процесс для проверки генератора кода",
        fModeSlave=1,
        masterNameIfSlave="tprc",
        gGran=[
            Gran("idle", "Процесс неактивен"),
            Gran("preference_port", "Настройка тестового порта"),
            Gran("read_port_value", "Чтение состояния порта"),
            Gran("pack_read_result_transmit", "Передача прочитанного значения по UART", flagPauseNext=1),
            Gran("timeout_wait_end_cmd_wait",
                 "Ожидание таймаута, либо команды окончания процесса",
                 flagCheckPauseEnd=1,
                 flagCheckEndInOnex=1),
            Gran("end_process", "Окончание процесса")
        ],
        mutex=[
            Mutex(typeMutexNum=Mutex.mNumSlaveActivateSwitch),
            Mutex(typeMutexNum=Mutex.mNumEndResetProcess),
        ]
    )

    issa = Process(
        name="issa",
        descriptor="SLAVE_1 процесс для проверки генератора кода",
        fModeSlave=1,
        masterNameIfSlave="tprc",
        gGran=[
            Gran("idle", "Процесс неактивен"),
            Gran("preference_port", "Настройка тестового порта"),
            Gran("read_port_value", "Чтение состояния порта"),
            Gran("pack_read_result_transmit", "Передача прочитанного значения по UART", flagPauseNext=1),
            Gran("timeout_wait_end_cmd_wait",
                 "Ожидание таймаута, либо команды окончания процесса",
                 flagCheckPauseEnd=1,
                 flagCheckEndInOnex=1),
            Gran("end_process", "Окончание процесса")
        ],
        mutex=[
            Mutex(typeMutexNum=Mutex.mNumSlaveActivateSwitch),
            Mutex(typeMutexNum=Mutex.mNumEndResetProcess),
        ]
    )

    trzk = Process(
        name="trzk",
        descriptor="SLAVE_2 процесс для проверки генератора кода",
        fModeSlave=1,
        masterNameIfSlave="tprc",
        gGran=[
            Gran("idle", "Процесс неактивен"),
            Gran("preference_port", "Настройка тестового порта"),
            Gran("read_port_value", "Чтение состояния порта"),
            Gran("pack_read_result_transmit", "Передача прочитанного значения по UART", flagPauseNext=1),
            Gran("timeout_wait_end_cmd_wait",
                 "Ожидание таймаута, либо команды окончания процесса",
                 flagCheckPauseEnd=1,
                 flagCheckEndInOnex=1),
            Gran("end_process", "Окончание процесса")
        ],
        mutex=[
            Mutex(typeMutexNum=Mutex.mNumSlaveActivateSwitch),
            Mutex(typeMutexNum=Mutex.mNumEndResetProcess),
        ]
    )

    prcList: [Process] = [tprc, hand, issa, trzk]
    """ Список всех процессов куста """


def writeToMutexFile(mutexPath, forMutex):
    """ Функция добавляет в конец файла mutex.h часть кода из переменной forMutex """

    """ Чтение файла в массив строк """
    fileRows: [str] = []  # список для чтения
    with open(mutexPath, 'r', encoding='utf-8') as f:
        for line in f:
            # Файл, читается построчно в список строк
            fileRows.append(line)
    f.close()  # закрываем файл

    # Поиск строки с тегом #endif в конце файла
    fTag = "#endif"  # тег для поиска
    # Обход строк текущего файла
    lastRow = len(fileRows)  # номер последней строки в списке строк
    numStr = 0
    for k in range(len(fileRows)):
        index = fileRows[k].find(fTag)
        if index >= 0:
            numStr = k
            """ ПОСЛЕДНЯЯ Искомая последовательность обнаружена """

    # Объединение строк файла
    newFile = ""
    for k in range(numStr):
        newFile += fileRows[k]
    # добавляем вставку в файл с новыми мьютексами
    newFile += forMutex
    # завершающая часть файла
    for k in range(numStr, lastRow):
        newFile += fileRows[k]

    # print(newFile)

    with open(mutexPath, 'w') as file_h:
        file_h.write(newFile)  # перезаписываем файл


def genCustFiles(filePath, prcList):
    """  Обход списка процессов и запись файлов на диск в указанную директорию """

    forMutexFile = ""

    for prc in prcList:
        thisPrc = OneProcessCppGen(prc)

        forMutexFile += thisPrc.mCode
        # print(this.cCode)

        # Если указана директория, записываем файлы в неё
        if len(filePath) > 0:
            if os.path.exists(filePath):  # путь существует
                if os.path.isdir(filePath):  # это папка

                    cFileDir = filePath + "/" + thisPrc.prc.nameProcess + "_process.c"

                    # Пытаемся открыть .c файл для чтения и записи, создаем файл, если он не существует
                    try:
                        file_c = open(cFileDir, 'r+')
                    except IOError:
                        file_c = open(cFileDir, 'w+')
                    file_c.close()  # закрываем файл
                    with open(cFileDir, 'w') as file_c:
                        file_c.write(thisPrc.cCode)  # перезаписываем файл

                    hFileDir = filePath + "/" + prc.nameProcess + "_process.h"

                    # Пытаемся открыть .h файл для чтения и записи, создаем файл, если он не существует
                    try:
                        file_h = open(hFileDir, 'r+')
                    except IOError:
                        file_h = open(hFileDir, 'w+')
                    file_h.close()  # закрываем файл
                    with open(hFileDir, 'w') as file_h:
                        file_h.write(thisPrc.hCode)  # перезаписываем файл

        # От повторного включения.
        # Поиск в файле мьютексов кода для данного процесса

    writeToMutexFile(CustModBus.pathFileMutex, forMutexFile)


if __name__ == '__main__':

    print(CustModBus.filePath)
    genCustFiles(CustModBus.filePath, CustModBus.prcList)

