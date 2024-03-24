import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import grapheme
from pydantic import BaseModel
from transformers import AutoTokenizer, GPT2TokenizerFast, PreTrainedTokenizerBase


# Load environment variables from .env file
load_dotenv()


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
    graphemes = list(grapheme.graphemes(input_text))

    # @TODO: think about whether we want to add special tokens or how to deal with them if we do
    encoding = tokenizer.encode(input_text, add_special_tokens=False)

    segments: list[Segment] = []

    curr_text = ""
    curr_tokens: list[Token] = []
    for idx, token_id in enumerate(encoding):
        curr_text = tokenizer.decode([x.id for x in curr_tokens] + [token_id])
        curr_tokens.append(Token(id=token_id, idx=idx))

        curr_graphemes = list(grapheme.graphemes(curr_text))
        if len(curr_graphemes) <= len(graphemes) and all(
            [graphemes[idx] == item for idx, item in enumerate(curr_graphemes)]
        ):
            segments.append(Segment(text=curr_text, tokens=curr_tokens))

            graphemes = graphemes[len(curr_graphemes):]
            curr_text = ""
            curr_tokens = []

    return segments


def load_tokenizer(tokenizer_name):
    # @ TODO: think of what other tokenizer classes might we want to support
    tokenizer_classes = [AutoTokenizer, GPT2TokenizerFast]

    tokenizer = None
    for tokenizer_class in tokenizer_classes:
        try:
            tokenizer = tokenizer_class.from_pretrained(tokenizer_name, token=os.getenv("HF_ACCESS_TOKEN"))
            break
        except Exception:
            continue

    return tokenizer


@app.post("/tokenize")
def tokenize(tokenization_input: TokenizationInput) -> list[Segment] | None:
    tokenizer = load_tokenizer(tokenization_input.tokenizer_name)
    if tokenizer is None:
        # @TODO: return something better
        return None

    return get_segments(tokenizer, tokenization_input.input_text)
