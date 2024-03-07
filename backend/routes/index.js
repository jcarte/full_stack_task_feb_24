var express = require('express');
var router = express.Router();
var fs = require("fs"),
    json;

// /* GET home page. */
// router.get('/', function(req, res, next) {
//   var dummy = {
//     "method": "GET",
//     "id": 11,
//     "title": "perfume Oil",
//     "description": "Mega Discount, Impression of A...",
//     "price": 13,
//     "discountPercentage": 8.4
//   }
//   res.send(dummy)
// });


//RECORD
/*
{
        "gh_direct_url": "https:\/\/gdprhub.eu\/index.php?title=VDAI_-_N\/A",
        "et_direct_url": "https:\/\/www.enforcementtracker.com\/ETid-1",
        "sources": [
            "test.com",
            "https:\/\/vdai.lrv.lt\/lt\/news\/view_item\/id.143"
        ],
        "companies": [
            "Vilnius City Municipality Administration"
        ],
        "summary": "Lithuanian DPA imposes a fine of EUR 15.000,00 for a failure to implement sufficient technical and organizational measures with regards to education procedures of an adopted child.Video surveillance was not sufficiently marked and a large part of the sidewalk of the facility was recorded. Surveillance of the public space in this way, i.e. on a large scale by private individuals, is not permitted.",
        "fine_amount": 4812.0,
        "fine_currency": "EUR",
        "sector": "Industry and Commerce",
        "gh_id": 2744.0,
        "et_id": "ETid-1"
    },
*/



//INPUT
    // var dummyData = {
    //       "CompanyName": "Trumpet Software Limited",
    //       "Industry": "SaaS, Sales Automation",
    //       "SalesTarget": "B2B",
    //       "Description": "Our company is a digital platform that provides personalized and interactive sales solutions. We offer tools for creating digital sales rooms, enabling businesses to centralize their buyer journeys, track engagement, and streamline marketing and sales processes. Our platform also offers features for auto-personalizing content and real-time notifications, aiming to reduce sales cycle times and increase revenue.",
    //   }


function getAllRecord(filename) {
  var filepath = __dirname + '/../' + filename;
  var file = fs.readFileSync(filepath,'utf8');
  return JSON.parse(file);
}

router.post('/', function(req, res) {
  console.log(req.body)

  var results = []
  var allRecords = getAllRecord('dummy-results.json');


  var companySearchTerms = req.body.CompanyName.length > 0 ? req.body.CompanyName.split(" ") : []
  var descriptionSearchTerms = req.body.Description.length > 0 ? req.body.Description.split(" ") : []

  for (const record of allRecords) {

    var compsConcat = record.companies.join(" ")
    var isCompanyMatch = companySearchTerms.some(comp => compsConcat.includes(comp));
    var isDescriptionMatch = descriptionSearchTerms.some(desc => record.summary.includes(desc));

    console.log(record.gh_id + '/' + record.et_id, ", company match: ", isCompanyMatch, ", desc match: ", isDescriptionMatch)

    if(isCompanyMatch || isDescriptionMatch)
      results.push(record)
  }

  res.json(results)
});

module.exports = router;
