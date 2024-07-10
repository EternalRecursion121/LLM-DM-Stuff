from datetime import datetime
import re
import os
import json

def format_messages_whatsapp(messages):
    # Regular expression to match lines that start with a timestamp and sender
    message_pattern = re.compile(r'(\d{2}/\d{2}/\d{4}, \d{2}:\d{2}) - ([^:]+): (.+)')
    
    formatted_messages = []

    for line in messages.split('\n'):
        match = message_pattern.match(line)
        if match:
            timestamp, author, content = match.groups()
            formatted_messages.append({
                'timestamp': timestamp,
                'author': author,
                'content': content
            })
        elif formatted_messages:
            # If it's not a new message, append the line to the content of the last message
            formatted_messages[-1]['content'] += '\n' + line

    return formatted_messages

def format_messages_discord(messages):
    formatted_messages = []

    for message in messages:
        content = message['content'] if message['content'] else "<Media omitted>"
        timestamp = datetime.fromisoformat(message['timestamp']).strftime('%d/%m/%Y, %H:%M')
        author = message['author']['username']
        
        formatted_messages.append({
            'timestamp': timestamp,
            'author': author,
            'content': content
        })

    return formatted_messages

def save_conversation(conversation, filename):
    # Create a new folder called 'conversations' if it doesn't exist
    folder_name = 'conversations'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    # Full path for the file
    file_path = os.path.join(folder_name, filename)
    
    # Write the conversation to a JSONL file
    with open(file_path, 'w', encoding='utf-8') as f:
        for message in conversation:
            json.dump(message, f, ensure_ascii=False)
            f.write('\n')

def save_conversation(conversation, filename):
    # Create a new folder called 'conversations' if it doesn't exist
    folder_name = 'conversations'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    # Full path for the file
    file_path = os.path.join(folder_name, filename)
    
    # Write the conversation to a JSONL file
    with open(file_path, 'w', encoding='utf-8') as f:
        for message in conversation:
            json.dump(message, f, ensure_ascii=False)
            f.write('\n')

def save_conversation_txt(conversation, filename):
    # Create a new folder called 'conversations_txt' if it doesn't exist
    folder_name = 'conversations_txt'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    # Full path for the file
    file_path = os.path.join(folder_name, filename)
    
    # Write the conversation to a txt file
    with open(file_path, 'w', encoding='utf-8') as f:
        for message in conversation:
            f.write(f"{message['author']}>{message['content']}\n")

def count_words(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    words = text.split()
    return len(words)

if __name__=="__main__":
    i = 0
    for file in os.listdir('discord'):
        with open(os.path.join('discord', file), 'r') as f:
            messages = json.load(f)

        conversation = format_messages_discord(messages)
        save_conversation(conversation, f"{i}.jsonl")
        save_conversation_txt(conversation, f"{i}.txt")
        
        txt_file_path = os.path.join('conversations_txt', f"{i}.txt")
        word_count = count_words(txt_file_path)
        print(f"File {i}.txt - Word count: {word_count}")
        
        i += 1

    for file in os.listdir('whatsapp'):
        with open(os.path.join('whatsapp', file), 'r', encoding='utf-8') as f:
            messages = f.read()
        conversation = format_messages_whatsapp(messages)
        save_conversation(conversation, f"{i}.jsonl")
        save_conversation_txt(conversation, f"{i}.txt")
        
        txt_file_path = os.path.join('conversations_txt', f"{i}.txt")
        word_count = count_words(txt_file_path)
        print(f"File {i}.txt - Word count: {word_count}")
        
        i += 1