# Keras_LSTM_NLP_early_termination_clinical_trials
Pipeline methodology of the creation of a Keras LSTM model to classify into 17 different labels the termination cause of a clinical trial using all the studies in ClinicalTrials.gov that specifies a premature termination reason

This model was trained on 500 epochs and the highest accuracy on the validation set of 62% (aka 9232 rows out of the 15008 with a prediction score >50%)

This project was done for my pharmacy thesis "what are the factors increasing risk of early termination in Phase 2 Trials on Rare Diseases"

Pipeline :
- First we extract from CT.gov API all the trials that have a value for why_stopped, which is a free text form that summarize in 128 char max the termination reason.

- After examination of the ~30k different causes and some documentation on the topics of trials termination, I decided to create 3 majors categories for a total of 17 labels :

  1. Scientific cause
    - efficacy/futility
    - safety/ethics/adverse events
    - completed early
  2. Administrative cause
    - slow accrual
    - business / sponsor reason
    - funding related
    - logistics
    - never started
    - study redesign needed
    - negligence or recommandation of legalities
    - organisational/workforce issues
  3. Others
    - others
    - covid 19 restriction
    - related to primary investigator
    - trial no longer needed
    - study competition
    - trial no longer needed

  ![nlp1](https://github.com/user-attachments/assets/bd6feabf-b4da-4d00-bea1-021581952686)![nlp2](https://github.com/user-attachments/assets/bfea7605-2b48-4002-abaa-66f9bd27eef7)



We turn these into binary one hot encoded variables and we manually annotate 40% of the dataset to use as training.

Then we use a pre-processing pipeline illustrated below.
This will allow sanitizing the values, and using lemmatization with Part of Speech, simplify the data in order to be able to filter out duplicate or nearly similar termination causes to decrease the workload.
![image](https://github.com/user-attachments/assets/226089e4-7535-4a27-bcf7-9126263941cb)


Next we will do an extra step of simplification described here : 
- trials with +3 termination causes will be labeled only as "others"
- trials with primary investigator (PI) + another cause will have the PI label removed 
  (i.e = "PI closed due to lack of accrual" => cause is slow accrual not PI)
  - same thing with "slow accrual" if it is the consequence of another reason

Then we can tokenize again and add a GloVe vectorization
We also add a L2 regularization and a dropout layer to make it harder and longer for the model to learn to avoid overfitting.
The model is illustrated below :
![image](https://github.com/user-attachments/assets/3b048071-5a35-497a-acba-e1a7de4b82dd)

During the training on 500 epochs, we only start saving every 25th models past epoch 300.
We then make predictions on each of these models on the test set and keep the one with the highest prediction scores.

We export all the rows with a prediction score >50% and all the others rows are then manually annotated to complete the whole set.
