# Text Classification Using Supervisioned Learning Models

In this project, we are going to use the free Reddit API to extract some posts by Web Scraping about Data Science, Machine Learning, Physics, Astronomy and Conspiracy. 

Once these data have been extracted, we will create a pipeline for pre-processing these data and we will use dimensionality reduction techniques to later train 3 classification models, KNN, RandomForest and Logistic Regression. 

After that, we will analyze the performance of each one of them by the Confusion Matrix and we will select the best model for these types of classification.


# Creating the API

Firstly, we've to create a free Reddit account at https://reddit.com in order to create the API used in this project. Basically, we gonna do a Web Scraping.

Then, go to the website https://reddit.com/wiki/api and read the terms. After this, visit https://www.reddit.com/prefs/apps and create your own API by clicking on the button "are you a developer? create an app..." down bellow.

A screen similar to this should appear and you must follow the following steps to complete:

![image](https://github.com/ksldados/Projetos-de-Machine-Learning-Engineering-by-Kariston/assets/114116067/38df59fa-7fbd-4dd4-a50f-317e2722b4cd)

1 - Click on "Script". 

2 - Create your API name. Here you can put any name that you want, without spaces. 

3 - Create a generic 'https'site. Even if it doesn't exist, no problem!

4 - Click on "create-app".

Done! Your API has been created and a similar window should appear like this:

![image](https://github.com/ksldados/Projetos-de-Machine-Learning-Engineering-by-Kariston/assets/114116067/31eb3a29-b01c-44c0-9fd2-71a4900b321c)

1 - It's your 'personal user script'. We'll use this to connect to the API.

2 - It's your 'secret' token. We'll also use this to connect to the API.

In general, to connect to the Reddit API, we'll use a specific Python Library called "praw". Read more here https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html.

# Starting coding

In this project, we gonna use some specifics packages that you can get them by installing the Python Interpreter using 'Anaconda3' installer.

Here's the packages:

![image](https://github.com/ksldados/Projetos-de-Machine-Learning-Engineering-by-Kariston/assets/114116067/7d476025-2e92-4ea6-b515-0020bcd43bbf)

To provide the data, a list of themes must be created to use for searches on Reddit. These will be the classes that we will use as target variable. 

![image](https://github.com/ksldados/Projetos-de-Machine-Learning-Engineering-by-Kariston/assets/114116067/9f73f5a2-3666-401e-8fde-2146b07e6c69)

After this, we must create a load data function by connecting to the Reddit API and load the Data by using the topics themes that we defined before. 
Firstly we extract data from Reddit accessing via API (all red boxes in the figure bellow should be complete using your API and Reddit account informations) and then, we count the number of characters using regular expressions. Define the condition to filter the posts (we will only return posts with 100 or more characters). Then, lists for results.

![image](https://github.com/ksldados/Projetos-de-Machine-Learning-Engineering-by-Kariston/assets/114116067/bd2f71fe-b7b8-4232-9767-2c6f3a6efb38)

Creating a Loop to enumerate the data:

![image](https://github.com/ksldados/Projetos-de-Machine-Learning-Engineering-by-Kariston/assets/114116067/cc50030b-03f4-420d-ade1-f79920050bda)

And now, we create control variables to separate the dataset into Train and Test using Random State.

![image](https://github.com/ksldados/Projetos-de-Machine-Learning-Engineering-by-Kariston/assets/114116067/c8b92df2-7508-4222-a883-a7676c2d9562)

# Data Pre-Processing and Attribute Extraction

The following steps will be done now.

1 - Remove symbols, numbers and url-like strings with custom preprocessor

2 - Vectorizes text using the term inverse frequency of document frequency

3 - Reduces to major values ​​using singular value decomposition

4 - Partitions data and labels into training/validation sets

![image](https://github.com/ksldados/Projetos-de-Machine-Learning-Engineering-by-Kariston/assets/114116067/38456476-d6d1-4775-88fc-526b5aa66437)

Creating the models we can obtain:

![image](https://github.com/ksldados/Projetos-de-Machine-Learning-Engineering-by-Kariston/assets/114116067/a249fede-fed8-4164-b90f-4d848e52ee95)


Running the Pipeline for all Models and visualizing the results, we have

![image](https://github.com/ksldados/Projetos-de-Machine-Learning-Engineering-by-Kariston/assets/114116067/1e6e3a33-e467-4834-b0c6-461a8ce9c4fb)



![image](https://github.com/ksldados/Projetos-de-Machine-Learning-Engineering-by-Kariston/assets/114116067/8fe32e4b-6c6c-4273-9df4-9c003d5c338b)




![image](https://github.com/ksldados/Projetos-de-Machine-Learning-Engineering-by-Kariston/assets/114116067/c495cd0a-d077-45c6-b5f1-7ecdf9642df0)



![image](https://github.com/ksldados/Projetos-de-Machine-Learning-Engineering-by-Kariston/assets/114116067/9f07845d-ef08-41e6-aaa6-bd295712e330)



![image](https://github.com/ksldados/Projetos-de-Machine-Learning-Engineering-by-Kariston/assets/114116067/69094432-e5c1-4de7-8b51-bc245fdb175f)

# Conclusion

We can conclude that the Logistic Regression model showed better accuracy results when compared to the KNN and RandomForest models.




