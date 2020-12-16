from statistics import median
from operator import itemgetter


def convert_praef_to_num(praef):
    if praef == "Erstwahl":
        return 1
    if praef == "Zweitwahl":
        return 2
    if praef == "Drittwahl":
        return 3
    if praef == "Viertwahl":
        return 4
    if praef == "Fünftwahl":
        return 5
    if praef == "Sechstwahl":
        return 6
    if praef == "Siebtwahl":
        return 7
    if praef == "Achtwahl":
        return 8
    if praef == "Neuntwahl":
        return 9
    if praef == "Zehntwahl":
        return 10
    return 1000

def sort_by_median(assignments):
    medians = []
    for index, item in enumerate(assignments):
        list = []
        median_with_index = []
        for studi in item["studis"]:
            list.append(studi[2])
        local_median = median(list)
        streuung = 0
        for entry in list:
            streuung += abs(entry - local_median)
        median_with_index.append(local_median)
        median_with_index.append(index)
        median_with_index.append(streuung / len(list))
        medians.append(median_with_index)
    medians = sorted(medians, key=itemgetter(0), reverse=True)
    medians = sorted(medians, key=itemgetter(2))
    index_of_items_sorted_by_medians = []
    for med in medians:
        index_of_items_sorted_by_medians.append(med[1])
    sorted_assignments = []
    for index in index_of_items_sorted_by_medians:
        sorted_assignments.append(assignments[index])
    return sorted_assignments
