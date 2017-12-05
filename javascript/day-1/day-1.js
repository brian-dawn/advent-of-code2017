
var captcha = require('./captcha.json');

function addDuplicates(sequence) {
  duplicatesTotal = 0;
  for (var i = 0; i < sequence.length; i++) {
    if (sequence[i] == sequence[i+1]) {
      duplicatesTotal += parseInt(sequence[i]);
    }
  }
  if (sequence.last == sequence.first) {
    return duplicatesTotal += parseInt(sequence[0]);
  }
  return duplicatesTotal;
};

console.log("sum of sequence's duplicates:   " + addDuplicates(captcha.long));
