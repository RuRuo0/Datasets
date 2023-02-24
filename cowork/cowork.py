import os


def get_work_dis():
    workers = ["XiaokaiZhang", "NaZhu", "JiaZou", "YimingHe"]
    timespan = "Week 1 (230227): form 2023-02-27 to 2023-03-05."
    start_pid = 1584
    workload = 15

    table = '#### {}\n<table align="center">\n	<tr>\n        <td align="center"><b>Worker</b></td>\n	    <td align="center"><b>WorkLoad</b></td>\n    <td align="center"><b>PID</b></td>\n	    <td align="center"><b>Skip</b></td>\n	    <td align="center"><b>Submitted</b></td>\n    </tr>\n'.format(timespan)
    body = '    <tr>\n        <td align="center">{}</td>\n	    <td align="center">{}</td>\n	    <td align="center">{}-{}</td>\n	    <td align="center">{}</td>\n	    <td align="center"><font color="red"><b>×</b></font></td>\n    </tr>\n'

    annotated = [int(filename.split(".")[0]) for filename in os.listdir("../data/formalized-problems")]
    for worker in workers:
        j = start_pid
        skip = []
        i = 0
        while i < workload:
            if j not in annotated:
                i += 1
            else:
                skip.append(j)
            j += 1
        table += body.format(worker, workload, start_pid, j - 1, skip)
        start_pid = j

    print(table + "</table>")


if __name__ == '__main__':
    get_work_dis()
