from __future__ import division
import tensorflow as tf
import csv
from utils import randomize_csv, count_images
import random

read_csv_path = 'train.csv'
write_csv_path = 'balanced.csv'

'''
Implementation of oversampling algorithm for tackling class imbalance in training a binary classification task
--------------------------------------------------------------------------------------------------------------
Executing this python script would:
    - Read a csv file named 'train.csv' from the current path
        -- Rows of csv file should contain: 'path, label' of the images
    - Output a csv file named 'balanced.csv' which has balanced classes (50/50 - True/False)
        -- Oversamples the class labeled '1' by default
'''

def calculate_num_sample(Total_epochs, Current_epoch, True_ratio, False_examples):
    TR_i = 0.5 - (0.5 - True_ratio) * (Current_epoch)/(Total_epochs)
    Num_sample = int(TR_i * False_examples / (1-TR_i))
    return Num_sample


def resample(read_csv_path, balanced_csv_path, resample_label, Total_epochs, Current_epoch):
    '''
    Oversamples the required class label according to the current epoch
    -------------------------------------------------------------------
    Inputs
    ------
        - read_csv_path --> the path of original csv file (imbalanced classes)
        - balanced_csv_path --> the required path of csv file with balanced classes (file is created)
        - resample_label --> the label of class to be oversampled
        - Total_epochs --> the total number of epochs the training is to return
        - Current_epoch --> the current epoch during training
    This function resamples according to the ratio of current epoch and total epochs
        - At first epoch the clases are perfectly balanced (50/50). The classes distribution change linearly
          towards the original distribution as the current epoch approaches total epochs.
    '''
    csv_file  = open(read_csv_path, "rb")
    reader = csv.reader(csv_file)
    csv_list = list(reader)
    Total_examples = len(csv_list)
    true_list = []
    True_examples =0
    for i in range(Total_examples):
        if csv_list[i][1] == resample_label:
            true_list.append(csv_list[i])
            True_examples+=1

    False_examples = Total_examples - True_examples
    True_ratio = True_examples/Total_examples
    sample_num = calculate_num_sample(Total_epochs,Current_epoch,True_ratio,False_examples)
    oversample_num = sample_num - True_examples
    loop_count = int(oversample_num / True_examples)

    oversample_list = []
    for i in range(loop_count):
        for j in range(True_examples):
            oversample_list.append(true_list[j])

    temp_len =  len(oversample_list)
    for i in range(oversample_num-temp_len):
        oversample_list.append(true_list[i])

    print len(oversample_list), oversample_num

    balanced_list = csv_list
    for i in range(oversample_num):
        balanced_list.append(oversample_list[i])

    random.shuffle(balanced_list)

    balanced_file  = open(balanced_csv_path, "wb")
    balanced_writer = csv.writer(balanced_file, delimiter=',')
    for i in range(len(balanced_list)):
        balanced_writer.writerow(balanced_list[i])

resample_num = resample(read_csv_path, write_csv_path, '1', 100, 0)
