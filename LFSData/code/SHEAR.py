import os 
import sys
import re

input_path = r'E:\python\virtualenv\Tool\LFSData\data\弱層資料整理\INPUT\V600SHEAR.txt'
output_folder = r'E:\python\virtualenv\Tool\LFSData\data\弱層資料整理\output_tet'
shear_output = ""

def transfer(input_path, output_folder):
    with open(input_path, 'r') as f:
        data = f.read()
    
    matches = re.findall(r'S T O R Y   F O R C E S\s+(STORY.*)["]+\s+ETABS', data, re.DOTALL)
    if matches:
        print(matches[0].strip())  # 使用strip來移除前後的空白

    shear_output = matches[0].strip()
    shear_output = f"{shear_output}\t\nADD 1 LINE"

    output_path = fr"{output_folder}\SHEAR.txt"
    with open(output_path, 'w+') as f:
        f.write(shear_output) 
    return output_path


if __name__ == "__main__":
    transfer(input_path, output_folder)    