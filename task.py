import csv
import os

import dao
import view_data as view

path = os.path.dirname(os.path.abspath(__file__))

# ToDo(denk) add file.conf
path_input_file = '/'.join((path, "\Data.csv"))
path_clean_data = '/'.join((path, "\CleanData.csv"))
path_top_click = '/'.join((path, "\TopMSV.csv"))
path_top_price = '/'.join((path, "\TopCpc.csv"))
path_regionality = '/'.join((path, "\Regionality.csv"))
path_highest_regionality = '/'.join((path, ".\HighestRegionality.csv"))

limit_for_regionality = 10
limit_for_top = 100
anomaly_for_avg_msv = 4198494144


def task_0():
    dao.create_bd_input_data()

    # TODO(denk) replace csv methods
    # Read From csv file an Fill up bd inputData
    with open(path_input_file, 'rb') as csv_file:
        input_data = csv.DictReader(csv_file, delimiter=',',
                                    fieldnames=view.view_input_data)
        # Remove csv header
        input_data = [row for row in input_data][1:]
        # Add Identifier for Unique requests
        for row in input_data:
            row.update({'Identifier': (row['Locode'] + row['Phrase'])})

        dao.insert_into_table('inputData', input_data)

    # Delete requests with all empty columns besides Unestimated Competition
    dao.delete_partly_empty_line_from_inputdata()

    # Update empty cells for AvgMsv < 100
    update_data = []
    get_empty_cells = dao.get_empty_cells_for_avg_less_100()

    for row in get_empty_cells:
        # Overlay bd schema to data
        row = dict(zip(view.view_bd_input_data, row))
        # Fill up empty cells
        for key, value in row.items():
            if value == '':
                row[key] = 0
        update_data.append(row)
    dao.update_bd_input_data(update_data)

    #  Mark rows with empty Competition CostPerClick by Label Unestimated
    #  and Fill up Competition CostPerClick by 0
    update_data = []
    get_empty_competition = dao.get_empty_competition()
    get_empty_costPerClick = dao.get_empty_costPerClick()

    for row in get_empty_competition:
        # Overlay bd schema to data
        row = dict(zip(view.view_bd_input_data, row))
        update_data.append(
            {'Unestimated': 0,
             'Competition': 0,
             'Identifier': row['Identifier']})

    for row in get_empty_costPerClick:
        # Overlay bd schema to data
        row = dict(zip(view.view_bd_input_data, row))
        update_data.append(
            {'Unestimated': 0,
             'CostPerClick': 0,
             'Identifier': row['Identifier']})
    dao.update_bd_input_data(update_data)

    # Delete Anomaly where AvgMsv > 4198494144,
    # It's more than 1 sigma in standard deviation for AvgMsv
    dao.delete_anomaly_from_inputdata(anomaly_for_avg_msv)

    # Validation data all Msv columns, Price and Competition should be Number
    update_data = []
    get_all_rows = dao.get_all_from_table_filter_correct('inputdata')

    for row in get_all_rows:
        numbers = row[2:17]
        avg_msv = row[14]
        try:
            sum(numbers)
        except TypeError:
            for index, item in enumerate(numbers, start=2):
                try:
                    if index < 15:
                        int(item)
                    else:
                        float(item)
                except ValueError:
                    temp = list(row)
                    temp[index] = avg_msv
                    # Overlay bd schema to data
                    update_data.append(
                        dict(zip(view.view_bd_input_data, temp)))
    dao.update_bd_input_data(update_data)

    # Correct AvgMsv
    # If AvgMsv > (Common avg)* 20 % than AvgMsv = Common avg
    update_data = []
    get_all_rows = dao.get_all_from_table_filter_correct('inputdata')

    for row in get_all_rows:
        period = row[2:14]
        avg_msv = row[14]
        avg = (sum(period) / 12)

        if abs(avg_msv - avg) > (avg / 5):
            # Overlay bd schema to data
            row = dict(zip(view.view_bd_input_data, row))
            update_data.append(
                {'AvgMsv': avg,
                 'Identifier': row['Identifier']})
    dao.update_bd_input_data(update_data)

    # write to CleanData.csv
    with open(path_clean_data, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=view.view_input_data)
        writer.writeheader()
        get_all_rows = dao.get_all_from_table_filter_correct('inputdata')
        for line in get_all_rows:
            # Overlay bd schema to data
            writer.writerow(dict(zip(view.view_input_data, line)))


