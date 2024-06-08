import asyncio
from clack import text
from .exit_on_cancel import exit_on_cancel
from .run import RunOptions
from .remove_backticks import remove_backticks
from .llm import get_simple_completion
from .test import format_message
import dedent

async def iterate_on_test(test_code: str, feedback: str, options: Partial[RunOptions]):
    print(format_message('\n'))
    test_contents = remove_backticks(
        await get_simple_completion(
            on_chunk=lambda chunk: print(format_message(chunk)),
            messages=[
                {
                    "role": "system",
                    "content": "You return code for a unit test only. No other words, just the code",
                },
                {
                    "role": "user",
                    "content": dedent.dedent(f"""
                        Here is a unit test file generated from the following prompt
                        <prompt>
                        {options.prompt}
                        </prompt>

                        The test will be located at `{options.testFile}` and the code to test will be located at 
                        `{options.outputFile}`.

                        The current test code is:
                        <code>
                        {test_code}
                        </code>

                        The user has given you this feedback on the test. Please update (or completely rewrite,
                        if needed) the test based on the feedback.

                        <feedback>
                        {feedback}
                        </feedback>

                        Please give me new code addressing the feedback.
                    """)
                },
            ],
        )
    )
    print(format_message('\n'))

    result = exit_on_cancel(
        await text(
            message='How does the generated test look? Reply "good", or provide feedback',
            default_value='good',
            placeholder='good',
        )
    )

    if result.lower().strip() != 'good':
        test_contents = await iterate_on_test(test_contents, result, options)

    return test_contents
