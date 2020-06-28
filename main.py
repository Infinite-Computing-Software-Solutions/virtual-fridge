# #sample data
# #ingredients in fridge
# fridgeingredients = {
# 	"cheese": {"quantity": 300,"unit": "g"},
# 	"ham": {"quantity": 500,"unit": "g"},
# 	"pasta": {"quantity": 1000,"unit": "g"}
# }
# #what we want after extracting:
# recipes = {
# 	"mac n cheese": {
# 		"cheese": {"quantity": 300,"unit": "g"},
# 		"pasta": {"quantity": 1000,"unit": "g"}
# 	},
# 	"sandwich": {
# 		"cheese": {"quantity": 300,"unit": "g"},
# 		"ham": {"quantity": 500,"unit": "g"},
# 		"bread": {"quantity": 300, "unit":"g"}
# 	},
# 	"guacamole": {
# 		"avacado": {"quantity": 200,"unit": "g"},
# 		"tomato": {"quantity": 400,"unit": "g"},
# 		"bread": {"quantity": 300, "unit":"g"}
# 	}
# }
# #actual database recipe structure after reading:
# recipes = {'MAsYQW4qNmX4pVkqXCy': {'author': 'kirito', 'description': 'something', 'image': 'Chickeneso1229a.jpg', 'ingredients': {"cheese": {"quantity": 300,"unit": "g"},
# 		"pasta": {"quantity": 1000,"unit": "g"}}, 'instructions': 'just eat it', 'name': 'mac n cheese'},
# 'MAsYaaaAbYI_5L1nqS8': {'author': 'kirito', 'description': 'random', 'image': 'Chickeneso1229a.jpg', 'ingredients': {"cheese": {"quantity": 300,"unit": "g"},
# 		"ham": {"quantity": 500,"unit": "g"},
# 		"bread": {"quantity": 300, "unit":"g"}}, 'instructions': 'figure it out', 'name': 'sandwich'}}
# #database structure -> usable structure
# def extractRecipes(recipes):
# 	r = {}
# 	for recipek,recipe in recipes.items():
# 		r[recipe['name']] = recipe['ingredients']
# 	return r

# def searchrecipes(fridgeingredients, recipes):
# 	maxmatch = []
# 	minmiss = []
# 	for recipek in recipes:
# 		matched = 0
# 		missing = 0
# 		for ingredientk in recipes[recipek]:
# 			if ingredientk in fridgeingredients:
# 				if int(recipes[recipek][ingredientk]["quantity"]) <= int(fridgeingredients[ingredientk]["quantity"]):
# 					matched += 1
# 				else:
# 					missing += 1
# 			else:
# 				missing += 1
# 		maxmatch.append([matched, recipek])
# 		minmiss.append([missing, recipek])
# 	maxmatch = sorted(maxmatch, reverse = 1)
# 	minmiss = sorted(minmiss)
# 	#maxmatch: uses as many ingredients in the fridge as possible
# 	'''
# 	return [r[1] for r in maxmatch]
# 	'''
# 	#minmiss: forces the person to buy as little ingredients as possible
# 	return [r[1] for r in minmiss]

# recipes = extractRecipes(recipes)
# print(searchrecipes(fridgeingredients,recipes))

			