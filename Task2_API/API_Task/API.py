import requests
import json

URL="https://www.themealdb.com/api/json/v1/1/search.php?s=chicken"

res=requests.get(URL)
data=res.json()

#Rename fields and Extract specific fields
combine=[]
for item in data['meals']:

    combine.append({
        "Meal_Name":item['strMeal'],
        "Meal_Category":item['strCategory'],
        "Meal_Area":item['strArea'],
        "Meal_Link_Youtube":item['strYoutube']
    })

with open ("meal_combine.json","w") as file:
   json.dump(combine,file,indent=4)

#Filter data based on a condition and Group related data
Indian_Meals=[]
for item in combine:
    if(item['Meal_Area']=='Indian'):
        Indian_Meals.append(item)
with open ("Indian_Meals.json","w") as file:
    json.dump(Indian_Meals,file,indent=4)

Chinese_Meals=[]
for item in combine:
    if(item['Meal_Area']=='Chinese'):
        Chinese_Meals.append(item)

with open ("Chinese_Meals.json","w") as file:
    json.dump(Chinese_Meals,file,indent=4)

print("Status_Code",res.status_code)
#Count items 
count_of_Combine=len(combine)
print("Number of Total Meals : ",count_of_Combine)

count_of_Indian_Meals=len(Indian_Meals)
print("Number of Indian Meals : ",count_of_Indian_Meals)

count_of_Chinese_Meals=len(Chinese_Meals)
print("Number of Chinese Meals : ",count_of_Chinese_Meals)
  


