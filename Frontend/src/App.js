import logo from './logo.svg';
import './App.css';
import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';
import * as React from 'react';

import Button from '@mui/material/Button';
import Checkbox from '@mui/material/Checkbox';
import FormControl from '@mui/material/FormControl';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormGroup from '@mui/material/FormGroup';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import Select from '@mui/material/Select';
import TextField from '@mui/material/TextField';

function App() {

var industry = "";

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

          <Button id="submit" variant="contained">Submit</Button>
        
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
