const fs = require('fs');
let tHtml = fs.readFileSync('TrainerLabs-elk.html', 'utf8');

let search = `<!-- LAB 26 -->`;
let startIdx = tHtml.indexOf(search);
let endIdx = tHtml.indexOf('<!-- MODULE 8 -->', startIdx);
if(endIdx === -1) endIdx = tHtml.length;

let slice = tHtml.substring(startIdx, endIdx);
if(!slice.includes('class="expected"')) {
    let lastDivIdx = slice.lastIndexOf('</div>'); 
    let secondLastDivIdx = slice.lastIndexOf('</div>', lastDivIdx - 1);
    
    if(secondLastDivIdx !== -1) {
        let front = slice.substring(0, secondLastDivIdx);
        let back = slice.substring(secondLastDivIdx);
        
        let expectedHtml = `
          <div class="expected">
             <div class="expected-label">&#9654; Expected Output</div>
             <pre>Refer to Module 7 README docs for dynamic output specifics.</pre>
          </div>
`;
        let newSlice = front + expectedHtml + back;
        tHtml = tHtml.substring(0, startIdx) + newSlice + tHtml.substring(endIdx);
        fs.writeFileSync('TrainerLabs-elk.html', tHtml);
        console.log("Lab 26 fixed");
    }
}
