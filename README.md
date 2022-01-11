# wikipediaSearchEngine
**LINK TO RUN SEARCH ENGINE**<br />
  http://c7da-109-65-90-30.ngrok.io/{relevant route}<br />
  if not work it beacuse the server is down/crashed.<br />

**Explanation about classes and their purpose**<br />
**document:**

**parser_module:<br />**
  This class get a wikipedia document as a list and break it into different fields.<br />
  (title,body text,anchors) also this class tokenize the text or body or anchor (depends on our choice)<br />
  and create a document object that after it will be sent to the indexer.:<br />
  When our engine get a query the query also will be sent to the parser and will be tokenized as we tokenized the text.<br />
  The toknize happend with regular expressions.<br /><br />
**indexer:<br />**
  The indexer get the document that the parser created and created a postings list for the search engine.<br />
  This class also write the postings list to the disk.:<br />
  after writing all the postings lists to the disk the indexer merage postings list by group of letters. <br /><br /> 
  
**inverted_index_gcp:<br />**
  
**configuration:<br />**
  This class responsible on the routes of the data:<br /><br />
**reader:<br />**
  This class helps us to read the data and iterate on it.:<br /><br />
**MultiFileReader:<br />**
  
**searcher:<br />**
  This class help us to get the relevants posting lists for given query<br /><br />
**ranker:<br />**
  This class gives a rank for each relevant document<br /><br />
**BM25:<br />**
  This class help us to get score for the relevants docs<br /><br />
**thesaurus:<br />**
  this class create a file of words and their synonms<br /><br />
**stemmer:<br />**
  This class get word and return the word in stemming<br /><br />
**utils:<br />**
  this class help us to save pkl objects and load pkl objects<br /><br />
