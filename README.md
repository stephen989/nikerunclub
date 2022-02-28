# nikerunclub
Python repository to download all your activity from the Nike Run Club API in case you don't trust Nike because they're snakes.

Run create_data.py to download all your runs. A single .json file which has a brief summary of each file will be downloaded. The entire workout details (pace, location etc.) for each run will then be downloaded and saved in .json files in your chosen directory. A bearer token is required to access your history. To get one, log in on Nike.com. Go to a "sensitive" page such as order history, look at the page source and search under Network for unite.nike.com. Find a request which has a bearer token attached to it and copy it.

Run create_clean_runs.py to create a .csv file for each file containing the detailed data for each run from the .json files. It creates a table by matching timestamps between the different measurements recorded, making the file about 10x smaller on disk than the original json with no loss of data.
