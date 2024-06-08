import asyncio
import argparse
from commands import config, update
from helpers import constants, error, run, interactive_mode, file_exists
from clack import outro
from kolorist import red

async def main():
    parser = argparse.ArgumentParser(prog=constants.commandName, description=f'{constants.projectName} CLI')
    parser.add_argument('file_path', nargs='?', help='File path to operate on')
    parser.add_argument('-p', '--prompt', type=str, help='Prompt to run')
    parser.add_argument('-t', '--test', type=str, help='The test script to run')
    parser.add_argument('-f', '--testFile', type=str, help='The test file to run')
    parser.add_argument('-m', '--maxRuns', type=int, help='The maximum number of runs to attempt')
    parser.add_argument('--thread', type=str, help='Thread ID to resume')
    parser.add_argument('-v', '--visual', type=str, help='Visually diff a local screenshot with the result of this URL')
    args = parser.parse_args()

    file_path = args.file_path
    file_extension = file_path.split('.')[-1] if file_path else None
    test_file_extension = file_extension.replace('x', '') if file_extension in ['jsx', 'tsx'] else file_extension

    test_file_path = args.testFile or (file_path.replace(f'.{file_extension}', f'.test.{test_file_extension}') if file_path else None)
    prompt_file_path = args.prompt or (file_path.replace(f'.{file_extension}', '.prompt.md') if file_path else None)

    if not test_file_path or not await file_exists.fileExists(test_file_path):
        test_file_path = ''

    run_options = {
        'outputFile': file_path,
        'promptFile': prompt_file_path,
        'testCommand': args.test,
        'testFile': test_file_path,
        'lastRunError': '',
        'maxRuns': args.maxRuns,
        'threadId': args.thread,
        'visual': args.visual,
    }

    try:
        if not args.file_path or not args.test:
            await interactive_mode.interactiveMode(run_options)
            return

        await run.runAll(run_options)
    except Exception as e:
        print(f"\n{red('✖')} {str(e)}")
        error.handleCliError(e)
        exit(1)

if __name__ == '__main__':
    asyncio.run(main())

async def signal_handler(signal, frame):
    print('\n')
    outro(red('Stopping.'))
    print('\n')
    exit()

asyncio.get_event_loop().add_signal_handler(asyncio.get_event_loop().SIGINT, signal_handler)
