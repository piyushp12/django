from tvDatafeed import TvDatafeed, Interval
import talib
import numpy as np
from symbols import symbols_dict, interval_dict
from scheduler import scheduler
from time import sleep
import asyncio
import time 
from datetime import datetime
import pandas as pd 
import pytz
import discord
user_jobs = {}
channel_jobs = {}
channel_add_job_state_dict={}
list_of_upadted_pivots_that_on_channel={} # this stors the pivot points for wich a alert is send to the chanel {key=channel id: value [list of pivotpoints]}
#############################################################################################################
async def RSI_divergence(latest_pivot,latest_6_pivot_high,latest_6_pivot_low, latest_pivot_high,latest_pivot_low):
    alerts = []
    if (latest_pivot.equals(latest_pivot_high)):
        for i in range(1,6):
            if latest_pivot['high'] > latest_6_pivot_high.iloc[-i]['high'] and latest_pivot['RSI'] < latest_6_pivot_high.iloc[-i]['RSI']:
                alert_msg = {f"{latest_pivot.name}":f"Bearish Regular Divergence Detected (RSI) at: {latest_pivot.name}, Price {round(latest_pivot['high'],7)}.\nInvalidation point (RSI) value {round(latest_6_pivot_high.iloc[-i]['RSI'],2)}"}
                alerts.append(alert_msg)
                break
            if latest_pivot['high'] < latest_6_pivot_high.iloc[-i]['high'] and latest_pivot['RSI'] > latest_6_pivot_high.iloc[-i]['RSI']:
                alert_msg = {f"{latest_pivot.name}":f"Bearish Hidden Divergence Detected (RSI) at: {latest_pivot.name}, Price {round(latest_pivot['high'],7)}.\nInvalidation point at Price {round(latest_6_pivot_high.iloc[-i]['high'],7)}"}
                alerts.append(alert_msg)
                break
    elif(latest_pivot.equals(latest_pivot_low)):
        for i in range(1,6):
            if latest_pivot['low'] < latest_6_pivot_low.iloc[-i]['low'] and latest_pivot['RSI'] > latest_6_pivot_low.iloc[-i]['RSI']:
                alert_msg = {f"{latest_pivot.name}":f"Bullish Regular Divergence Detected (RSI) at: {latest_pivot.name}, Price {round(latest_pivot['low'],7)}.\nInvalidation point (RSI) value {round(latest_6_pivot_low.iloc[-i]['RSI'],2)}"}
                alerts.append(alert_msg)
                break
            if latest_pivot['low'] > latest_6_pivot_low.iloc[-i]['low'] and latest_pivot['RSI'] < latest_6_pivot_low.iloc[-i]['RSI']:
                alert_msg = {f"{latest_pivot.name}":f"Bullish Hidden Divergence Detected (RSI) at: {latest_pivot.name}, Price {round(latest_pivot['low'],7)}.\nInvalidation point at Price {round(latest_6_pivot_low.iloc[-i]['low'],7)}"}
                alerts.append(alert_msg)
                break
    else: 
        pass
            
    return alerts

