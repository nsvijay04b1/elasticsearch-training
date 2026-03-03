const fs = require('fs');
let html = fs.readFileSync('TrainerLabs-elk.html', 'utf8');
html = html.replace(/<div class="trainer-note">\s*<strong>Trainer Note:<\/strong>/gi, '<div class="trainer-note">');
fs.writeFileSync('TrainerLabs-elk.html', html);
