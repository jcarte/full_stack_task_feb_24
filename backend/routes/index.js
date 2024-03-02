var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  var dummy = {
    "method": "GET",
    "id": 11,
    "title": "perfume Oil",
    "description": "Mega Discount, Impression of A...",
    "price": 13,
    "discountPercentage": 8.4
  }
  res.send(dummy)
});


router.post('/', function(req, res) {
  //console.log(req)
  var dummy = {"test": "POST Test"} 
  res.json(dummy)
});

module.exports = router;
