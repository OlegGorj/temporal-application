const { main } = require('../index.js');

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