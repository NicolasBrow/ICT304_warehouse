###
# Created by Matthew Gilham
# Purpose: Assignment One of ICT304
# Functions script
# Last Updated:01/04/2024

# Current functions list
# read_invoice_csv: reads invoices from a designated csv
# prompt_yes_no: prompts user for yes or no. Returns answer as true/false
# read_inventory_csv: reads inventory from a designated csv
# update_inventory: updates inventory array with predictions from predictor
# write_inventory_csv: override inventory .csv with updated version
# calculate_stock_difference: checks for currentStock below minStock
# purchase_order_printer: prints the items to be ordered
# create_inventory_queue: creates the invetory queue based on frequency
# read_bays_csv: reads in the bays csv
# catergorize_items: assigns items to bays
# bay_printer: formats and prints bay locations and stock item in that bay

# imports
import csv
from datetime import datetime
from collections import deque
from collections import Counter

# reads invoices from a designated csv
def read_invoice_csv(invoicePath):
    invoice = []
    with open(invoicePath, 'r', newline='') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if None in row:
                continue
            invoice_id, customer_id, item_id, item_name, item_desc, item_price, item_qty, total_cost, date_invoiced = row
            try:
                invoice_id = int(invoice_id)
                customer_id = int(customer_id)
                item_id = int(item_id)
                item_price = float(item_price)
                item_qty = int(item_qty)
                total_cost = float(total_cost)
                date_invoiced = datetime.strptime(date_invoiced, '%Y-%m-%d').date()
            except ValueError:
                print(f"Error processing invoices row: {row}")
                continue
            invoice.append([invoice_id, customer_id, item_id, item_name, item_desc, item_price, item_qty, total_cost, date_invoiced])
    return invoice

# prompts user for a yes/no
def prompt_yes_no(prompt_message):
    while True:
        user_input = input(prompt_message).strip().lower()
        if user_input == 'yes' or user_input == 'y':
            return True
        elif user_input == 'no' or user_input == 'n':
            return False
        else:
            print("Please enter 'yes' or 'no'.")

# reads inventory from a designated csv
def read_inventory_csv(inventoryPath):
    inventory = []
    with open(inventoryPath, 'r', newline='') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            try:
                item_id, item_name, item_desc, item_price, current_stock, min_stock, length, width, height = row
                item_id = int(item_id)
                item_price = float(item_price.replace('$', ''))
                current_stock = int(current_stock)
                if min_stock == '':
                    min_stock = -1
                else:
                    min_stock = int(min_stock)
                length = int(length)
                width = int(width)
                height = int(height)
            except ValueError:
                print(f"Error processing inventory row: {row}")
                continue
            inventory.append([item_id, item_name, item_desc, item_price, current_stock, min_stock, length, width, height])

    return inventory

# updates inventory array with predictions from predictor
def update_inventory(inventory, predictions):
    for prediction in predictions:
        stock_id, min_stock = prediction
        for item in inventory:
            if item[0] == stock_id:
                item[5] += min_stock
                break

# override inventory .csv with updated version
def write_inventory_csv(filename, inventory):
    headers = ["itemID", "itemName", "itemDesc", "itemPrice", "currentStock", "minStock", "length", "width", "height"]
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        for item in inventory:
            writer.writerow(item)

# calculate difference between current stock and minStock
def calculate_stock_difference(inventory):
    stock_difference = []
    for item in inventory:
        current_stock = item[4]
        min_stock = item[5]
        if current_stock < min_stock:
            difference = min_stock - current_stock
            stock_difference.append([item[0], difference])
    return stock_difference

# printer for stock to be ordered
def purchase_order_printer(toOrder):
    print("\n" + "Items that need to be ordered are as follows: " + "\n")
    for item in toOrder:
        print("Order " + str(item[1]) + " of item with itemID of " + str(item[0]))

# create invetory queue
def create_inventory_queue(inventory, invoices):
    item_counts = {}

    for item in inventory:
        item_id = item[0]

        count = 0

        for invoice in invoices:
            if item_id == invoice[2]:
                count += 1

        item_counts[item_id] = count

    sorted_items = sorted(item_counts.items(), key=lambda x: x[1], reverse=True)

    inventory_queue = deque()

    for item_id, _ in sorted_items:
        inventory_queue.append(item_id)

    return inventory_queue

# reads warehouse bays into queues from designated csv
def read_bays_csv(layoutPath):
    large_queue = deque()
    small_queue = deque()

    with open(layoutPath, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for index, row in enumerate(reader):
            if not row:
                continue
            bay_location = row[0]
            if index < 10:
                large_queue.appendleft(bay_location)
            else:
                small_queue.appendleft(bay_location)

    return large_queue, small_queue

# assign items to bays
def categorize_items(inventoryQueue, largeQueue, smallQueue, inventory):
    categorizedItems = []

    while inventoryQueue:
        item_id = inventoryQueue[0]
        item_data = next((x for x in inventory if x[0] == item_id), None)

        if item_data:
            length, width, height = item_data[6:9]
            min_stock = int(item_data[5])
            total_mass = (length * width * height) * (min_stock * 1.1)

            if total_mass > 125000 or length > 500 or width > 500 or height > 500:
                if largeQueue:
                    bay_location = largeQueue[0]
                    largeQueue.popleft()
                    categorizedItems.append([item_id, bay_location])
                    inventoryQueue.popleft()
                else:
                    break
            else:
                if smallQueue:
                    bay_location = smallQueue[0]
                    smallQueue.popleft()
                    categorizedItems.append([item_id, bay_location])
                    inventoryQueue.popleft()
                else:
                    break
        else:
            inventoryQueue.pop(0)

    return categorizedItems

# print out bay locations
def bay_printer(categorizedItems):
    for item in categorizedItems:
        print("Item: " + str(item[0]) + " is to be located in bay: " + str(item[1]))