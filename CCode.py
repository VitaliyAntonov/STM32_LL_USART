
from Gran import Gran
from Mutex import Mutex
from Process import Process
import datetime


def tab(n) -> str:
    """ Функция заполняет строку указанным количеством пробелов"""
    return " ".ljust(n)


def rn(n) -> str:
    """ Функция создаёт указанное количество пустых строк """
    return "\r\n" * n


def date() -> str:
    """ Функция формирует текущую дату """
    # {datetime.date.today().day}.{datetime.date.today().month}.{datetime.date.today().year}
    day = str(datetime.date.today().day)
    if len(day) < 2:
        day = f"0{day}"
    month = str(datetime.date.today().month)
    if len(month) < 2:
        month = f"0{month}"
    year = str(datetime.date.today().year)
    return f"{day}.{month}.{year}"


def date_day() -> str:
    day = str(datetime.date.today().day)
    if len(day) < 2:
        day = f"0{day}"
    return day


def date_month() -> str:
    month = str(datetime.date.today().month)
    if len(month) < 2:
        month = f"0{month}"
    return month


def date_year() -> str:
    return str(datetime.date.today().month)


class CCode:
    """ Код для отдельных частей реализации процесса """

    def __init__(self, prc: Process):

        self.prc: Process = prc
        """ Описание процесса в классе Process """

        self.uGransCreateList()
        """ Создаём список полных имён гранул процесса в верхнем регистре """

        self.uGrans: [str] = []
        """ Список полных имён гранул в верхнем регистре """

        self.up_gelimiter_c: str = f"// {prc.nameProcess}_process.c  {'-'.rjust(70, '-')}\r\n"
        """ Верхний разделитель для файла name_process.c """

        self.file_up_header: str = f"\r\n/**  {prc.nameProcess}_process.c\r\n" \
                                   f"{tab(2)}*  {prc.descriptorProcess}\r\n" \
                                   f"{tab(2)}*  {date()}г.  Антонов В.Е.  kaligraf@yandex.ru */{rn(3)}"
        """ Шапка файлов name_process.c и name_process.h """

        self.cInclude: str = f'#include "{prc.nameProcess}_process.h" {rn(3)}'
        """ инструкция #include для файла name_process.c """

        self.externSlave = ""
        """ Инструкции extern вызываемых SLAVE процессов в процессе МАСТЕР """
        for nSprc in prc.slaveListIfMaster:
            self.externSlave += f"extern void {nSprc}_process(void);\r\n"
        self.externSlave += f"{rn(3)}"

        self.processControl = ""
        """ Назначение структуры переменных Контроль процесса"""
        self.processControl += f"/** Контроль процесса {prc.nameProcess}_process() */\r\n"
        self.processControl += f"process_control  {prc.nameProcess}_pc = {{0,}};{rn(2)}"

        self.processValue = ""
        """ Назначение переменных процесса(структура)"""
        self.processValue += f"/** Переменные процесса {prc.nameProcess}_process() */\r\n"
        self.processValue += f"{prc.valStruct}  {prc.nameProcess}Val = {{0,}};{rn(2)}"

        self.processMutex = ""
        """ Переменная MUTEX флагов процесса """
        self.processMutex += f"/** Переменная для хранения MUTEX флагов процесса {prc.nameProcess}_process() */\r\n"
        self.processMutex += f"mutex_value  {prc.nameProcess}Mutex = {{0}};{rn(3)}"

        self.processCreate = ""
        """  Объявление функции процесса  """
        self.processCreate += f"/** {prc.descriptorProcess} */\r\n"
        self.processCreate += f"void {prc.nameProcess}_process(void){{ {rn(2)}"

        self.checkEndOnex = ""
        """ Проверка флага принудительного завершения процесса """
        self.checkEndOnex += f"{tab(4)}if(check_onex({prc.nameProcess}, " \
                             f"{prc.nameProcess.upper()}_RESET_PROCESS_END_inONEX)){{\r\n"
        self.checkEndOnex += f"{tab(8)}reset_onex({prc.nameProcess}, " \
                             f"{prc.nameProcess.upper()}_RESET_PROCESS_END_inONEX));\r\n"

        self.ifOnexStop = ""
        """ ЕСЛИ ЗАВЕРШЕНИЕ - поиск активного процесса и его принудительная остановка """
        for nPr in range(len(prc.slaveListIfMaster)):
            self.ifOnexStop += f"{tab(8)}if(check_switch({prc.slaveListIfMaster[nPr]}, " \
                               f"{prc.slaveListIfMaster[nPr].upper()}_SLAVE_ACTIVATE_SWITCH)){{\r\n"
            self.ifOnexStop += f"{tab(12)}set_onex({prc.slaveListIfMaster[nPr]}, " \
                               f"{prc.slaveListIfMaster[nPr].upper()}_RESET_PROCESS_END_inONEX));\r\n"
            self.ifOnexStop += f"{tab(8)}}}\r\n"
        self.ifOnexStop += f"{tab(4)}}}{rn(2)}"

        self.inSlaveProcess = ""
        """ Вход в SLAVE процессы """
        for nPr in range(len(prc.slaveListIfMaster)):
            if nPr < 1:
                self.inSlaveProcess += f"{tab(4)}if(check_switch({prc.slaveListIfMaster[nPr]}, " \
                                       f"{prc.slaveListIfMaster[nPr].upper()}_SLAVE_ACTIVATE_SWITCH)){{\r\n"
            else:
                self.inSlaveProcess += f"else if(check_switch({prc.slaveListIfMaster[nPr]}, " \
                                       f"{prc.slaveListIfMaster[nPr].upper()}_SLAVE_ACTIVATE_SWITCH)){{\r\n"

            self.inSlaveProcess += f"{tab(8)}{prc.slaveListIfMaster[nPr]}_process();\r\n"
            self.inSlaveProcess += f"{tab(4)}}}"
            if nPr >= (len(prc.slaveListIfMaster) - 1):
                self.inSlaveProcess += f"else{{"
        self.inSlaveProcess += f"{rn(2)}"

        self.processGranulesCode = ""
        """ Обход и назначение гранул процесса """
        for numGr in range(len(prc.gGran)):
            if numGr == 0:
                self.processGranulesCode += f"{tab(8)}__in_gran({prc.nameProcess}, {self.uGrans[numGr]}){rn(2)}"
            else:
                self.processGranulesCode += f"{tab(8)}__close_gran_in_gran({prc.nameProcess}, {self.uGrans[numGr]}){rn(2)}"

            # если установлен флаг flagPauseNext
            if prc.gGran[numGr].flagPauseNext > 0:
                self.processGranulesCode += f"{tab(12)}pause_next_gran({prc.nameProcess}, " \
                                            f"20, {self.uGrans[numGr + 1]});{rn(2)}"

            # если установлен флаг flagCheckPauseEnd
            if prc.gGran[numGr].flagCheckPauseEnd > 0:
                self.processGranulesCode += f"{tab(12)}if(check_pause_end({prc.nameProcess})){{\r\n"
                self.processGranulesCode += f"{tab(16)}next_gran_no_block({prc.nameProcess}, {self.uGrans[numGr + 1]});\r\n"
                self.processGranulesCode += f"{tab(12)}}}{rn(1)}"

            # если установлен флаг flagCheckEndInOnex
            if prc.gGran[numGr].flagCheckEndInOnex > 0:
                self.processGranulesCode += f"{tab(12)}if(check_onex({prc.nameProcess}, {prc.nameProcess.upper()}" \
                                            f"_RESET_PROCESS_END_inONEX)){{\r\n"
                self.processGranulesCode += f"{tab(16)}reset_onex({prc.nameProcess}, {prc.nameProcess.upper()}" \
                                            f"_RESET_PROCESS_END_inONEX);\r\n"
                self.processGranulesCode += f"{tab(16)}next_gran_no_block({prc.nameProcess}, {self.uGrans[numGr + 1]});\r\n"
                self.processGranulesCode += f"{tab(12)}}}{rn(2)}"

            # для гранулы завершения процесса
            if prc.gGran[numGr].name == "end_process":
                # в режиме mode SLAVE
                if prc.fModeSlave > 0:
                    self.processGranulesCode += f"{tab(12)}reset_switch({prc.nameProcess}, {prc.nameProcess.upper()}" \
                                                f"_SLAVE_ACTIVATE_SWITCH);\r\n"
                    self.processGranulesCode += f"{tab(12)}next_gran({prc.nameProcess}, {self.uGrans[0]});{rn(2)}"

        # Макрос завершения процесса
        self.processGranulesCode += f"""{tab(8)}__end_gran_end_process({self.prc.nameProcess}){rn(2)}"""
        self.processGranulesCode += f"{tab(4)}}}\r\n}}{rn(2)}"

        # нижний разделитель
        self.processGranulesCode += f"// END: {self.prc.nameProcess}_process.c  {'-'.rjust(65, '-')}{rn(2)}"

    def uGransCreateList(self):
        """ Функция формирует список полных имён гранул в верхнем регистре в переменной self.uGrans """
        for numGr in range(len(self.prc.gGran)):
            self.uGrans.append(f"{self.prc.nameProcess.upper()}_GRAN_{self.prc.gGran[numGr].name.upper()}")






