module.exports = {
    'env': {
      'node': true,
      'es2021': true,
      'jest': true
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
    },
    'globals': {
      'describe': 'readonly',
      'test': 'readonly',
      'expect': 'readonly',
      'beforeEach': 'readonly',
      'afterEach': 'readonly',
      'jest': 'readonly'
    }
  };
  