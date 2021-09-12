import datetime


def get_medinfo(words_list):
    num_dict = {
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
        'six': 6,
        'seven': 7,
        'eight': 8,
        'nine': 9,
        'ten': 10
    }
    
    def get_medname(words_list):
        list_rx = ['RX', 'rx', 'RX#', 'rx#', 'RX:', 'rx:']
        if 'MG' in words_list or 'mg' in words_list:
            index = words_list.index('MG' or 'mg')
            str_name = ' '.join(words_list[index-3:index])
            return str_name
        elif any(item in list_rx for item in words_list):
            index = words_list.index(item)
            str_name = ' '.join(words_list[index:index+1])
            return str_name
        else:
            return 'medicine name not found'

    def get_times(words_list):
        if 'times' in words_list:
            index = words_list.index('times') - 1
            str_times = words_list[index]
            if len(str_times) > 2:
                num_times = num_dict.get(str_times)
            else:
                num_times = int(str_times)
        elif 'once' in words_list:
            num_times = 1
        elif 'twice' in words_list:
            num_times = 2
        elif 'every' in words_list:
            if words_list[words_list.index('every') + 1] == 'day':
                num_times = 1
            elif 'hours' in words_list:
                str_times = words_list[words_list.index('hours') - 1]
                if len(str_times) > 2:
                    nums = str_times.split("-")
                    avg = (int(nums[0]) + int(nums[1])) / 2
                    num_times = int(14/avg)
                else:
                    num_times = int(14 / int(str_times))
            else:
                num_times = 1
        else:
            num_times = 1

        if num_times == 1:
            if 'morning' in words_list:
                return [9]
            elif 'night' in words_list:
                return [21]
            else:
                return [12]
        elif num_times == 2:
            return [12, 18]
        elif num_times == 3:
            return [9, 12, 18]
        elif num_times == 4:
            return [9, 12, 18, 21]
        else:
            return None

    def get_freq(words_list):
        days_list = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

        if 'daily' in words_list:
            return 1
        elif 'day' in words_list and words_list[words_list.index('day') - 1] == 'a':
            return 1
        elif 'every' in words_list:
            if words_list[words_list.index('every') + 1] == 'day':
                return 1
            elif 'days' in words_list:
                str_days = words_list[words_list.index('days') - 1]
                if len(str_days) > 2:
                    return num_dict.get(str_days)
                else:
                    return int(str_days)
            elif 'week' in words_list:
                return 7
            elif 'weeks' in words_list:
                str_weeks = words_list[words_list.index('weeks') - 1]
                if len(str_weeks) > 2:
                    return num_dict.get(str_weeks)
                else:
                    return int(str_weeks)
            else:
                return 1
        else:
            return 1

    med_name = get_medname(words_list)
    med_freq = get_freq(words_list)
    med_times = get_times(words_list)
    med_reminder = {
        "Name": med_name,
        "Frequency": med_freq,
        "Times": [i for i in med_times]
    }

    return med_reminder


# words_list1 = ['Take', 'one', 'capsule', 'by', 'mouth', 'three', 'times', 'daily']
# words_list2 = ['Take', 'one', 'tablet', 'orally', '2', 'times', 'a', 'day']
# words_list3 = ['Take', 'two', 'pills', 'once', 'a', 'day', 'in', 'the', 'morning']
# words_list4 = ['Take', 'pills', 'every', 'day']
# words_list5 = ['Take', 'pills', 'every', '4-6', 'hours']
# words_list6 = ['Take', 'pills', 'every', '3', 'days']
#
#
# med_reminder1 = get_medinfo(words_list1)
# med_reminder2 = get_medinfo(words_list2)
# med_reminder3 = get_medinfo(words_list3)
# med_reminder4 = get_medinfo(words_list4)
# med_reminder5 = get_medinfo(words_list5)
# med_reminder6 = get_medinfo(words_list6)
#
#
# print(med_reminder1)
# print(med_reminder2)
# print(med_reminder3)
# print(med_reminder4)
# print(med_reminder5)
# print(med_reminder6)







