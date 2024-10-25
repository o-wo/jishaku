# -*- coding: utf-8 -*-

"""
jishaku.repl.repl_builtins
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Builtin functions and variables within Jishaku REPL contexts.

:copyright: (c) 2021 Devon (scarletcafe) R
:license: MIT, see LICENSE for more details.

"""

import inspect
import typing

import aiohttp
import discord
from redbot.core.bot import Red
from redbot.core.utils import chat_formatting

from jishaku.types import ContextA


async def http_get_bytes(*args: typing.Any, **kwargs: typing.Any) -> bytes:
    """
    Performs a HTTP GET request against a URL, returning the response payload as bytes.

    The arguments to pass are the same as :func:`aiohttp.ClientSession.get`.
    """

    async with aiohttp.ClientSession() as session:
        async with session.get(*args, **kwargs) as response:
            response.raise_for_status()

            return await response.read()


async def http_get_json(url: str, *args: typing.Any, **kwargs: typing.Any) -> typing.Dict[typing.Any, typing.Any]:
    """
    Performs a HTTP GET request against a URL,
    returning the response payload as a dictionary of the response payload interpreted as JSON.

    The arguments to pass are the same as :func:`aiohttp.ClientSession.get`.
    """

    async with aiohttp.ClientSession() as session:
        async with session.get(url, *args, **kwargs) as response:
            response.raise_for_status()

            return await response.json(loads=discord.utils._from_json)


async def http_post_bytes(*args: typing.Any, **kwargs: typing.Any) -> bytes:
    """
    Performs a HTTP POST request against a URL, returning the response payload as bytes.

    The arguments to pass are the same as :func:`aiohttp.ClientSession.post`.
    """

    async with aiohttp.ClientSession() as session:
        async with session.post(*args, **kwargs) as response:
            response.raise_for_status()

            return await response.read()


async def http_post_json(*args: typing.Any, **kwargs: typing.Any) -> typing.Dict[typing.Any, typing.Any]:
    """
    Performs a HTTP POST request against a URL,
    returning the response payload as a dictionary of the response payload interpreted as JSON.

    The arguments to pass are the same as :func:`aiohttp.ClientSession.post`.
    """

    async with aiohttp.ClientSession() as session:
        async with session.post(*args, **kwargs) as response:
            response.raise_for_status()

            return await response.json()


def get_var_dict_from_ctx(ctx: ContextA, prefix: str = '_') -> typing.Dict[str, typing.Any]:
    """
    Returns the dict to be used in REPL for a given Context.
    """

    raw_var_dict = {
        'author': ctx.author,
        'bot': ctx.bot,
        'channel': ctx.channel,
        'ctx': ctx,
        'find': discord.utils.find,
        'get': discord.utils.get,
        'guild': ctx.guild,
        'me': ctx.me,
        'http_get_bytes': http_get_bytes,
        'http_get_json': http_get_json,
        'http_post_bytes': http_post_bytes,
        'http_post_json': http_post_json,
        'message': ctx.message,
        'request': request,
        'cf': chat_formatting,
        'reply': ctx.message.reference and ctx.message.reference.resolved,
        'rtfs': inspect.getsource,
        'getprop': findprop
    }

    return {f'{prefix}{k}': v for k, v in raw_var_dict.items()}


def findprop(obj: typing.Any, prop: str) -> typing.List[str]:
    return [i for i in dir(obj) if prop.lower() in i]


async def request(bot: Red, *args: typing.Any, **kwargs: typing.Any) -> typing.Union[bytes, dict]:
    """
    Performs a HTTP request against a URL, returning the response payload as bytes.

    The arguments to pass are the same as :func:`aiohttp.ClientSession.get`,
    with an additional ``json`` bool which indicates whether to return the result as JSON (defaults to ``True``).
    """
    json = kwargs.pop('json', True)

    async with bot.session.request(*args, **kwargs) as response:
        response.raise_for_status()

        if json:
            return await response.json(loads=discord.utils._from_json)

        return await response.read()

