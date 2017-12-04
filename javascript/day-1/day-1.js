
var captcha = require('./captcha.json');

function addDuplicates(sequence) {
  duplicatesTotal = 0;
  for (var i = 0; i < sequence.length; i++) {
    console.log(sequence.length);
    if (sequence[i] == sequence[i+1]) {
      console.log("found a duplicate:    " + sequence[i]);
      duplicatesTotal += i+i;
    }
    return duplicatesTotal;
  }
};

console.log("sum of sequence's duplicates:   " + addDuplicates(captcha.short));
