import os.path

from typing import Union


LOG_FILE = '/app_2.log'
HANDLER = 'BIG'


class LogParser:

    def __init__(self, path_to_file: str, handler: str) -> None:
        self.path_to_file = path_to_file
        self.handler = handler
        self.serviceable_statuses = []
        self.faulty_statuses = []
        self.true_sensors = set()
        self.false_sensors = set()

    def sensor_data(self, line: str) -> Union[tuple, None]:
        """
        Take sensor data from the log line
        :param line: log line from the file
        :return: None or tuple with data
        """
        line_list = line.split('- > ')
        if len(line_list) > 1:
            data = line_list[1].replace("'", "").strip()
            if self.handler in data:
                return tuple(data.split(';'))
        return None

    def analysis_file(self) -> None:
        """
        Open log file add data to the class object
        :return: None
        """
        with open(self.path_to_file, 'r') as log:
            for line in log:
                sensor_info = self.sensor_data(line)
                if sensor_info is None:
                    continue
                state = sensor_info[-2]
                name = sensor_info[2]
                if state == '02':
                    self.serviceable_statuses.append(sensor_info)
                    self.true_sensors.add(name)
                elif state == 'DD':
                    self.faulty_statuses.append(sensor_info)
                    self.false_sensors.add(name)
                if name in self.true_sensors and name in self.false_sensors:
                    self.true_sensors.remove(name)

    def number_of_serviceable_sensors(self) -> int:
        """
        Print the number of successful entries
        :return: integer
        """
        return len(self.serviceable_statuses)

    def number_of_faulty_sensors(self) -> int:
        """
        Print the number of faulty entries
        :return: integer
        """
        return len(self.faulty_statuses)

    def print_statistics(self) -> None:
        """
        Print statistic from log file to the console
        :return: None
        """
        counter_dict = dict()
        underscore = '_' * 10
        print(underscore + f'Failed test {len(self.false_sensors)} devices' + underscore)
        for dev1 in self.false_sensors:
            print(f'Device {dev1} was removed')
        print(underscore + f'Success test {len(self.true_sensors)} devices' + underscore)
        for dev2 in self.serviceable_statuses:
            name = dev2[2]
            if name not in self.true_sensors:
                continue
            if name in counter_dict:
                counter_dict[name] += 1
            else:
                counter_dict[name] = 1
        for key, value in counter_dict.items():
            print(f'Device {key} sent {value} statuses')


def main():
    """
    Start the process of parsing the log file
    """
    dir_path = os.path.abspath(os.path.dirname(__file__))
    parser = LogParser(dir_path + LOG_FILE, HANDLER)
    parser.analysis_file()
    print('OK status: ', parser.number_of_serviceable_sensors())
    print('Fail status: ', parser.number_of_faulty_sensors())
    parser.print_statistics()


if __name__ == '__main__':
    main()