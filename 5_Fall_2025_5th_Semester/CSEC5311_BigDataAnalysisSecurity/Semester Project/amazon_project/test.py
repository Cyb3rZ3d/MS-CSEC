file_path = r"C:\Users\rubva\GitHub\MS-CSEC\5_Fall_2025_5th_Semester\CSEC5311_BigDataAnalysisSecurity\Semester Project\amazon_project\amazon-meta.txt"

with open(file_path, 'r', encoding='latin-1') as file:
    for i in range(30):
        line = file.readline()
        print(repr(line))