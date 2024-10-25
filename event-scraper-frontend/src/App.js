import React, { useState } from 'react';
import './App.css';  // Make sure to link the updated CSS file

function App() {
  const [foodEvents, setFoodEvents] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const fetchFoodEvents = async () => {
    setLoading(true);
    setError('');

    try {
      const response = await fetch('http://localhost:5000/scrape', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error('Failed to fetch events. Status code: ' + response.status);
      }

      const data = await response.json();
      
      // Check if there are any events in the response
      if (data.food_events && data.food_events.length > 0) {
        setFoodEvents(data.food_events);
      } else {
        setError('No food-related events found. 😞');
      }

    } catch (err) {
      setError('Error fetching data: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <h1> Free Food Finder </h1>
      <p className="subtitle">Looking for free food on campus? Let us help! Just click the button below and we’ll find events for you.</p>
      <button onClick={fetchFoodEvents} disabled={loading} className="scrape-btn">
        {loading ? 'Scraping for food...' : 'Find Free Food!'}
      </button>

      {error && <p className="error">{error}</p>}

      <h2 className="events-header">Events with Free Food:</h2>
      {foodEvents.length > 0 ? (
        <ul className="event-list">
          {foodEvents.map((eventUrl, index) => (
            <li key={index} className="event-card">
              <a href={eventUrl} target="_blank" rel="noopener noreferrer" className="event-link">
                🎉 Free Food Event #{index + 1}: {eventUrl}
              </a>
            </li>
          ))}
        </ul>
      ) : !loading && !error ? (
        <p className="empty-state">Nothing yet... Click "Find Free Food!" to see the events!</p>
      ) : null}
    </div>
  );
}

export default App;
