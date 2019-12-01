# GeneratingQuestionAnswers

The whole project of Question Answer pairs generation has fallen into three vital steps, one is Preprocessing the Freebase data to generate the test instances of the Text Generation model, the second is to generate the keywords for test instance and finally the last step is to implement a text generation model which is trained by a WikiAnswers dataset to generate questions from the keywords obtained from previous step.

### 1. Preprocessing the data - 
#### Preprocessing_freebase.IPYNB
	We have done the following steps for preprocessing the knowledge graph. 
Initially, the knowledge graph will be in RDF format. So, we had to preprocess the file containing RDF triples with URI links by removing the URI links and extracted the values like subject, predicate, object and predicate’s domain and range.
From these values, we made sure that process only unique predicates. We extracted unique subject, predicate and object, predicate pairs

Before processing, the data is in RDF format
<http://rdf.freebase.com/ns/american_football.football_player.footballdb_id>    <http://rdf.freebase.com/ns/type.object.type>   <http://rdf.freebase.com/ns/type.property> <http://rdf.freebase.com/ns/american_football.football_player.footballdb_id>	<domain>	<http://rdf.freebase.com/ns/american_football.football_player> 
<http://rdf.freebase.com/ns/american_football.football_player.footballdb_id>	<range>	<type.enumeration>
<http://rdf.freebase.com/ns/m.01001tl3>  <http://rdf.freebase.com/ns/music.recording.artist>        <http://rdf.freebase.com/ns/m.01s7hcz>
And here is how Processed Data is -
Predicate List -
<american_football.football_player.footballdb_id>  
Domains and Ranges -   
<american_football.football_player.footballdb_id>	<domain>	<american_football.football_player> 
<american_football.football_player.footballdb_id>	<range>	<type.enumeration>
Subject Predicate Object -
<m.01001tl3>  <music.recording.artist>        <m.01s7hcz>	

### 2. Approach to generate QA pair for an Entity E -
#### QuestionKeywords_AnswerExtractor.IPYNB
The Knowledge Graph(KG) contains information about various entities in the form of triples. A triple consists of a subject, predicate, and object. The subjects/objects(person, place, etc.) are the nodes of the knowledge graph whereas predicates are the edges of the KG. The predicates define the relationship between the subject and the object. To generate the QA pair, we need two modules.
Questions keywords and Answer Extractor: This is language independent and extracts required knowledge about the entity E from the KG.
RNN based Natural Language Question Generator: This is language-dependent and when fed with the information extracted from the first part it generates natural language QA pairs.

Questions keywords and Answer Extractor - 
The keywords are a concise representation of the natural language question. For example, let's take the entity as “William Shakespeare”. We have natural language question as “Who was the author of the play Hamlet?”. The keywords identified are {‘Author’,’Play’,’Hamlet’}. We can have a Question and answer pair as ({‘Author’,’Play’,’Hamlet’},“William Shakespeare”). In the Knowledge Graph, “Author”, “Play”, “Hamlet” are the nodes that are connected to the entity “William Shakespeare”. We must first identify the entity node in the KG and get all its neighbors.
Given a predicate pi, let sub(pi) be the subject of pi and obj(pi) be the object of pi. Let domain(pi) and range(pi) be the domain and range of pi respectively. Let {sub(pi), domain(pi), pi, obj(pi), range(pi)} be the 5-tuple associated with every pi. We use the following rules to generate QKA pairs from 5-tuples:
Unique Forward Relation
Unique Reverse Relation

Question Answer Keywords are generated as follows - 
Cantata misericordium, op. 69   form    compositional_form      Cantata
Тацу    recording       release_track   Тацу
С тобой и без тебя      release release_track   Тацу
Over You        canonical_version       recording       Over You
Jay Nash        artist  recording       Over You
Dirty   release release Generation
Generation      release release_track   Dirty
Auf die Zechn-Tanz      composer        composer        Peter Havlicek
Peter Havlicek  composer        composition     Auf die Zechn-Tanz

### 3. RNN based Natural Language Question Generator - 

As part of Natural Language question generator, we considered the question keywords that are identified in the previous step as input sequence and generate a question as output sequence. Instead of considering the set of keywords as a bag of words, we are giving importance to the order of occurrence of each keyword thereby making sure to generate semantically valid questions from the set of keywords. 
The model to generate question from set of keywords is inspired from RNN based encoder and decoder. In this approach, We used LSTM model, the keywords of different lengths are encoded to a fixed length vector representation and then compute the probability of the question output sequence for that given encoded vector representation. We feed the model with these output sequences and finally select the question with highest probability from all the generated questions. 
#### GenerateCorrectKeywords.py  
To generate keywords required to train the model.

#### modelrnnlstm.IPYNB
LSTM model implementation to generate question sentence from the input keywords.

Sample Output: 
Input sentence: ticking sound alternator starter battery
Decoded sentence: what to human part of the the battery is the battery

Input sentence: measurement is speed wind measured
Decoded sentence: what measurement is wind speed measured east and in parallel what

Input sentence: jim morrison died
Decoded sentence: jim jordans baseball what the s _END

Input sentence: mexico bigger australia
Decoded sentence: how much can chemistry be considered in water _END

Input sentence: teachings muslim influenced arts
Decoded sentence: cool quad procedures of flower in a and life in spain

Input sentence: bacterial infections cause cancer
Decoded sentence: how chemistry is a creme brulee in _END

Input sentence: man loves woman
Decoded sentence: about a soldier wear for a _END
