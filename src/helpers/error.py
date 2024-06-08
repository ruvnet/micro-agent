class KnownError(Exception):
    pass

def handle_cli_error(error: Exception) -> None:
    if not isinstance(error, KnownError):
        if hasattr(error, 'stack'):
            print(dim(str(error.stack).split('\n')[1:]).join('\n'))
        print(f"\n    {dim(f'ai-shell v{version}')}")
        print("\n    Please open a Bug report with the information above:")
        print("    https://github.com/BuilderIO/micro-agent/issues/new")
