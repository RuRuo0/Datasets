import os
from core.aux_tools.utils import load_json, save_json
"""
每周提交完成后：
1.check_json_format()                  # 确保 json 格式正确
2.format_annotation(week_number=13)    # 更改 annotation id 并核对是否有漏标
3.check_notes(add_notes=True)          # 确保 未标注的问题都添加了 notes
4.main.py                              # 批量运行
"""

formalized_path = "../../data/formalized-problems/"
raw_data_path = "../../data/raw-problems/"
weeks = {
    1: [{"worker": "XiaokaiZhang", "dataset": "Geometry3k-Triangle", "pid": (1584, 1864)},
        {"worker": "NaZhu", "dataset": "Geometry3k-Triangle", "pid": (1865, 2026)},
        {"worker": "JiaZou", "dataset": "Geometry3k-Triangle", "pid": (2028, 2233)},
        {"worker": "YimingHe", "dataset": "Geometry3k-Triangle", "pid": (2236, 2396)}],
    2: [{"worker": "XiaokaiZhang", "dataset": "Geometry3k-Triangle", "pid": (2397, 2570)},
        {"worker": "NaZhu", "dataset": "Geometry3k-Triangle", "pid": (2572, 2742)},
        {"worker": "JiaZou", "dataset": "Geometry3k-Triangle", "pid": (2744, 2885)},
        {"worker": "YimingHe", "dataset": "Geometry3k-Triangle", "pid": (2887, 3083)}],
    3: [{"worker": "NaZhu", "dataset": "Geometry3k-Triangle", "pid": (3273, 3448)},
        {"worker": "JiaZou", "dataset": "Geometry3k-Triangle", "pid": (3451, 3624)},
        {"worker": "YimingHe", "dataset": "Geometry3k-Triangle", "pid": (3625, 3791)}],
    4: [{"worker": "XiaokaiZhang", "dataset": "Geometry3k-Other", "pid": (1585, 1803)},
        {"worker": "NaZhu", "dataset": "Geometry3k-Other", "pid": (1804, 1924)},
        {"worker": "YimingHe", "dataset": "Geometry3k-Other", "pid": (2048, 2154)}],
    5: [{"worker": "YimingHe", "dataset": "Geometry3k-Other", "pid": (2155, 2261)},
        {"worker": "JiaZou", "dataset": "Geometry3k-Other", "pid": (1926, 2046)},
        {"worker": "JiaZou", "dataset": "Geometry3k-Other", "pid": (2265, 2386)},
        {"worker": "NaZhu", "dataset": "Geometry3k-Other", "pid": (2387, 2502)},
        {"worker": "XiaokaiZhang", "dataset": "Geometry3k-Other", "pid": (2503, 2625)},
        {"worker": "YanjunGuo", "dataset": "Geometry3k-Triangle", "pid": (3089, 3165)},
        {"worker": "YanjunGuo", "dataset": "Geometry3k-Other", "pid": (2626, 2652)},
        {"worker": "QikeHuang", "dataset": "Geometry3k-Triangle", "pid": (3171, 3253)},
        {"worker": "QikeHuang", "dataset": "Geometry3k-Other", "pid": (2653, 2680)},
        {"worker": "XiaoxiaoJin", "dataset": "Geometry3k-Triangle", "pid": (3857, 3919)},
        {"worker": "XiaoxiaoJin", "dataset": "Geometry3k-Other", "pid": (2712, 2747)},
        {"worker": "Yangli", "dataset": "Geometry3k-Triangle", "pid": (3920, 4007)},
        {"worker": "Yangli", "dataset": "Geometry3k-Other", "pid": (2748, 2780)},
        {"worker": "ChenyangMao", "dataset": "Geometry3k-Triangle", "pid": (4009, 4075)},
        {"worker": "ChenyangMao", "dataset": "Geometry3k-Other", "pid": (2781, 2809)},
        {"worker": "DengfengYue", "dataset": "Geometry3k-Triangle", "pid": (4335, 4430)},
        {"worker": "DengfengYue", "dataset": "Geometry3k-Other", "pid": (2923, 2956)},
        {"worker": "FangzhenZhu", "dataset": "Geometry3k-Triangle", "pid": (4435, 4501)},
        {"worker": "FangzhenZhu", "dataset": "Geometry3k-Other", "pid": (2957, 2984)},
        {"worker": "ZheZhu", "dataset": "Geometry3k-Triangle", "pid": (4502, 4582)},
        {"worker": "ZheZhu", "dataset": "Geometry3k-Other", "pid": (2986, 3007)}],
    6: [{"worker": "YimingHe", "dataset": "GeoQA", "pid": (4586, 4645)},
        {"worker": "JiaZou", "dataset": "GeoQA", "pid": (4646, 4705)},
        {"worker": "NaZhu", "dataset": "GeoQA", "pid": (4706, 4765)},
        {"worker": "XiaokaiZhang", "dataset": "GeoQA", "pid": (4766, 4825)},
        {"worker": "YanjunGuo", "dataset": "Geometry3k-Other", "pid": (3008, 3097)},
        {"worker": "QikeHuang", "dataset": "Geometry3k-Other", "pid": (3100, 3193)},
        {"worker": "XiaoxiaoJin", "dataset": "Geometry3k-Other", "pid": (3196, 3290)},
        {"worker": "Yangli", "dataset": "Geometry3k-Other", "pid": (3293, 3396)},
        {"worker": "ChenyangMao", "dataset": "Geometry3k-Other", "pid": (3398, 3485)},
        {"worker": "DengfengYue", "dataset": "Geometry3k-Other", "pid": (3901, 3997)},
        {"worker": "ZheZhu", "dataset": "Geometry3k-Other", "pid": (3584, 3681)}],
    7: [{"worker": "YimingHe", "dataset": "GeoQA", "pid": (4826, 4885)},
        {"worker": "JiaZou", "dataset": "GeoQA", "pid": (4886, 4945)},
        {"worker": "NaZhu", "dataset": "GeoQA", "pid": (4946, 5005)},
        {"worker": "XiaokaiZhang", "dataset": "GeoQA", "pid": (5006, 5065)},
        {"worker": "YanjunGuo", "dataset": "Geometry3k-Other", "pid": (3486, 3583)},
        {"worker": "QikeHuang", "dataset": "Geometry3k-Other", "pid": (3684, 3792)},
        {"worker": "XiaoxiaoJin", "dataset": "Geometry3k-Other", "pid": (3793, 3900)},
        {"worker": "Yangli", "dataset": "Geometry3k-Other", "pid": (4109, 4195)},
        {"worker": "ChenyangMao", "dataset": "Geometry3k-Other", "pid": (4196, 4289)},
        {"worker": "DengfengYue", "dataset": "Geometry3k-Other", "pid": (4290, 4380)},
        {"worker": "ZheZhu", "dataset": "Geometry3k-Other", "pid": (4382, 4471)},
        {"worker": "YiwenHuang", "dataset": "Geometry3k-Triangle", "pid": (3254, 3270)},
        {"worker": "YiwenHuang", "dataset": "Geometry3k-Triangle", "pid": (3795, 3855)},
        {"worker": "YiwenHuang", "dataset": "Geometry3k-Other", "pid": (2682, 2711)},
        {"worker": "RunanWang", "dataset": "Geometry3k-Triangle", "pid": (4079, 4169)},
        {"worker": "RunanWang", "dataset": "Geometry3k-Other", "pid": (2810, 2844)},
        {"worker": "YifanWang", "dataset": "Geometry3k-Triangle", "pid": (4170, 4244)},
        {"worker": "YifanWang", "dataset": "Geometry3k-Other", "pid": (2849, 2890)},
        {"worker": "FangzhenZhu", "dataset": "Geometry3k-Other", "pid": (3999, 4108)}],
    8: [{"worker": "YimingHe", "dataset": "GeoQA", "pid": (5066, 5125)},
        {"worker": "JiaZou", "dataset": "GeoQA", "pid": (5126, 5185)},
        {"worker": "NaZhu", "dataset": "GeoQA", "pid": (5186, 5245)},
        {"worker": "XiaokaiZhang", "dataset": "GeoQA", "pid": (5246, 5305)},
        {"worker": "YanjunGuo", "dataset": "GeoQA", "pid": (5306, 5365)},
        {"worker": "QikeHuang", "dataset": "GeoQA", "pid": (5366, 5425)},
        {"worker": "XiaoxiaoJin", "dataset": "GeoQA", "pid": (5426, 5485)},
        {"worker": "Yangli", "dataset": "GeoQA", "pid": (5486, 5545)},
        {"worker": "ChenyangMao", "dataset": "GeoQA", "pid": (5546, 5605)},
        {"worker": "DengfengYue", "dataset": "GeoQA", "pid": (5672, 5731)},
        {"worker": "ZheZhu", "dataset": "GeoQA", "pid": (5792, 5851)}],
    9: [{"worker": "YimingHe", "dataset": "GeoQA", "pid": (5852, 5911)},
        {"worker": "JiaZou", "dataset": "GeoQA", "pid": (5912, 5971)},
        {"worker": "NaZhu", "dataset": "GeoQA", "pid": (5972, 6031)},
        {"worker": "XiaokaiZhang", "dataset": "GeoQA", "pid": (6032, 6091)},
        {"worker": "YanjunGuo", "dataset": "GeoQA", "pid": (6092, 6151)},
        {"worker": "QikeHuang", "dataset": "GeoQA", "pid": (6152, 6211)},
        {"worker": "XiaoxiaoJin", "dataset": "GeoQA", "pid": (6212, 6271)},
        {"worker": "Yangli", "dataset": "GeoQA", "pid": (6272, 6331)},
        {"worker": "ChenyangMao", "dataset": "GeoQA", "pid": (6332, 6391)},
        {"worker": "DengfengYue", "dataset": "GeoQA", "pid": (6392, 6451)},
        {"worker": "ZheZhu", "dataset": "GeoQA", "pid": (6452, 6511)},
        {"worker": "ChengQin", "dataset": "GeoQA", "pid": (6512, 6531)},
        {"worker": "YiwenHuang", "dataset": "Geometry3k-Triangle", "pid": (4245, 4330)},
        {"worker": "YiwenHuang", "dataset": "Geometry3k-Other", "pid": (2895, 2921)},
        {"worker": "YiwenHuang", "dataset": "Geometry3k-Other", "pid": (4475, 4498)},
        {"worker": "RunanWang", "dataset": "Geometry3k-Other", "pid": (4499, 4585)},
        {"worker": "RunanWang", "dataset": "GeoQA", "pid": (5606, 5611)},
        {"worker": "YifanWang", "dataset": "GeoQA", "pid": (5612, 5671)},
        {"worker": "FangzhenZhu", "dataset": "GeoQA", "pid": (5732, 5791)}],
    10: [{"worker": "YimingHe", "dataset": "GeoQA", "pid": (6532, 6591)},
         {"worker": "JiaZou", "dataset": "GeoQA", "pid": (6592, 6651)},
         {"worker": "NaZhu", "dataset": "GeoQA", "pid": (6652, 6711)},
         {"worker": "XiaokaiZhang", "dataset": "GeoQA", "pid": (6712, 6771)},
         {"worker": "YanjunGuo", "dataset": "GeoQA", "pid": (6772, 6831)},
         {"worker": "QikeHuang", "dataset": "GeoQA", "pid": (6832, 6891)},
         {"worker": "XiaoxiaoJin", "dataset": "GeoQA", "pid": (6952, 7011)},
         {"worker": "Yangli", "dataset": "GeoQA", "pid": (7012, 7071)},
         {"worker": "ChenyangMao", "dataset": "GeoQA", "pid": (7072, 7131)},
         {"worker": "DengfengYue", "dataset": "GeoQA", "pid": (7252, 7311)},
         {"worker": "ZheZhu", "dataset": "GeoQA", "pid": (7372, 7431)}],
    11: [{"worker": "YimingHe", "dataset": "GeoQA", "pid": (7492, 7551)},
         {"worker": "JiaZou", "dataset": "GeoQA", "pid": (7552, 7611)},
         {"worker": "NaZhu", "dataset": "GeoQA", "pid": (7612, 7671)},
         {"worker": "XiaokaiZhang", "dataset": "GeoQA", "pid": (7672, 7731)},
         {"worker": "YanjunGuo", "dataset": "GeoQA", "pid": (7732, 7791)},
         {"worker": "QikeHuang", "dataset": "GeoQA", "pid": (7792, 7851)},
         {"worker": "XiaoxiaoJin", "dataset": "GeoQA", "pid": (7852, 7911)},
         {"worker": "Yangli", "dataset": "GeoQA", "pid": (7912, 7971)},
         {"worker": "ChenyangMao", "dataset": "GeoQA", "pid": (7972, 8031)},
         {"worker": "DengfengYue", "dataset": "GeoQA", "pid": (8032, 8091)},
         {"worker": "ZheZhu", "dataset": "GeoQA", "pid": (8092, 8151)},
         {"worker": "ChengQin", "dataset": "GeoQA", "pid": (6512, 6531)},
         {"worker": "YiwenHuang", "dataset": "GeoQA", "pid": (6892, 6951)},
         {"worker": "RunanWang", "dataset": "GeoQA", "pid": (7132, 7191)},
         {"worker": "YifanWang", "dataset": "GeoQA", "pid": (7192, 7251)},
         {"worker": "FangzhenZhu", "dataset": "GeoQA", "pid": (7312, 7371)},
         {"worker": "ChengQin", "dataset": "GeoQA", "pid": (7432, 7491)}],
    12: [{"worker": "YimingHe", "dataset": "GeoQA", "pid": (8152, 8211)},
         {"worker": "JiaZou", "dataset": "GeoQA", "pid": (8212, 8271)},
         {"worker": "NaZhu", "dataset": "GeoQA", "pid": (8272, 8331)},
         {"worker": "XiaokaiZhang", "dataset": "GeoQA", "pid": (8332, 8391)},
         {"worker": "YanjunGuo", "dataset": "GeoQA", "pid": (8392, 8451)},
         {"worker": "QikeHuang", "dataset": "GeoQA", "pid": (8452, 8511)},
         {"worker": "XiaoxiaoJin", "dataset": "GeoQA", "pid": (8572, 8631)},
         {"worker": "Yangli", "dataset": "GeoQA", "pid": (8632, 8691)},
         {"worker": "ChenyangMao", "dataset": "GeoQA", "pid": (8692, 8751)},
         {"worker": "DengfengYue", "dataset": "GeoQA", "pid": (8872, 8931)},
         {"worker": "ZheZhu", "dataset": "GeoQA", "pid": (8992, 9051)}],
    13: [{"worker": "YimingHe", "dataset": "GeoQA", "pid": (9112, 9171)},
         {"worker": "JiaZou", "dataset": "GeoQA", "pid": (9172, 9231)},
         {"worker": "NaZhu", "dataset": "GeoQA", "pid": (9232, 9291)},
         {"worker": "XiaokaiZhang", "dataset": "GeoQA", "pid": (9292, 9351)},
         {"worker": "YanjunGuo", "dataset": "GeoQA", "pid": (9352, 9411)},
         {"worker": "QikeHuang", "dataset": "GeoQA", "pid": (9412, 9471)},
         {"worker": "XiaoxiaoJin", "dataset": "GeoQA", "pid": (9472, 9531)},
         {"worker": "Yangli", "dataset": "GeoQA", "pid": (9532, 9591)},
         {"worker": "ChenyangMao", "dataset": "GeoQA", "pid": (9592, 9595)},
         {"worker": "ChenyangMao", "dataset": "GeoQAPlus", "pid": (9596, 9651)},
         {"worker": "DengfengYue", "dataset": "GeoQAPlus", "pid": (9652, 9711)},
         {"worker": "ZheZhu", "dataset": "GeoQAPlus", "pid": (9712, 9771)},
         {"worker": "ChengQin", "dataset": "GeoQAPlus", "pid": (9772, 9831)},
         {"worker": "YiwenHuang", "dataset": "GeoQA", "pid": (8512, 8571)},
         {"worker": "RunanWang", "dataset": "GeoQA", "pid": (8752, 8811)},
         {"worker": "YifanWang", "dataset": "GeoQA", "pid": (8812, 8871)},
         {"worker": "FangzhenZhu", "dataset": "GeoQA", "pid": (8932, 8991)},
         {"worker": "ChengQin", "dataset": "GeoQA", "pid": (9052, 9111)}]
}
aids = {
    1: "2023-03-12",
    2: "2023-03-19",
    3: "2023-03-26",
    4: "2023-04-02",
    5: "2023-04-09",
    6: "2023-04-16",
    7: "2023-04-23",
    8: "2023-04-30",
    9: "2023-05-07",
    10: "2023-05-14",
    11: "2023-05-21",
    12: "2023-05-28",
    13: "2023-06-04"
}


