import csv,sys,os
project_dir = "/home/cosmeticsApp/application"
sys.path.append(project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'backendApp.settings'

import django
django.setup()

from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from modelsViews.models import(warningsModel,
							   ingredientsModel,
							   ingredientFunctionsModel,
							   banedSubstancesModel, 
							   restrictedSubstancesModel,
							   colorantsModel,
							   preservativesModel,
							   uvFiltersModel)

def importIngredients():
	
	savedIngredients = 0
		
	def getFunctionId(functionName):
		try:
			fetchedFunction = (ingredientFunctionsModel.objects.values('id').get(name=functionName))
			fetchedFunctionId = fetchedFunction.get('id')
		except ObjectDoesNotExist:
			print("Function: " + functionName + " does not exist")
			fetchedFunctionId = -1
		return(fetchedFunctionId)
	
	def getIngredientId(ingredientReferenceNumber):
		try:
			fetchedIngredient = (ingredientsModel.objects.values('id').get(referenceNumber=ingredientReferenceNumber))
			fetchedIngredientId = fetchedIngredient.get('id')
		except ObjectDoesNotExist:
			print("Ingredient: " + str(ingredientReferenceNumber) + " does not exist")
			fetchedIngredientId = -1
		
		return(fetchedIngredientId)
	def getWarningId(warningReferenceNumber):
		try:
			fetchedWarning = (warningsModel.objects.values('id').get(referenceNumber=warningReferenceNumber))
			fetchedWarningId = fetchedWarning.get('id')
		except ObjectDoesNotExist:
			print("Warning: " + str(warningReferenceNumber) + " does not exist")
			fetchedWarningId = -1
		
		return(fetchedWarningId)
	
	def prepareIngredientConfig(restriction):
		riskLevel   = 0
		hittedRules = 0
		age         = 0
		checkForAdditionalRestrictions = False
		
		def getRestricted(referenceNumber):
			try:
				fetchedData = (restrictedSubstancesModel.objects.values('other', 'wordingWarnings').get(referenceNumber=referenceNumber))
			except ObjectDoesNotExist:
				print("Restriction: " + referenceNumber + " does not exist")
				fetchedData = {'other':'','wordingWarnings':''}
			return(fetchedData)
		def getColorant(referenceNumber):
			try:
				fetchedData = (colorantsModel.objects.values('other','wordingWarnings').get(referenceNumber=referenceNumber))
			except ObjectDoesNotExist:
				print("Colorant: " + referenceNumber + " does not exist")
				fetchedData = {'other':'','wordingWarnings':''}
			return(fetchedData)
		def getPreservative(referenceNumber):
			try:
				fetchedData = (preservativesModel.objects.values('other', 'wordingWarnings').get(referenceNumber=referenceNumber))
			except ObjectDoesNotExist:
				print("Preservative: " + referenceNumber + " does not exist")
				fetchedData = {'other':'','wordingWarnings':''}
			return(fetchedData)
		def getUVFilter(referenceNumber):
			try:
				fetchedData = (uvFiltersModel.objects.values('other', 'wordingWarnings').get(referenceNumber=referenceNumber))
			except ObjectDoesNotExist:
				print("UV Filter: " + referenceNumber + " does not exist")
				fetchedData = {'other':'','wordingWarnings':''}
			return(fetchedData)
		def loopThrueRules(warningTextIn):
			warningText = warningTextIn.upper()
			tempRulesSet = 0
			tempRisk     = 0
			if 'adult use only'.upper() in warningText:
				tempRulesSet |= 2**5
				tempRisk += 1
			if 'by adults only'.upper() in warningText:
				tempRulesSet |= 2**5
				tempRisk += 1
			if 'children is not advisable'.upper() in warningText:
				tempRulesSet |= 2**6
				tempRisk += 1
			if 'use a pea-sized amount for'.upper() in warningText:
				tempRulesSet |= 2**7
				tempRisk += 1
			if 'Keep out of reach of chindren'.upper() in warningText:
				tempRulesSet |= 2**8
				tempRisk += 1
			if 'powder away from children'.upper() in warningText:
				tempRulesSet |= 2**8
				tempRisk += 1
			if 'Not to be used in oral and lip products'.upper() in warningText:
				tempRulesSet |= 2**9
				tempRulesSet |= 2**10
				tempRisk += 1
			if 'Not to be used in oral products and in products applied on mucous membranes'.upper() in warningText:
				tempRulesSet |= 2**9
				tempRulesSet |= 2**10
				tempRisk += 1
			if 'Not to be used in lip products, oral products and spray products'.upper() in warningText:
				tempRulesSet |= 2**9
				tempRulesSet |= 2**10
				tempRulesSet |= 2**26
				tempRisk += 1
			if 'Not to be used in oral producrs and eye products'.upper() in warningText:
				tempRulesSet |= 2**9
				tempRulesSet |= 2**12
				tempRisk += 1
			if 'Rinse eyes immediately'.upper() in warningText:
				tempRulesSet |= 2**12
				tempRisk += 1
			if 'Avoid contact with eyes'.upper() in warningText:
				tempRulesSet |= 2**12
				tempRisk += 1
			if 'Not to be used on eyebrows'.upper() in warningText:
				tempRulesSet |= 2**13
				tempRisk += 1
			if 'not use to dye eyelashes or eyebrows'.upper() in warningText:
				tempRulesSet |= 2**13
				tempRisk += 1
			if 'Not to be used in leave-on products designed for application'.upper() in warningText:
				tempRulesSet |= 2**14
				tempRisk += 1
			if 'For leave-on products designed for children'.upper() in warningText:
				tempRulesSet |= 2**14
				tempRisk += 1
			if 'to be used in applications that may lead to exposure'.upper() in warningText:
				tempRulesSet |= 2**15
				tempRisk += 1
			if 'to be used on peeling or irritated'.upper() in warningText:
				tempRulesSet |= 2**16
				tempRisk += 1
			if 'Avoid contact with eyes or damaged skin'.upper() in warningText:
				tempRulesSet |= 2**16
				tempRulesSet |= 2**12
				tempRisk += 1
			if 'not apply to irritated or damaged'.upper() in warningText:
				tempRulesSet |= 2**16
				tempRisk += 1
			if 'black henna'.upper() in warningText:
				tempRulesSet |= 2**17
				tempRisk += 1
			if 'have a rash'.upper() in warningText:
				tempRulesSet |= 2**18
				tempRisk += 1
			if 'can cause severe allergic'.upper() in warningText:
				tempRulesSet |= 2**19
				tempRisk += 1
			if 'Can cause allergic'.upper() in warningText:
				tempRulesSet |= 2**19
				tempRisk += 1
			if 'professional use'.upper() in warningText:
				tempRulesSet |= 2**20
				tempRisk += 1
			if 'suitable gloves'.upper() in warningText:
				tempRulesSet |= 2**22
				tempRisk += 1
			if 'Rinse well'.upper() in warningText:
				tempRulesSet |= 2**23
				tempRisk += 1
			if 'formation of nitrosamines'.upper() in warningText:
				tempRulesSet |= 2**24
				tempRisk += 1
			if 'substances forming nitrosamines'.upper() in warningText:
				tempRulesSet |= 2**24
				tempRisk += 1
			if 'Do not use with nitrosating'.upper() in warningText:
				tempRulesSet |= 2**24
				tempRisk += 1
			if 'in nitrite-free containers'.upper() in warningText:
				tempRulesSet |= 2**25
				tempRisk += 1
			if 'to be used in aerosol'.upper() in warningText:
				tempRulesSet |= 2**26
				tempRisk += 1
			if 'to be used in sprays'.upper() in warningText:
				tempRulesSet |= 2**26
				tempRisk += 1
			if 'ph '.upper() in warningText:
				tempRulesSet |= 2**27
				tempRisk += 1
			if 'ph>'.upper() in warningText:
				tempRulesSet |= 2**27
				tempRisk += 1
			if 'ph='.upper() in warningText:
				tempRulesSet |= 2**27
				tempRisk += 1
			if 'ph<'.upper() in warningText:
				tempRulesSet |= 2**27
				tempRisk += 1
			if 'free from chromate'.upper() in warningText:
				tempRulesSet |= 2**28
				tempRisk += 1
			if 'ree from cyanide'.upper() in warningText:
				tempRulesSet |= 2**29
				tempRisk += 1
			if 'Contains alcakali'.upper() in warningText:
				tempRulesSet |= 2**30
				tempRisk += 1
			if 'Contains Benzophenone'.upper() in warningText:
				tempRulesSet |= 2**31
				tempRisk += 1
			if 'Contains Thiomersal'.upper() in warningText:
				tempRulesSet |= 2**32
				tempRisk += 1
			if 'Contains Phenylmercuric'.upper() in warningText:
				tempRulesSet |= 2**33
				tempRisk += 1
			if 'Contains phenylenediamines'.upper() in warningText:
				tempRulesSet |= 2**34
				tempRisk += 1
			if 'Contains chloroacetamide'.upper() in warningText:
				tempRulesSet |= 2**35
				tempRisk += 1
			if 'Contains glutaral'.upper() in warningText:
				tempRulesSet |= 2**36
				tempRisk += 1
			if 'Contains Chlorobutanol'.upper() in warningText:
				tempRulesSet |= 2**37
				tempRisk += 1
			if 'Contains Dichlorophen'.upper() in warningText:
				tempRulesSet |= 2**38
				tempRisk += 1
			if 'Contains resorcinol'.upper() in warningText:
				tempRulesSet |= 2**39
				tempRisk += 1
			if 'Contains formaldehyde'.upper() in warningText:
				tempRulesSet |= 2**40
				tempRisk += 1
			if 'Contains ammonium monofluorophosphate'.upper() in warningText:
				tempRulesSet |= 2**41
				tempRisk += 1
			if 'Contains ammonium fluoride'.upper() in warningText:
				tempRulesSet |= 2**42
				tempRisk += 1
			if 'Contains sodium monofluorophosphate'.upper() in warningText:
				tempRulesSet |= 2**43
				tempRisk += 1
			if 'Contains potassium monofluorophosphate'.upper() in warningText:
				tempRulesSet |= 2**44
				tempRisk += 1
			if 'Contains calcium fluoride'.upper() in warningText:
				tempRulesSet |= 2**45
				tempRisk += 1
			if 'Contains sodium fluoride'.upper() in warningText:
				tempRulesSet |= 2**46
				tempRisk += 1
			if 'Contains potassium'.upper() in warningText:
				tempRulesSet |= 2**47
				tempRisk += 1
			if 'Contains stannous fluoride'.upper() in warningText:
				tempRulesSet |= 2**48
				tempRisk += 1
			if 'Contains Cetylamine hydrofluoride'.upper() in warningText:
				tempRulesSet |= 2**49
				tempRisk += 1
			if 'blindness'.upper() in warningText:
				tempRulesSet |= 2**50
				tempRisk += 1
			if 'Avoid skin contact'.upper() in warningText:
				tempRulesSet |= 2**51
				tempRisk += 1
			if 'After colouring your hair'.upper() in warningText:
				tempRulesSet |= 2**52
				tempRisk += 1
			if 'Can cause blindness'.upper() in warningText:
				tempRulesSet |= 2**53
				tempRisk += 1
			if 'Avoid skin contact'.upper() in warningText:
				tempRulesSet |= 2**54
				tempRisk += 1
			if 'after colouring your hair'.upper() in warningText:
				tempRulesSet |= 2**55
				tempRisk += 1
			
			return(tempRulesSet,tempRisk)
		
		def loopThrueAgeRules(warningTextIn):
			warningText = warningTextIn.upper()
			ageRule = 0
			if 'under 3 years of'.upper() in warningText:
				ageRule = 3
			if 'under three years of'.upper() in warningText:
				ageRule = 3
			if '3 years of age'.upper() in warningText:
				ageRule = 3
			if 'the age of 16'.upper() in warningText:
				ageRule = 16
			if 'under 18 years'.upper() in warningText:
				ageRule = 18
			return(ageRule)
		
		restrictionStruc = restriction.split("/")
		#II - BANNED, III - RESTRICTED, IV - COLORANT, V - PRESERVATIVE, VI - UV filter
		if restrictionStruc[0]   == "II":
			hittedRules |= 2**0
			riskLevel += 100
		elif restrictionStruc[0] == "III":
			hittedRules |= 2**1
			riskLevel += 1
			checkForAdditionalRestrictions = True
			if restrictionStruc[1] == "I":
				additionalRestrictions = getRestricted(restrictionStruc[2])
			else:
				additionalRestrictions = getRestricted(restrictionStruc[1])
		elif restrictionStruc[0] == "IV":
			riskLevel += 1
			hittedRules |= 2**2
			checkForAdditionalRestrictions = True
			if restrictionStruc[1] == "I":
				additionalRestrictions = getColorant(restrictionStruc[2])
			else:
				additionalRestrictions = getColorant(restrictionStruc[1])
		elif restrictionStruc[0] == "V":
			riskLevel += 1
			hittedRules |= 2**3
			checkForAdditionalRestrictions = True
			if restrictionStruc[1] == "I":
				additionalRestrictions = getPreservative(restrictionStruc[2])
			else:
				additionalRestrictions = getPreservative(restrictionStruc[1])
		elif restrictionStruc[0] == "VI":
			riskLevel += 1
			hittedRules |= 2**4
			checkForAdditionalRestrictions = True
			if restrictionStruc[1] == "I":
				additionalRestrictions = getUVFilter(restrictionStruc[2])
			else:
				additionalRestrictions = getUVFilter(restrictionStruc[1])
		
		if checkForAdditionalRestrictions:		
			if type(additionalRestrictions) is dict: 
				if additionalRestrictions.get('other') != None:
					tempHittedRules, tempRiskLevel = loopThrueRules(additionalRestrictions.get('other'))
					age = loopThrueAgeRules(additionalRestrictions.get('other'))
					riskLevel += tempRiskLevel
					hittedRules |= tempHittedRules
				if additionalRestrictions.get('wordingWarnings') != None:
					tempHittedRules, tempRiskLevel = loopThrueRules(additionalRestrictions.get('wordingWarnings'))
					tempAge = loopThrueAgeRules(additionalRestrictions.get('other'))
					if age < tempAge:
						age = tempAge
					riskLevel += tempRiskLevel
					hittedRules |= tempHittedRules
				
		return(riskLevel, hittedRules, age)
	
	
	ingredients = csv.reader(open("substancesCSV/ingredients.csv"), 
								  quotechar='"', delimiter=",", 
					  			  quoting=csv.QUOTE_ALL, skipinitialspace=True)
	lineNo = 1 
	for row in ingredients:
		lineNo +=1
		if len(row) != 10:
			print("length error in line: " + str(lineNo) + " refNO: " + str(row[0]))
			continue
		ingredient 		 = ingredientsModel()	
		
		ingredient.referenceNumber      = row[0]
		ingredient.name                 = row[1]
		ingredient.casNumber            = row[4]
		ingredient.ecNumber             = row[5]
		ingredient.description          = row[6].replace("\n", " ")
		ingredient.restriction          = row[7].replace("\n", " ")
		ingredient.updateDate           = row[9]
		ingredient.riskLevel            = 1
		
		wFunctions   = row[8].replace("\n", " ")
		wRiskLevel   = ingredient.riskLevel
		wAge         = 0
		wHittedRules = 0
		
		try:
			ingredient.save()
			savedIngredients += 1
			if savedIngredients % 100 == 0:
				print(savedIngredients)
		except IntegrityError as e:
			#print ("Skipped duplicate: " + ingredient.referenceNumber)
			continue
			
		wIngredientId = getIngredientId(ingredient.referenceNumber)
		
		#Create restrictions in config table
		if ingredient.restriction != "":
			numberOfPossibleRestrictions = 1
			numberOfPossibleRestrictions += ingredient.restriction.count(" ")
			if numberOfPossibleRestrictions == 1:
				wTempRiskLevel, wTempHittedRules, wAge = prepareIngredientConfig(ingredient.restriction)
				wRiskLevel += wTempRiskLevel
				wHittedRules |= wTempHittedRules
			else:
				restrictionsList = ingredient.restriction.split(" ")
				while numberOfPossibleRestrictions != 0:
					numberOfPossibleRestrictions -= 1
					wTempRiskLevel, wTempHittedRules, wTempAge = prepareIngredientConfig(restrictionsList[numberOfPossibleRestrictions])
					wRiskLevel += wTempRiskLevel
					wHittedRules |= wTempHittedRules
					if wAge < wTempAge:
						wAge = wTempAge
		
		#Update risk level if needed
		if wRiskLevel > 1:
			if wRiskLevel > 3:
				wRiskLevel = 3
			try:
				ingredientsModel.objects.filter(id=wIngredientId).update(riskLevel=wRiskLevel)
			except IntegrityError as e:
				print("Did not changed score "+ str(wRiskLevel) + " to " + str(ingredient.referenceNumber))
			
			
		#Add functions
		numberOfFunctions = 1 
		numberOfFunctions += wFunctions.count(',')
		if numberOfFunctions == 1:
			if wFunctions != "":
				tempFunctId = getFunctionId(wFunctions)
				if tempFunctId != -1:
					try:
						ingredient.functions.add(tempFunctId)
					except IntegrityError as e:
						print("Did not added function "+ wFunctions + " to " + str(ingredient.referenceNumber))
		else:
			functionsList = wFunctions.split(", ")
			while numberOfFunctions != 0:
				numberOfFunctions -= 1
				if functionsList[numberOfFunctions] != "":
					tempFunctId = getFunctionId(functionsList[numberOfFunctions])
					if tempFunctId != -1:
						try:
							ingredient.functions.add(tempFunctId)
						except IntegrityError as e:
							print("Did not added function "+functionsList[numberOfFunctions] + " to " + str(ingredient.referenceNumber))
		
		#Add warnings
		ruleRefNumber = 1
		while(wHittedRules != 0):
			if wHittedRules % 2 != 0:
				tempWarningId = getWarningId(str(ruleRefNumber))
				if tempWarningId != -1:
					try:
						ingredient.warnings.add(tempWarningId)
					except IntegrityError as e:
						print("Did not added warning "+ str(ruleRefNumber) + " to " + str(ingredient.referenceNumber))
			ruleRefNumber += 1
			wHittedRules >>= 1	
			
		#Add age
		if wAge != 0:
			try:
				ingredientsModel.objects.filter(id=wIngredientId).update(cannotBeUsedUnderAge=wAge)
			except IntegrityError as e:
				print("Did not changed age "+ str(wAge) + " to " + str(ingredient.referenceNumber))

importIngredients()