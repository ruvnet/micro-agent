import os from 'os';
import path from 'path';
import { expect, describe, it, vi, afterEach } from 'vitest';
import { getConfig, setConfigs, showConfigUI } from './config';

const mocks = vi.hoisted(() => {
  return {
    lstat: vi.fn(),
    readFile: vi.fn(),
    writeFile: vi.fn(),
    select: vi.fn(),
    text: vi.fn(),
    isCancel: vi.fn(),
    exit: vi.fn(),
  };
});

vi.mock('fs/promises', () => {
  return {
    default: {
      lstat: mocks.lstat,
      readFile: mocks.readFile,
      writeFile: mocks.writeFile,
    },
  };
});

vi.mock('@clack/prompts', () => {
  return {
    select: mocks.select,
    text: mocks.text,
    isCancel: mocks.isCancel,
  };
});

const realProcess = process;
global.process = { ...realProcess, exit: mocks.exit };

const configFilePath = path.join(os.homedir(), '.micro-agent');

describe('getConfig', () => {
  const defaultConfig = {
    ANTHROPIC_KEY: undefined,
    ANTHROPIC_MODEL: 'claude-3-opus-20240229',
    LANGUAGE: 'en',
    MODEL: 'gpt-4o',
    OPENAI_API_ENDPOINT: 'https://api.openai.com/v1',
    OPENAI_KEY: undefined,
  };

  it('should return an object with defaults and the env if no config is provided', async () => {
    mocks.lstat.mockRejectedValueOnce(
      new Error('ENOENT: no such file or directory')
    );
    const result = await getConfig();
    expect(result).toEqual({
      ...defaultConfig,
      ...process.env,
    });
  });

  it('should return the parsed config object if a valid config is provided', async () => {
    mocks.lstat.mockRejectedValueOnce(
      new Error('ENOENT: no such file or directory')
    );
    const cliConfig = {
      OPENAI_KEY: 'my-openai-key',
      MODEL: 'gpt-3.5-turbo',
      LANGUAGE: 'en',
    };
    const result = await getConfig(cliConfig);
    expect(result).toEqual({
      ...defaultConfig,
      ...cliConfig,
      ...process.env,
    });
  });

  it('should ignore invalid config keys', async () => {
    mocks.lstat.mockRejectedValueOnce(
      new Error('ENOENT: no such file or directory')
    );
    const cliConfig = {
      OPENAI_KEY: 'my-openai-key',
      INVALID_KEY: 'invalid-value',
    };
    const result = await getConfig(cliConfig);
    expect(result).toEqual({
      ...defaultConfig,
      OPENAI_KEY: 'my-openai-key',
      ...process.env,
    });
  });

  it('should check if the config file exists', async () => {
    mocks.lstat.mockResolvedValueOnce(true);
    mocks.readFile.mockResolvedValueOnce('');

    await getConfig();

    expect(mocks.lstat).toHaveBeenCalledWith(configFilePath);
  });

  it('should read the config file if it exists', async () => {
    mocks.lstat.mockResolvedValueOnce(true);
    mocks.readFile.mockResolvedValueOnce('');

    await getConfig();

    expect(mocks.readFile).toHaveBeenCalledWith(configFilePath, 'utf8');
  });

  it('should return the parsed config object from the config file', async () => {
    const expected = {
      OPENAI_KEY: 'my-openai-key',
      MODEL: 'gpt-3.5-turbo',
      LANGUAGE: 'en',
    };
    mocks.lstat.mockResolvedValueOnce(true);
    mocks.readFile.mockResolvedValueOnce(
      'OPENAI_KEY=my-openai-key\nMODEL=gpt-3.5-turbo\nLANGUAGE=en\n'
    );

    const result = await getConfig();

    expect(result).toEqual({
      ...defaultConfig,
      ...expected,
      ...process.env,
    });
  });

  it('should ignore invalid config keys in the config file', async () => {
    mocks.lstat.mockResolvedValueOnce(true);
    mocks.readFile.mockResolvedValueOnce(
      'OPENAI_KEY=my-openai-key\nINVALID_KEY=invalid-value\n'
    );
    const result = await getConfig();
    expect(result).toEqual({
      ...defaultConfig,
      OPENAI_KEY: 'my-openai-key',
      ...process.env,
    });
  });
});

describe('setConfigs', () => {
  it('should write the provided key-value pairs to the config file', async () => {
    mocks.lstat.mockResolvedValueOnce(true);
    mocks.readFile.mockResolvedValueOnce('');
    const keyValues: [string, string][] = [
      ['OPENAI_KEY', 'my-openai-key'],
      ['MODEL', 'gpt-3.5-turbo'],
      ['LANGUAGE', 'en'],
    ];

    await setConfigs(keyValues);

    expect(mocks.writeFile).toHaveBeenCalledWith(
      configFilePath,
      'OPENAI_KEY=my-openai-key\nMODEL=gpt-3.5-turbo\nLANGUAGE=en\n',
      'utf8'
    );
  });

  it('should throw an error for invalid config keys', async () => {
    mocks.lstat.mockResolvedValueOnce(true);
    mocks.readFile.mockResolvedValueOnce('');
    const keyValues: [string, string][] = [
      ['OPENAI_KEY', 'my-openai-key'],
      ['INVALID_KEY', 'invalid-value'],
    ];

    await expect(setConfigs(keyValues)).rejects.toThrow(
      'Invalid config property: INVALID_KEY'
    );
  });
});

