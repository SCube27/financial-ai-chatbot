import json
import openai
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import yfinance as yf

# Reading the api key using the openai library
openai.api_key = open('API_KEY', 'r').read()

# Function for fetching the stock price (Parameter will be the ticker of the stock)
def get_stock_price(ticker):
    return str(yf.Ticker(ticker).history(period='1y').iloc[-1].Close)
    # we return the string for the stock price asked in the prompt for the period of last one year and fetch the last/latest position of the sotck marked as -1

# Function for calculating Simple Moving Average for the given window of time period of stock price
def calculate_SMA(ticker, window):
    data = yf.Ticker(ticker).history(period='1y').Close
    return str(data.rolling(window=window).mean().iloc[-1])

# Function for calculating Exponential Moving Average
def calculate_EMA(ticker, window):
    data = yf.Ticker(ticker).history(period='1y').Close
    return str(data.ewm(span=window, adjust=False).mean().iloc[-1])

# Function for calculating Relative Strength Index i.e to get the previous strength or weakness of the stock
def calculate_RSI(ticker):
    data = yf.Ticker(ticker).history(period='1y').Close
    delta = data.diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)
    ema_up = up.ewm(com=14-1, adjust=False).mean()
    ema_down = down.ewm(com=14-1, adjust=False).mean() 
    rs = ema_up / ema_down
    return str(100 - (100 / (1+rs)).iloc[-1])

# Function for calculating Moving Average Convergence Divergence
def calculate_MACD(ticker):
    data = yf.Ticker(ticker).history(period='1y').Close
    short_EMA = data.ewm(span=12, adjust=False).mean()
    long_EMA = data.ewm(span=26, adjust=False).mean()
    
    MACD = short_EMA - long_EMA
    signal = MACD.ewm(span=9, adjust=False).mean()
    MACD_histogram = MACD - signal

    return f'{MACD[-1]}, {signal[-1]}, {MACD_histogram[-1]}'

def plot_stock_price(ticker):
    data = yf.Ticker(ticker).history(period='1y')
    plt.figure(figsize=(10, 5))
    plt.plot(data.index, data.Close)
    plt.title(f'{ticker} Stock Price Over Last Year')
    plt.xlabel('Date')
    plt.ylabel('Stock Price ($)')
    plt.grid(True)
    plt.savefig('stock.png')
    plt.close()

# Creating a list of functions and their overall description which will be taken by API 
Functions = [
    {
        'name' : 'get_stock_price',
        'description' : 'Gets the latest stock price given the ticker symbol of the company.',
        'parameters' : {
            'type' : 'object',
            'properties' : {
                'ticker' : {
                    'type' : 'string',
                    'description' : 'The stock ticker symbol for a company (for example GOOG for Google). Note FB is renamed to META.'
                }
            },
            'required' : ['ticker']
        }
    },
    {
        'name' : 'calculate_SMA',
        'description' : 'Calculate the simple moving average for a given stock ticker and a window.',
        'parameters' : {
            'type' : 'object',
            'properties' : {
                'ticker' : {
                    'type' : 'string',
                    'description' : 'The stock ticker symbol for a company (for example GOOG for Google). Note FB is renamed to META.'
                },
                'window' : {
                    'type' : 'integer',
                    'description' : 'The timeframe to consider when calculating the SMA.'
                }
            },
            'required' : ['ticker', 'window'],
        },
    },
    {
        'name' : 'calculate_EMA',
        'description' : 'Calculate the exponential moving average for a given stock ticker and a window.',
        'parameters' : {
            'type' : 'object',
            'properties' : {
                'ticker' : {
                    'type' : 'string',
                    'description' : 'The stock ticker symbol for a company (for example GOOG for Google). Note FB is renamed to META.'
                },
                'window' : {
                    'type' : 'integer',
                    'description' : 'The timeframe to consider when calculating the EMA.'
                }
            },
            'required' : ['ticker', 'window'],
        },
    },
    {
        'name' : 'calculate_RSI',
        'description' : 'Calculate the RSI for a given stock ticker.',
        'parameters' : {
            'type' : 'object',
            'properties' : {
                'ticker' : {
                    'type' : 'string',
                    'description' : 'The stock ticker symbol for a company (for example GOOG for Google). Note FB is renamed to META.'
                },
            },
            'required' : ['ticker'],
        },
    },
    {
        'name' : 'calculate_MACD',
        'description' : 'Calculate the Moving Average Convergence/Divergence for a given stock ticker.',
        'parameters' : {
            'type' : 'object',
            'properties' : {
                'ticker' : {
                    'type' : 'string',
                    'description' : 'The stock ticker symbol for a company (for example GOOG for Google). Note FB is renamed to META.'
                },
            },
            'required' : ['ticker'],
        },
    },
    {
        'name' : 'plot_stock_price',
        'description' : 'Plot the stock price for the last year given the ticker symbol of the company.',
        'parameters' : {
            'type' : 'object',
            'properties' : {
                'ticker' : {
                    'type' : 'string',
                    'description' : 'The stock ticker symbol for a company (for example GOOG for Google). Note FB is renamed to META.'
                },
            },
            'required' : ['ticker'],
        }, 
    },
]

