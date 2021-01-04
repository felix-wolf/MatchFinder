from operator import itemgetter
from munkres import DISALLOWED
from statistics import median
from . import database_helper
from functools import reduce
import random
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
    if praef == "Veto":
        return DISALLOWED
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

def check_user_credentials(matr_nr, hashed_verteilung_id):
    if matr_nr != None and matr_nr.isdigit():
        verteilung, teilnehmer, error = check_membership(hashed_verteilung_id, matr_nr)
        if error == None:
            return None, verteilung, teilnehmer
        else:
            return error, None, None
    else:
        return "Matrikelnummer muss eine Zahl sein!", None, None

def check_membership(hashed_verteilung_id, matr_nr):
    verteilung_to_id = database_helper.get_verteilung_by_hashed_id(hashed_verteilung_id)
    if verteilung_to_id != None:
        list_id = verteilung_to_id.teilnehmer_list_id
        teilnehmer_to_verteilung = database_helper.get_teilnehmer_list_by_id(list_id)
        if teilnehmer_to_verteilung != None:
            for teil in teilnehmer_to_verteilung.teilnehmer:
                if int(teil.matr_nr) == int(matr_nr):
                    if not verteilung_to_id.editable:
                        praef = database_helper.get_praeferenz(teil.id, verteilung_to_id.id)
                        if praef != None:
                            return None, None, "Präferenzen wurden bereits angegeben!"

                    return verteilung_to_id, teil, None
    return None, None, "Matrikelnummer ungültig!"

def sort_by_median(assignments):
    #if len(assignments) == 1:
    if True:
        medians = []
        for index, item in enumerate(assignments):
            weights = list(map(lambda x: x[2], item["studis"]))
            local_median = median(weights)
            streuung = reduce((lambda x, y: x + abs(y - local_median)), weights, 0)
            medians.append([local_median, index, streuung / len(weights)])
        medians = sorted(sorted(medians, key=itemgetter(0), reverse=True), key=itemgetter(2))
        assignments = list(map(lambda x: assignments[x], map(lambda x: x[1], medians)))
    return assignments

def duplicate_themen(themen, max_per):
    new_themen = copy.deepcopy(themen)
    for index in range(max_per - 1):
        new_themen += list(map(lambda x: x, themen))
    return new_themen

def duplicate_teilnehmer_praefs(teilnehmer_praefs, max_per):
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

    if len(indices_of_no_praefs) == len (praeferenzen):
        random.shuffle(praeferenzen)
    preference_string = "".join(list(map(
        lambda x: str(convert_praef_to_num(x)) + ",", praeferenzen)))
    return preference_string[:-1]

def create_csv(data):
    rtn = "Name,Thema,Wahl\n"
    return rtn + "".join(map(lambda x: x[0] + "," + x[1] + "," + str(x[2]) + "\n", data))

def create_txt(data):
    rtn = "ALS TABELLE:\n\n"
    rtn += "===== Auswertung der Verteilung =====\n"
    rtn += "| Name | Thema | Wahl |"
    for studi in data:
        rtn += "\n|" + studi[0] + "|" + studi[1] + "|" + str(studi[2]) + "|"
    rtn += "\n\n\n\nALS LISTE:\n\n"
    rtn += "===== Auswertung der Verteilung =====\n"
    themen = sorted(list(set(map(lambda x: x[1], data))))
    for thema in themen:
        rtn += "- " + thema + " -- "
        rtn += "".join(map(str, map(lambda x: x + ", ", sorted(list(
                    map(lambda c: c[0], filter(lambda x: x[1] == thema, data)))))))
        rtn = rtn[:-2] + "\n"
    return rtn
