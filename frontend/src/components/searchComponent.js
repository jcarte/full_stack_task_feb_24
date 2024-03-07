import React, {useState} from 'react';

import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Stack from '@mui/material/Stack';

// import Checkbox from '@mui/material/Checkbox';
// import FormControl from '@mui/material/FormControl';
// import FormControlLabel from '@mui/material/FormControlLabel';
// import FormGroup from '@mui/material/FormGroup';
// import InputLabel from '@mui/material/InputLabel';
// import MenuItem from '@mui/material/MenuItem';
// import Select from '@mui/material/Select';

function SearchComponent(props) {
    console.log("SC: Start")
    
    //var industry = "";
    const [company, setCompany] = useState('');
    const [description, setDescription] = useState('');

    const submitClicked = () => {

        console.log(company)
        console.log(description)

        // var dummyData = {
        //       "CompanyName": "Trumpet Software Limited",
        //       "Industry": "SaaS, Sales Automation",
        //       "SalesTarget": "B2B",
        //       "Description": "Our company is a digital platform that provides personalized and interactive sales solutions. We offer tools for creating digital sales rooms, enabling businesses to centralize their buyer journeys, track engagement, and streamline marketing and sales processes. Our platform also offers features for auto-personalizing content and real-time notifications, aiming to reduce sales cycle times and increase revenue.",
        //   }
    
        var data = {
          "company": company,
          "description": description
        }

        props.onSubmit(data)
    }

    return (
            <Stack 
                spacing={3} 
                direction="row"
                justifyContent="center"
                alignItems="center" 
                >
                <TextField 
                    id="company-name" 
                    label="Company Name" 
                    // variant="outlined" 
                    value={company}
                    onInput={ e=>setCompany(e.target.value)}
                    />

                <TextField 
                    id="description" 
                    label="Description" 
                    // variant="outlined" 
                    value={description}
                    onInput={ e=>setDescription(e.target.value)}
                    />

                <Button id="submit" 
                    variant="contained" 
                    onClick={submitClicked}
                    >
                        Submit
                    </Button>
            

            {/* <FormControl fullWidth>
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

                {/* add "OTHER" with free text input *//*}

                </Select>
            </FormControl> */}

            {/* <FormGroup>
                <FormControlLabel id="b2b" control={<Checkbox />} label="B2B" />
                <FormControlLabel id="b2c" control={<Checkbox />} label="B2C" />
                 </FormGroup> */}
</Stack>
            
    )
}
export default SearchComponent;