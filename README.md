# IST-664

This is final project for a short 10 week course in Natural Language Processing (NLP). In this project, two classifiers are [ensembled](https://en.wikipedia.org/wiki/Ensemble_learning) with a [recurrent neural network](https://www.youtube.com/watch?v=6niqTuYFZLQ). Specifically, a [long short-term memory](https://en.wikipedia.org/wiki/Long_short-term_memory) (LSTM) generative learning agent was deployed, with two classifiers assisting as [rules-based](https://en.wikipedia.org/wiki/Rule-based_machine_learning) components.

The first classifier attempts to predict whether a given sentence is a question. The second predicts what StackOverflow channel best represents a given sentence. Therefore, the ensembled application executes the LSTM agent when a given sentence is predicted as a question. If the agent is incapable of returning an adequate response, then the second classifier proposes a stackoverflow channel.

## Dependency

Since this project is a proof of concept, the necessary build has been automated using a [`Vagrantfile`](https://github.com/jeff1evesque/ist-664/blob/master/Vagrantfile). This local development requires both [vagrant](https://www.vagrantup.com/) + [virtualbox](https://www.virtualbox.org/) to be installed. However, a supplied [`docker-compose.yml`](https://github.com/jeff1evesque/ist-664/blob/master/docker-compose.yml) could simulate a big data scenario, where ingested data is distributed across multiple mongodb nodes. For production systems, kubernetes would likely replace the `docker-compose` variant. Additionally, supplied [utility](https://github.com/jeff1evesque/ist-664/tree/master/utility) scripts can be used to install and configure [cuda](https://www.geforce.com/hardware/technology/cuda) and gpu-based [tensorflow](https://www.tensorflow.org/).

Lastly, a supplied [`config-TEMPLATE.py`](https://github.com/jeff1evesque/ist-664/blob/master/config-TEMPLATE.py), will need to be copied in the same directory as `config.py`. Though values can be adjusted, the `mongos_endpoint` will need to match the mongodb endpoint. Specifically, if the local vagrant instance was deployed, then the following configurations would be appropriate:

```bash
# general
mongos_endpoint = ['localhost:27017']
database = 'reddit'
collection = 'qa_reddit'
data_directory = 'data'
```

## Data

Three different datasets are used to generate respective models

- [StackOverflow](https://github.com/jeff1evesque/ist-664/tree/master/StackOverflow/data): original large json split into multiple files then pickled
- [QuestionAnswerCMU](https://github.com/jeff1evesque/ist-664/tree/master/QuestionAnswerCMU/data)
- [Reddit](https://github.com/jeff1evesque/ist-664/tree/master/Reddit/data)

## Execution

The [`run.py`](https://github.com/jeff1evesque/ist-664/blob/master/run.py) is an entrypoint script supporting the following features:

- `--insert`: inserts relative `Reddit/data/` data into the specified mongodb endpoint
- `--train`: trains an LSTM recurrent neural network for the "inserted" mongodb data
- `--local`: implement the local trained LSTM model
- `--drop`: drops all documents in the default mongodb collection used during `--insert`
- `--generic`: implements a pretrained LSTM model based on 1M comment-reply pairs

## Motivation

The objective of this project was to perform classification analysis:

- [`StackOverflow_Classification.ipynb`](https://github.com/jeff1evesque/ist-664/blob/master/StackOverflow/StackOverflow_Classification.ipynb)
- [`StackOverflow_SKLearn.ipynb`](https://github.com/jeff1evesque/ist-664/blob/master/StackOverflow/StackOverflow_SKLearn.ipynb)
- [`QuestionAnswerCMU_Classification.ipynb`](https://github.com/jeff1evesque/ist-664/blob/master/QuestionAnswerCMU/QuestionAnswerCMU_Classification.ipynb)

Additionally, two write-ups are provided, discussing both the analysis, and ensembled application of both classifiers with the trained LSTM neural network:

- [`Wilson_Levesque_Final_Project.docx`](Wilson_Levesque_Final_Project.docx)
- [`Wilson_Levesque_Final_Project2.docx`](Wilson_Levesque_Final_Project2.docx)