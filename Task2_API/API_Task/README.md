🍽 Meal API Project

What is this?



A small Python project that fetches meal data from a public API, processes it, and saves it in neat JSON files.

It shows all meals, and also filters Indian and Chinese meals.



API Used



TheMealDB API

&nbsp;– public and free, no API key needed.



Setup



Make sure Python is installed (3.7+).



Install requests library:



pip install requests





Download the project files or clone the repository.



How to Run

python your\_script\_name.py



What happens when you run it:



Fetches meals from the API



Renames and selects important fields: Meal\_Name, Meal\_Category, Meal\_Area, Meal\_Link\_Youtube



Filters meals into Indian and Chinese



Counts total meals and prints results



Saves the data in:



meal\_combine.json → all meals



Indian\_Meals.json → Indian meals



Chinese\_Meals.json → Chinese meals



Output Example

{

&nbsp; "Meal\_Name": "Chicken Handi",

&nbsp; "Meal\_Category": "Chicken",

&nbsp; "Meal\_Area": "Indian",

&nbsp; "Meal\_Link\_Youtube": "https://www.youtube.com/watch?v=example"

}



