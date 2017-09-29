# 6.00 Problem Set 1a
# Denis Savenkov
# ps1a.py

# Determines remaining credit card balance after a year of making
# the minimum payment each month

# retrieve user input
out_bal = float(raw_input("Enter the outstanding balance on your credit card: "))
ann_rate = float(raw_input("Enter the annual credit card interest rate as a decimal: "))
min_rate = float(raw_input("Enter the minimum monthly payment rate as a decimal: "))

# initialuze variable to calculate total amount paid
total_paid = 0

# calculate for each month and print out
for month in range(1, 13):
    # calculate minimum monthly payment of balance at start of the month
    min_monthly = round(min_rate * out_bal, 2)
    
    # calculate interest paid
    int_paid = round((ann_rate / 12) * out_bal, 2)
    
    # calculate principal paid off
    pr_paid = round(min_monthly - int_paid, 2)
    
    # update balance
    out_bal -= pr_paid
    
    # update total amount paid
    total_paid += min_monthly
    
    print "Month: " + str(month)
    print "Minimum monthly payment: " + "$" + str(min_monthly)
    print "Principle paid: " + "$" + str(pr_paid)
    print "Remaining balance: " + "$" + str(out_bal)

# print out the result
print "RESULT"
print "Total amount paid: " + "$" + str(total_paid)
print "Remaining balance: " + "$" + str(out_bal)
