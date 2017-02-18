var katex = require('./katex');

function renderToString() {
  console.log(katex.renderToString(process.argv[2]));
}
