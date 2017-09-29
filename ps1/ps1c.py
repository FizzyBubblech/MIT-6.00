# 6.00 Problem Set 1c
# Denis Savenkov
# ps1c.py

# Uses bisection search to find the fixed minimum monthly payment needed
# to finish paying off credit card debt within a year

# retrieve user input
out_bal = float(raw_input("Enter the outstanding balance on your credit card: "))
ann_rate = float(raw_input("Enter the annual credit card interest rate as a decimal: "))

# initialize state variables
bal = out_bal
epsilon = -0.1
low = bal / 12.0
high = (bal * (1 + (ann_rate / 12.0))**12) / 12.0
min_payment = (high + low) / 2.0

# calculate if the balance will be payed off in a year with current guess
month = 0
while month < 12:
    bal = bal * (1 + ann_rate / 12.0) - min_payment
    month += 1
    
# search for correct answer
while not epsilon < bal < 0 :
    if bal < 0:
        high = min_payment
    else:
        low = min_payment
    min_payment = (high + low) / 2.0
    bal = out_bal
    month = 0    
    while month < 12:
        bal = bal * (1 + ann_rate / 12.0) - min_payment
        month += 1

# round
min_payment = round(min_payment, 2)
bal = round(bal, 2)

# print out the result
print "RESULT"
print "Monthly payment to pay off debt in 1 year:", min_payment
print "Number of months needed:", month
print "Balance:", bal
