from statistics import median
from operator import itemgetter
import copy


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
    return praef

def comvert_num_to_praef(num):
    if num == 1 or num == '1':
        return "Erstwahl"
    if num == 2 or num == '2':
        return "Zweitwahl"
    if num == 3 or num == '3':
        return "Drittwahl"
    if num == 4 or num == '4':
        return "Viertwahl"
    if num == 5 or num == '5':
        return "Fünftwahl"
    if num == 6 or num == '6':
        return "Sechstwahl"
    if num == 7 or num == '7':
        return "Siebtwahl"
    if num == 8 or num == '8':
        return "Achtwahl"
    if num == 9 or num == '9':
        return "Neuntwahl"
    if num == 10 or num == '10':
        return "Zehntwahl"
    return num

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


def duplicate_themen(themen, max_per):
    new_themen = copy.deepcopy(themen)
    for index in range(max_per - 1):
        for thema in themen:
            new_themen.append(thema)
    return new_themen

def duplicate_teilnehmer_praefs(teilnehmer_praefs, max_per):
    print(teilnehmer_praefs)
    new_teilnehmer_praefs = copy.deepcopy(teilnehmer_praefs)
    teilnehmer_praefs.pop(0)
    for index in range(max_per - 1):
        for praef in teilnehmer_praefs:
            new_teilnehmer_praefs.append(praef)
    return new_teilnehmer_praefs

def convert_preferences(praeferenzen):

    indices_of_no_praefs = []
    for index, praef in enumerate(praeferenzen):
        praeferenzen[index] = convert_praef_to_num(praef)
        if praef == "Keine Präferenz":
            indices_of_no_praefs.append(index)
    possible_number = 1

    for index in indices_of_no_praefs:
        while True:
            if not possible_number in praeferenzen:
                praeferenzen[index] = possible_number
                break
            else: possible_number += 1

    preference_string = ""
    for praef in praeferenzen:
        preaf = convert_praef_to_num(praef)
        preference_string = preference_string + str(praef) + ","
    return preference_string[:-1]

