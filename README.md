# IO_Query_Dataset, an extension of the spyder dataset as seen here: https://yale-lily.github.io/spider

This is a dataset that is labelled for entity recognition in querries

The data consists of 800+ queries that have been labeled with 'I' for being part of an entity and 'O' for being outside of an entity. 

The purpose of the dataset is to help target key words in queries for search engine optimization. 

Please report any misslabeled data points to drewb97@gmail.com

WHY DATA WAS FORMED 
  - In the spider data set there are column / table names and column / table "text names". The "text names" are how the column or table name would appear in text (an example would be to take out the underscores). Much of the spider data set however deals with names that are not linked directly to their textual representation. The creators of IRNet have a good approach for token linking but that appraoch involves iterating over all values in a sequence and then matching corresponding n-grams. The data that is provided here attempts to show where in a sequence those tokens reside. You will notice that many entities that correspond to rows in a column are left out (CONDITIONAL CLAUSES IN SQL), in a future addition to this dataset I will include those for linking as well. 

IRNet: https://github.com/microsoft/IRNet

HOW DATA WAS FORMED 
  - In order to actually match tokens in the SQL statements to their corresponding Natural Language Question, I parsed the SQL statement for the columns and tables it was pertaining to. Then I got the corresponding "text names" from the question. If the sets included from the SQL statement and the Natural Language Question were the same I threw those into the dataset, if not I did not include the example. This data was only taken from the Spyder Training set.  