# Created a dictionary that maps the function name with its function call
available_functions = {
    'get_stock_price' : get_stock_price,
    'calculate_SMA' : calculate_SMA,
    'calculate_EMA' : calculate_EMA,
    'calculate_RSI' : calculate_RSI,
    'calculate_MACD' : calculate_MACD,
    'plot_stock_price' : plot_stock_price
}

# Building the web application using streamlit
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# title of the web page
st.title('Stock Analysis Assistant')

# Taking the user input
user_input = st.text_input("Your Input:")

# If user input is present then we process it and send it to openai api to process the output
if user_input:
    try:
        # Sent the processed input to openai api
        st.session_state['messages'].append({'role' : 'user', 'content' : f'{user_input}'})

        # Return the response output from the api
        response = openai.ChatCompletion.create(
            model = 'gpt-3.5-turbo-0613',
            messages = st.session_state['messages'],
            functions = Functions,
            function_call = 'auto'
        )

        # Response message for the output generated
        response_message = response['choices'][0]['message']

        # Only run the model if we get a function call
        if response_message.get('function_call'):
            function_name = response_message['function_call']['name'] # got the function name
            function_args = json.loads(response_message['function_call']['arguments']) # to get the function args
            # for functions with a single argument
            if function_name in ['get_stock_price', 'calculate_RSI', 'calculate_MACD', 'plot_stock_price']:
                args_dict = {'ticker': function_args.get('ticker')}
            # for functions with two arguments
            elif function_name in ['calculate_SMA', 'calculate_EMA']: 
                args_dict = {'ticker': function_args.get('ticker'), 'window': function_args.get('window')}

            function_to_call = available_functions[function_name]
            function_response = function_to_call(**args_dict)

            if function_name == 'plot_stock_price':
                st.image('stock.png')
            else:
                st.session_state['messages'].append(response_message)
                st.session_state['messages'].append(
                    {
                        'role' : 'function',
                        'name' : function_name,
                        'content' : function_response
                    }
                )
                second_response = openai.ChatCompletion.create(
                    model = 'gpt-3.5-turbo-0613',
                    messages = st.session_state['messages']
                )
                st.text(second_response['choices'][0]['message']['content'])
                st.session_state['messages'].append({'role' : 'assistant', 'content' : second_response['choices'][0]['message']['content']})
                st.session_state['messages']
        # if function call is not made only display the text as asked by user
        else:
            st.text(response_message['content'])
            st.session_state['messages'].append({'role' : 'assistant', 'content' : response_message['content']})
    except Exception as e:
        raise e

