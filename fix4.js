const fs = require('fs');
let tHtml = fs.readFileSync('TrainerLabs-elk.html', 'utf8');

const labsToFix = [22, 23, 24, 25, 26];

for (let i of labsToFix) {
    let search = `<!-- LAB ${i} -->`;
    let startIdx = tHtml.indexOf(search);
    if (startIdx === -1) continue;
    
    let endIdx = tHtml.indexOf('<!-- LAB', startIdx + 10);
    if (endIdx === -1) endIdx = tHtml.indexOf('</div>\n    </div>\n\n    <!-- MODULE 8 -->', startIdx);
    if (endIdx === -1) endIdx = tHtml.length; // Fallback

    let slice = tHtml.substring(startIdx, endIdx);
    
    // Check if expected output exists already
    if (!slice.includes('class="expected"')) {
        console.log(`Fixing missing expected output for Lab ${i}`);
        
        // Find the last </div> before the next lab starts, which closes lab-body
        let lastDivIdx = slice.lastIndexOf('</div>\n      </div>');
        if(lastDivIdx !== -1) {
            let front = slice.substring(0, lastDivIdx);
            let back = slice.substring(lastDivIdx);
            
            let expectedHtml = `
          <div class="expected">
            <div class="expected-label">&#9654; Expected Output</div>
            <pre>Refer to Module 7 README or instructor guide for dynamic query output examples.</pre>
          </div>
`;
            
            let newSlice = front + expectedHtml + back;
            tHtml = tHtml.substring(0, startIdx) + newSlice + tHtml.substring(endIdx);
        }
    }
}
fs.writeFileSync('TrainerLabs-elk.html', tHtml);
