import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET =GSPREAD_CLIENT.open('love_sandwiches')

def  get_sales_data():
    """
    get slaes figure input from the user
    """
    while True:
        print("Please enter sales data from the list market.")
        print("Data should be six numbers, seperated by commas.")
        print("Example:10,20,30,40,50,60\n")
        data_str = input("Enter your data here:")
        sales_data=data_str.split(",")
        
        if validate_data(sales_data):
            print("data is valid!")
            break
    return sales_data
def validate_data(values):
    """
    Get sales figures input from the user.
    Run a while loop to collect a valid string of data from the user
    via the terminal, which must be a string of 6 numbers separated
    by commas. The loop will repeatedly request data, until it is valid.
    """
    
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"exactly 6 values required, you provided(len(values))"
            )
    except ValueError as e:
      print(f"invalid data: {e}, please try again\n")
      return False

    return True      

def update_sales_worksheet(data):
      """
      update sales worksheet, add new row with list data provided.
      """ 
      print("updating sales worksheet...\n")
      sales_worksheet = SHEET.worksheet("sales")
      sales_worksheet.append_row(data)
      print("sales worksheet updated successfully.\n")


def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.
    The surplus is defined as the sales figure subtracted from the stock:
    - Positive surplus indicates waste
    - Negative surplus indicates extra made when stock was sold out.
    """
    print("calculating surplus data...\n")
    stock=SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)

    return surplus_data 

def update_surplus_data(update_data):
    """
    This function takes the calculated surplus data
    as an argument and updates it
    """ 
    print("Updating Surplus Data..\n")
    surplus_sheet=SHEET.worksheet("surplus")
    surplus_sheet.append_row(update_data)
    print("Surplus Data Sussessfully Updated!..\n")



    
def main():
    """
    run all progam functions
    """
    data = get_sales_data()
    sales_data = [int(num)for num in data]
    update_sales_worksheet(sales_data)
    new_surplus_data = calculate_surplus_data(sales_data)
    
    update_surplus_data(new_surplus_data)

print("Welcome to sandwiches data automation")
main()