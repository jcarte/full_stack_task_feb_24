var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  var dummy = {
    "id": 11,
    "title": "perfume Oil",
    "description": "Mega Discount, Impression of A...",
    "price": 13,
    "discountPercentage": 8.4
  }
  res.send(dummy)
});

module.exports = router;
