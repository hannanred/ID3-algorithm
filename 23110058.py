import math
import numpy as np
import pandas as pd
import pprint
import sys

class Tree:
    def __init__(self, ds: np.ndarray, enc: np.ndarray):
        self.data_set = ds
        self.enc = enc
        
    def create_list(self, ds: np.ndarray, enc: np.ndarray, heading) -> list:
        data = []
        for row, elem in enumerate(data_set):
            _list = []
            index_e = 1
            temp = data_set[row]
            length = len(temp)
            counter = 0
            while(counter < length):
                item = temp[counter]
                _list.append(encodings[index_e].split(",")[item])
                index_e += 1
                counter += 1
            data.append(_list)
        return data

    def table(self, ds: np.ndarray, enc: np.ndarray) -> pd.DataFrame:
        heading = [i for i in encodings[0].split(',')]
        data = self.create_list(ds, enc, heading)
        data_frame = pd.DataFrame(data, columns=heading)
        return data_frame

    def entropy(self, data_frame: pd.DataFrame) -> int:
        number_values = data_frame[data_frame.keys()[-1]].value_counts()
        while True:
            if len(number_values) == 1:
                return 0
            elif number_values[0] == number_values[1]:
                return 1
            else:
                entropy = 0
                total = 0
                for i in number_values:
                    total += i
                for value in number_values:
                    entropy -= (value/total) * np.log2(value/total)
                return entropy


    def inf_gain(self, data_frame: pd.DataFrame) -> dict:
        whole_entropy = self.entropy(data_frame)
        whole_length = len(data_frame)
        gain = {}
        attributes = []
        lenth_of_df = len(data_frame.keys()) - 1
        x = 0
        while x < lenth_of_df:
            attributes.append(data_frame.keys()[x])
            x += 1
        length_of_attribute = len(attributes)
        attribute_index = 0    
        while attribute_index < length_of_attribute:
            sub_table = data_frame[attributes[attribute_index]].unique()
            gain[attributes[attribute_index]] = whole_entropy
            length_of_sub_table = len(sub_table)
            sub_table_index = 0
            while sub_table_index < length_of_sub_table:
                sub_entropy = self.entropy(data_frame.loc[data_frame[attributes[attribute_index]]==sub_table[sub_table_index]])
                sub_length = len(data_frame.loc[data_frame[attributes[attribute_index]]==sub_table[sub_table_index]])
                gain[attributes[attribute_index]] -= (sub_length/whole_length) * sub_entropy
                sub_table_index += 1
            attribute_index += 1
        return gain

    def selectRoot(self, table: pd.DataFrame) -> int:
        information_gain = self.inf_gain(table)
        maximum = -1.0
        for temp in information_gain.values():
            if(temp > maximum):
                maximum = temp
        for key, value in information_gain.items():
            if maximum == value:
                return key


    def decision(self, data_frame: pd.DataFrame) -> dict:
        decision_tree = {}
        max_gain = self.selectRoot(data_frame)
        most_gain_attributes = data_frame[max_gain].unique()
        decision_tree[max_gain] = {}
        length_of_attributes = len(most_gain_attributes)
        attributes_index = 0
        while attributes_index < length_of_attributes:
            sub_table = data_frame.loc[data_frame[max_gain]==most_gain_attributes[attributes_index]]
            
            values = sub_table[sub_table.keys()[-1]].unique()
            if len(values) != 1: 
                decision_tree[max_gain][most_gain_attributes[attributes_index]] = self.decision(sub_table)
            elif len(values) == 1:
                decision_tree[max_gain][most_gain_attributes[attributes_index]] = values[0]
            attributes_index += 1
        return decision_tree
    def print(self, data_frame):
        pprint.pprint(decision_tree)


encodings = np.loadtxt(sys.argv[2], dtype=str)
data_set = np.loadtxt(sys.argv[1], dtype=int, delimiter=",")
tree = Tree(data_set, encodings)
data_frame = tree.table(data_set, encodings)
decision_tree = tree.decision(data_frame)
tree.print(decision_tree)
