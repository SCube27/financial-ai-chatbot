# Financial AI Chatbot
- A ChatGPT powered AI chatbot for assisting real time information regarding searched stocks.

### Tech Stack Used:
1. Python
2. Pandas
3. Matplotlib
4. Streamlit
5. Yahoo Finance API (yfinance)
6. OpenAI API (openai)

## Features:
1. Gives the real time price of the searched stock, fetched through the yahoo finance API to the user.

2. Plots the visualizations and graphs of the stock performance in the specified time period by the user.

3. Calculates **Simple Moving Average**(*SMA*), **Exponential Moving Average**(*EMA*), **Relative Strength Index**(*RSI*) and **Moving Average Convergence / Divergence**(*MACD*) for given time frame of a specific stock asked.

## Installation & Setup:
1. Clone the repository locally:
```
git clone https://github.com/SCube27/financial-ai-chatbot.git
```

2. Install the required libraries:
```
pip install -r requirements.txt
```

3. From [Open AI](platforms.openai.com) create your account if not already present and generate an `API Key`.

4. Create a file named `API_KEY` in this cloned reposeitory and paste the generated key from OpenAI.

5. Run the model:
```
streamlit run main.py
```

6. Follow the link given in the console to access the chatbot.

*** (Note: The OpenAi API requires some amount of credits. If using the API for first time the credits might be free else a small amount has to be paid to use API services and make model running.) ***

### Outputs:
- The outputs for the project are present in the outputs folder.

### Thank You!