#############################################################################################################
async def Stochastic_divergence(latest_pivot,latest_6_pivot_high,latest_6_pivot_low, latest_pivot_high,latest_pivot_low):
    alerts = []
    if (latest_pivot.equals(latest_pivot_high)):
        for i in range(1,6):
            if latest_pivot['high'] > latest_6_pivot_high.iloc[-i]['high'] and latest_pivot['slowd'] < latest_6_pivot_high.iloc[-i]['slowd']:
                alert_msg = {f"{latest_pivot.name}":f"Bearish Regular Divergence Detected (Stochastic) at: {latest_pivot.name}, Price {round(latest_pivot['high'],7)}.\nInvalidation point (Stochastic) value {round(latest_6_pivot_high.iloc[-i]['slowd'],2)}"}
                alerts.append(alert_msg)
                break
            if latest_pivot['high'] < latest_6_pivot_high.iloc[-i]['high'] and latest_pivot['slowd'] > latest_6_pivot_high.iloc[-i]['slowd']:
                alert_msg = {f"{latest_pivot.name}":f"Bearish Hidden Divergence Detected (Stochastic) at: {latest_pivot.name}, Price {round(latest_pivot['high'],7)}.\nInvalidation point at Price {round(latest_6_pivot_high.iloc[-i]['high'],7)}"}
                alerts.append(alert_msg)
                break

    elif(latest_pivot.equals(latest_pivot_low)): 
        for i in range(1,6):
            if latest_pivot['low'] < latest_6_pivot_low.iloc[-i]['low'] and latest_pivot['slowd'] > latest_6_pivot_low.iloc[-i]['slowd']:
                alert_msg = {f"{latest_pivot.name}":f"Bullish Regular Divergence Detected (Stochastic) at: {latest_pivot.name}, Price {round(latest_pivot['low'],7)}.\nInvalidation point (Stochastic) value {round(latest_6_pivot_low.iloc[-i]['slowd'],2)}"}
                alerts.append(alert_msg)
                break
            if latest_pivot['low'] > latest_6_pivot_low.iloc[-i]['low'] and latest_pivot['slowd'] < latest_6_pivot_low.iloc[-i]['slowd']:
                alert_msg = {f"{latest_pivot.name}":f"Bullish Hidden Divergence Detected (Stochastic) at: {latest_pivot.name}, Price {round(latest_pivot['low'],7)}.\nInvalidation point at Price {round(latest_6_pivot_low.iloc[-i]['low'],7)}"}
                alerts.append(alert_msg)
                break
    else: 
        pass
    return alerts

#############################################################################################################
async def OBV_divergence(latest_pivot,latest_6_pivot_high,latest_6_pivot_low, latest_pivot_high,latest_pivot_low):
    alerts = []
    if (latest_pivot.equals(latest_pivot_high)):
        for i in range(1,6):
            if latest_pivot['high'] > latest_6_pivot_high.iloc[-i]['high'] and latest_pivot['obv'] < latest_6_pivot_high.iloc[-i]['obv']:
                alert_msg = {f"{latest_pivot.name}":f"Bearish Regular Divergence Detected (obv) at: {latest_pivot.name}, Price {round(latest_pivot['high'],7)}.\nInvalidation point (obv) value {round(latest_6_pivot_high.iloc[-i]['obv'],2)}"}
                alerts.append(alert_msg)
                break
            if latest_pivot['high'] < latest_6_pivot_high.iloc[-i]['high'] and latest_pivot['obv'] > latest_6_pivot_high.iloc[-i]['obv']:
                alert_msg = {f"{latest_pivot.name}":f"Bearish Hidden Divergence Detected (obv) at: {latest_pivot.name}, Price {round(latest_pivot['high'],7)}.\nInvalidation point at Price {round(latest_6_pivot_high.iloc[-i]['high'],7)}"}
                alerts.append(alert_msg)
                break
    elif(latest_pivot.equals(latest_pivot_low)):   
        for i in range(1,6): 
            if latest_pivot['low'] < latest_6_pivot_low.iloc[-i]['low'] and latest_pivot['obv'] > latest_6_pivot_low.iloc[-i]['obv']:
                alert_msg = {f"{latest_pivot.name}":f"Bullish Regular Divergence Detected (obv) at: {latest_pivot.name}, Price {round(latest_pivot['low'],7)}.\nInvalidation point (obv) value {round(latest_6_pivot_low.iloc[-i]['obv'],2)}"}
                alerts.append(alert_msg)
                break
            if latest_pivot['low'] > latest_6_pivot_low.iloc[-i]['low'] and latest_pivot['obv'] < latest_6_pivot_low.iloc[-i]['obv']:
                alert_msg = {f"{latest_pivot.name}":f"Bullish Hidden Divergence Detected (obv) at: {latest_pivot.name}, Price {round(latest_pivot['low'],7)}.\nInvalidation point at Price {round(latest_6_pivot_low.iloc[-i]['low'],7)}"}
                alerts.append(alert_msg)
                break
    else: 
        pass
    return alerts

