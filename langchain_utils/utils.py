#!/usr/bin/env python3


def get_token_count(s: str, model_name: str = 'gpt-3.5-turbo') -> int:
    from tiktoken import encoding_for_model

    enc = encoding_for_model(model_name)
    tokenized_text = enc.encode(s)

    # calculate the number of tokens in the encoded text
    return len(tokenized_text)
