import './App.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import React, {useState} from 'react';




import SearchComponent from './components/searchComponent'
import ResultsComponent from './components/resultsComponent'


export default function App() {
  console.log("Start")

  
  const [results, setResults] = useState([]);
  const [hasStarted, setHasStarted] = useState(false);

  const submitSearch = (search) => {

    setHasStarted(true)//show the results screen only after button pressed once

    // var dummyData = {
    //       "CompanyName": "Trumpet Software Limited",
    //       "Industry": "SaaS, Sales Automation",
    //       "SalesTarget": "B2B",
    //       "Description": "Our company is a digital platform that provides personalized and interactive sales solutions. We offer tools for creating digital sales rooms, enabling businesses to centralize their buyer journeys, track engagement, and streamline marketing and sales processes. Our platform also offers features for auto-personalizing content and real-time notifications, aiming to reduce sales cycle times and increase revenue.",
    //   }

    var requestData = {
      "CompanyName": search.company,
      "Description": search.description
    }


    fetch("http://localhost:3001", 
      {
          method: "POST", 
          body: JSON.stringify(requestData),
          mode: 'cors',
          headers: {
              'Content-Type': 'application/json',
          }
      })
      .then((res) => {
        console.log("got results")
        return res.json()
      })
      .then((json) => {
        console.log(`json: ${json}`)
        setResults(json)
      })
      .catch(rejected => {
        console.log(rejected);
    });

  }



  return (
    <div className="App">
      <div className="search-container">
        <SearchComponent onSubmit={submitSearch}/>
      </div>
      <div className="results-container">
        { hasStarted && <ResultsComponent data={results}/>}
      </div>
    </div>
  );
}