def check_json_format():
    for filename in os.listdir(formalized_path):
        try:
            load_json(formalized_path + filename)
        except:
            print(filename + " ×")


def check_notes(add_notes=False):
    for filename in os.listdir(formalized_path):
        data = load_json(formalized_path + filename)
        if "Shape()" in data["construction_cdl"] and "notes" not in data:
            print(data["annotation"] + "  " + filename)
            if add_notes:
                data["notes"] = "Not annotated and without notes added."
                save_json(data, formalized_path + filename)


def format_annotation(week_number):
    week = weeks[week_number]
    aid = aids[week_number]
    files_formalized = os.listdir(formalized_path)
    for item in week:
        dataset_path = raw_data_path + item["dataset"] + "/"
        files_raw = os.listdir(dataset_path)
        for pid in range(int(item["pid"][0]), int(item["pid"][1]) + 1):
            filename = "{}.json".format(pid)
            if filename not in files_raw:
                continue

            if filename not in files_formalized:
                print("<skip>\t{}\t{}\t{}".format(item["worker"], item["dataset"], pid))
                continue

            data = load_json(formalized_path + filename)
            data["annotation"] = item["worker"] + "_" + aid
            save_json(data, formalized_path + filename)


if __name__ == '__main__':
    check_json_format()
    # for key in aids:
    #     format_annotation(week_number=key)
    # check_notes(add_notes=True)
