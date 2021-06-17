# ![](https://ga-dash.s3.amazonaws.com/production/assets/logo-9f88ae6c9c3871690e33280fcf557f33.png) Train-Test-Split & Bias/Variance

> Unit 3: Required

---

## Materials We Provide

| Topic | Description | Link |
| --- | --- | --- |
| Lesson | Bias and Variance Lesson | [Here](./bias-and-variance.ipynb) |
| Solution  | Solution code for lesson prompts | [Here](./solution-code/bias-and-variance-solution.ipynb) |
| Practice  | Train Test Split and Cross Validation Lab (includes solutions) | [Here](./practice/)
| Datasets | Average weight of the body and the brain for 62 mammal species | [Here](./data/mammals.txt) |

> In this lesson, we use the Boston housing dataset (imported from scikit-learn) and the average weight of mammal bodies/brains (included). These datasets are appropriate for linear modeling based on their generally intuitive features.

---

## Learning Objectives

After this lesson, students will be able to:
- **Describe** what error due to bias is and what error due to variance is
- **Identify** the bias-variance tradeoff
- **Describe** what overfitting and underfitting means in the context of model building
- **Explain** problems associated with over and underfitting
- **Grasp** why train, test split is necessary
- **Explore** kfolds, LOOCV, and three split methods

---

## Student Requirements

Before this lesson(s), students should already be able to:
- Read into data using the Pandas library
- Perform statistical exploration with Pandas
- Create simple data visualizations with matplotlib
- Define the basic parameters of sampling and experimental design

---

## Lesson Outline

> TOTAL (170 min)
- Bias and Variance Trade-off (35 min)
  - Bias? Variance? (10 min)
  - Exploring the Bias-Variance Tradeoff (15 min)
  - Brain and body weight mammal dataset (5 min)
  - Making a prediction (5 min)
- Making a prediction from a sample (15 min)
  - Let's try something completely different
- Balancing Bias and Variance (10 min)
- Train-test-split (50 min)
  - Evaluation procedure #1: Train and test on the entire dataset (do not do this)
  - Problems with training and testing on the same data
  - Evaluation procedure #2: Train/test split
  - Comparing test performance with a null baseline
- K-folds cross-validation (45 min)
  - Leave-one-out-cross-validation
  - Intro to cross validation with the Boston data
- Three way data split (15 min)
- Additional Resources

---


## Additional Resources

For more information on this topic, check out the following resources:

- [Understanding the Bias-Variance Tradeoff](http://scott.fortmann-roe.com/docs/BiasVariance.html)
- [University of Washington Machine Learning Course Slides](https://courses.cs.washington.edu/courses/cse546/12wi/slides/)
- [An Intuitive Explanation of Overfitting](https://www.quora.com/What-is-an-intuitive-explanation-of-overfitting/answer/Jessica-Su)
