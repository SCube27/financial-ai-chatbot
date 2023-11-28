### financial-ai-chatbot
## A ChatGPT powered AI chatbot for assisting information regarding stocks

# **Features:**
1. Gives the recent stock price taken by the yahoo finance API to the user.
2. Plots the visualizations and graphs for the last year of a given stock.
3. Can calculate *SMA*, *EMA*, *RSI* and *MACD* for given time frame of a specific stock asked.
_(More features could be added with the time)_

# **How To Use:**
1. Clone the repository to your local server.
2. From [Open AI](platforms.openai.com) create your account if not. Generate an API Key store it in the file named API_KEY in this repository by removing the existing text.
3. Using command prompt navigate to the location where this repository is stored.
4. Or you can use the code editor of your choice, open this repository and use its associated terminal.
5. In the command line install the following libraries :
        _a. json_
        _b. openai_
        _c. pandas_
        _d. matplotlib_
        _e. streamlit_
        _f. yfinance_
    
    (Note : You should have latest python preinstalled in your PC)
    **To add the following libraries in Windows use following command**
    ```pip install json openai==0.28 pandas matplotlib streamlit yfinance```

    **To add the following libraries in MacOS use following command**
    ```pip3 install json openai==0.28 pandas matplotlib streamlit yfinance```

6. Once the libraries are installed, navigate to the repo using command line or open it in your code editor and use its terminal. Type the following command :
    ```streamlit run main.py```

*** (Note: The OpenAi API requires some amount of credits. If using the API for first time the credits might be free else a small amount has to be paid to use API services and make model running.) ***

# Thank You!