# ![](https://ga-dash.s3.amazonaws.com/production/assets/logo-9f88ae6c9c3871690e33280fcf557f33.png) Working With API Data

> Unit 4: Required

---

## Materials We Provide

| Topic | Description | Link |
| --- | --- | --- |
| Lesson | Part 1: APIs | [Here](./intro-to-web-services-apis.ipynb) |
| Lesson | Part 2: Webscraping Demo (Optional; time permitting) | [Here](./webscraping-in-class.ipynb) |
| Solutions | Sample solutions to lesson prompts | [Here](./solution-code/webscraping-in-class-solutions.ipynb) |
| Practice | In-Class Practice Using APIs | [Here](./practice/apis_practice-lab.ipynb) |
|          | Case Study Twitter APIs and NLP           | [Here](./practice/twitter_api_nlp-lab.ipynb)  |
|          | Practice Webscraping with Selenium (Requires Chrome)   | [Here](./practice/webscraping_selenium-lab.ipynb)       |
| Practice Solutions  | Solution code for all 3 practice activities | [Here](./practice/solution-code/) |
| Slides | Sample slide decks for this topic (PPTX; deprecated) | [Here](./APIs/assets/slides/) |

> Please note: This lesson makes use of datasets from the `requests` library. The optional practice materials also include a `twitter-python` package. The webscraping module requires `selenium` and `geckodriver` and is best taught using Google Chrome.

---

## Learning Objectives

#### Part 1: Intro to Web Services & APIs
_After this lesson, students will be able to:_
- Identify relevant HTTP Verbs & their uses.
- Describe Application Programming Interfaces (APIs) and know how to make calls and consume API data.
- Access public APIs and get information back.
- Read and write data in JSON format.
- Demonstrate how to use the `requests` library.

#### Part 2: Webscraping in Class (Optional)
_After this lesson, students will be able to:_
- Revisit how to locate elements on a webpage
- Aquire unstructure data from the internet using Beautiful soup.
- Discuss limitations associated with simple requests and urllib libraries
- Introduce Selenium as a solution, and implement a scraper using selenium (Instructor Demo only)

---

## Student Requirements

Before this lesson(s), students should already be able to:
- Interpret and use Python dictionaries
- Build Pandas DataFrames from dictionaries
- Perform simple data manipulation on Pandas objects\
- Build `for` and `while` loops in Python
- Use `pip install` for package management

---

## Lesson Outline

### Outline: Part 1 (Web Services & APIs)
> TOTAL (170 min)

- Introduction to APIs
- What is an API? (10 min)
- Famous APIs (5 min)
    - Facebook
    - Yelp
    - Echonest
- Web APIs (5 min)
- Making API calls (5 min)
- HTTP (10 min)
- Web applications (5 min)
- Demo: HTTP (10 min)
- Independent practice: HTTP (10 min)
- HTTP Request (10 min)
    - HTTP Request methods
    - HTTP Request structure
- HTTP Response (5 min)
    - Response types overview
- JSON (10 min)
- Independent practice: validating JSON (10 min)
- Guided practice: pulling data from APIs (35 min)
    - Example 1: Star Wars (15 min)
    - Submit queries to the API (10 min)
    - Example 2: Google Geocode (10 min)
- OAuth (15 min)
- Independent practice: python APIs (30 min)
- Closing questions


### Outline: Part 2 (Webscraping in Class)
> TOTAL (170 min)

- Introduction (10 min)
- Building a web scraper (5 min)
- Retrieving data from the HTML page (65 min)
    - Retrieving the restaurant names (20 min)
    - Challenge: Retrieving the restaurant locations (15 min)
    - Retrieving the restaurant prices (10 min)
    - Retrieving the restaurant number of bookings (20 min)
- Introducting Selenium (90 min)
    - Running JavaScript before scraping (15 min)
    - Using regex to only get digits (20 min)
    - Challenge: Use Pandas to create a DataFrame of bookings (40 min)
    - Auto-typing using Selenium (15 min)
- Summary

---

## Installation Notes

When running this lesson, please check the following environment requirements:
1. Have Beautiful Soup installed: ```pip install bs4```


**If including Selenium demo:**
1.  Install Selenium: ```pip install selenium```
1.  Install the [FireFox browser](https://www.mozilla.org/en-US/firefox/new/).
1.  Install GeckoDriver: ```pip install geckodriver```

---

## Additional Resources

For more information on this topic, check out the following resources:

- Find elements: [Selenium docs](http://selenium-python.readthedocs.io/locating-elements.html#locating-elements)
- Using Selenium to enter website information: [demo](http://thiagomarzagao.com/2013/11/12/webscraping-with-selenium-part-1/)
- Python regex tester: [here](http://pythex.org/)
- Setup Firefox profile: [here](http://stackoverflow.com/questions/9907492/how-to-get-firefox-working-with-selenium-webdriver-on-mac-osx)
