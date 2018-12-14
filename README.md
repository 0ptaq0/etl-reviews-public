# etl-reviews :clapper:
Phyton application to download and storage film reviews from web services.

## Installation

Make sure you have installed Python 2.7 on your PC (best 2.7.13 x64)
If you have troubles with installing pip please visit https://pip.pypa.io/en/stable/installing/#do-i-need-to-install-pip
On your local drive go to folder when you want this project to be stored 
> example E:\Program Files 
then open command line and type
```
git clone https://github.com/ArkadiuszParafiniuk/etl-reviews.git
```
open etl-reviews folder, then open command line again and type
```
pip install -r requirements.txt
```
Next thing you have to do is database table creation:
In etl.py file, in __main__ section uncomment everything what is between:
```
"# # # code below is for first launch of the program and testing purpose
    # # First Launch"
```
and
```
"# # Testing purpose"
```
then run open command line, type
```
python etl.py
```
and close it
Now you are ready to run the program


## User guide
### Run a program
Go to app folder, open command line and type
```
python etl.py
```
### First launch
#### Inserting movie reviews - mode 1
Below label **E T L** you have a blank text area. Type there the movie title you want to extract details about.
> example Matrix

Click on button **Extract**
Info text on the bare bottom will let you know how many movie reviews were found on filmweb for given film.
Click on Transform
Info text on the bare bottom will give you details about average users rating.
Click on Load
Info text on the bare bottom will show you database's transaction details:
- how many reviews were already there and were updated
- how many new reviews were inserted into database
> But where can I see the results?

Simply press **Search** button and you will be filled with reviews

### Every other launch
#### Inserting movie reviews - mode 2
You can insert movie reviews into database even faster!
Just type the title below **E T L** label and hit **ETL** button.

#### Showing results
When you finally gathered some data and want to see them all press **Search** button in upper space.
You will se all the reviews in database.
> There are too many of them! I want to see reviews only for **Matrix** movie

Please type the movie title in empty search field in upper space and click Search.

#### Extracting data
When you click **Extract data to CSV** button, every movie review from database is saved in temp/movie_reviews_output.csv file 
Also you can save single movie review. In order to do that view the results as described in section **[Showing results]** and click on the specific one. You will see the review in separate window and big button **Export this review to text file**. After clicking that it will be saved in temp folder as **Review - {title of movie review}.txt**

#### Erasing data
Click on **Clean Data** button. Congratulations! You have deleted all the records from database.