#############################################################################################################   
async def CVD_divergence(latest_pivot,latest_6_pivot_high,latest_6_pivot_low, latest_pivot_high,latest_pivot_low):
    alerts = []
    if (latest_pivot.equals(latest_pivot_high)):
        for i in range(1,6):
            if latest_pivot['high'] > latest_6_pivot_high.iloc[-i]['high'] and latest_pivot['cvd'] < latest_6_pivot_high.iloc[-i]['cvd']:
                alert_msg = {f"{latest_pivot.name}":f"Bearish Regular Divergence Detected (cvd) at: {latest_pivot.name}, Price {round(latest_pivot['high'],7)}.\nInvalidation point (cvd) value {round(latest_6_pivot_high.iloc[-i]['cvd'],2)}"}
                alerts.append(alert_msg)
                break
            if latest_pivot['high'] < latest_6_pivot_high.iloc[-i]['high'] and latest_pivot['cvd'] > latest_6_pivot_high.iloc[-i]['cvd']:
                alert_msg = {f"{latest_pivot.name}":f"Bearish Hidden Divergence Detected (cvd) at: {latest_pivot.name}, Price {round(latest_pivot['high'],7)}.\nInvalidation point at Price {round(latest_6_pivot_high.iloc[-i]['high'],7)}"}
                alerts.append(alert_msg)
                break
    elif(latest_pivot.equals(latest_pivot_low)):

        for i in range(1,6):
            if latest_pivot['low'] < latest_6_pivot_low.iloc[-i]['low'] and latest_pivot['cvd'] > latest_6_pivot_low.iloc[-i]['cvd']:
                alert_msg = {f"{latest_pivot.name}":f"Bullish Regular Divergence Detected (cvd) at: {latest_pivot.name}, Price {round(latest_pivot['low'],7)}.\nInvalidation point (cvd) value {round(latest_6_pivot_low.iloc[-i]['cvd'],2)}"}
                alerts.append(alert_msg)
                break
            if latest_pivot['low'] > latest_6_pivot_low.iloc[-i]['low'] and latest_pivot['cvd'] < latest_6_pivot_low.iloc[-i]['cvd']:
                alert_msg = {f"{latest_pivot.name}":f"Bullish Hidden Divergence Detected (cvd) at: {latest_pivot.name}, Price {round(latest_pivot['low'],7)}.\nInvalidation point at Price {round(latest_6_pivot_low.iloc[-i]['low'],7)}"}
                alerts.append(alert_msg)
                break
    else: 
        pass
    return alerts

#############################################################################################################
async def MACD_divergence(latest_pivot,latest_6_pivot_high,latest_6_pivot_low, latest_pivot_high,latest_pivot_low):
    alerts = []
    if (latest_pivot.equals(latest_pivot_high)):
        for i in range(1,6):
            if latest_pivot['high'] > latest_6_pivot_high.iloc[-i]['high'] and latest_pivot['macd'] < latest_6_pivot_high.iloc[-i]['macd'] and latest_pivot['histogram'] < latest_6_pivot_low.iloc[-i]['histogram']:
                alert_msg = {f"{latest_pivot.name}":f"Bearish Regular Divergence Detected (macd+histo) at: {latest_pivot.name}, Price {round(latest_pivot['high'],7)}.\nInvalidation point (macd) value {round(latest_6_pivot_high.iloc[-i]['macd'],2)} (histogram) value {round(latest_6_pivot_high.iloc[-i]['histogram'],2)}"}
                alerts.append(alert_msg)
                break
            if latest_pivot['high'] < latest_6_pivot_high.iloc[-i]['high'] and latest_pivot['macd'] > latest_6_pivot_high.iloc[-i]['macd'] and latest_pivot['histogram'] > latest_6_pivot_low.iloc[-i]['histogram']:
                alert_msg = {f"{latest_pivot.name}":f"Bearish Hidden Divergence Detected (macd+histo) at: {latest_pivot.name}, Price {round(latest_pivot['high'],7)}.\nInvalidation point at Price {round(latest_6_pivot_high.iloc[-i]['high'],7)}"}
                alerts.append(alert_msg)
                break
    elif(latest_pivot.equals(latest_pivot_low)):
        for i in range(1,6):
            if latest_pivot['low'] < latest_6_pivot_low.iloc[-i]['low'] and latest_pivot['macd'] > latest_6_pivot_low.iloc[-i]['macd'] and latest_pivot['histogram'] > latest_6_pivot_low.iloc[-i]['histogram']:
                alert_msg = {f"{latest_pivot.name}":f"Bullish Regular Divergence Detected (macd+histo) at: {latest_pivot.name}, Price {round(latest_pivot['low'],7)}.\nInvalidation point (macd) value {round(latest_6_pivot_low.iloc[-i]['macd'],2)} (histogram) value {round(latest_6_pivot_low.iloc[-i]['histogram'],2)}"}
                alerts.append(alert_msg)
                break
            if latest_pivot['low'] > latest_6_pivot_low.iloc[-i]['low'] and latest_pivot['macd'] < latest_6_pivot_low.iloc[-i]['macd'] and latest_pivot['histogram'] < latest_6_pivot_low.iloc[-i]['histogram']:
                alert_msg = {f"{latest_pivot.name}":f"Bullish Hidden Divergence Detected (macd+histo) at: {latest_pivot.name}, Price {round(latest_pivot['low'],7)}.\nInvalidation point at Price {round(latest_6_pivot_low.iloc[-i]['low'],7)}"}
                alerts.append(alert_msg)
                break
    else: 
        pass
    return alerts

