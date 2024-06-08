import asyncio
from clack import intro, note, outro, log
from .generate import generate
from .test import is_fail, test
from aiofile import async_open
from kolorist import green, yellow
from .constants import command_name
from .visual_generate import visual_generate
from .file_exists import file_exists

async def run_one(options):
    if options.visual:
        log.step('Running...')
        result = await visual_generate(options)
        if is_fail(result.testResult):
            async with async_open(options.outputFile, 'w') as afp:
                await afp.write(result.code)
            return {
                'code': result.code,
                'testResult': result.testResult,
            }
        else:
            return result

    log.step('Generating code...')
    result = await generate(options)

    async with async_open(options.outputFile, 'w') as afp:
        await afp.write(result)
    log.step('Updated code')

    log.step('Running tests...')
    testResult = await test(options)

    return {
        'code': result,
        'testResult': testResult,
    }

async def run_all(options):
    if not options.get('skipIntro', False):
        intro('🦾 Micro Agent')

    results = []
    testResult = None
    if not options.visual:
        log.step('Running tests...')
        testResult = await test(options)

        if testResult.type == 'success':
            outro(green('All tests passed!'))
            return

    async for result in run(options):
        results.append(result)

    return results

async def run(options):
    passed = False
    maxRuns = options.get('maxRuns', 20)
    for i in range(maxRuns):
        result = await run_one(options)
        yield result

        if result['testResult']['type'] == 'success':
            outro(green('All tests passed!'))
            passed = True
            break
        options['lastRunError'] = result['testResult']['message']

    if not passed:
        log.message(yellow(f'Max runs of {maxRuns} reached.'))
        if options['prompt'] and not await file_exists(options['promptFile']):
            async with async_open(options['promptFile'], 'w') as afp:
                await afp.write(options['prompt'])
        note(
            f'{create_command_string(options)}',
            'You can resume with this command with:'
        )
        outro(yellow('Stopping.'))
        print('\n')
