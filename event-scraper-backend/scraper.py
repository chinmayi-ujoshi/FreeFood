import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed

# Function to get event links from the main page
def get_event_links(session, main_url):
    try:
        response = session.get(main_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e: 
        print(f"Error fetching {main_url}: {e}")
        return []
    
    soup = BeautifulSoup(response.content, 'html.parser')
    events = soup.select('div.text-wrapper h3 a')
    event_links = [urljoin(main_url, event['href']) for event in events if 'href' in event.attrs]
    return event_links

# Check event for food-related keywords
def check_event_for_food(session, event_url):
    try:
        response = session.get(event_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {event_url}: {e}")
        return None
    
    soup = BeautifulSoup(response.content, 'html.parser')

    # Try to find the event description
    description = soup.find('div', class_='event-description')
    if description:
        description_text = description.get_text().lower()  # Convert text to lowercase for easier keyword matching
        # List of keywords related to food
        food_keywords = ['food', 'breakfast', 'lunch', 'dinner', 'snacks', 'refreshments', 'meal']
        # Check if any food-related keyword is in the description
        if any(keyword in description_text for keyword in food_keywords):
            return event_url  # Return the event URL if food is mentioned
    return None

# Scrape events and find those that mention food
def scrape_events_with_food(main_url):
    food_events = []
    
    with requests.Session() as session:
        event_links = get_event_links(session, main_url)
        
        # Using ThreadPoolExecutor for concurrency
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(check_event_for_food, session, event_link): event_link for event_link in event_links}
            
            for future in as_completed(futures):
                event_url = futures[future]
                try:
                    food_event_url = future.result()
                    if food_event_url:
                        food_events.append(food_event_url)  # Store the event link if food is mentioned
                except Exception as e:
                    print(f"Error processing event {event_url}: {e}")
    
    return food_events

# Example usage
if __name__ == "__main__":
    main_url = "https://calendar.syracuse.edu/events/"  # Replace with your main event page URL
    food_events = scrape_events_with_food(main_url)
    
    if food_events:
        print("Events that mention food:")
        for event_url in food_events:
            print(f"URL: {event_url}")
    else:
        print("No food-related events found.")