#############################################################################################################
from datetime import timezone
async def botjob(symbol, exchange, message,is_private, interval_message, interval=Interval.in_1_hour):
    start_time = time.time()
    # print(f"--------------------START Symbol: {symbol}--------------------")
    # tv = TvDatafeed(username="piyush_sharmam7pd2", password="Mobiloitte@1")
    tv = TvDatafeed(username='tmv_crypto', password='TahNaf5253&')
    
    df = tv.get_hist(symbol=symbol, exchange=exchange, interval=interval, n_bars=200)
    
    df['RSI'] = talib.RSI(df['close'])
    df['slowk'], df['slowd'] = talib.STOCH(df['high'], df['low'], df['close'])
    df['obv'] = (np.sign(df['close'].diff()) * df['volume']).fillna(0).cumsum()
    df['cvd'] = df['volume'].diff().cumsum()
    fast_period,slow_period,signal_period,prd=12,26,9,5
    df['macd'], df['signal'], df['histogram'] = talib.MACD(df['close'], fastperiod=fast_period, slowperiod=slow_period, signalperiod=signal_period)

    current_price = df['close'].iloc[-1]  
    LEN = 5
    df['PivotHigh'] = df['high'] == df['high'].rolling(2 * LEN + 1, center=True).max()
    df['PivotLow'] = df['low'] == df['low'].rolling(2 * LEN + 1, center=True).min()

    latest_6_pivot_high = df[df['PivotHigh']].tail(6)
    latest_6_pivot_low = df[df['PivotLow']].tail(6)

    latest_pivot_high = latest_6_pivot_high.iloc[-1].copy()
    latest_pivot_low = latest_6_pivot_low.iloc[-1].copy()
    latest_6_pivot_high = latest_6_pivot_high.iloc[:-1]
    latest_6_pivot_low = latest_6_pivot_low.iloc[:-1]
    latest_6_pivot_high=latest_6_pivot_high[::-1]
    latest_6_pivot_low=latest_6_pivot_low[::-1]

    rsi_alerts = []
    stochastics_alerts = []
    obv_alerts = []
    cvd_alerts = []
    macd_alerts = []

    latest_pivot = []
    if(latest_pivot_high.name > latest_pivot_low.name):
        latest_pivot = latest_pivot_high
    else:   
        latest_pivot = latest_pivot_low   

    rsi_alerts = await RSI_divergence(latest_pivot,latest_6_pivot_high,latest_6_pivot_low, latest_pivot_high,latest_pivot_low) 
    stochastics_alerts = await Stochastic_divergence(latest_pivot,latest_6_pivot_high,latest_6_pivot_low, latest_pivot_high,latest_pivot_low)
    obv_alerts = await OBV_divergence(latest_pivot,latest_6_pivot_high,latest_6_pivot_low, latest_pivot_high,latest_pivot_low)
    cvd_alerts = await CVD_divergence(latest_pivot,latest_6_pivot_high,latest_6_pivot_low, latest_pivot_high,latest_pivot_low)
    macd_alerts = await MACD_divergence(latest_pivot,latest_6_pivot_high,latest_6_pivot_low, latest_pivot_high,latest_pivot_low)


    def merge_json_list(json_list):
        result_dict = {}
        for json_obj in json_list:
            for key, value in json_obj.items():
                if key in result_dict:
                    result_dict[key].append(value)
                else:
                    result_dict[key] = [value]
        return result_dict
    
  
    rsi_alerts=merge_json_list(rsi_alerts)
    stochastics_alerts=merge_json_list(stochastics_alerts)
    obv_alerts=merge_json_list(obv_alerts)
    cvd_alerts=merge_json_list(cvd_alerts)
    macd_alerts=merge_json_list(macd_alerts)

    def merge_all_dicts(**dicts):
        result = {}
        
        for name, alerts in dicts.items():
            for key, alert_messages in alerts.items():
                if key not in result:
                    result[key] = {name: alert_messages}
                else:
                    result[key][name] = alert_messages
        return result
    
    merged_result = merge_all_dicts(
        rsi_alerts=rsi_alerts,
        stochastics_alerts=stochastics_alerts,
        obv_alerts=obv_alerts,
        cvd_alerts=cvd_alerts,
        macd_alerts=macd_alerts
    )
    await add_to_formatted_message(message, merged_result,symbol,current_price,is_private,interval_message)
    end_time = time.time()
    runtime = end_time - start_time
    print(f"--------------------END Symbol: {symbol} - execution time: {runtime}--------------------")



