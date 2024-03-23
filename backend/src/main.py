from fastapi import FastAPI
import grapheme
from pydantic import BaseModel
from transformers import AutoTokenizer, PreTrainedTokenizerBase

app = FastAPI()


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
    # Encode the input text, getting token ids
    encoding = tokenizer.encode(input_text, add_special_tokens=False)

    # Prepare accumulators for bytes and tokens
    byte_acc: list[str] = []
    token_acc: list[Token] = []
    segments: list[Segment] = []

    # Split input text into graphemes
    input_graphemes = grapheme.graphemes(input_text)

    for idx, token_id in enumerate(encoding):
        # Decode each token id to its corresponding string representation
        token_str = tokenizer.decode([token_id])

        byte_acc.append(token_str)
        token_acc.append(Token(id=token_id, idx=idx))

        # Attempt to decode the accumulated bytes to text
        segment_text = ''.join(byte_acc)
        graphemes = list(grapheme.graphemes(segment_text))

        # Check if the decoded text matches the input graphemes so far
        if graphemes == input_graphemes[:len(graphemes)]:
            segments.append(Segment(text=segment_text, tokens=token_acc))
            byte_acc = []
            token_acc = []
            input_graphemes = input_graphemes[len(graphemes):]

    return segments


@app.post("/tokenize")
def tokenize(tokenization_input: TokenizationInput) -> list[Segment] | None:
    try:
        tokenizer = AutoTokenizer.from_pretrained(tokenization_input.tokenizer_name)
    except ValueError:
        # @TODO: return something better
        return None

    segments = get_segments(tokenizer, tokenization_input.input_text)

    return segments
