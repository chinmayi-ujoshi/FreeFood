import tiktoken

def count_tokens_for_event_summary(description_text):
    system_message = {"role": "system", "content": "You are an event summarizer."}
    user_message = {"role": "user", "content": f"Summarize the following event description and mention if free food is available: {description_text}"}
    
    # Combine all messages into a single list
    messages = [system_message, user_message]
    
    # Use tiktoken to get the encoding for the GPT-3.5-turbo model
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    
    total_tokens = 0
    
    # For each message, calculate the number of tokens
    for message in messages:
        # Tokens for the role (system/user/assistant) + content
        total_tokens += len(encoding.encode(message['role'])) + len(encoding.encode(message['content']))
    
    return total_tokens

# Example usage
description_text = "This event will have free food, including snacks and refreshments for all attendees.This event will have free food, including snacks and refreshments for all attendees.This event will have free food, including snacks and refreshments for all attendees.This event will have free food, including snacks and refreshments for all attendees.This event will have free food, including snacks and refreshments for all attendees.This event will have free food, including snacks and refreshments for all attendees.This event will have free food, including snacks and refreshments for all attendees.This event will have free food, including snacks and refreshments for all attendees.This event will have free food, including snacks and refreshments for all attendees."
token_count = count_tokens_for_event_summary(description_text)
print(f"Total tokens used: {token_count}")
