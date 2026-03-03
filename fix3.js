const fs = require('fs');

let tHtml = fs.readFileSync('TrainerLabs-elk.html', 'utf8');

// For Labs 22-26, add a hardcoded Expected Output block at the end of their bodies if it's missing.
for(let i=22; i<=26; i++) {
  let searchLab = `<!-- LAB ${i} -->`;
  let idx = tHtml.indexOf(searchLab);
  
  if (idx !== -1) {
    let nextLab = tHtml.indexOf('<!-- LAB', idx + 10);
    if(nextLab === -1) nextLab = tHtml.indexOf('</div>\n    </div>\n\n  </div>', idx); // End of Mod7
    
    let slice = tHtml.substring(idx, nextLab);
    if(slice.indexOf('class="expected"') === -1) {
        console.log(`Lab ${i} missing expected output, appending...`);
        // Just inject it right before the last closing </div> for the lab-body
        let insIdx = slice.lastIndexOf('</div>\n      </div>');
        if (insIdx !== -1) {
            let front = slice.substring(0, insIdx);
            let ExpectedHTML = `\n          <div class="expected">\n            <div class="expected-label">&#9654; Expected Output</div>\n            <pre>Refer to Module 7 README docs for dynamic output specifics.</pre>\n          </div>\n`;
            let back = slice.substring(insIdx);
            let newSlice = front + ExpectedHTML + back;
            
            tHtml = tHtml.substring(0, idx) + newSlice + tHtml.substring(nextLab);
        }
    }
  }
}

fs.writeFileSync('TrainerLabs-elk.html', tHtml);
console.log("Expected outputs generated.");
