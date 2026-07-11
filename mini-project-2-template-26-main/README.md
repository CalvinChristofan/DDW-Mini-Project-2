# Mini Project 2: Math Quiz App

## Learning Objectives
In this mini project, you will develop a web app that evaluate math infix expressions using Streamlit. By the end of this assignment, you should be able to:
- Create a multi pages web app using Streamlit.
- Use OOP to process math infix expression.
- Read and Update tables in a local Excel file from Streamlit.

Parts of the code in this app use Pandas library which you will learn on Week 9. You can ignore these lines of code or you can also search for more information of what it does. These parts of the code will be given for you.

## App Overview

The way that the app works is that users can create math questions which can be sent as a challenge to other users. So part of this application is that it allows you to create multiple users. You create your users in the page called "Users". 

The next feature is that the app allows you to create a math question. User will enter a math expression in infix notation and send this question to other users. The app allows you to send a single math challenge to *multiple* users. You create your questions in the page called "Questions".

The next feature is that one can select a user and try to attempt the challenge. We use a simple drop down list to select which user you are currently acting as. Of course, in a real world app, you need to implement an authentication system and this authentication will identify which user is attempting the challenge. You do this in the page called "Challenge".

Depending on which user you select, you will see different challenges sent to you. When you select one of the challenges, you will see the math questions and you can enter the answer. The app will record the elapsed time from when you select a challenge to the time you click the submit button for the answer. This time duration will be recorded and used to sort the Hall of Fame page.

The last feature is the Hall of Fame page where this page displays all the challenges created in the system. For each challenge, it displays the question, the correct answer and the top three users that answer this questions with the shortest duration. You can see this information in the "Hall of Fame" page.

## Expected Output

