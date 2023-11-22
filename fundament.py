import os
from parse.parse_def import parse_def
from parse.parse_tst import parse_tst
from parse.parse_obj import parse_obj
from parse.parse_ste import parse_ste
from parse.parse_var import parse_var
import json
import pandas as pd

def save_data(data, json_file, excel_file):
    with open(json_file, "w", encoding="utf-8") as json_output:
        json.dump(data, json_output, ensure_ascii=False, indent=2)

    df = pd.json_normalize(data)
    df.to_excel(excel_file, index=False)

def main():
    xml_file = "rhel-8.oval.xml"

    if not os.path.exists("examples"):
        os.makedirs("examples\\json")
        os.makedirs("examples\\xlsx")

    json_def_file = os.path.join("examples", "json", "definitions.json")
    excel_def_file = os.path.join("examples", "xlsx", "definitions.xlsx")
    json_obj_file = os.path.join("examples", "json", "objects.json")
    excel_obj_file = os.path.join("examples", "xlsx", "objects.xlsx")
    json_tst_file = os.path.join("examples", "json", "tests.json")
    excel_tst_file = os.path.join("examples", "xlsx", "tests.xlsx")
    json_ste_file = os.path.join("examples", "json", "states.json")
    excel_ste_file = os.path.join("examples", "xlsx", "states.xlsx")
    json_var_file = os.path.join("examples", "json", "variables.json")
    excel_var_file = os.path.join("examples", "xlsx", "variables.xlsx")

    def_data = parse_def(xml_file)
    obj_data = parse_obj(xml_file)
    tst_data = parse_tst(xml_file)
    sta_data = parse_ste(xml_file)
    var_data = parse_var(xml_file)

    save_data(def_data, json_def_file, excel_def_file)
    save_data(obj_data, json_obj_file, excel_obj_file)
    save_data(tst_data, json_tst_file, excel_tst_file)
    save_data(sta_data, json_ste_file, excel_ste_file)
    save_data(var_data, json_var_file, excel_var_file)

if __name__ == "__main__":
    main()
    print("jumbo (￢‿￢ )")