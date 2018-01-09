import csv,sys,os
project_dir = "/home/cosmeticsApp/application"
sys.path.append(project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'backendApp.settings'

import django
django.setup()

from django.db import IntegrityError

from modelsViews.models import (banedSubstancesModel, 
							    restrictedSubstancesModel,
							    colorantsModel,
								preservativesModel,
							    uvFiltersModel)

		
def importBannedSubstances():		
	banned = csv.reader(open("substancesCSV/substanceII.csv"), 
							 quotechar='"', 
							 delimiter=",", 
							 quoting=csv.QUOTE_ALL, 
							 skipinitialspace=True)	
	print ("Importing banned substances.. [START]")
	counter = 0
	for row in banned:
		lineNo +=1
		if len(row) != 12:
			print("length error in line: " + str(lineNo))
		post = banedSubstancesModel()
		post.referenceNumber = row[0]
		post.chemicalName    = row[1]
		post.casNumber       = row[2]
		post.ecNumber        = row[3]
		post.regulation      = row[4]
		post.regulatedBy     = row[5]
		post.otherDirective  = row[6]
		post.sccsOpinion     = row[7]
		post.iupacName       = row[8]
		post.ingredients     = row[9]
		post.cmr             = row[10]
		post.updateDate      = row[11]	
		try:
			post.save()
			counter += 1
		except IntegrityError as e:
			print ("Skipped duplicate: " + post.referenceNumber)
	print ("Importing banned substances.. [END]")
	return counter

def importRestrictedSubstances():
	restricted = csv.reader(open("substancesCSV/substanceIII.csv"), 
								 quotechar='"', 
								 delimiter=",", 
								 quoting=csv.QUOTE_ALL, 
								 skipinitialspace=True)	
	print ("Importing restricted substances.. [START]")
	counter = 0
	for row in restricted:
		post = restrictedSubstancesModel()
		post.referenceNumber = row[0]
		post.chemicalName    = row[1]
		post.glossary        = row[2]
		post.casNumber       = row[3]
		post.ecNumber        = row[4]
		post.productType     = row[5]
		post.maxConcetration = row[6]
		post.other           = row[7]
		post.wording         = row[8]
		post.regulation      = row[9]
		post.regulatedBy     = row[10]
		post.otherDirective  = row[11]
		post.sccsOpinion     = row[12]
		post.iupacName       = row[13]
		post.ingredients     = row[14]
		post.cmr             = row[15]
		post.updateDate      = row[16]	
		try:
			post.save()
			counter += 1
		except IntegrityError as e:
			print ("Skipped duplicate: " + post.referenceNumber)
	print ("Importing restricted substances.. [END]")
	return counter
	
def importColorants():
	colorants = csv.reader(open("substancesCSV/substanceIV.csv"), 
								quotechar='"', 
								delimiter=",", 
								quoting=csv.QUOTE_ALL, 
								skipinitialspace=True)	
	print ("Importing colorants.. [START]")
	counter = 0	
	for row in colorants:
		post = colorantsModel()
		post.referenceNumber = row[0]
		post.chemicalName    = row[1]
		post.colourIndex     = row[2]
		post.casNumber       = row[3]
		post.ecNumber        = row[4]
		post.colour          = row[5]
		post.productType     = row[6]
		post.maxConcentration= row[7]
		post.other           = row[8]
		post.wordingWarnings = row[9]
		post.regulation      = row[10]
		post.regulatedBy     = row[11]
		post.otherDirective  = row[12]
		post.sccsOpinion     = row[13]
		post.iupacName       = row[14]
		post.ingredients     = row[15]
		post.cmr             = row[16]
		post.updateDate      = row[17]	
		try:
			post.save()
			counter += 1
		except IntegrityError as e:
			print ("Skipped duplicate: " + post.referenceNumber)
	print ("Importing colorants.. [END]")
	return counter

def importPreservatives():
	preservatives = csv.reader(open("substancesCSV/substanceV.csv"), 
				    				quotechar='"', 
									delimiter=",", 
									quoting=csv.QUOTE_ALL, 
									skipinitialspace=True)	
	print ("Importing preservatives.. [START]")
	counter = 0	
	for row in preservatives:
		post = preservativesModel()
		post.referenceNumber = row[0]
		post.chemicalName    = row[1]
		post.glossary        = row[2]
		post.casNumber       = row[3]
		post.ecNumber        = row[4]
		post.productType     = row[5]
		post.maxConcentration= row[6]
		post.other           = row[7]
		post.wordingWarnings = row[8]
		post.regulation      = row[9]
		post.regulatedBy     = row[10]
		post.otherDirective  = row[11]
		post.sccsOpinion     = row[12]
		post.iupacName       = row[13]
		post.ingredients     = row[14]
		post.cmr             = row[15]
		post.updateDate      = row[16]	
		try:
			post.save()
			counter += 1
		except IntegrityError as e:
			print ("Skipped duplicate: " + post.referenceNumber)
	print ("Importing preservatives.. [END]")
	return counter
	
def importUVFilters():

	uvFilters = csv.reader(open("substancesCSV/substanceVI.csv"), 
			    				quotechar='"', 
								delimiter=",", 
								quoting=csv.QUOTE_ALL, 
								skipinitialspace=True)	
	print ("Importing UV fitlers.. [START]")
	counter = 0	
	for row in uvFilters:
		post = uvFiltersModel()
		post.referenceNumber = row[0]
		post.chemicalName    = row[1]
		post.glossary        = row[2]
		post.casNumber       = row[3]
		post.ecNumber        = row[4]
		post.productType     = row[5]
		post.maxConcentration= row[6]
		post.other           = row[7]
		post.wordingWarnings = row[8]
		post.regulation      = row[9]
		post.regulatedBy     = row[10]
		post.otherDirective  = row[11]
		post.sccsOpinion     = row[12]
		post.iupacName       = row[13]
		post.ingredients     = row[14]
		post.cmr             = row[15]
		post.updateDate      = row[16]	
		try:
			post.save()
			counter += 1
		except IntegrityError as e:
			print ("Skipped duplicate: " + post.referenceNumber)
	print ("Importing UV fitlers.. [END]")
	return counter	

bannedCounter        = importBannedSubstances()
restrictedCounter    = importRestrictedSubstances()
colorantsCounter     = importColorants()
preservativesCounter = importPreservatives()
uvFiltersCounter     = importUVFilters()

print(str(bannedCounter)        + " new banned substances added \n"     +
	  str(restrictedCounter)    + " new restricted substances added \n" +
	  str(colorantsCounter)     + " new colorant added \n"              +
	  str(preservativesCounter) + " new preservatices added \n"         +
	  str(uvFiltersCounter)     + " new uv filters added \n"            +
	  "[PROGRAM END]")