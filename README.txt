In order to run the script in the format

python payment_engine.py transactions.csv > client_account.csv

you will need to add the PaymentProcessor directory to your PYTHONPATH.
As suggested I used pandas for the csv file handling so this will need to be installed.  This can be done by

pip install -r requirements.txt

Both the above install and the program should be invoked from the PaymentProcessor/TranactionEngine directory.

General Design
==============
The payment_engine.py file simply reads the csv into a TransactionList object, creates an empty AccountManager
and calls the TransactionList process() method. After the process has completed it outputs the accounts from the
AccountManager.
The AccountManager holds the accounts for the bank.  I expect in a real application it would be an interface to
a database.  Accounts are accessed by client id and if none exist one is created and returned.
The TransactionList contains the contents of the transaction.csv file in the form of a pandas DataFrame.
When instructed it processes itself by going through each row in the list.  It creates a transaction object
with all but the client id which it uses to get an account.  It then instructs the transaction objsct to apply
itself to the account.
The transaction object's apply_to() method contains the transaction logic i.e. which method in the account to
call and if the transaction completes and could be disputed its data is saved in the account.
The Account object has methods corresponding to each transaction types.  It implements them according to the
spec by moving funds to and from held and available as appropriate.  The tx id and amount for each possibly
disputed transaction are stored in the account.  If a transaction is disputed then the data is moved to a
disputed list where it waits until it is resolved or chargedback at which point it is deleted from the account.

Correctness (and completeness)
==============================
I believe I have covered all the requirements.  I set up some unit tests for the Transaction object mainly to
show that it could handle the different types and also for dealing with incorrect inputs.  The latter being
something that could potentially crash the program.  I considered setting up unit tests for the account object
as that performs the majority of the functionality but the methods are very simple and also apart from deposit()
they all require some preconditions and that was easier to do by using a transaction list and running the
program.  I created a number of different scenarios and put each in their own csv file.  These can be found in
the input_csv_files directory (the unit test file is in the tests directory).  The csv files contain scenarios
with regular transactions and with erroneous transactions.  Given more time I would have produced more
scenarios.

Efficiency
==========
I did spend some time considering efficiency.  The accounts are stored in the account manager in a dict with
the client id as the key and the account object itself as the value.  This duplicates client id but gives more
efficient search results than going through a list looking for an attribute of an object.
The TransactionList creates a Transaction first during which the input is checked.  Only if it is okay does it
get the account.
The necessary data for a disputable transaction is stored in the account. This is a key value of tx and amount.
A dispute has a client id so only that client's account needs to be searched for the transaction not the whole
list.
Creating an object instance for each transaction is inefficient but see maintainability.
Tests might prove that it would be more efficient to sort the transactions so the ones for each client are
grouped together to minimise the geting of the accounts.  This would definitely be the case if the accounts
were stored in a database.

Maintainability
===============
I have tried to keep each method as short as possible.  It is hopefully obvious what each one does from reading
the code.  I included docstrings but they are of more benefit to the caller of the method than anyone
maintaining it.
The TransactionList could have had the logic for applying transactions to the account but with different and more
complex transactions it would become bloated.  Having a transient Transaction object which has the transaction
logic inside seemed to make more sense.  Currently it is just one class covering all type with an if elif
construct but it is possible to have a separate subclass for each transaction type which defines its own logic.
It wasn't worth doing that for the small examples given.

Other
=====
The spec said the tx id is unique and I did not test for this just assumed it to be so.
The dispute description was not clear as it said the client was disputing the transaction whereas when I read
the description of dispute and chargeback it would appear that it is the person on the other end of the
transaction doing the dispute.  So only deposits are disputed and if the client has to give the money back
(chargeback) then the account is frozen as they are obviously untrustworthy.  That was how I interpreted it.
Withdrawls can't take the available funds below zero but I have allowed disputes to do this.
If a withdrawl is made before a deposit then the transaction fails and no account is created.
If a client id in a dispute/resole/chargeback does not match the original client id for the tx id then the
operation is not performed.
