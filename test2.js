const fs = require('fs');
let html = fs.readFileSync('TrainerLabs-elk.html', 'utf8');
let m1 = [...html.matchAll(/<div class="trainer-note">/g)];
console.log("Trainer notes total now: ", m1.length);
