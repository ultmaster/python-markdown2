var katex = require('./katex');

function abc (string) {
  console.log(katex.renderToString(string));
}

abc('E=mc^2');
for (var i = 0; i < process.argv.length; ++i)
  console.log(process.argv[i]);