# 6.00 Problem Set 1b
# Denis Savenkov
# ps1b.py

# Determines fixed minimum monthly payment needed to finish paying off
# credit card debt in 1 year

# retrieve user input
out_bal = float(raw_input("Enter the outstanding balance on your credit card: "))
ann_rate = float(raw_input("Enter the annual credit card interest rate as a decimal: "))

# initialize variables
min_payment = 0
bal = out_bal
month_rate = ann_rate / 12.0

# create a loop to guess a minimal monthly payment
# needed to pay off balance in a year
while bal > 0:
    #increment a guess by 10 
    min_payment += 10
    #reset variables
    bal = out_bal
    month = 0
    
    #loop to calculate amount paid in a year with current guess
    while month < 12 and bal > 0:
        bal = bal * (1 + month_rate) - min_payment
        month += 1

# round balance
bal = round(bal, 2)

# print out result
print "RESULT"
print "Monthly payment to pay off debt in 1 year:", min_payment
print "Number of months needed:", month
print "Balance:", bal

