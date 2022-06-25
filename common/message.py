from termcolor import colored
def message(a):
    #''.center(100,'*')
    #print(a)
    print()
    print (colored(a, 'green'))
    try:
        #import telepot
        import telegram_send
#telegram_send.send(messages=["Wow that was easy!"])
    except:
        try:
            import pip
            pip.main(['install', 'telegram_send'])
            #!pip install telepot
        except Exception as e:
            print(e)
            print('install telegram_send pip package ')
    TOKEN = "1920193166:AAEIi9AsdfsL6Imbo7pZn-PaVN9JsdfsMLocthiIKo"  #Enter token of telegram , it will notify during order updates
    chat_id = "13513433780503"   #chatid in telegram 
    try:
        import telegram_send
        telegram_send.send(messages=[a])
        #import telepot
        #bot = telepot.Bot(TOKEN)"Wow that was easy!"
    except Exception as e:
        print(e)
        print('unable to send message')

