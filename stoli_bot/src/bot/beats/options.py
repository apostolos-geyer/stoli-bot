from interactions import slash_option, OptionType


def title():
    """Decorator for a beat name option, required on all beats commands"""

    def fun(command):
        return slash_option(
            name="title",
            description="The title of your beat",
            opt_type=OptionType.STRING,
            required=True,
            max_length=32,
        )(command)

    return fun


def producer():
    """Decorator for a producer name option, required on all beats commands"""

    def fun(command):
        return slash_option(
            name="producer",
            description="Your producer name",
            opt_type=OptionType.STRING,
            required=True,
            max_length=32,
        )(command)

    return fun


def beat_url():
    """Decorator for a beat url option, used when sending a beat hosted online"""

    def fun(command):
        return slash_option(
            name="url",
            description="The url of your beat",
            opt_type=OptionType.STRING,
            required=True,
            max_length=2000,
        )(command)

    return fun


def beat_file():
    """Decorator for a beat file option, used when sending a beat as an attachment"""

    def fun(command):
        return slash_option(
            name="file",
            description="The file containing your beat",
            opt_type=OptionType.ATTACHMENT,
            required=True,
        )(command)

    return fun


def key():
    """Decorator for a key option, optional on all beats commands"""

    def fun(command):
        return slash_option(
            name="key",
            description="The key of your beat",
            opt_type=OptionType.STRING,
            required=False,
            max_length=3,  # TODO: validate key or provide options, right now restricting to 3 chars should be enough.
        )(command)

    return fun


def detune():
    """Decorator for a detune option (in cents) optional on all beats commands"""

    def fun(command):
        return slash_option(
            name="detune",
            description="The detune of your beat, in cents, if any.",
            opt_type=OptionType.NUMBER,
            required=False,
            min_value=-100,
            max_value=100,
        )(command)

    return fun


def bpm():
    """Decorator for a bpm option, optional on all beats commands"""

    def fun(command):
        return slash_option(
            name="bpm",
            description="The bpm of your beat",
            opt_type=OptionType.NUMBER,
            required=False,
            min_value=1,
            max_value=999,
        )(command)

    return fun
