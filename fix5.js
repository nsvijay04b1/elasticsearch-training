const fs = require('fs');
let tHtml = fs.readFileSync('TrainerLabs-elk.html', 'utf8');

const labsToFix = [22, 23, 24, 25, 26];

for (let i of labsToFix) {
    let search = `<!-- LAB ${i} -->`;
    let startIdx = tHtml.indexOf(search);
    if (startIdx === -1) continue;
    
    // Find next lab or end of mod7
    let nextLabIdx = tHtml.indexOf('<!-- LAB', startIdx + 10);
    if (nextLabIdx === -1) {
        nextLabIdx = tHtml.indexOf('<!-- MODULE 8 -->', startIdx);
    }
    if (nextLabIdx === -1) {
        nextLabIdx = tHtml.length;
    }

    let slice = tHtml.substring(startIdx, nextLabIdx);
    
    // Check if expected output exists already
    if (!slice.includes('class="expected"')) {
        console.log(`Fixing missing expected output for Lab ${i}`);
        
        let lastDivIdx = slice.lastIndexOf('</div>'); 
        let secondLastDivIdx = slice.lastIndexOf('</div>', lastDivIdx - 1);

        if(secondLastDivIdx !== -1) {
            let front = slice.substring(0, secondLastDivIdx);
            let back = slice.substring(secondLastDivIdx);
            
            let expectedHtml = `
          <div class="expected">
             <div class="expected-label">&#9654; Expected Output</div>
             <pre>Refer to Module 7 README or instructor guide for dynamic query output examples.</pre>
          </div>
`;
            
            let newSlice = front + expectedHtml + back;
            tHtml = tHtml.substring(0, startIdx) + newSlice + tHtml.substring(nextLabIdx);
        }
    }
}
fs.writeFileSync('TrainerLabs-elk.html', tHtml);
