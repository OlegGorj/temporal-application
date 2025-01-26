module.exports = {
  'env': {
    'node': true,
    'es2021': true
  },
  'extends': 'eslint:recommended',
  'parserOptions': {
    'ecmaVersion': 'latest',
    'sourceType': 'module'
  },
  'rules': {
    'indent': ['error', 2],
    'semi': ['error', 'always'],
    'quotes': ['error', 'single']
  }
};

// filepath: index.js
function main() {
  console.log('Application started');
}

main();

module.exports = { main };

