In order to run the script in the format
python payment_engine.py transactions.csv > client_account.csv 
you will need to add the PaymentProcessor directory to your PYTHONPATH.
As suggested I used pandas for the csv file handling so this will need to be installed.  This can be done by
pip install -r requirements.txt
Both the above install and the program should be invoked from the PaymentProcessor/TranactionEngine directory
