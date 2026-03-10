

Deep learning

Deep Learning is a part of Machine Learning.
It uses Neural Networks with many layers to learn patterns from data.

Suppose you want a system that detects cats in images.

In Traditional ML
You manually give features like:

shape of ears
color
edges
texture

Then ML learns from these features.
So process is:

Image → Human extracts features → ML model → Result
In Deep Learning

You do not extract features manually.

The neural network learns features automatically.
Image → Neural Network → Result

It learns:

edges
shapes
patterns
object structure
automatically.

Neural networks
A Neural Network is a group of connected nodes that learn patterns from data and make predictions, similar to how neurons work in the human brain.


| Neuron                               | Perceptron                    |
| ------------------------------------ | ----------------------------- |
| General concept of a processing unit | Specific type of neuron       |
| Used in modern neural networks       | Early model of neural network |
| Can use many activation functions    | Uses step function            |
| Can solve complex problems           | Only simple binary problems   |


3. Structure of a Neural Network

A neural network has three main layers.

1. Input Layer

This layer receives the data.

Example inputs:
study hours
attendance
previous marks

2. Hidden Layer

This layer processes the data and learns patterns.

Example pattern:
More study hours → higher chance of passing.

A neural network can have many hidden layers.

3. Output Layer
This layer gives the final result.

Example output:
Pass
Fail









RNN
Parallel processing is problem
Limited context window



LLM

Computer does not know the meaning of word it uses statistical probability to predict new word.

It is the system works on probability + bit randomness

LLM uses neural network to autocomplete any sentence

We can train LLM on movie related article
Then if we give half sentence it completes it automatically


Not only movie LLM is trained on every big dataset so that it can predict any solution simply.
We'll get neural network in model which contains trillions of parameters and they have capacity to understand and capture complex patterns

Eg of LLM ->gpt3 ->Chatgpt uses gpt 3 

Now LLM can predict wrong output because it does not understands any meaning just rely on probability so we also need to correct it

How LLM Trained

1)Data curation 
Data collection
   1)Internet
   2)Books
   3)Wikipedia
   4)GitHub
We require very big dataset

2)Data cleaning and filtering
  
3)Remove duplicates
  
4)Remove semantic duplicates

5)remove same things

2)Tokenization
After getting the data we need to tokenize the data into tokens(words)

Then we will make embeddings from tokens

3)Model archicture





