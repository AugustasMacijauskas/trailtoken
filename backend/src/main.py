import os

from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
import grapheme
from marshmallow import Schema, fields
from transformers import AutoTokenizer, GPT2TokenizerFast, PreTrainedTokenizerBase, BertTokenizer, BertTokenizerFast
from tokenizers.tools import EncodingVisualizer


# Load environment variables from .env file
load_dotenv()


app = Flask(__name__)

# Setup CORS with origins loaded from environment variables
origins = [
    os.getenv("LOCALHOST_URL"),
    os.getenv("FRONTEND_URL"),

]
origins = [origin for origin in origins if origin is not None]
CORS(app, resources={r"/tokenize": {"origins": origins, "allow_headers": ["Content-Type"]}})


class TokenSchema(Schema):
    id = fields.Int()
    idx = fields.Int()


class SegmentSchema(Schema):
    text = fields.Str()
    tokens = fields.List(fields.Nested(TokenSchema))


class Token:
    def __init__(self, id: int, idx: int):
        self.id = id
        self.idx = idx

    def to_dict(self):
        return {"id": self.id, "idx": self.idx}


class Segment:
    def __init__(self, text: str, tokens: list[Token]):
        self.text = text
        self.tokens = tokens

    def to_dict(self) -> dict:
        return {"text": self.text, "tokens": [token.to_dict() for token in self.tokens]}


# @TODO: add test cases for this code
def get_segments_bert_tokenizer(tokenizer: PreTrainedTokenizerBase, input_text: str) -> list[dict]:
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

    # @TODO: add explanations for what this code is doing
    texts = [tokenizer.decode(segment) for segment in tokens_id_list]
    texts = [text if idx == 0 or text == "" else " " + text for idx, text in enumerate(texts)]
    texts = [text if not text.startswith(" ##") else text[1:] for text in texts]

    tokens = [
        [Token(id=token_id, idx=token_index) for token_id, token_index in zip(token_ids, token_indices)]
        for token_ids, token_indices in zip(tokens_id_list, token_index_list)
    ]

    return [Segment(text=text, tokens=tokens).to_dict() for text, tokens in zip(texts, tokens)]


def get_segments(tokenizer: PreTrainedTokenizerBase, input_text: str) -> list[dict]:
    is_bert = isinstance(tokenizer, (BertTokenizer, BertTokenizerFast))
    print(f"{is_bert=}")

    if is_bert:
        return get_segments_bert_tokenizer(tokenizer, input_text)

    # @TODO: think about whether we want to add special tokens or how to deal with them if we do
    encoding = tokenizer.encode(input_text, add_special_tokens=False)

    graphemes = list(grapheme.graphemes(input_text))

    id2token = {v: k for k, v in tokenizer.get_vocab().items()}

    segments: list[Segment] = []

    curr_text = ""
    curr_tokens: list[Token] = []
    for idx, token_id in enumerate(encoding):
        curr_text = tokenizer.decode([token.id for token in curr_tokens] + [token_id])

        curr_tokens.append(Token(id=token_id, idx=idx))

        if idx > 0 and id2token[curr_tokens[0].id].startswith("▁"):
            curr_text = " " + curr_text

        curr_graphemes = list(grapheme.graphemes(curr_text))

        if len(curr_graphemes) <= len(graphemes) and all(
            graphemes[idx] == item for idx, item in enumerate(curr_graphemes)
        ):
            segments.append(Segment(text=curr_text, tokens=curr_tokens))

            graphemes = graphemes[len(curr_graphemes):]            
            curr_text = ""
            curr_tokens = []

    return [segment.to_dict() for segment in segments]


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


@app.route("/tokenize", methods=["POST"])
def tokenize():
    # Parse the input using Marshmallow or directly from Flask's request object
    data = request.get_json()
    tokenizer_name = data.get("tokenizer_name")
    input_text = data.get("input_text")

    if not tokenizer_name or not input_text:
        return jsonify({"error": "Missing tokenizer_name or input_text"}), 400

    tokenizer = load_tokenizer(tokenizer_name)
    if tokenizer is None:
        return jsonify({"error": "Failed to load tokenizer"}), 400

    segments = get_segments(tokenizer, input_text)
    segment_schema = SegmentSchema(many=True)

    result = segment_schema.dump(segments)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
