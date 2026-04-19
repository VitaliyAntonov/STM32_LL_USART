

class Gran:
    """ Класс Gran - описание гранулы процесса """

    def __init__(self,
                 name="",
                 descriptor="",
                 flagPauseNext=0,
                 flagCheckPauseEnd=0,
                 flagCheckEndInOnex=0,
                 ):
        # self.date = f"{date_day()}_{date_month()}_{date_year()}"

        self.name = name
        """ Имя гранулы процесса. При создании enum гранул к имени гранулы
         добавляется тег PROCESSnAME_GRAN_  - Пример: TEST_GRAN_IDLE """

        self.descriptor = descriptor
        """ Описание функционала гранулы. При генерации enum из этого поля
         формируется комментарий над тегом имени гранулы """

        self.flagPauseNext = flagPauseNext
        """ При наличии этого флага(flagPauseNext=1) в коде гранулы генерируется макрос
         pause_next_gran(processName, Pause, NextGran) """

        self.flagCheckPauseEnd = flagCheckPauseEnd
        """ При наличии этого флага в грануле генерируется макрос с условием
         if(check_pause_end(processName)){}"""

        self.flagCheckEndInOnex = flagCheckEndInOnex
        """ При наличии этого флага в грануле генерируется проверка наличия inONEX флага 
        name_RESET_PROCESS_END_inONEX и переход к грануле name_PROCESS_END """