#############################################################################################################
async def add_to_formatted_message(message, merged_result,symbol,current_price,is_private,interval_message):
    if not merged_result:
        return
    if message.channel.id not in list_of_upadted_pivots_that_on_channel:
        list_of_upadted_pivots_that_on_channel[message.channel.id] = {}
    if symbol not in list_of_upadted_pivots_that_on_channel[message.channel.id]:
        list_of_upadted_pivots_that_on_channel[message.channel.id][symbol] = []
    message_chunk = f"Symbol : {symbol}\nCurrent Price: {round(current_price,7)}"
    embed = discord.Embed(title=message_chunk)
    # embed.set_author(name=message_chunk)
    embed.set_footer(text=interval_message)
    for keys, values in merged_result.items():
        if keys in list_of_upadted_pivots_that_on_channel[message.channel.id][symbol]:
            continue
        else:
            list_of_upadted_pivots_that_on_channel[message.channel.id][symbol].append(keys)
            for key, value in values.items():
                # embed_list=[]
                if "rsi_alerts" in key:
                    description= f"\n\tRSI Divergences\n"
                elif "stochastics_alerts" in key:
                    description = f"\n\tStochastic Divergences\n"
                elif "obv_alerts" in key:
                    description = f"\n\tOBV Divergences\n"
                elif "cvd_alerts" in key:
                    description = f"\n\tCVD Divergences\n"
                elif "macd_alerts" in key:
                    description = f"\n\tMACD+Histo Divergences:\n"
                formatted_message = ''
                for alert in value:
                    if "Bullish Regular" in alert:
                        alert = f"""```diff\n+ {alert}\n```"""
                        embed.add_field(name=description,value=alert,inline=False)
                        # embed = discord.Embed(
                        #     title=description,
                        #     color=discord.Color.green(),
                        #     description=alert
                        # )
                        # embed.set_author(name=message_chunk)
                        # embed.set_footer(text=interval_message)
                        # embed_list.append(embed)
                    elif "Bearish Regular" in alert:
                        alert = f"""```diff\n- {alert}\n```"""
                        embed.add_field(name=description,value=alert,inline=False)
                        # embed = discord.Embed(
                        #     title=description,
                        #     color=discord.Color.red(),
                        #     description=alert
                        # )
                        # embed.set_author(name=message_chunk)
                        # embed.set_footer(text=interval_message)
                        # embed_list.append(embed)
                    elif "Bearish Hidden" in alert:
                        alert = f"""```yaml\n{alert}\n```"""
                        embed.add_field(name=description,value=alert,inline=False)
                        # embed = discord.Embed(
                        #     title=description,
                        #     color=discord.Color.blue(),
                        #     description=alert
                        # )
                        # embed.set_author(name=message_chunk)
                        # embed.set_footer(text=interval_message)
                        # embed_list.append(embed)
                    elif "Bullish Hidden" in alert:
                        alert = f"""```\n{alert}\n```"""
                        embed.add_field(name=description,value=alert,inline=False)
                        # embed = discord.Embed(
                        #     title=description,
                        #     color=discord.Color.orange(),
                        #     description=alert
                        # )
                        # embed.set_author(name=message_chunk)
                        # embed.set_footer(text=interval_message)
                        # embed_list.append(embed)
        await message.author.send(embed=embed) if is_private else await message.channel.send(embed=embed)


