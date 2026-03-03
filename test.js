const fs = require('fs');

try {
  const contentIn = fs.readFileSync('TrainerLabs-elk.html', 'utf8');
  let m1 = [...contentIn.matchAll(/<div class="trainer-note">/g)];
  console.log("Trainer notes total: ", m1.length);
  
  let stripped = contentIn.replace(/<strong[^>]*>Trainer.*?Note:?<\/strong>\s*/gi, "<strong>Trainer Note:</strong> "); // reset first
  fs.writeFileSync('TrainerLabs-elk.html', stripped);

// let stripped2 = stripped.replace(/<strong[^>]*>Trainer.*?Note:?<\/strong>\s*(.*)/gi, function(match, innerText) {
//          return `<b>${innerText.trim()}</b>`;
// });
  
  // console.log("Removed trainer note strong tags");
} catch(e) { }
