import csv,sys,os
project_dir = "/home/cosmeticsApp/application"
sys.path.append(project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'backendApp.settings'

import django
django.setup()

from django.db import IntegrityError

from modelsViews.models import (ingredientFunctionsModel, warningsModel)						
							
functions = csv.reader(open("substancesCSV/functions.csv"), quotechar='"', delimiter=",", quoting=csv.QUOTE_ALL, skipinitialspace=True)
counter = 0
for row in functions:
	post = ingredientFunctionsModel()
	post.name                  = row[0]
	post.description           = row[1]
	try:
		post.save()
		counter += 1
	except IntegrityError as e:
		print ("Skipped duplicate: " + post.name)
print (str(counter) + " new functions added")	

warnings = csv.reader(open("substancesCSV/warnings.csv"), quotechar='"', delimiter=",", quoting=csv.QUOTE_ALL, skipinitialspace=True)
counter = 0
for row in warnings:
	post = warningsModel()
	post.referenceNumber       = row[0]
	post.description           = row[1]
	try:
		post.save()
		counter += 1
	except IntegrityError as e:
		print ("Skipped duplicate: " + post.referenceNumber)
print (str(counter) + " new warnings added")	
