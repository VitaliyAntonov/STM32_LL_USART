
from Process import Process
from CCode import tab, date, rn


class OneProcessCppGen:
    """ Класс генерирует код одного процесса для файлов проекта:
     - name_process.c - код процесса
     - name_process.h - заголовочный файл
     - mutex.h - файл объявлений мьютекс-ов

     Как входные данные о процессе используются данные класса Process
     """

    def __init__(self, process):

        self.prc: Process = process
        """ Загруженное описание процесса, в классе Process """

        self.uGrans: [str] = []
        """ Список полных имён гранул в верхнем регистре """

        self.cCode: str = ""
        """ Код файла name_process.c """

        self.hCode: str = ""
        """ Код файла name_process.h """

        self.mCode: str = ""
        """ Код процесса для файла mutex.h """

        self.uGransCreateList()  # формирует список полных имён гранул

        self.cFileCode()  # формируем файл name_process.c
        self.hFileCode()  # формируем файл name_process.h
        self.mFileCode()  # код для файла mutex.h

        self.codePrint()  # выводим в консоль

    """ -------------------------------------------------------------------------------- """

    def uGransCreateList(self):
        """ Функция формирует список полных имён гранул в верхнем регистре в переменной self.uGrans """
        for numGr in range(len(self.prc.gGran)):
            self.uGrans.append(f"{self.prc.nameProcess.upper()}_GRAN_{self.prc.gGran[numGr].name.upper()}")

    """ -------------------------------------------------------------------------------- """

    def cFileCode(self):
        """ Генерация кода для файла name_process.c """

        # верхний разделитель
        self.cCode += f"// {self.prc.nameProcess}_process.c  {'-'.rjust(70, '-')}"

        # "Шапка файла "
        self.cCode += f"\r\n/**  {self.prc.nameProcess}_process.c\r\n"
        self.cCode += f"{tab(2)}*  {self.prc.descriptorProcess}\r\n"
        self.cCode += f"{tab(2)}*  {date()}г.  Антонов В.Е.  kaligraf@yandex.ru */{rn(3)}"

        # include
        self.cCode += f'#include "{self.prc.nameProcess}_process.h" {rn(3)}'

        # проверка флага fModeMaster
        if self.prc.fModeMaster > 0:
            # extern-ы для процессов
            for nSprc in self.prc.slaveListIfMaster:
                self.cCode += f"extern void {nSprc}_process(void);\r\n"
            self.cCode += f"{rn(3)}"

        # Контроль процесса
        self.cCode += f"/** Контроль процесса {self.prc.nameProcess}_process() */\r\n"
        self.cCode += f"process_control  {self.prc.nameProcess}_pc = {{0,}};{rn(2)}"
        # Переменные процесса
        self.cCode += f"/** Переменные процесса {self.prc.nameProcess}_process() */\r\n"
        self.cCode += f"{self.prc.valStruct}  {self.prc.nameProcess}Val = {{0,}};{rn(2)}"
        # Переменная MUTEX флагов процесса
        self.cCode += f"/** Переменная для хранения MUTEX флагов процесса {self.prc.nameProcess}_process() */\r\n"
        self.cCode += f"mutex_value  {self.prc.nameProcess}Mutex = {{0}};{rn(3)}"

        # Объявление функции процесса
        self.cCode += f"/** {self.prc.descriptorProcess} */\r\n"
        self.cCode += f"void {self.prc.nameProcess}_process(void){{ {rn(2)}"

        to = 0

        # проверка флага fModeMaster
        if self.prc.fModeMaster > 0:

            to = 1

            # Проверка флага принудительного завершения процесса
            self.cCode += f"{tab(4)}if(check_onex({self.prc.nameProcess}, " \
                          f"{self.prc.nameProcess.upper()}_RESET_PROCESS_END_inONEX)){{\r\n"
            self.cCode += f"{tab(8)}reset_onex({self.prc.nameProcess}, " \
                          f"{self.prc.nameProcess.upper()}_RESET_PROCESS_END_inONEX);\r\n"

            # ЕСЛИ ЗАВЕРШЕНИЕ - поиск активного процесса и его принудительная остановка
            for nPr in range(len(self.prc.slaveListIfMaster)):
                self.cCode += f"{tab(8)}if(check_switch({self.prc.slaveListIfMaster[nPr]}, " \
                              f"{self.prc.slaveListIfMaster[nPr].upper()}_SLAVE_ACTIVATE_SWITCH)){{\r\n"
                self.cCode += f"{tab(12)}set_onex({self.prc.slaveListIfMaster[nPr]}, " \
                              f"{self.prc.slaveListIfMaster[nPr].upper()}_RESET_PROCESS_END_inONEX);\r\n"
                self.cCode += f"{tab(8)}}}\r\n"
            self.cCode += f"{tab(4)}}}{rn(2)}"

            # Вход в SLAVE процессы
            for nPr in range(len(self.prc.slaveListIfMaster)):
                if nPr < 1:
                    self.cCode += f"{tab(4)}if(check_switch({self.prc.slaveListIfMaster[nPr]}, " \
                                  f"{self.prc.slaveListIfMaster[nPr].upper()}_SLAVE_ACTIVATE_SWITCH)){{\r\n"
                else:
                    self.cCode += f"else if(check_switch({self.prc.slaveListIfMaster[nPr]}, " \
                     f"{self.prc.slaveListIfMaster[nPr].upper()}_SLAVE_ACTIVATE_SWITCH)){{\r\n"

                self.cCode += f"{tab(8)}{self.prc.slaveListIfMaster[nPr]}_process();\r\n"
                self.cCode += f"{tab(4)}}}"
                if nPr >= (len(self.prc.slaveListIfMaster) - 1):
                    self.cCode += f"else{{"
            self.cCode += f"{rn(2)}"

        # Обход и назначение гранул процесса
        for numGr in range(len(self.prc.gGran)):
            if numGr == 0:
                self.cCode += f"{tab(to*4+4)}__in_gran({self.prc.nameProcess}, {self.uGrans[numGr]}){rn(2)}"
            else:
                self.cCode += f"{tab(to*4+4)}__close_gran_in_gran({self.prc.nameProcess}, {self.uGrans[numGr]}){rn(2)}"

            # если установлен флаг flagPauseNext
            if self.prc.gGran[numGr].flagPauseNext > 0:
                self.cCode += f"{tab(to*4+8)}pause_next_gran({self.prc.nameProcess}, " \
                              f"20, {self.uGrans[numGr + 1]});{rn(2)}"

            # если установлен флаг flagCheckPauseEnd
            if self.prc.gGran[numGr].flagCheckPauseEnd > 0:
                self.cCode += f"{tab(to*4+8)}if(check_pause_end({self.prc.nameProcess})){{\r\n"
                self.cCode += f"{tab(to*4+12)}next_gran_no_block({self.prc.nameProcess}, {self.uGrans[numGr + 1]});\r\n"
                self.cCode += f"{tab(to*4+8)}}}{rn(1)}"

            # если установлен флаг flagCheckEndInOnex
            if self.prc.gGran[numGr].flagCheckEndInOnex > 0:
                self.cCode += f"{tab(to*4+8)}if(check_onex({self.prc.nameProcess}, {self.prc.nameProcess.upper()}" \
                              f"_RESET_PROCESS_END_inONEX)){{\r\n"
                self.cCode += f"{tab(to*4+12)}reset_onex({self.prc.nameProcess}, {self.prc.nameProcess.upper()}" \
                              f"_RESET_PROCESS_END_inONEX);\r\n"
                self.cCode += f"{tab(to*4+12)}next_gran_no_block({self.prc.nameProcess}, {self.uGrans[numGr + 1]});\r\n"
                self.cCode += f"{tab(to*4+8)}}}{rn(2)}"

            # для гранулы завершения процесса
            if self.prc.gGran[numGr].name == "end_process":
                # в режиме mode SLAVE
                if self.prc.fModeSlave > 0:
                    self.cCode += f"{tab(to*4+8)}reset_switch({self.prc.nameProcess}, {self.prc.nameProcess.upper()}" \
                                  f"_SLAVE_ACTIVATE_SWITCH);\r\n"
                    self.cCode += f"{tab(to*4+8)}next_gran({self.prc.nameProcess}, {self.uGrans[0]});{rn(2)}"

        # Макрос завершения процесса
        self.cCode += f"""{tab(to*4+4)}__end_gran_end_process({self.prc.nameProcess})\r\n"""

        # проверка флага fModeMaster
        if self.prc.fModeMaster > 0:
            self.cCode += f"\r\n{tab(4)}}}\r\n"

        self.cCode += f"}}{rn(2)}"

        # нижний разделитель
        self.cCode += f"// END: {self.prc.nameProcess}_process.c  {'-'.rjust(65, '-')}{rn(2)}"

    """ -------------------------------------------------------------------------------- """

    def hFileCode(self):
        """ Генерация кода для файла name_process.h """

        # верхний разделитель
        self.hCode += f"// {self.prc.nameProcess}_process.h  {'-'.rjust(70, '-')}"

        # "Шапка файла "
        self.hCode += f"\r\n/**  {self.prc.nameProcess}_process.h\r\n"
        self.hCode += f"{tab(2)}*  {self.prc.descriptorProcess}\r\n"
        self.hCode += f"{tab(2)}*  {date()}г.  Антонов В.Е.  kaligraf@yandex.ru */{rn(3)}"

        # define для исключения дублирования .h файла
        self.hCode += f"#ifndef  GENERATE_{self.prc.nameProcess.upper()}_PROCESS_H\r\n"
        self.hCode += f"#define  GENERATE_{self.prc.nameProcess.upper()}_PROCESS_H{rn(3)}"

        # include-s
        self.hCode += f'#include "../../Inc/main.h"\r\n'
        self.hCode += f'#include "../process/process_control.h"\r\n'
        self.hCode += f'#include "../process/mutex.h"{rn(3)}'

        # переменные процесса
        self.hCode += f'/** Переменные процесса {self.prc.nameProcess}_process() */\r\n'
        self.hCode += f'typedef struct{{{rn(2)}'
        self.hCode += f'{tab(4)}/** Копия системного таймера для задания паузы */\r\n'
        self.hCode += f'{tab(4)}uint32_t    sysTickFix;{rn(2)}'
        self.hCode += f'{tab(4)}/** Пауза - миллисекунд */\r\n'
        self.hCode += f'{tab(4)}uint32_t    pause;{rn(2)}'
        self.hCode += f'{tab(4)}/** Флаги процесса */\r\n'
        self.hCode += f'{tab(4)}uint32_t    flags;{rn(2)}'
        self.hCode += f'}}{self.prc.nameProcess}_process_value;{rn(3)}'

        # enum гранул процесса
        self.hCode += f'typedef enum{{{rn(2)}'
        for numGr in range(len(self.prc.gGran)):
            # если есть комментарий к грануле
            if len(self.prc.gGran[numGr].descriptor) > 0:
                self.hCode += f'{tab(4)}/** {self.prc.gGran[numGr].descriptor} */\r\n'
            # Полное имя гранулы в верхнем регистре
            self.hCode += f'{tab(4)}{self.uGrans[numGr]},{rn(2)}'
        # завершающая строка enum
        self.hCode += f'}}{self.prc.nameProcess}_process_grans;{rn(2)}'

        # define для исключения дублирования .h файла завершение
        self.hCode += f"{rn(3)}#endif  //  #ifndef   GENERATE_{self.prc.nameProcess.upper()}_PROCESS_H{rn(2)}"
        # нижний разделитель
        self.hCode += f"// END: {self.prc.nameProcess}_process.h  {'-'.rjust(65, '-')}{rn(2)}"

    """ -------------------------------------------------------------------------------- """

    def mFileCode(self):
        """ Код процесса для файла mutex.h """
        # верхний разделитель
        self.mCode += f"// {self.prc.nameProcess} for mutex.h  {'-'.rjust(68, '-')}\r\n"

        # enum определения мьютекс-ов
        self.mCode += f"typedef enum {self.prc.nameProcess.upper()}_mutex{{\r\n"
        self.mCode += f"{tab(4)}/** Входящий ONEX - Остановка процесса по внешней команде */\r\n"
        self.mCode += f"{tab(4)}{self.prc.nameProcess.upper()}_RESET_PROCESS_END_inONEX = FLAG_1,\r\n"

        # проверка флага fModeSlave
        if self.prc.fModeSlave > 0:
            self.mCode += f"{tab(4)}/** SWITCH - SLAVE процесс активирован */\r\n"
            self.mCode += f"{tab(4)}{self.prc.nameProcess.upper()}_SLAVE_ACTIVATE_SWITCH = FLAG_2,\r\n"

        self.mCode += f"}}{self.prc.nameProcess.upper()}_mutex;\r\n"

        self.mCode += f"extern mutex_value {self.prc.nameProcess}Mutex;\r\n"
        # нижний разделитель
        self.mCode += f"// END: {self.prc.nameProcess} for mutex.h  {'-'.rjust(63, '-')}{rn(2)}"

    """ -------------------------------------------------------------------------------- """

    """ -------------------------------------------------------------------------------- """

    def codePrint(self):
        pass
        # print(self.cCode)
        # print(self.hCode)
        # print(self.mCode)

    """ -------------------------------------------------------------------------------- """