import sqlite3
db_path = '/Users/admin/Desktop/Discord-django/Discord_Taher/db.sqlite3'
connection = sqlite3.connect(db_path)
cursor = connection.cursor()
cursor.execute("SELECT * FROM App_cryptopair")
data = cursor.fetchall()
print("data",data)
cursor.close()
connection.close()

#############################################################################################################
async def find_symbol_exchange(message, is_private,interval=Interval.in_1_hour):
    misfire_grace_time = 180
    max_instances = 1000
    user_id = message.author.id
    channel_id=""
    
    

    if not is_private:
        channel_id= message.channel.id
        channel_add_job_state_dict[channel_id]=True
    # for symbol in symbols_dict:
    #     await asyncio.sleep(1)  
    #     exchange, symbol = symbols_dict[symbol]
    symbols_dict = {}
    for symbol in data:
        symbol_id, symbol, exchange = symbol
        symbols_dict[symbol] = (exchange, symbol)

        
        if interval == Interval.in_15_minute:
            job = scheduler.add_job(botjob, 'interval', minutes=1, args=[symbol, exchange, message,is_private,"15 minutes interval", interval], misfire_grace_time=misfire_grace_time, max_instances=max_instances)
        elif interval == Interval.in_1_hour:
            job = scheduler.add_job(botjob, 'interval', hours=1, args=[symbol, exchange, message,is_private,"1 hour interval", interval], misfire_grace_time=misfire_grace_time, max_instances=max_instances)
        elif interval == Interval.in_4_hour:
            job = scheduler.add_job(botjob, 'interval', hours=4, args=[symbol, exchange, message,is_private,"4 hours interval", interval], misfire_grace_time=misfire_grace_time, max_instances=max_instances)
        elif interval == Interval.in_daily:
            job = scheduler.add_job(botjob, 'interval', days=1, args=[symbol, exchange, message,is_private,"1 day interval", interval], misfire_grace_time=misfire_grace_time, max_instances=max_instances)
        elif interval == Interval.in_weekly:
            job = scheduler.add_job(botjob, 'interval', weeks=1, args=[symbol, exchange, message,is_private,"1 week interval", interval], misfire_grace_time=misfire_grace_time, max_instances=max_instances)
        await asyncio.sleep(2)
        if is_private:
            if user_id not in user_jobs:
                user_jobs[user_id] = []
            user_jobs[user_id].append(job)
        else:
            if channel_id not in channel_jobs:
                channel_jobs[channel_id] = []
            channel_jobs[channel_id].append(job)
    channel_add_job_state_dict[channel_id]=False

async def stop_all_jobs(message,is_private):
    await message.author.send("Initiating the bot's stop process. Stopping scheduled jobs and cleaning up resources.") if is_private else await message.channel.send("Initiating the bot's stop process. Stopping scheduled jobs and cleaning up resources.")
    if is_private:
        user_id = message.author.id
        if user_id in user_jobs:
            for job in user_jobs[user_id]:

                scheduler.remove_job(job.id)
            del user_jobs[user_id]
    else:
        channel_id= message.channel.id
        if channel_id in channel_jobs:
            while(channel_add_job_state_dict[channel_id]):
                for job in channel_jobs[channel_id]:
                    try:
                        scheduler.remove_job(job.id)
                    except Exception as e:
                        pass
                await asyncio.sleep(5) 
            for job in channel_jobs[channel_id]:
                    try:
                        scheduler.remove_job(job.id)
                    except Exception as e:
                        pass
            del channel_jobs[channel_id]
    await message.author.send("Bot stop process completed successfully.") if is_private else await message.channel.send("Bot stop process completed successfully.")

