import os
import pandas as pd
import matplotlib.pyplot as plt


def analyze_personality_data(p_type_data_path):
    personality_type_data = pd.read_excel(p_type_data_path, header=None)
    personality_career = personality_type_data[1].value_counts(normalize=True)*100
    personality_career = personality_career.head(5)
    personality_career.plot()
    plt.xlabel('Career')
    plt.ylabel('Percentage of people')
    plt.show()


def get_p_type_data_path(p_type):
    """Return xlsx file path of the corresponding personality type"""
    return 'static/personality types data' + f'/{p_type}.xlsx'


if __name__ == '__main__':
    p_type = 'ESFP'
    p_type_data_path = get_p_type_data_path(p_type)
    analyze_personality_data(p_type_data_path)