def task_1():

    # Update values in inputData because
    # It has the same fields like schema bd top_msv_click nad top_msv_price
    # Should change 'US NYC' to 'USNYC'
    dao.modify_input_data()

    get_all_rows = dao.get_all_from_table_filter_correct('inputdata')

    # For click
    dao.create_bd_top_msv_click()

    # Turn data in top_msv_click
    # structure [{phrase: {locode1: sum_of_requests_for_locode1, ...}},{...}]
    data_for_click = {}
    for row in get_all_rows:
        locode = row[0]
        phrase = row[1]
        period = row[2:14]

        if phrase in data_for_click.keys():
            data_for_click.get(phrase).update({locode: sum(period)})
        else:
            data_for_click.setdefault(phrase, {locode: sum(period)})

    # Modify data to structure
    # [{phrase: , locode1: , locode2: , total: sum_of_msv}, {...}]
    insert_data_for_click = []
    for phrase, total in data_for_click.items():
        temp = {'phrase': phrase,
                'total': sum(total.values())}
        temp.update(total)
        insert_data_for_click.append(temp)
    dao.insert_into_table('topclick', insert_data_for_click)

    # Write to TopMSVClick.csv  with limit 100
    with open(path_top_click, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=view.view_top_click)
        writer.writeheader()
        get_phrases = dao.get_top_phrase_by_click_with_limit(limit_for_top)

        for line in get_phrases:
            # Overlay bd schema to data
            writer.writerow(dict(zip(view.view_top_click, line)))

    # For price
    dao.create_bd_top_msv_price()

    # Turn data in top_msv_price
    # structure [{phrase: {locode1: price, locode2: price, ...}},{...}]
    data_for_price = {}
    for row in get_all_rows:
        locode = row[0]
        phrase = row[1]
        price = row[16]

        if phrase in data_for_price.keys():
            data_for_price.get(phrase).update({locode: price})
        else:
            data_for_price.setdefault(phrase, {locode: price})

    # Modify data to structure
    # [{phrase: , locode1: price, locode2: price, MaxCostPerClick: }, {...}]
    insert_data_for_price = []
    for phrase, price in data_for_price.items():
        temp = {'phrase': phrase,
                'MaxCostPerClick': max(price.values())}

        temp.update(price)
        insert_data_for_price.append(temp)

    dao.insert_into_table('topprice', insert_data_for_price)

    # Write to TopMSVPrice.csv with limit 100
    with open(path_top_price, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=view.view_top_price)
        writer.writeheader()
        get_phrases = dao.get_top_phrase_by_price_with_limit(limit_for_top)

        for line in get_phrases:
            # Overlay bd schema to data
            writer.writerow(dict(zip(view.view_top_price, line)))


def task_2():
    dao.create_bd_regionality()

    # Define regionality
    update_data = []
    get_all = dao.get_all_fields_instead_of_total_from_top_click()
    for row in get_all:
        requests = row[1:6]
        # Calculate Percent of requests of a phrase
        temp = [item * 1. / sum(requests) for item in requests]
        # Subtract min value from
        temp = [item - min(temp) for item in temp]
        # Add phrase
        temp.insert(0, row[0])
        # Overlay bd schema to data
        update_data.append(dict(zip(view.view_regionality, temp)))
    dao.insert_into_table('regionality', update_data)

    # Write to Regionality.csv
    with open(path_regionality, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=view.view_regionality)
        writer.writeheader()
        get_phrases = dao.get_all_from_table('regionality')

        for line in get_phrases:
            # Overlay bd schema to data
            writer.writerow(dict(zip(view.view_top_price, line)))

    # Define highest regoinality
    output_data = []
    # Select locodes from view
    for locode in view.view_regionality[1:]:
        output_data.append([(
            "'{1}' Phrases with the highest Regionality score for "
            "'{0}'".format(locode, limit_for_regionality),)])
        output_data.append(
            dao.get_sort_regionality_by_locode_with_limit(
                locode, limit_for_regionality))

    # Write to HighestRegionality.csv
    with open(path_highest_regionality, 'w') as csvfile:
        writer = csv.writer(csvfile)
        for lines in output_data:
            for line in lines:
                writer.writerow(line)


def main():
    task_0()
    task_1()
    task_2()


if __name__ == "__main__":
    main()
