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


router.post('/', function(req, res) {
  //console.log(req)
  // var dummy = {"test": "POST Test"} 

  var filepath = __dirname + '/../' + 'dummy-results.json';
  var file = fs.readFileSync(filepath,'utf8');
  var dummy = JSON.parse(file);
  res.json(dummy)
});

module.exports = router;
