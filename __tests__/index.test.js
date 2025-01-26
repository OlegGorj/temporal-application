const { main } = require('../src/index.js');

describe('main function', () => {
  let consoleLogSpy;

  beforeEach(() => {
    consoleLogSpy = jest.spyOn(console, 'log');
  });

  afterEach(() => {
    consoleLogSpy.mockRestore();
  });

  test('should log application started message', () => {
    main();
    expect(consoleLogSpy).toHaveBeenCalledWith('Application started');
  });

  test('main function should be defined', () => {
    expect(main).toBeDefined();
  });
});

module.exports = {
  env: {
    node: true,
    es2021: true,
    jest: true
  },
  extends: 'eslint:recommended',
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module'
  },
  rules: {
    indent: ['error', 2],
    semi: ['error', 'always'],
    quotes: ['error', 'single']
  }
};
