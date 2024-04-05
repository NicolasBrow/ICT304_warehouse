###
# Created by Matthew Gilham
# Purpose: Assignment One of ICT304
# Main script of the project
# Last Updated: 01/04/2024

# imports
from funcs import *
import os


def main():
    # Get the current directory
    currentDirectory = os.getcwd()

    # Define the folder name
    folderName = "Database"

    # Construct the file paths
    invoicePath = os.path.join(currentDirectory, folderName, 'Invoices.csv')
    inventoryPath = os.path.join(currentDirectory, folderName, 'Inventory.csv')
    layoutPath = os.path.join(currentDirectory, folderName, 'Layout.csv')

    # Read invoices from DB
    invoices = read_invoice_csv(invoicePath)

    # Predictor
    # Currently does not work and does nothing
    response = prompt_yes_no("Do you want to update and predict new stock amounts? (yes/no): ")
    #if response:
        # Train
        #train(invoices)

        # Get .pkl
        #TO DO

        # Predict
        #TO DO
        # predictions = predict()

    predictions = [
        [1, 2],
        [3, 4],
        [5, 6],
        [7, 8],
        [9, 10]
    ]

    # Read inventory from DB
    inventory = read_inventory_csv(inventoryPath)

    # Update inventory
    update_inventory(inventory, predictions)

    response = prompt_yes_no("Do you want to update the inventory database? (yes/no): ")
    if response:
        # Write inventory to database
        write_inventory_csv(inventoryPath, inventory)

    # Check stock v min
    toOrder = calculate_stock_difference(inventory)

    response = prompt_yes_no("Do you want to print purchase orders? (yes/no): ")
    if response:
        # Print PO's
        purchase_order_printer(toOrder)

    response = prompt_yes_no("Do you want to reorganize stock locations? (yes/no): ")
    if response:
        # Create inventory queue
        inventoryQueue = create_inventory_queue(inventory, invoices)

        # Read in Bays into queues
        largeQueue, smallQueue = read_bays_csv(layoutPath)

        # assign bays
        categorizedItems = categorize_items(inventoryQueue, largeQueue, smallQueue, inventory)

        response = prompt_yes_no("Do you want to print stock locations? (yes/no): ")
        if response:
            # bay printer
            bay_printer(categorizedItems)


if __name__ == "__main__":
    main()
