# SQLAlchemy-Challenge
This is the 8th homework from the coding bootcamp course.
This homework is to use a library in Python, called 'sqlalchemy' to set up a connection to sql file to read, query for results, and also set up an API using the 'flask' library. The content of this homework is about the temperature and rainfall in Hawaii hence it involves converting date to string and vice versa.

## Key Reflects

### New Findings
Within the Jupyternotebook part of homework, after I created the base and connection to .sqlite file, I tried to use different methods to showcase the dataset, such as a inspector to view the columns and their types, SQL codes within engine.execute() to view raw data, session.query().all() to see data in a list of tuples, convert to a dataframe based on the query etc.. If there is no .all() at the end of a query then we need to use a for loop to view the data.
It is very convenient to use the 'datetime' library to play around with date types, as the dates within the raw data are purely TEXT (which basically is STR) then iy is required to convert it into date type to use calculation methods in the library, such as datetime.timedelta(days='').
When plotting for the precipitation plot, it was confused as one date has multiple precipitation values as there are many station observation results. In this case when generating a line plot, it will only take the maximum values as the y-axis.
Within the API part, I attempted to use the 'link' for some of the route addresses, it actually worked and it saved me lots of time when testing out my API on the web page with the simple click on the link, but not for the substitudes of start and end variable for dates ones.

### New Tricks
1. '\N{degree sign} to show the little circle of a temperature unit
2. histogram graphs has a prarmeter called 'bins', the more the bins value, the more accurate the result is
3. for the bonus part II, where it asks to store daily temperature summaries for a set of date range, used 'while' loop. If choose to use a 'for' loop then I would define the range first, there is a function within the datetime lib to calculate a range of period
4. to change the key order in a dictionary:
   i. set the desired key order in a list of key names, such as ordered_list = ['key1','key2,...]
  ii. set the new ordered dict, new_dict = {k:old_dict[k] for k in ordered_list}
  
  well, it worked when I tried in jupyter notebook but not from the web page of APIs...

### Uncertainties
1. I had a problem with plots when set the xticks and its labels. For example in the precipitation plot, I tried number of times but it just did not work at all... I found that there are sub functions within matplotlib should have tried it
2. I had a conclustion about the bonus part I regarding to t-test results. Not sure if it is correct
3. For the start and end dates in the API, I have used many conditions in the 'if' statement. Not sure if there is any other easy way of doing that...
4. Again, within the API part, if the typed dates are not in the '%Y-%m-%d' format then the page itself will return an error message, either a type error or lead to the classic '404'. I intended to achieve, for example, if the user typed '..../14-4-1', then my pre-stored error message appears to ask the user to check the input format
