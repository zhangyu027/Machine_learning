# ![](https://ga-dash.s3.amazonaws.com/production/assets/logo-9f88ae6c9c3871690e33280fcf557f33.png) Decision Trees, Random Forests

> Unit 4: Required

## Materials We Provide

| Topic | Description | Link |
| --- | --- | --- |
| Lesson | Part 1. Decision Trees | [Here](./decision-trees.ipynb) |
|        | Part 2. Ensembles & Random Forests | [Here](./ensembles-random-forests.ipynb)
| Solution  | None needed (exercises and codealongs are done by-hand in groups) | N/A |
| Datasets | MLB player data | [hitters.csv](./data/hitters.csv)
| | Titanic survivors | [titanic.csv](./data/titanic.csv)
| | Vehicles (test) | [vehicles_test.csv](./data/vehicles_test.csv)
|  | Vehicles (train) | [vehicles_train.csv](./data/vehicles_train.csv)
| Practice | Random Forest from Scratch | [Here](./practice)
| Source Materials | Original files used to create this lesson | [Here](./slides/) |

> The MLB player data and Titanic datasets were chosen for this lesson because they are small enough to make very interpretable decision trees without much tuning. The vehicle data is very small, chosen as an easy example students could do by hand. It also provides a pre-split test set.

---

## Learning Objectives 

This lesson has two parts. Decision trees are introduced in part one, while random forests and other ensemble methods are elaborated on in part two. If you have limited class time, focus specifically on part one.


### Part One: Decision Trees

After this lesson, students will be able to:
- Explain how a decision tree is created.
- Build a decision tree model in scikit-learn.
- Tune a decision tree model and explain how tuning impacts the model.
- Interpret a tree diagram.
- Describe the key differences between regression and classification trees.
- Decide whether or not a decision tree is an appropriate model for a given problem.



### Part Two: Ensembles & Random Forests

After this lesson, students will be able to:
- Define how and why decision trees can be improved using bagging and random forests.
- Build random forest models for classification and regression.
- Explain how to extract the most important predictors in a random forest model.

---

## Student Requirements
Before this lesson, students should already be able to:
- Build and evaluate classification models in sklearn
- Explain how and when to apply different resampling methods
- Define the concepts of cross-validation and overfitting

---

## Lesson Outline

> **Important:** Part Two is about 100 minutes of material and is less detail-oriented. If you only have a fraction of a class period, we recommended that you only focus entirely on part one.


### Lesson Outline (Part One: Decision Trees)

> TOTAL (170 min)
- Introduction
- A: Regression Trees (115 min)
    - Group Exercise (20 min)
    - Building a Regression Tree by Hand (30 min)
    - How Does a Computer build a Regression Tree? (15 min)
    - Demo: Choosing the Ideal Cutpoint for a Given Feature (15 min)
    - Building a Regression Tree in scikit-learn (10 min)
    - What Happens When We Grow a Tree Too Deep? (5 min)
    - Tuning a Regression Tree (15 min)
    - Making Predictions for the Testing Data (5 min)
- B: Classification Trees (45 min)
    - Comparing Regression Trees and Classification Trees (10 min)
    - Splitting Criteria for Classification Trees (20 min)
    - Building a Classification Tree in scikit-learn (15 min)
- Summary: Comparing Decision Trees With Other Models (10 min)


### Lesson Outline (Part Two: Ensembles & Decision Trees)

> TOTAL (100 min - to leave room for projects if needed)
- Introduction
- A: Manual Ensembling (15 min)
- B: Bagging (30 min)
    - Manually Implementing Bagged Decision Trees (15 min)
    - Bagged Decision Trees in scikit-learn (5 min)
    - Estimating Out-of-Sample Error (10 min)
- C: Random Forests (10 min)
- D: Building and Tuning Decision Trees and Random Forests (30 min)
    - Optional: Predicting Salary With a Decision Tree (15 min)
    - Predicting Salary With a Random Forest (10 min)
    - Comparing Random Forests With Decision Trees (5 min)
- E (*Optional*): Tuning Individual Parameters (15 min)
- Summary


----

## Additional Resources

*If you're interested in reading more about decision trees and random forests, check out these resources:*
- [Induction of Decision Trees](http://hunch.net/~coms-4771/quinlan.pdf)
- [Top 10 Algorithms in Data Mining](http://www.cs.uvm.edu/~icdm/algorithms/10Algorithms-08.pdf)


*If you're looking for additional references, we recommend the following books:*
- __CHAPTER 8__ - [An Introduction to Statistical Learning](http://www-bcf.usc.edu/~gareth/ISL/) - This book provides a fantastic introduction to machine learning models and the statistics behind them. The visuals and explanations are really easy to understand. PDF available to download on the website.
- __CHAPTER 9__ - [Elements of Statistical Learning](http://statweb.stanford.edu/~tibs/ElemStatLearn/) - This book is by most of the same authors as the previous book, but goes into more detail. PDF available to download on the website.
- __CHAPTER 8__ - [Applied Predictive Modeling](https://www.amazon.com/Applied-Predictive-Modeling-Max-Kuhn/dp/1461468485) - While this book features R code, the discussion of different predictive models and sampling methodologies are hard to beat.  
