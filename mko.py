from WDMTMKv2 import *

#  класс работы с МКО #
class TA1:
    def __init__(self):
        self.bus = BUS_1
        self.bus_state = 0
        self.TTml_obj = TTmkEventData()
        self.state = 1

    def init(self):
        self.state = TmkOpen()  # функция подключает драйвер к вызвавшему функцию процессу
        tmkdone(ALL_TMKS)
        tmkconfig(0)
        bcreset()
        bcgetstate()
        bcdefbase(1)
        bcgetbase()
        bcdefbus(self.bus)
        bcgetbus()
        tmkgethwver()
        return self.state

    read_status = 0x0000
    answer_word = 0xFFFF
    command_word = 0x0000

    def disconnect(self):
        close_status = TmkClose()
        return close_status

    def change_bus(self):
        if self.bus == BUS_2:
            self.bus = BUS_1
        else:
            self.bus = BUS_2
        bcdefbus(self.bus)

    def SendToRT(self, addr, subaddr, data, leng):
        self.bus_state = 0
        self.change_bus()
        if subaddr <= 0:
            subaddr = 1
        for i in range(36):
            bcputw(i, 0xFEFE)
        control_word = ((addr & 0x1F) << 11) + (0x00 << 10) + ((subaddr & 0x1F) << 5) + (leng & 0x1F)
        bcputw(0, control_word)
        for i in range(leng):
            bcputw(i+1, data[i])
        bcstart(1, DATA_BC_RT)
        self.command_word = bcgetw(0)
        self.answer_word = bcgetansw(DATA_BC_RT) & 0xFFFF
        if self.answer_word == 0xFEFE:
            self.bus_state = 1 if self.bus == BUS_1 else 2
            self.change_bus()
            bcputw(0, control_word)
            bcstart(1, DATA_BC_RT)
            self.command_word = bcgetw(0)
            self.answer_word = bcgetansw(DATA_BC_RT) & 0xFFFF  # bcgetw(1)
        if self.answer_word == 0xFEFE:
            self.state = 2
        return self.answer_word

    def ReadFromRT(self, addr, subaddr, leng):
        self.bus_state = 0
        self.change_bus()
        if subaddr <= 0:
            subaddr = 1
        for i in range(36):
            bcputw(i, 0xFEFE)
        control_word = ((addr & 0x1F) << 11) + (0x01 << 10) + ((subaddr & 0x1F) << 5) + (leng & 0x1F)
        bcputw(0, control_word)
        bcstart(1, DATA_RT_BC)
        self.command_word = bcgetw(0)
        self.answer_word = bcgetansw(DATA_RT_BC) & 0xFFFF  # bcgetw(1)
        if self.answer_word == 0xFEFE:
            self.bus_state = 1 if self.bus == BUS_1 else 2
            self.change_bus()
            bcputw(0, control_word)
            bcstart(1, DATA_RT_BC)
            self.command_word = bcgetw(0)
            self.answer_word = bcgetansw(DATA_RT_BC) & 0xFFFF  # bcgetw(1)
        if self.answer_word == 0xFEFE:
            self.state = 2
        frame = []
        for i in range(2, 2+leng):
            word = bcgetw(i)
            frame.append(word)
        return frame

    def Send_Cntrl_Comm(self, addr, subaddr, leng):
        self.bus_state = 0
        self.change_bus()
        control_word = ((addr & 0x1F) << 11) + (0x00 << 10) + ((subaddr & 0x1F) << 5) + (leng & 0x1F)
        bcputw(0, control_word)
        bcstart(1, CTRL_C_A)
        self.command_word = bcgetw(0)
        self.answer_word = bcgetansw(CTRL_C_A) & 0xFFFF
        if self.answer_word == 0xFEFE:
            self.state = 2
        return self.answer_word


# класс для разбора подпрограмм для создания циклограмм
# циклограмма согласно данному шаблону
# ["Name", [[Address, Subaddress, Wr/R, [Data], Data length, Start time, Finish time, Interval, Delay], [...], [...]]]
#    |          |          |        |      |         |          |           |          |         |
#    |          |          |        |      |         |          |           |          |         -- Задержка отправки
#    |          |          |        |      |         |          |           |          --- Интервал отправки
#    |          |          |        |      |         |          |           - Время остановки посылок
#    |          |          |        |      |         |          --- Время старта отправки от запуска программы
#    |          |          |        |      |         --- Длина данных для приема/отправки
#    |          |          |        |      ------------- Данные для отправки (при приеме не имеет значения)
#    |          |          |        -------------------- Отправка - "0", Прием - "1"
#    |          |          ----------------------------- Подадрес
#    |          ---------------------------------------- Адрес ОУ
#    --------------------------------------------------- Имя циклограммы
class PollingProgram:
    def __init__(self, program=[]):
        program_def = ["None", [0, 0, 0, [0], 0, 0, 0, 0.1, 0]]
        self.program = program if program else program_def
        self.name = self.program[0]
        self.cycle = []
        self.parcer()

    def parcer(self):
        for i in range(len(self.program[1])):
            start_time = self.program[1][i][5]
            stop_time = self.program[1][i][6]
            interval = self.program[1][i][7]
            delay = self.program[1][i][8]
            try:
                tr_number = int((stop_time - start_time)//interval)
            except ZeroDivisionError:
                tr_number = 1
            for j in range(tr_number):
                time = start_time + j*interval + delay
                addr = self.program[1][i][0]
                subaddr = self.program[1][i][1]
                direct = self.program[1][i][2]
                data = self.program[1][i][3]
                leng = self.program[1][i][4]
                data_set = [time, addr, subaddr, direct, data, leng]
                # print(data_set)
                self.cycle.append(data_set)
        self.cycle.sort()
        # print(self.cycle)
        pass

        pass

