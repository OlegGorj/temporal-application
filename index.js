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

function main() {
    console.log("Application started");
}

main();

