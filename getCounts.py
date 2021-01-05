import csv
import os

output_dir = 'output'

data = []
with open('ConvolabelOutput_momin.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        #
        if row['Recording'] == 'C167_20150708':
            if os.path.exists(os.path.join(output_dir, 'C167_20150708', row['Block'])):
                start_block = ''
                end_block = ''
                for csv_file in os.listdir(os.path.join(output_dir, 'C167_20150708', row['Block'])):
                    if csv_file.endswith('.csv'):
                        with open(os.path.join(output_dir, 'C167_20150708', row['Block'], csv_file)) as csvfile_block:
                            reader2 = csv.DictReader(csvfile_block)

                            for row2 in reader2:
                                if reader2.line_num == 2:
                                    start_block = row2['timestamp']
                                else:
                                    end_block = row2['timestamp']

                            if end_block == '':
                                end_block = start_block.split('_')[1].strip()
                            else:
                                end_block = end_block.split('_')[1].strip()
                            start_block = start_block.split('_')[0].strip()
                            # print row['Block'], start_block, end_block
                            data.append([int(row['Block']), int(start_block), int(end_block), 0, 0, 0])
                            # print row['Block']
                            break  # get out of the inner csv reading as only one csv

with open('C167_20150708_last_momin.csv') as csvfile:
    # fieldnames = ['Index', 'File_Name', 'DLP_File_Date_UTC', 'Number_Recordings', 'File_Hours', 'ClientGroup_Name', 'ClientGroup_ID', 'Child_ChildKey', 'Child_ChildID', 'Child_DOB', 'Child_Age', 'Child_Gender', 'DLP', 'ITS_Version', 'AWC', 'Turn_Count', 'Child_Voc_Count', 'CHN', 'Child_Voc_Duration', 'Child_NonVoc_Duration', 'FAN_Word_Count', 'FAN', 'FAN_NonVoc_Duration', 'MAN_Word_Count', 'MAN', 'MAN_NonVoc_Duration', 'CXN', 'OLN', 'TVN', 'NON', 'SIL', 'FUZ', 'AVA_RS', 'AVA_SS', 'EMLU', 'AVA_DA', 'Recording_Index', 'Elapsed_Time', 'Clock_Time_TZAdj', 'Average_SignalLevel', 'Peak_SignalLevel', 'Block_Duration', 'Block_Number', 'Block_Type', 'Init_by']

    reader = csv.DictReader(csvfile)
    block_num = 0
    current_block = 0

    for row in reader:
        # 1 sec room for error in making block
        if float(row['Elapsed_Time']) * 1000 >= data[current_block][1] - 1000 and float(row['Elapsed_Time']) * 1000 <= \
                data[current_block][
                    2] + 1000:
            # print data[current_block][0], row['Elapsed_Time'], row['Clock_Time_TZAdj'], row['Child_Voc_Count'], row[
            #     'Child_Voc_Duration'], row['AWC'], data[current_block][1], data[current_block][2]
            data[current_block][3] += float(row['Child_Voc_Count'])
            data[current_block][4] += float(row['Child_Voc_Duration'])
            data[current_block][5] += float(row['AWC'])
            block_num = data[current_block][0]

        elif block_num > 0:
            if current_block + 1 < len(data):
                while data[current_block + 1][0] == block_num:
                    current_block += 1
                    data[current_block][3] = data[current_block - 1][3]
                    data[current_block][4] = data[current_block - 1][4]
                    data[current_block][5] = data[current_block - 1][5]
            else:
                break;
            current_block += 1
            block_num = 0
print 'Block', 'Child_Voc_Count', 'Child_Voc_Duration', 'AWC'
for d in data:
    print d[0], d[3], d[4], d[5]
