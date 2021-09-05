import os
import csv

folder = os.getcwd()

TRANS_TYPE = 1
PURCHASE_TYPE = 2
GOO = 4
AREA = 12
LAND_AREA = 13
FLOOR = 14
CONTRACT_YEAR = 15
PRICE = 18
DEPOSIT = 19
RENT = 20

# info = {
# "13년":{
#     "중구": {
#         "오피스텔": {
#             "100m":{"price": 100, "count": 10},
#             "200m":,
#             "300m":,
#             "400m":,
#             "500m":,
#         },
#         "연립다세대": {},
#         "아파트": {},
#     },
#     "해운대구": {
#         "오피스텔": {},
#         "연립다세데": {},
#         "아파트": {},
#     }
#   }
# }

info = {}


def get_new_mean_value(old_value, price):
    old_price = old_value["price"]
    count = old_value["count"]
    return {"price": (old_price * count + price) / (count + 1), "count": count + 1}


for local_path in os.listdir(folder):
    filename, extender = tuple(local_path.split("."))
    if extender == "csv":
        distance = filename.split("_")[1]
        f = open(local_path, "r", encoding="utf-8")
        rdf = csv.reader(f)
        FIRSTLINE = True
        for line in rdf:
            if FIRSTLINE:
                FIRSTLINE = False
                continue
            if line[PURCHASE_TYPE] == "매매":
                try:
                    info[line[CONTRACT_YEAR]]
                except KeyError:
                    info[line[CONTRACT_YEAR]] = {}
                finally:
                    try:
                        info[line[CONTRACT_YEAR]][line[GOO]]
                    except KeyError:
                        info[line[CONTRACT_YEAR]][line[GOO]] = {}
                    finally:
                        try:
                            info[line[CONTRACT_YEAR]][line[GOO]][line[TRANS_TYPE]]
                        except KeyError:
                            info[line[CONTRACT_YEAR]][line[GOO]][line[TRANS_TYPE]] = {}
                        finally:
                            try:
                                info[line[CONTRACT_YEAR]][line[GOO]][line[TRANS_TYPE]][
                                    distance
                                ] = get_new_mean_value(
                                    info[line[CONTRACT_YEAR]][line[GOO]][
                                        line[TRANS_TYPE]
                                    ][distance],
                                    float(line[PRICE]) / float(line[AREA]),
                                )
                            except KeyError:
                                info[line[CONTRACT_YEAR]][line[GOO]][line[TRANS_TYPE]][
                                    distance
                                ] = {
                                    "price": float(line[PRICE]) / float(line[AREA]),
                                    "count": 1,
                                }
                       
        f.close()


GOO_LIST = (
    "중구",
    "동구",
    "영도구",
    "부산진구",
    "동래구",
    "남구",
    "북구",
    "사하구",
    "금정구",
    "강서구",
    "연제구",
    "수영구",
    "사상구",
    "해운대구",
    "기장군",
    "서구",
)

YEAR_GENERATOR = range(2010, 2019)  # 2010~2018년까지

DISTANCE_LISTS = ["100m", "200m", "300m", "400m", "500m"]
TYPE_LISTS = ["연립다세대", "오피스텔", "아파트"]
print(local_path)
f = open("output.csv", "w",  newline='',encoding="utf-8")
wr = csv.writer(f)

for GOO_NAME in GOO_LIST:
    for TYPE in TYPE_LISTS:
        rows = [[DISTANCE] for DISTANCE in DISTANCE_LISTS]
        print(rows)
        first_row = [GOO_NAME + "_" + str(TYPE)]

        for year in range(2010, 2019):  # 두번 연속으로 해야한다.
            first_row.append(str(year))
        for year in range(2010, 2019):
            first_row.append(str(year))

        for YEAR in YEAR_GENERATOR:
            for i, DISTANCE in enumerate(DISTANCE_LISTS):
                try:
                    rows[i].append(info[str(YEAR)][GOO_NAME][TYPE][DISTANCE]["price"])
                except KeyError:
                    rows[i].append("NO_EXIST")
        for YEAR in YEAR_GENERATOR:
            for i, DISTANCE in enumerate(DISTANCE_LISTS):
                try:
                    rows[i].append(info[str(YEAR)][GOO_NAME][TYPE][DISTANCE]["count"])
                except KeyError:
                    rows[i].append("NO_EXIST")
        rows.insert(0, first_row)
        rows.append([])
        rows.append([])
        wr.writerows(rows)