describe('showConfigUI', () => {
  it('should show the basic config options', async () => {
    mocks.lstat.mockRejectedValue(
      new Error('ENOENT: no such file or directory')
    );
    mocks.select.mockResolvedValueOnce('cancel');

    await showConfigUI();

    expect(mocks.select).toHaveBeenCalledWith({
      message: 'Set config' + ':',
      options: [
        {
          label: 'OpenAI Key',
          value: 'OPENAI_KEY',
          hint: 'sk-...',
        },
        {
          label: 'OpenAI API Endpoint',
          value: 'OPENAI_API_ENDPOINT',
          hint: 'https://api.openai.com/v1',
        },
        {
          label: 'Model',
          value: 'MODEL',
          hint: 'gpt-4o',
        },
        {
          label: 'Done',
          value: 'cancel',
          hint: 'Exit',
        },
      ],
    });
  });

  it('should return nothing if the user cancels', async () => {
    mocks.lstat.mockRejectedValue(
      new Error('ENOENT: no such file or directory')
    );
    mocks.select.mockResolvedValueOnce('cancel');

    expect(await showConfigUI()).toBeUndefined();
  });

  it('should ask the user to set the OpenAI key', async () => {
    mocks.lstat.mockRejectedValue(
      new Error('ENOENT: no such file or directory')
    );
    mocks.select
      .mockResolvedValueOnce('OPENAI_KEY')
      .mockResolvedValueOnce('cancel');
    mocks.text.mockResolvedValueOnce('my-openai-key');

    await showConfigUI();

    expect(mocks.text).toHaveBeenCalledTimes(1);
    expect(mocks.text).toHaveBeenCalledWith({
      message: 'Enter your OpenAI API key',
      validate: expect.any(Function),
    });
  });

  it('should set the OpenAI key if the user provides one', async () => {
    mocks.lstat.mockRejectedValue(
      new Error('ENOENT: no such file or directory')
    );
    mocks.select
      .mockResolvedValueOnce('OPENAI_KEY')
      .mockResolvedValueOnce('cancel');
    mocks.text.mockResolvedValueOnce('my-openai-key');

    await showConfigUI();

    expect(mocks.writeFile).toHaveBeenCalledTimes(1);
    expect(mocks.writeFile).toHaveBeenCalledWith(
      configFilePath,
      'OPENAI_KEY=my-openai-key\n',
      'utf8'
    );
  });

  it('should ask the user to set the OpenAI API endpoint', async () => {
    mocks.lstat.mockRejectedValue(
      new Error('ENOENT: no such file or directory')
    );
    mocks.select
      .mockResolvedValueOnce('OPENAI_API_ENDPOINT')
      .mockResolvedValueOnce('cancel');
    mocks.text.mockResolvedValueOnce('https://api.openai.com/v1');

    await showConfigUI();

    expect(mocks.text).toHaveBeenCalledTimes(1);
    expect(mocks.text).toHaveBeenCalledWith({
      message: 'Enter your OpenAI API Endpoint',
    });
  });

  it('should set the OpenAI API endpoint if the user provides one', async () => {
    mocks.lstat.mockRejectedValue(
      new Error('ENOENT: no such file or directory')
    );
    mocks.select
      .mockResolvedValueOnce('OPENAI_API_ENDPOINT')
      .mockResolvedValueOnce('cancel');
    mocks.text.mockResolvedValueOnce('https://api.openai.com/v1');

    await showConfigUI();

    expect(mocks.writeFile).toHaveBeenCalledTimes(1);
    expect(mocks.writeFile).toHaveBeenCalledWith(
      configFilePath,
      'OPENAI_API_ENDPOINT=https://api.openai.com/v1\n',
      'utf8'
    );
  });

  it('should ask the user to set the model', async () => {
    mocks.lstat.mockRejectedValue(
      new Error('ENOENT: no such file or directory')
    );
    mocks.select.mockResolvedValueOnce('MODEL').mockResolvedValueOnce('cancel');
    mocks.text.mockResolvedValueOnce('gpt-4o');

    await showConfigUI();

    expect(mocks.text).toHaveBeenCalledTimes(1);
    expect(mocks.text).toHaveBeenCalledWith({
      message: 'Enter the model you want to use',
    });
  });

  it('should set the model if the user provides one', async () => {
    mocks.lstat.mockRejectedValue(
      new Error('ENOENT: no such file or directory')
    );
    mocks.select.mockResolvedValueOnce('MODEL').mockResolvedValueOnce('cancel');
    mocks.text.mockResolvedValueOnce('gpt-4o');

    await showConfigUI();

    expect(mocks.writeFile).toHaveBeenCalledTimes(1);
    expect(mocks.writeFile).toHaveBeenCalledWith(
      configFilePath,
      'MODEL=gpt-4o\n',
      'utf8'
    );
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });
});
