from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import grapheme
from pydantic import BaseModel
from transformers import AutoTokenizer, PreTrainedTokenizerBase
from tokenizers.tools import EncodingVisualizer


app = FastAPI()

# Add CORSMiddleware to the application instance
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


class TokenizationInput(BaseModel):
    tokenizer_name: str
    input_text: str


class Token(BaseModel):
    id: int
    idx: int


class Segment(BaseModel):
    text: str
    tokens: list[Token]


def get_segments(tokenizer: PreTrainedTokenizerBase, input_text: str) -> list[Segment]:
    print(list(grapheme.graphemes(input_text)))

    encoding = tokenizer._tokenizer.encode(input_text)

    char_states = EncodingVisualizer._EncodingVisualizer__make_char_states(input_text, encoding, [])

    current_consecutive_chars = [char_states[0]]
    segments_raw = []

    for cs in char_states[1:]:
        if cs.partition_key() == current_consecutive_chars[0].partition_key():
            # If the current character is in the same "group" as the previous one
            current_consecutive_chars.append(cs)
        else:
            # Otherwise we make a span for the previous group
            segments_raw.append(current_consecutive_chars)
            # An reset the consecutive_char_list to form a new group
            current_consecutive_chars = [cs]

    segments_raw.append(current_consecutive_chars)

    token_index_list = [x[-1].tokens for x in segments_raw]

    tokens_id_list = [[encoding.ids[token_idx] for token_idx in segment] for segment in token_index_list]

    texts = [tokenizer.decode(segment) for segment in tokens_id_list]
    print(texts)

    tokens = [
        [Token(id=token_id, idx=token_index) for token_id, token_index in zip(token_ids, token_indices)]
        for token_ids, token_indices in zip(tokens_id_list, token_index_list)
    ]

    return [Segment(text=text, tokens=tokens) for text, tokens in zip(texts, tokens)]


@app.post("/tokenize")
def tokenize(tokenization_input: TokenizationInput) -> list[Segment] | None:
    try:
        tokenizer = AutoTokenizer.from_pretrained(tokenization_input.tokenizer_name)
    except ValueError:
        # @TODO: return something better
        return None

    return get_segments(tokenizer, tokenization_input.input_text)


if __name__ == "__main__":
    tokenizer = AutoTokenizer.from_pretrained("openai-community/gpt2")
    print(get_segments(tokenizer, "👩‍👦‍👦 👩‍👧‍👦 👩‍👧‍👧 👩‍👩‍👦 👩‍👩‍👧 🇨🇿"))
