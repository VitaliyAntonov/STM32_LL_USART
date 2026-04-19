
from Gran import Gran
from Mutex import Mutex


def tab(n) -> str:
    """ Функция заполняет строку указанным количеством пробелов"""
    return " ".ljust(n)


class Process:
    """ Класс Process - описание процесса """

    def __init__(self,
                 name="",
                 descriptor="",
                 gGran=None,
                 mutex=None,
                 folderName="",
                 fModeMaster=0,
                 fModeSlave=0,
                 fModePeriodic=0,
                 slaveListIfMaster=None,
                 masterNameIfSlave=""
                 ):

        self.nameProcess = name
        """ Имя процесса в нижнем регистре(маленькие буквы)"""

        self.descriptorProcess = descriptor
        """ Комментарий - краткое описание процесса """

        self.gGran: [Gran] = gGran
        """ Список гранул процесса, упакованных в класс Gran """

        self.mutex: [Mutex] = mutex

        self.folderName: str = folderName
        """ Имя папки, в которой располагается процесс """

        self.valStruct: str = f"{self.nameProcess}_process_value"
        """ Имя структуры переменных процесса """

        self.fModeMaster: int = fModeMaster
        """ ФЛАГ. Режим работы процесса MASTER. Если = 1, то режим включен. """

        self.fModeSlave: int = fModeSlave
        """ ФЛАГ. Режим работы процесса SLAVE. Если = 1, то режим включен. """

        self.fModePeriodic: int = fModePeriodic
        """ ФЛАГ. Режим работы процесса PERIODIC. Если = 1, то режим включен. """

        self.genEndGran: int = 0
        """ ФЛАГ. Генерировать гранулу end_process. Если = 1, то гранула генерируется. """

        self.onExStartGran: int = 0
        """ ФЛАГ. Генерировать функции для внешней активации старта с указанных гранул.
         Если = 1, то добавляется список гранул, с которых стартует внешняя активация процесса."""

        # self.masterDefIfSlave: Process = Any
        self.masterDefIfSlave = None
        """ Вызывающий процесс для SLAVE процесса - экземпляр класса Process
        Для SLAVE процесса обозначается MASTER, если SLAVE режим включен """

        self.masterNameIfSlave = masterNameIfSlave
        """ Имя - Вызывающий процесс для SLAVE процесса """

        self.slaveListIfMaster: [str] = slaveListIfMaster
        """ Для MASTER процесса приводится список имён SLAVE процессов, если режим MASTER включен """

        self.periodicTimeout = 0
        """ Время паузы между обходами гранул процесса при периодическом режиме """

        self.onExStartGransList: [Gran] = None
        """ Список гранул, для которых генерируются функции внешней активации. 
        Для этих функций добавляется extern в файле мьютекс-ов"""

    def about(self):
        """ Функция выводит в печать поля класса Process """
        print("Процесс : ")
        print(f"{tab(4)}{self.nameProcess}_process : {self.descriptorProcess}")
        print("Гранулы процесса : ")
        # обход списка гранул - объектов класса Gran
        if self.gGran is not None:
            if len(self.gGran) > 0:
                for tGran in self.gGran:
                    print(f'{tab(4)}{tGran.name} : {tGran.descriptor}')
            else:
                print("ERROR: Пуст список гранул!")
        else:
            print(f"ERROR: Список гранул процесса {self.nameProcess}_process не задан!")

    def getGranName(self, num) -> str:
        return self.gGran[num].name



