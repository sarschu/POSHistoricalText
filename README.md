# Warning

This is not user-friendly and well prepared code but just the collection 
of all the scripts I used. You are welcome to use it, but there is no support.


# Part-of-speech tagging for Middle High German text


PoS (part-of-speech) tagging is a preprocessing step which
is indispensible for many Natural Language Processing
(NLP) tasks and needs to be done with high accuracy to
ensure success in the subsequent task. Being of such im-
portance, it is a well studied field offering a variety of tech-
niques suitable for different languages. However, most of
these approaches use a large number of training examples.
Even if it comes to unsupervised methods, the unlabeled
amount of data has to be satisfactorily large. Yet, there are
scenarios in which neither labeled nor unlabeled data is suf-
ficiantly available. Digital Humanities (DH) is a field of
research that is developing fast. It holds its very own kind
of challenges and scientific issues both interesting for Hu-
manities and Computer Science. One of the problems for
NLP is the non-canonical nature of text especially found
in projects dealing with historical text. These texts deviate
from text that has been the main focus of NLP so far by
lacking standardized orthography and grammar. This can
often lead to a decrease in performance of tools trained on
standard text (Melero et al. (2012) and Eisenstein (2013)).
Data needed for the training of dedicated tools for these
texts is often not available. However, these non-canonical
texts are usually closely related to the standard language
from which they deviate e.g., the modern stage of the lan-
guage. This knowledge can be used to facilitate tagging.
To illustrate this, we investigate PoS tagging of a unique
late Middle High German (MHG) text which can be located
in the transition period between MHG and Early New High
German (ENHG). This fact leads to a text with mixed fea-
tures of two historical stages of German.
In this paper, we investigate PoS tagging for historical texts
sharing a lot of the challenges of PoS tagging for low re-
sourced languages. We do this by means of what we call
expanding exploration adding more external resources af-
ter each step. We compare different approaches towards
boosting performance of PoS tagging of text for which no
suitable PoS tagger is available and no or really limited
annotated data is available. Departing from the assump-
tion that we have no text external resources to our disposal,
we experiment with unsupervised and weakly supervised
learning methods (Section 3). Moreover, we follow exper-
iments performed by Garrette and Baldridge (2013) who
describe PoS tagging research for low resourced languages
using really small amounts of annotated data. Expanding to

## Methods
* We experiment with k-means clustering informing
the clustering algorithm with the number of PoS we
have annotated in our gold standard. Moreover, we
initialize our cluster centroids with prototypical words
for each PoS inspired by (Haghighi and Klein, 2006). 1
* We train a neural net using nlpnet (Fonseca et al.,
2013) on our training set.
* We train a CRF tagger (Lafferty et al., 2001) using
context windows of 5 tokens.
* In order to boost performance, we apply self-taught
learning during training of the NN tagger and the CRF
tagger.
* model transfer: using taggers for closely related lan-
guages.
* stacking using a CRF meta-learner to combine the
knowledge of the NN tagger and the CRF classifier in-
troduced in Section 3 and the two taggers for closely-
related languages.
* tritraining using two classifiers to inform our third
classifier about which sentence from the unlabeled
data set to add to the training process.
