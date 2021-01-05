import csv
import os
from shutil import copyfile

output_dir = 'output'
output_dir_temp = 'output_momin'
data = []
with open('ConvolabelOutputAll.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:

        #
        if row['Recording'] != '':

            if os.path.exists(os.path.join(output_dir, row['Recording'], row['Block'])):

                start_block = ''
                end_block = ''
                # for csv_file in os.listdir(os.path.join(output_dir, row['Recording'] , row['Block'])):
                #     if csv_file.endswith('.csv'):
                if row['Recording'] != '':
                    if os.path.exists(
                            os.path.join(output_dir, row['Recording'], row['Block'], row['Recording'] + "_labels.csv")):
                        csv_path = os.path.join(output_dir, row['Recording'], row['Block'],
                                                row['Recording'] + "_labels.csv")
                    else:
                        csv_path = os.path.join(output_dir, row['Recording'], row['Block'],
                                                row['Recording'][:len(row['Recording']) - 2] + " (2)_labels.csv")
                    if os.path.exists(csv_path):
                        dest = os.path.join(output_dir_temp,os.path.dirname(csv_path))
                        if not os.path.exists(dest):
                            os.makedirs(dest)

                        copyfile(csv_path, os.path.join(dest, os.path.basename(csv_path)))

                    else:
                        print csv_path
