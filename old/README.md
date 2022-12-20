There are two files in this project. 

- `category_glossary.py`: generate dictionary using wikipedia api
  - input: specify the domain in a list
  - output: 
    - terms for each domain under `Glossaries` directory
    - A csv file called `All_Terms.csv` which includes all the terms
- `glossary_transcripts.py`: apply `rake` to extract keyword expression from corpus, then use edit distance to look up the dictionary
  - input: corpus directory under `data` directory
  - output: the terms appeared in each corpus under `output` directory, and is in json format

There are also several parameters you can tune in this project
1. The domain list in category_glossary.py, see the main function
2. The options of `Rake`, see line 91 in `glossary_transcripts.py`
3. The threshold of the look up method, see line 159 in `glossary_transcripts.py`

Some notes about the threshold:

As is mentioned above, this code use edit distance to match each rake keyword to the dictionary.
The edit distance simply means to measure the differences between rake keyword and term.

This code first calculate the edit distance between one rake keyword and all terms in the dictionary.
After we find the term that has the shortest distance, we still set a threshold for the term.

(sorted_distances[0][1] / (sum([len(sorted_distances[0][0]), len(cleaned_keyword)]) / 2)) < 0.1:

Basically, this simply means whether the differences between the keyword and the term is under 10%.
Therefore, if you want to have more keywords for one corpus, I will suggest you to increase this threshold.