import asyncio
import dedent
from .llm import get_completion
from aiofiles import open as aio_open
from kolorist import blue
from .run import RunOptions
from .system_prompt import system_prompt

async def generate(options: RunOptions) -> str:
    async with aio_open(options.prompt_file, 'r') as f:
        prompt = await f.read()
    async with aio_open(options.output_file, 'r') as f:
        prior_code = await f.read()
    async with aio_open(options.test_file, 'r') as f:
        test_code = await f.read()

    async with aio_open('package.json', 'r') as f:
        package_json = await f.read()

    user_prompt = dedent(f"""
        Here is what I need:

        <prompt>
        {prompt or 'Pass the tests'}
        </prompt>

        The current code is:
        <code>
        {prior_code or 'None'}
        </code>

        The file path for the above is {options.output_file}.

        The test code that needs to pass is:
        <test>
        {test_code}
        </test>

        The file path for the test is {options.test_file}.

        The error you received on that code was:
        <error>
        {options.last_run_error or 'None'}
        </error>

        {dedent(f'''
        Don't use any node modules that aren't included here unless specifically told otherwise:
        <package-json>
        {package_json}
        </package-json>''') if package_json else ''}

        Please give me the code that satisfies the prompt and test.

        Be sure to use good coding conventions. For instance, if you are generating a typescript
        file, use types (e.g. for function parameters, etc).
    """)

    if process.env.MA_DEBUG:
        print(f"\n\n{blue('Prompt:')}", user_prompt, '\n\n')

    return await get_completion({
        "options": options,
        "messages": [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
    })
