## Seeking Investors for My AI-Driven, Deep Learning Trading Project

I want to make a Deep Learning (Artificial Intelligence) model that will change how we do options selling. If this works, I also want to try it with stocks, other options, foreign markets, and more. For this, I need investors who can support me. Your investment will let me work on this project full time.
As the sole developer of this system, I will have the flexibility to dedicate my full efforts towards this project. With proper funding and support, I aim to create an innovative trading platform and grow it into a successful business.

## Want To Join?

If you're interested in this project, I would love to talk more. You can contact me at:

- Email: kodakandlasrikar99@gmail.com
- Phone no: (+91) 9176462946
- LinkedIn: [https://www.linkedin.com/in/srikar-kodakandla/]

Let's work together to change trading.

## About Me

I have extensive experience building algorithmic trading strategies and systems, including 4+ years of active trading experience across stocks, options, currencies, and commodities. In addition to trading system development, I have a strong background in cutting-edge deep learning techniques.

## About this project : Fully automated nifty options trading

It is fully automated algo trading , It trades for you in Nifty options using Zerodha kite . You don't need to pay 4000 indian rupees monthly for kite api because this program uses selenium to access zerodha kite website

The Program follows supertrend strategy with adx to trade options , i rigorously backtested nifty in 5 min chart and find out the best supertrend values and adx values. when ever supertrend gives buy signal , This program sells options corresponding to the buy signal. it also checks all combinations of nifty options to sell , to see which combination gives more profits, there is a risk paramater in kite_strategy.py , where 50 is lowest possible risk , where it tries to sell options with 50 points difference (if nifty is at 14000 and supertrend gives buy signal then it tries to sell 14050PE and buys 14000PE) and if you choose 500 then , it tries to select  options with 500 points difference (selecting 13500PE buy and 14000 PE sell). when the option goes above 95% of your profit , then it sells and selects next week options and trades with them.

![Screenshot from 2022-06-25 20-14-25](https://user-images.githubusercontent.com/46400867/175778598-47c9f645-084d-46e8-a4ae-5e90cee7b07a.png)

as shown in the screenshot , it sells corresponding options when ever a signal is triggered in supertrend indicator


you can use crontab to schedule to trade everyday , write the below code in "crontab -e"

>59 08 * * 1-5  DISPLAY=:10 screen -dmS srikartrade ipython3 kite_strategy.py # it trades by above explained strategy 

>59 08 * * 1-5  DISPLAY=:10 screen -dmS check_database ipython3 check_database.py  #to check if the live data is fetching from fyers api

>30 15 * * 1-5 screen -XS database quit # it stops trade at 3:30 PM as markets closes at that time


The program uses selenium to make trades in zerodha kite and it uses fyers account to get past data . Fyers provides free api for past data and trading.

This code is kept publicly in github for educational purpose only .I am not responsible with your profit and losses.

