import csv
import os

output_dir = 'output'

with open('OutputMomin.csv', 'wb') as csvWriteFile:
    csvwriter = csv.writer(csvWriteFile, delimiter=',', )
    csvwriter.writerow(['Recording', 'Block', 'Child_Voc_Count', 'Child_Voc_Duration', 'AWC'])
    for csv_files in os.listdir(os.path.join('ADEX Output for Momin', 'ADEX Output with Segment Data')):
        if csv_files.endswith(".csv"):

            with open(os.path.join('ADEX Output for Momin', 'ADEX Output with Segment Data', csv_files)) as csvfile:
                # fieldnames = ['Index', 'File_Name', 'DLP_File_Date_UTC', 'Number_Recordings', 'File_Hours', 'ClientGroup_Name', 'ClientGroup_ID', 'Child_ChildKey', 'Child_ChildID', 'Child_DOB', 'Child_Age', 'Child_Gender', 'DLP', 'ITS_Version', 'AWC', 'Turn_Count', 'Child_Voc_Count', 'CHN', 'Child_Voc_Duration', 'Child_NonVoc_Duration', 'FAN_Word_Count', 'FAN', 'FAN_NonVoc_Duration', 'MAN_Word_Count', 'MAN', 'MAN_NonVoc_Duration', 'CXN', 'OLN', 'TVN', 'NON', 'SIL', 'FUZ', 'AVA_RS', 'AVA_SS', 'EMLU', 'AVA_DA', 'Recording_Index', 'Elapsed_Time', 'Clock_Time_TZAdj', 'Average_SignalLevel', 'Peak_SignalLevel', 'Block_Duration', 'Block_Number', 'Block_Type', 'Init_by']

                data_dict = dict()
                block_array = []
                recording = os.path.basename(csv_files).replace(".csv", "")
                if os.path.exists(os.path.join(output_dir, recording)):
                    tmpDirs = [d for d in os.listdir(os.path.join(output_dir, recording)) if
                               os.path.isdir(os.path.join(output_dir, recording, d))]
                    tmpDirs = sorted(tmpDirs, key=len)

                    for block_folders in tmpDirs:
                        block_name = block_folders
                        if os.path.exists(
                                os.path.join(output_dir, recording, block_name, recording + "_labels.csv")):
                            csv_path = os.path.join(output_dir, recording, block_name, recording + "_labels.csv")
                        else:
                            csv_path = os.path.join(output_dir, recording, block_name,
                                                    recording[:len(recording) - 2] + " (2)_labels.csv")
                        if os.path.exists(csv_path):
                            # print(recording)
                            start_block = ''
                            end_block = ''
                            with open(csv_path) as csvfile_block:
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
                                data_dict[recording + ":" + block_name] = [int(block_name), int(start_block),
                                                                           int(end_block), 0, 0, 0, recording]
                                block_array.append(int(block_name))
                            # print row['Block']
                            # break  # get out of the inner csv reading as only one csv
                        else:
                            print "csv not found" + csv_path
                            continue
                else:
                    print("folder not found: " + os.path.join(output_dir, recording))
                block_array.sort()
                if len(block_array) == 0:
                    continue
                # now we have the data from the output folder
                reader = csv.DictReader(csvfile)
                block_num = 0
                current_block = 0
                for row in reader:
                    # 1 sec room for error in making block
                    if data_dict[recording + ":" + str(block_array[current_block])][
                        1] - 1000 <= float(row['Elapsed_Time']) * 1000 <= \
                            data_dict[recording + ":" + str(block_array[current_block])][2] + 1000:
                        # print data[current_block][0], row['Elapsed_Time'], row['Clock_Time_TZAdj'],
                        # row['Child_Voc_Count'], row[ 'Child_Voc_Duration'], row['AWC'], data[current_block][1],
                        # data[current_block][2]
                        data_dict[recording + ":" + str(block_array[current_block])][3] += float(row['Child_Voc_Count'])
                        data_dict[recording + ":" + str(block_array[current_block])][4] += float(
                            row['Child_Voc_Duration'])
                        data_dict[recording + ":" + str(block_array[current_block])][5] += float(row['AWC'])
                        block_num = data_dict[recording + ":" + str(block_array[current_block])][0]

                    elif block_num > 0:
                        if current_block + 1 < len(data_dict):
                            while data_dict[recording + ":" + str(block_array[current_block + 1])][0] == block_num:
                                current_block += 1
                                data_dict[recording + ":" + str(block_array[current_block])][3] = \
                                    data_dict[recording + ":" + str(str(block_array[current_block - 1]))][3]
                                data_dict[recording + ":" + str(block_array[current_block])][4] = \
                                    data_dict[recording + ":" + str(block_array[current_block - 1])][4]
                                data_dict[recording + ":" + str(block_array[current_block])][5] = \
                                    data_dict[recording + ":" + str(block_array[current_block - 1])][5]
                        else:
                            break
                        current_block += 1
                        block_num = 0

            for key in sorted(data_dict.keys(), key=lambda x:int(x.split(":")[1])):
                d = data_dict[key]
                #print(d[6], d[0], float("{:.2f}".format(d[3])), float("{:.2f}".format(d[4])),
                #      float("{:.2f}".format(d[5])))
                csvwriter.writerow([d[6], d[0], float("{:.2f}".format(d[3])), float("{:.2f}".format(d[4])),
                                    float("{:.2f}".format(d[5]))])
