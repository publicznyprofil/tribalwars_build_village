import datetime
import matplotlib.pyplot as plt


def get_data():
    x, y = [], []
    with open('brute_force_log.txt') as log_file:
        for line in log_file.readlines():
            if ';' not in line:
                continue
            build_time, found_datetime = line.split(';')
            build_time = int(build_time)
            found_datetime = datetime.datetime.strptime(found_datetime.strip(), '%Y-%m-%d %H:%M:%S')

            x.append(found_datetime)
            y.append(build_time)
    return x, y

x, y = get_data()
plt.plot(x, y, label='linear')

plt.legend()
plt.show()
