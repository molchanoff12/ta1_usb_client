'''
    модуль собирающий в себе стандартизованные функции разбора данных
    Стандарт:
    параметры:
        frame - в виде листа с данными
    возвращает:
        table_list - список подсписков (подсписок - ["Имя", "Значение"])
'''

import crc16


def frame_parcer(frame):
    data = []
    if frame[0] == 0x0FF1:  # проверка на метку кадра
        if frame[1] == 0x0C61:  # Системный кадр
            #
            data.append(["Метка кадра", "0x%04X" % frame[0]])
            data.append(["Определитель", "0x%04X" % frame[1]])
            data.append(["Номер кадра, шт", "%d" % frame[2]])
            data.append(["Время кадра, с", "%d" % ((frame[3] << 16) + frame[4])])
            #
            data.append(["Ток 1, мА", "%d" % frame[5]])
            data.append(["Ток 2, мА", "%d" % frame[6]])
            data.append(["Ток 3, мА", "%d" % frame[7]])
            data.append(["Ток 4, мА", "%d" % frame[8]])
            data.append(["Указатель чтения", "%d" % frame[9]])
            data.append(["Указатель записи", "%d" % frame[10]])
            data.append(["Ошибки МКО", "%d" % frame[11]])
            data.append(["Счетчик включений", "%d" % ((frame[12] >> 8) & 0xFF)])
            data.append(["Рабочий комплект", "%d" % (frame[12] & 0xFF)])
            data.append(["Разность времени", "%d" % frame[13]])
            data.append(["Ошибки ВШ", "%d" % ((frame[14] >> 8) & 0xFF)])
            data.append(["Неответы ВШ", "%d" % (frame[14] & 0xFF)])
            data.append(["Статус ВШ", "0х%02X" % frame[15]])
            data.append(["Температура", "%d" % frame[16]])
            #
            data.append(["CRC-16", "0x%04X" % crc16.calc(frame, 32)])
            pass
        elif frame[1] == 0x0C62 or frame[1] == 0x0C63 or frame[1] == 0x0C64:  # МПП1-2 или МПП3-4 или МПП5-6
            # подготовка
            if frame[1] == 0x0C62:
                mpp_num_1, a_1, b_1 = 1, 1.0, 0.0
                mpp_num_2, a_2, b_2 = 2, 1.0, 0.0
            elif frame[1] == 0x0C63:
                mpp_num_1, a_1, b_1 = 3, 1.0, 0.0
                mpp_num_2, a_2, b_2 = 4, 1.0, 0.0
            elif frame[1] == 0x0C64:
                mpp_num_1, a_1, b_1 = 5, 1.0, 0.0
                mpp_num_2, a_2, b_2 = 6, 1.0, 0.0
            else:
                mpp_num_1, a_1, b_1 = 5, 1.0, 0.0
                mpp_num_2, a_2, b_2 = 6, 1.0, 0.0
            #
            data.append(["Метка кадра", "0x%04X" % frame[0]])
            data.append(["Определитель", "0x%04X" % frame[1]])
            data.append(["Номер кадра, шт", "%d" % frame[2]])
            data.append(["Время кадра, с", "%d" % ((frame[3] << 16) + frame[4])])
            #
            data.append(["МПП", "%d" % mpp_num_1])
            data.append(["Кол-во оставшихся измерений, шт", "%d" % frame[5]])
            data.append(["Время регистрации, с", "%d" % ((frame[6] << 16) + frame[7])])
            data.append(["Время регистрации, мкс", "%d" % ((frame[8] << 16) + frame[9])])
            data.append(["Длительность импульса, с", "%.3g" % (((frame[10] << 16) + frame[11])*(10**-6)/40)])
            data.append(["Число переходов через 0, шт", "%d" % frame[12]])
            data.append(["Пиковое значение, кВ", "%.3g" % (a_1 * frame[13])])
            data.append(["Мощность импульса, кВ*с", "%.3g" % (a_1*((frame[14] << 16) + frame[15])*(10**-6)/40)])
            data.append(["Среднее, кВ", "%.3g" % (a_1 * frame[16] + b_1)])
            data.append(["Шум, кВ", "%.3g" % (a_1 * frame[17])])
            #
            data.append(["МПП", "%d" % mpp_num_2])
            data.append(["Кол-во оставшихся измерений, шт", "%d" % frame[18]])
            data.append(["Время регистрации, с", "%d" % ((frame[19] << 16) + frame[20])])
            data.append(["Время регистрации, мкс", "%d" % ((frame[21] << 16) + frame[22])])
            data.append(["Длительность импульса, с", "%.3g" % (((frame[23] << 16) + frame[24])*(10**-6)/40)])
            data.append(["Число переходов через 0, шт", "%d" % frame[25]])
            data.append(["Пиковое значение, кВ", "%.3g" % (a_2 * frame[26])])
            data.append(["Мощность импульса, кВ*с", "%.3g" % (a_2*((frame[27] << 16) + frame[28])*(10**-6)/40)])
            data.append(["Среднее, кВ", "%.3g" % (a_2 * frame[29] + b_2)])
            data.append(["Шум, кВ", "%.3g" % (a_2 * frame[30])])
            #
            data.append(["CRC-16", "0x%04X" % crc16.calc(frame, 32)])
            pass
        elif frame[1] == 0x0C65:  # ДЭП
            pass
        elif frame[1] == 0x0C66:  # БДЭП
            pass
        elif frame[1] == 0x0C67:  # Помеховые матрица
            pass
        else:
            data.append(["Неизвестный определитель", "0"])

    else:
        data.append(["Данные не распознаны", "0"])
    return data