[See video of the expected output](https://sutdapac-my.sharepoint.com/:v:/g/personal/oka_kurniawan_sutd_edu_sg/EVg3IAggibhKu_E-x8wepoMBoRJ3fj20Qji83cKSgqBJ4A?e=KRaANl).

## Project Structure

Once you have downloaded the repository, you can go to the repository and to the folder for this mini project. The commands below assume you are working from Github Codespace. Check the guide to launch Github Codespace. If you work from your local computer, the path might be different depending on where you download the mini project directory.

Assuming you are at `root` folder of your project in Codespace, list down all the files.

```shell
ls
```

The last command should output the following:

```shell
Home.py		
README.md	
library.py
Pipfile		
pages
config.yaml
Mini Project 2 - Instructor Database.xlsx
```

Notes:
- This handout can be found in the file `README.md`.
- `Home.py` is the main Python script that gives us the main home page for the Streamlit application. 
- `Pipfile` is a text file that describes the packages you need to create the virtual environment.
- `library.py` is the Python file for you to do your exercises.
- `pages` is a folder containing a few files which creates multiple pages in your web app.

## Creating a Virtual Environment

> A **virtual environment** is a collection of packages that you separate out for specific projects. For example, this project requires Streamlit and runs on Python 3.10. Since we do not want conflict with our default system Python, we install the packages we need into a different space and activate that space (the _environment_) when we run our project. (It is _virtual_ because all your environments are still on the same physical machine.) 

In the following steps, we will only display the Unix/Linux commands which you can do in Vocareum. If you want to work locally, see the [appendix](#appendix-setup-for-local-machine).

Go to the root folder of mini project 2 template.

```shell
$ cd /workspaces/10-020-data-driven-world-summer-2026-2d-mini-project-2-mini-project-2-template-xxx
```

First make sure that you have installed `pipenv` package. If not, run the following command in the terminal.

```shell
python -m pip install --user pipenv
```

<a id="local"></a>
We will call `mini-project-2-template` the **root** folder of our application. 

From the root folder, install the packages specified in the `Pipfile`.
```shell
python -m pipenv install
```

The above steps will install Streamlit.


To activate the virtualenv, run
```shell
python -m pipenv shell
```

Alternatively, every time you run a command, you can prepend that command with the following:
```shell
python -m pipenv run
```

Ok, so let's enter into the shell by typing:
```shell
python -m pipenv shell
```

You should see the word `(mini-project-2-template)` in your prompt something like:

```shell
(mini-project-2-template) user $
```

_To exit the virtual environment at the end of this mini project, simply type:_
```shell
exit
```

All the subsequent exercises assume you are in the virtualenv shell.


## Multi-Page App

Similar to Mini Project 1, we have `Home.py` which is our home page for our Streamlit application. We only have text to display here. One thing to note is that we use `st.write()` which supports Markdown syntax to create the HTML page.

```python
st.write("""
# Welcome to Mini Project 2

In this project, you will create a simple math game which you can send to different users.

To get started:
1. Click the User page and add a few users.
1. Click the Questions page and add some questions. Select which user you want to challenge.
1. Click the Challenge page and select that particular user. Choose the Challenge you want to attempt and put in the answer.
1. Click the Hall of Fame to see how you fare with other users.
""")
```

One important file in the root folder is `library.py`. This is the file which you will put your OOP code to evaluate the math infix expression.

If you list the files under `pages` directory, you will see we have a few files which correspond to the different pages in our web app. 

```shell
ls pages
```

This will output the following:
```shell
1_Users.py		
2_Questions.py	
3_Challenge.py
4_Hall_of_Fame.py
```

You will need to modify some of these files in the subsequent exercises.

## Exercise 0: Running the Streamlit Application

Most applications usually require a persistent data store (a **database**). In this mini project, you will use a local Excel file as your database. It is included in this folder. 

We can try running the web app. In order to do that, make sure you are inside the virtual environment by typing the following command.
```shell
python -m pipenv shell
```

To run the web app, type the following in the terminal.
```shell
streamlit run Home.py
```

The output looks like the following:

```shell
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://10.0.12.48:8501
  External URL: http://207.46.224.91:8501
```

Streamlit will attempt to open a web browser at `localhost:8051`. Do a `CTRL-click` on the `Local URL` link in Codespace and it will open the web page for you. You should be able to see the Home page with a sidebar menu.

Go to the page `Users` and ensure that you can see the users from the Mini Project 2 Excel file.

To stop the web app, type `CTRL+C` in the terminal. 

## Users Page

The code for the `Users` page has been provided and you can see it under `pages/1_Users.py`. Let's dissect some of these so that you can use it for your subsequent pages.

```python
import streamlit as st
import pandas as pd
```

The only extra line added from the first mini project is `import pandas`. This package makes it easy to deal with data in tables (a table is called a **DataFrame** in Pandas).

```python
filename = "Mini Project 2 - Instructor Database.xlsx"
users = pd.read_excel(filename, sheet_name="Users")
users
```

You can see that the Excel file in the first line above has five sheets:
* Users
* Questions
* Challenges
* Challenge-Users
* Timerecord

Each sheet contains a table that acts as our database. For example, the sheet `Users` contains `id`, `username` and `name` fields in the table.

In the second line, `pandas` is reading the data from worksheet `Users`.

In the third line of the Python code, we have a single line `users`. This is a [Magic](https://docs.streamlit.io/develop/api-reference/write-magic/magic) command in Streamlit. Whenever we put a variable name, Streamlit will try to guess its data type and try to find the best widget to display this data (it's secretly calling `st.write()`). In this case `users` is a `DataFrame` and the users will be displayed as a table in the Users page.

![](https://www.dropbox.com/scl/fi/ebwvnwmwpc3icd5meky9k/mp2_users_table.png?rlkey=mfgz1qcushwy3o3xbqlijo146&st=nkinm4bn&raw=1)

```python
with st.form("new_user", clear_on_submit=True):
    new_username = st.text_input("New Username:")
    new_name = st.text_input("Full Name:")

    submit = st.form_submit_button("Update User Table")
```

In the above code, we create a form for data submission when creating a user [^formsubmitbutton]. The form `new_user` contains three widgets:

* a Text Input widget whose value is stored in a variable called `new_username`.
* another Text Input widget whose value is stored into a variable called `new_name` .
* and a submit Button whose return value is stored in a variable called `submit`. 

[^formsubmitbutton]: https://docs.streamlit.io/develop/api-reference/execution-flow/st.form_submit_button

Notice that the label for each widget is specified in the argument of these functions.

```python
if submit:
    if new_username and new_name:
        users.loc[len(users)] = [len(users), new_username, new_name]
        with pd.ExcelWriter(filename, mode='a', if_sheet_exists='replace') as f:
            users.to_excel(f, sheet_name="Users", index=False)
            
        st.rerun()
```

Recall that `submit` is the variable that we assign `st.form_submit_button()`. It is a boolean and will be `True` when the button is clicked. This means that all the code under `if submit` line will be executed when the button "Update User Table" is clicked.

There are a few things happening here:

1. We check if the text input that stores username and name is empty or not. If both are not empty, we add one more row into the DataFrame `users` with the id, the username and the name of the user. 
1. The code `users.loc[len(users)] = ...` is part of Pandas data frame library. What it does is to add a new row at the bottom of the DataFrame. Since you have not learnt it, you can skip this line.
1. Since the id is just an integer that increases accordingly, we can use `len(users)` to get the next id (recall that the length of a list is always one greater than the index of the last element in the list). 
1. Next, we open the Excel file with `with pd.ExcelWriter(...)` and write the updated DataFrame with `users.to_excel(...)`. 
1. The last line forces Streamlit to run `Users.py` from top to bottom again. Thus, it should read the Excel file again, and you should see the User table at the top of the page updated with the latest user created.

You should test your app by adding new user using the form before moving on to the first exercise.

## Exercise 1: Infix Evaluation

Before proceeding, you need to write a class called `EvaluateExpression` which is the computation object used to evaluate the infix notation. In order to help you with this, we created a jupyter notebook to scaffold the problem into various steps. Do the task inside the jupyter notebook `mp2_exercises.ipynb`. 

[Watch this video on how the infix evaluation works](https://sutdapac-my.sharepoint.com/:v:/g/personal/oka_kurniawan_sutd_edu_sg/EbLA8Ft2QyNFn6GzpoKcHUgBAvmyZkI2hNxrvuw9EKt5hA?e=UQ7PvZ)

Once you have completed that task, copy-paste your code inside `library.py` found in your root directory.

```python
class Stack:
    pass

class EvaluateExpression:
    pass
```

To test your `library.py`, run the following command from the root directory.

```shell
pytest
```

It should output something like the following. Make sure there are no failures in the test before proceeding to the next exercise.

```shell
pytest
===================== test session starts ======================
platform darwin -- Python 3.11.5, pytest-8.3.5, pluggy-1.5.0
rootdir: /.../mini-project-2-template/
collected 4 items                                              

test_library.py ....                                     [100%]

====================== 4 passed in 0.02s =======================
(mp_calc) (py312) ➜  mp_calc git:(main) ✗ 
```

## Exercise 2: Questions Page

Now, we are ready to make use of the code for the infix notation evaluation. Open the file `pages/2_Questions.py` to do the following tasks.

```python
from library import EvaluateExpression
```

Here, we imported the `EvaluateExpression` class into our Streamlit script. The first few lines are familiar as they read the Users table from your Excel file.

### Task 1

The first task to read another table stored in the sheet called `Questions` in the Excel file. Update the following code.

```python
# TODO: Task 1
# read the sheet with the name "Questions"
#
# question_data = None
```

Make sure you store the DataFrame in the variable `question_data` as it will be used in other parts of the script.

Hint: you can infer from how we read the Users table above.

### Create New Question Form

The next few lines of the script are shown below.

```python
st.header("Questions List")
st.write(question_data)

st.header("Create New Question")
with st.form("new_question"):
    expression = st.text_input("Write a Math expression:")
    expression
```

What these lines of code do is the following:
* The first line creates a header called "Questions List".
* The next line displays `question_data` which we read from the Excel file in Task 1.
* We then create another header called "Create New Questions".
* We then create a form called `new_question`. 
* Inside this form, we create a Text Input widget and store the value into a variable called `expression`.
* Then, we use the Magic command to display the `expression` data.

### Tasks 2 and 3

What you need to do in this part is to evaluate the math expression and get the resulting answer. To do this, we will do the following:

1. First, we will create an object instance of `EvaluateExpression` class and store it as `evaluator`. This is to be done in Task 2. **Remember to pass on the `expression` variable to be evaluated.**
   ```python
    # TODO: Task 2
    # create an object instance of EvaluateExpression class
    # pass on the math expression to the object
    #
    # evaluator = None
    ```
1. Second, we need to call the method `evaluate()` to compute the result. Store the result as a number into `answer`. 
   ```python
    # TODO: Task 3
    # call the evaluate() method of the EvaluateExpression object
    # and store it
    #
    # answer = None
    ```

### Sending Challenges to Other Users

One of the features in this app is that you can send the math question to multiple users. To do this, we create a drop-down list widget for you to select which users you want to send the question to.

```python
selected_users = st.multiselect("Select Users to answer this challenge.", users["username"])
submit = st.form_submit_button("Create Question")
```

### Tasks 4 

In this task, we need to read the Excel file again for two other tables. 

* Challenges table
* Challenge-Users table

These two tables are in the `Challenges` and `Challenge-Users` worksheets respectively. Modify the following code in your file.

```python
# TODO: Task 4
# read Challenges and Challenge-Users tables 
# from the Excel file to update
#
# read the Challenges worksheet into challenge_data variable
# challenge_data = None
#
# read the Challenge-Users worksheet into assoc_data variable
# assoc_data = None
```

Make sure you store the DataFrames into `challenge_data` and `assoc_data` respectively. In `challenge_data`, we track the which challenge id uses which question id. In `assoc_data`, we track which challenge id is sent to which users. 

The next few lines of the script update the DataFrames for the three tables:

* First, we create a new id for each new entry in the tables.
  ```python
  question_id = len(question_data)
  challenge_id = len(challenge_data)
  assoc_id = len(assoc_data)
  ```
* Next, we update the Questions DataFrame and the Challenges DataFrame. Compare the variable inside the list on the right hand side with the field names in respective worksheets.
  ```python
  question_data.loc[question_id] = [question_id, expression, answer]
  challenge_data.loc[challenge_id] = [challenge_id, question_id]
  ```
* Lastly, for each user selected, we update the Challenge-User table. This table associates each challenge to individual users.
  ```python
  for user in selected_users:
      user_id = int(users.loc[users["username"] == user, "id"].iloc[0])
      assoc_data.loc[assoc_id] = [assoc_id, challenge_id, user_id]
  ```
  Here, we search for the `user_id` from the `users` DataFrame that correspond to the selected users. Then we add the `challenge_id` and `user_id` pair as an `assoc_id` into the `assoc_data` DataFrame.

### Task 5

Once the DataFrames have been updated, we can store it back in the Excel file. In order to do these, ask the following questions:

* What are the names of the variables that store the data frame which we are to update?

Modify the following code in your file.

```python
# TODO: Task 5
# update the Excel file with the new data
#
# update the Questions worksheet
# question_data.to_excel(...)
#
# update the Challenges worksheet
# challenge_data.to_excel(...)
#
# update the Challenge-Users worksheet
# assoc_data.to_excel(...)
```

Hint: You can refer to `pages/1_Users.py` to see how to write a DataFrame into an Excel sheet.

Once you are done with this part, your web app should be working fine. The other two pages are written for you and you need not do anything. However, it is good if you try to understand what the code is doing and see if you can rewrite and modify this page to make it better.

## Exercise 3

This is an open ended exercise for Mini Project 2. You need to create a new page called `5_Improved.py`. Your task is the following:

* Choose one of the previous existing pages and create an improved version of that page.
* The improvement must involve not only the **User Experience** but also the **Code Quality**.

You need to satisfy the following constraints:

* Your overall app should continue to work as it is either using the old version or the improved version. For example, let's say you create an improved version of the `2_Question.py` page. Users should still be able to use the other pages either when they create the questions using the old page `2_Question.py` or the new page `5_Improved.py`.
* The improvements must comprises both categories: User Experience and Code Quality.
* You cannot replace your user-defined functions with a third party library.
* You are allowed to refactor your code when calling Streamlit or Pandas libraries with an alternative functions in those libraries to make the code better.

Use the following guide to do this design exercise:

* Do some research about good User Interface/User Experience for an app.
* Do some research about Code Quality and some of the metrics you can use to measure good code.
* Brainstorm some of the pain points in using the various pages of the current app.
* List down various improvements that could potentially be done on the app. Consider the cost of doing those improvements as well.
* Use Pugh Chart to choose which page that you would like to improve. 
* Document all your design considerations and decisions and present them during your checkoff.
* Be prepared to do ["whiteboard coding"](https://coderpad.io/resources/learn/whiteboard-for-programmers/) on any part of the project when requested during checkoff.

## Appendix: Setup for Local Machine

You can choose to do the mini project on your local machine first before submitting to Github. 

### Install Git

You need to have Git to do the project. Download and install the software according to your OS:

- Windows: [Git for Windows](https://git-scm.com/download/win)
- Mac OS: [Git for MacOS](https://git-scm.com/download/mac)
- Unix: [Git for Unix](https://git-scm.com/downloads/linux)

### Accepting an Assignment from Github Classroom

Find the link to accept the Github Classroom assignment from eDimension for the respective week. When you accept the Github Classroom assignments, it will create a private repository of the project in your Github account. 

If you do the project with more than one person, add your teammates when accepting the assignment in Github classroom. This allows your teammates to have access to the repository as well. 

Once you have your own student copy of the repository, you can clone the repository to your local machine.

### Downloading Repository

Clone the mini project repository from Github. On your local computer's terminal or Git Bash, type the following:

```shell
cd /path/to/your/projects/folder  # change this
git clone https://your-mini-project-2-repo-url
```

**Replace the URL** with your mini project 2 URL from the Github repository page, then follow all the Virtual Environment steps above.

### Installing Environment Locally

The `Pipfile` was tested in Vocareum with Python 3.12. Some packages may break if you use a different Python version -- welcome to software engineering dependency hell! We recommend using Miniconda just for this course and create a separate environment for it.

[Download Miniconda](https://www.anaconda.com/docs/getting-started/miniconda/install), then open Anaconda Prompt (Windows) or Terminal (Mac/Linux). Run

```shell
conda create -n ddw python=3.12 pipenv
conda activate ddw 
```
This will create a new environment called `ddw` with Python 3.12 and Pipenv installed, and activate it.

Then follow the steps [above](#local). You can directly use `pipenv` for all commands instead of `python -m pipenv`.

### Submission

When you are done with local changes, do this to get all your updates into Github:

```shell
cd /path/to/your/projects/folder/mini-project-2  # change this
git add .
git commit -m "Completed version"  # or some update message
git push  # follow the instructions
```

You need to connect your Github account to Gradescope for submission. See the instruction in eDimension for this. You only need to do this once. After connecting your Github account, you can choose your repository to submit to Gradescope submission for your 2D Mini Project assignment.
