import asyncio
import os
from clack import intro, log, spinner, text
from glob import glob
from .run import run_all
from .llm import get_simple_completion
from .config import get_config, set_configs
from .file_exists import file_exists
from .remove_backticks import remove_backticks
from .test import format_message
from kolorist import gray, green
from .exit_on_cancel import exit_on_cancel
from .iterate_on_test import iterate_on_test
from .constants import DEFAULT_TEST_COMMAND

async def interactive_mode(options: dict):
    print('')
    intro('🦾 Micro Agent')

    config = await get_config()

    if not config.get('OPENAI_KEY'):
        openai_key = exit_on_cancel(await text('Welcome newcomer! What is your OpenAI key? (this is kept private)'))
        await set_configs([('OPENAI_KEY', openai_key)])

    prompt = exit_on_cancel(await text('What would you like to do?', placeholder='A function that ...'))

    file_path = options.get('outputFile')
    if not file_path:
        files = await glob('*/*/*', ignore=['node_modules/**'])
        file_string = '\n'.join(files[:100])
        loading = spinner()
        loading.start()

        recommended_file_path = remove_backticks(await get_simple_completion(prompt, file_string))
        loading.stop()

        file_path = exit_on_cancel(await text('What file would you like to create or edit?', default=recommended_file_path, placeholder=recommended_file_path))

    log.info('Generating test...')

    print(format_message('\n'))

    example_tests = await glob('**/*.{test,spec}.*', ignore=['node_modules/**'])
    two_tests = example_tests[:2]
    two_test_files = [await file_exists(test) for test in two_tests]

    package_json_contents = await file_exists('package.json', default='')

    test_file_path = file_path.replace(/.(\w+)$/, '.test.\\1')

    test_contents = remove_backticks(await get_simple_completion(prompt, two_test_files, package_json_contents, test_file_path))

    result = exit_on_cancel(await text('How does the generated test look? Reply "good", or provide feedback', default='good', placeholder='good'))

    if result.lower().strip() != 'good':
        options['testFile'] = test_file_path
        options['outputFile'] = file_path
        options['prompt'] = prompt
        test_contents = await iterate_on_test(test_contents, result, options)

    await file_exists(test_file_path, content=test_contents, write=True)
    log.success(f'{green("Test file generated!")} {gray(test_file_path)}')
    test_command = exit_on_cancel(await text('What command should I run to test the code?', default=DEFAULT_TEST_COMMAND.format(test_file_path.split('/')[-1].split('.')[0]), placeholder=DEFAULT_TEST_COMMAND))

    log.info('Agent running...')

    await run_all({**options, 'testCommand': test_command, 'outputFile': file_path, 'testFile': test_file_path, 'promptFile': file_path.replace(/.(\w+)$/, '.prompt.md'), 'prompt': prompt, 'lastRunError': ''})
