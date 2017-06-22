INTRODUCTION

Widgetcorp is a (fictional) company which uses Searchlight to learn how people express intent about topics and products relevant to their business. As part of their new Global Widget Initiative, their Digital Marketing team wants to study national and regional differences in what people search for and what specific words they use.

Widgetcorp wants us to help them understand local search volume data from around the world. We're starting with English phrases in 5 locations: Australia, Canada, United Kingdom, United States, and New York City. (We'll include more regions and languages later.)

Widgetcorp has selected 800 search phrases, and we have collected monthly search volume (MSV) data for each phrase in all 5 locations. The file Data.csv contains all the collected data. The fields are:

Locode                    Conductor location code: AU, CA, GB, US, or US NYC
Phrase                    the search phrase
2016-04 through 2017-03   MSV for a specific month for this Locode and Phrase
AvgMsv                    12-month average of MSV for this Locode and Phrase
Competition               a measure of ad-buying interest in this Locode and Phrase
CostPerClick              typical bid price to buy ads for this Locode and Phrase

We need your help with these 3 tasks:

0. Data Cleaning
1. Top Keywords
2. Regionality

Each task is described in detail below.


0. DATA CLEANING

This dataset is not 100% trustworthy. Most of it is accurate, but it contains some errors.
We need your help repairing, deleting, marking, or otherwise working around these errors.
Make a copy of Data.csv and rename it CleanData.csv. Apply these changes to CleanData.csv:

a. Repair blank cells
Some cells are intentionally empty, but others are data collection errors. Fill empty cells according to this rule:
IF (AvgMsv < 100) AND (AvgMsv is not empty) for this row, THEN fill all empty numeric cells on this row with 0

b. 'AvgMsv' consistency check
In theory, the average of all 12 monthly columns should equal the 'AvgMsv' column.
In practice, this is not always exactly true because MSV values are rounded in a complicated way.
Consider AvgMsv "good enough" if it is within +/- 20% of the average of all monthly columns.
Inspect any rows which fail this test and make whatever changes you think are appropriate.

Feel free to do any additional data quality testing which you think might be useful.
As you do tasks #1 and #2, you may discover other unknown errors or suspicious values.
Do whatever you think is best for correcting or avoiding these problems.
Keep a record of any suspected errors you found and any changes you made to the data.


1. TOP KEYWORDS

Widgetcorp wants to see which phrases have the largest total search volume.
Create a new table called TopMsv by reshaping the 'AvgMsv' column.
Each row in this table should represent one Phrase. The columns should be:
[ Phrase, AU, CA, GB, US, US NYC, Total ]
Sort with the largest 'Total' values at the top and keep only the top 100 rows.

Widgetcorp also wants to see which phrases have the most expensive ads.
Create another table similar to TopMsv, but use 'CostPerClick' instead of 'AvgMsv'.
Instead of total search volume, calculate maximum CostPerClick across all regions.
Sort by maximum CostPerClick and keep only the top 100 rows.

Extra Credit:
Create visualizations of the top 10 results from each table. Choose whatever kind of plot you like.
Just be sure our client can easily understand what they're looking at!


2. REGIONALITY

Widgetcorp wants us to define a "Regionality" score for each (Locode,Phrase) pair.
Phrases which are unusually popular in a region should have high Regionality.
Phrases which are rare in a region should have low Regionality.

For example:
  ('GB','thames ferry') should have a high score
  ('US','thames ferry') should have a low score
  
Invent your own formula for "Regionality." You may want to try a few and choose your favorite.
Make a Regionality table shaped like the previous tables: each row is a Phrase, each column is a Locode.
Find the 10 Phrases with the highest Regionality score for each Locode.


SAVE AND SEND

Email us the following:

  CleanData.csv
  the TopMsv, TopCpc, and Regionality tables as separate CSV files OR as tabs in a single Excel file.
  code, extra spreadsheets, or any other files you used for calculations
  documentation briefly explaining your methods and decisions

Documentation can be a .txt file, a PDF report, notes within Excel, or some other format of your choosing.
Customers will not see this documentation, so don't worry too much about formatting and presentation.
Clear and simple docs are good enough!
