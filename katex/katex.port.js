var katex = require('./katex');

console.log(process.argv[2]);
console.log(katex.renderToString(process.argv[2]));
