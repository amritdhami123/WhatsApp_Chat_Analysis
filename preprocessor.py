import re
import pandas as pd

def preprocess(text):
    pattern = r"\d{1,2}/\d{1,2}/\d{4},\s\d{1,2}:\d{2}\u202f[ap]m\s-\s"

    messages = re.split(pattern, text)[1:]
    dates = re.findall(pattern, text)

    df = pd.DataFrame({"user_message": messages, "message_date": dates})

    df["message_date"] = df["message_date"].str.replace(r"\s[–-]\s$", "", regex=True)
    df["datetime"] = pd.to_datetime(df["message_date"], format="%d/%m/%Y, %I:%M\u202f%p")
    df = df.drop(columns=["message_date"]).rename(columns={"datetime": "date"})

    users = []
    messages = []

    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['date'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce')
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    df = df.loc[df['user'] != 'group_notification'].copy()
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by='date', ascending=True)
    df = df.reset_index(drop=True)

    return df
