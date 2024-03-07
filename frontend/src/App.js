import logo from './logo.svg';
import './App.css';
import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';
import React, {useState} from 'react';

import Button from '@mui/material/Button';
import Checkbox from '@mui/material/Checkbox';
import FormControl from '@mui/material/FormControl';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormGroup from '@mui/material/FormGroup';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import Select from '@mui/material/Select';
import TextField from '@mui/material/TextField';

import Box from '@mui/material/Box';
import { DataGrid } from '@mui/x-data-grid';


function App() {
  console.log("Start")
  var industry = "";

  const [results, setResults] = useState([]);

  const submitSearch = () => {

    var dummyData = {
          "CompanyName": "Trumpet Software Limited",
          "Industry": "SaaS, Sales Automation",
          "SalesTarget": "B2B",
          "Description": "Our company is a digital platform that provides personalized and interactive sales solutions. We offer tools for creating digital sales rooms, enabling businesses to centralize their buyer journeys, track engagement, and streamline marketing and sales processes. Our platform also offers features for auto-personalizing content and real-time notifications, aiming to reduce sales cycle times and increase revenue.",
      }

    fetch("http://localhost:3001", 
      {
          method: "POST", 
          body: JSON.stringify(dummyData),
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


  const columns = [
    {
      field: 'gh_direct_url',
      headerName: 'GDPR Hub Link',
      width: 150,
      editable: false,
    },
    {
      field: 'et_direct_url',
      headerName: 'GDPR Enforcement Tracker Link',
      width: 150,
      editable: false,
    },
    {
      field: 'fine_amount',
      headerName: 'Fine Amount',
      type: 'number',
      width: 110,
      editable: false,
    },
    {
      field: 'fine_currency',
      headerName: 'Fine Currency',
      width: 150,
      editable: false,
    }
  ];


  return (
    <div className="App">
      <header className="App-header">
        {/* <img src={logo} className="App-logo" alt="logo" /> */}
        <p>
          {/* Edit <code>src/App.js</code> and save to reload.. */}
        </p>

          <TextField id="company-name" label="Company Name" variant="outlined" />
          
          <FormControl fullWidth>
            <InputLabel id="industry-label">Industry</InputLabel>
            <Select
              labelId="industry-label"
              id="industry"
              value={industry}
              label="Industry"
              // onChange={handleChange}
            >
              <MenuItem value={0}>Fintech/Financial Services</MenuItem>
              <MenuItem value={1}>Medtech/Healthcare</MenuItem>
              <MenuItem value={2}>eCommerce/Retail</MenuItem>
              <MenuItem value={3}>Mobility/Logistics</MenuItem>
              <MenuItem value={4}>Sustainability</MenuItem>
              <MenuItem value={5}>LegalTech/Regtech</MenuItem>
              <MenuItem value={6}>PropTech/Real Estate</MenuItem>
              <MenuItem value={7}>Education/EdTech</MenuItem>
              <MenuItem value={8}>SaaS</MenuItem>
              <MenuItem value={9}>Agency/Consultancy</MenuItem>
              <MenuItem value={10}>Marketing/Advertising</MenuItem>

              {/* add "OTHER" with free text input */}

            </Select>
          </FormControl>

          <FormGroup>
            <FormControlLabel id="b2b" control={<Checkbox />} label="B2B" />
            <FormControlLabel id="b2c" control={<Checkbox />} label="B2C" />
          </FormGroup>

          <TextField id="description" label="Description" variant="outlined" />

          <Button id="submit" variant="contained" onClick={submitSearch}>Submit</Button>
          {/* <p>{JSON.stringify(results)}</p> */}

          <Box sx={{ height: 400, width: '100%' }}>
            <DataGrid
              getRowId={(row) =>  row.gh_id + '/' + row.et_id}
              rows={results}
              columns={columns}
              initialState={{
                pagination: {
                  paginationModel: {
                    pageSize: 5,
                  },
                },
              }}
              pageSizeOptions={[5]}
              checkboxSelection
              disableRowSelectionOnClick
            />
          </Box>

        
        {/* <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a> */}
      </header>
    </div>
  );
}

export default App;
