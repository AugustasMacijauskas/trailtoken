import pytest
from transformers import AutoTokenizer

from main import app, get_segments


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@pytest.mark.parametrize(
    "input_text, tokenizer_name, expected_output",
    [
        (
            "Hello world",
            "openai-community/gpt2",
            [
                {"text": "Hello", "tokens": [{"id": 15496, "idx": 0}]},
                {"text": " world", "tokens": [{"id": 995, "idx": 1}]},
            ],
        ),
        (
            "New lines\\n\\n\\n\\n\\n       Spaces",
            "openai-community/gpt2",
            [
                {"text": "New", "tokens": [{"id": 3791, "idx": 0}]},
                {"text": " lines", "tokens": [{"id": 3951, "idx": 1}]},
                {"text": "\\", "tokens": [{"id": 59, "idx": 2}]},
                {"text": "n", "tokens": [{"id": 77, "idx": 3}]},
                {"text": "\\", "tokens": [{"id": 59, "idx": 4}]},
                {"text": "n", "tokens": [{"id": 77, "idx": 5}]},
                {"text": "\\", "tokens": [{"id": 59, "idx": 6}]},
                {"text": "n", "tokens": [{"id": 77, "idx": 7}]},
                {"text": "\\", "tokens": [{"id": 59, "idx": 8}]},
                {"text": "n", "tokens": [{"id": 77, "idx": 9}]},
                {"text": "\\", "tokens": [{"id": 59, "idx": 10}]},
                {"text": "n", "tokens": [{"id": 77, "idx": 11}]},
                {"text": " ", "tokens": [{"id": 220, "idx": 12}]},
                {"text": " ", "tokens": [{"id": 220, "idx": 13}]},
                {"text": " ", "tokens": [{"id": 220, "idx": 14}]},
                {"text": " ", "tokens": [{"id": 220, "idx": 15}]},
                {"text": " ", "tokens": [{"id": 220, "idx": 16}]},
                {"text": " ", "tokens": [{"id": 220, "idx": 17}]},
                {"text": " Spaces", "tokens": [{"id": 48086, "idx": 18}]},
            ],
        ),
        (
            "👩‍👦‍👦 👩‍👧‍👦 👩‍👧‍👧 👩‍👩‍👦 👩‍👩‍👧 🇨🇿 Emojis: 🧑🏾‍💻️🧑🏿‍🎓️🧑🏿‍🏭️🧑🏿‍💻️",
            "openai-community/gpt2",
            [
                {
                    "text": "👩‍👦‍👦",
                    "tokens": [
                        {"id": 41840, "idx": 0},
                        {"id": 102, "idx": 1},
                        {"id": 447, "idx": 2},
                        {"id": 235, "idx": 3},
                        {"id": 41840, "idx": 4},
                        {"id": 99, "idx": 5},
                        {"id": 447, "idx": 6},
                        {"id": 235, "idx": 7},
                        {"id": 41840, "idx": 8},
                        {"id": 99, "idx": 9},
                    ],
                },
                {
                    "text": " 👩‍👧‍👦",
                    "tokens": [
                        {"id": 50169, "idx": 10},
                        {"id": 102, "idx": 11},
                        {"id": 447, "idx": 12},
                        {"id": 235, "idx": 13},
                        {"id": 41840, "idx": 14},
                        {"id": 100, "idx": 15},
                        {"id": 447, "idx": 16},
                        {"id": 235, "idx": 17},
                        {"id": 41840, "idx": 18},
                        {"id": 99, "idx": 19},
                    ],
                },
                {
                    "text": " 👩‍👧‍👧",
                    "tokens": [
                        {"id": 50169, "idx": 20},
                        {"id": 102, "idx": 21},
                        {"id": 447, "idx": 22},
                        {"id": 235, "idx": 23},
                        {"id": 41840, "idx": 24},
                        {"id": 100, "idx": 25},
                        {"id": 447, "idx": 26},
                        {"id": 235, "idx": 27},
                        {"id": 41840, "idx": 28},
                        {"id": 100, "idx": 29},
                    ],
                },
                {
                    "text": " 👩‍👩‍👦",
                    "tokens": [
                        {"id": 50169, "idx": 30},
                        {"id": 102, "idx": 31},
                        {"id": 447, "idx": 32},
                        {"id": 235, "idx": 33},
                        {"id": 41840, "idx": 34},
                        {"id": 102, "idx": 35},
                        {"id": 447, "idx": 36},
                        {"id": 235, "idx": 37},
                        {"id": 41840, "idx": 38},
                        {"id": 99, "idx": 39},
                    ],
                },
                {
                    "text": " 👩‍👩‍👧",
                    "tokens": [
                        {"id": 50169, "idx": 40},
                        {"id": 102, "idx": 41},
                        {"id": 447, "idx": 42},
                        {"id": 235, "idx": 43},
                        {"id": 41840, "idx": 44},
                        {"id": 102, "idx": 45},
                        {"id": 447, "idx": 46},
                        {"id": 235, "idx": 47},
                        {"id": 41840, "idx": 48},
                        {"id": 100, "idx": 49},
                    ],
                },
                {
                    "text": " 🇨🇿",
                    "tokens": [
                        {"id": 12520, "idx": 50},
                        {"id": 229, "idx": 51},
                        {"id": 101, "idx": 52},
                        {"id": 8582, "idx": 53},
                        {"id": 229, "idx": 54},
                        {"id": 123, "idx": 55},
                    ],
                },
                {"text": " Em", "tokens": [{"id": 2295, "idx": 56}]},
                {"text": "oj", "tokens": [{"id": 13210, "idx": 57}]},
                {"text": "is", "tokens": [{"id": 271, "idx": 58}]},
                {"text": ":", "tokens": [{"id": 25, "idx": 59}]},
                {
                    "text": " 🧑🏾‍💻️",
                    "tokens": [
                        {"id": 12520, "idx": 60},
                        {"id": 100, "idx": 61},
                        {"id": 239, "idx": 62},
                        {"id": 8582, "idx": 63},
                        {"id": 237, "idx": 64},
                        {"id": 122, "idx": 65},
                        {"id": 447, "idx": 66},
                        {"id": 235, "idx": 67},
                        {"id": 8582, "idx": 68},
                        {"id": 240, "idx": 69},
                        {"id": 119, "idx": 70},
                        {"id": 37929, "idx": 71},
                    ],
                },
                {
                    "text": "🧑🏿‍🎓️",
                    "tokens": [
                        {"id": 8582, "idx": 72},
                        {"id": 100, "idx": 73},
                        {"id": 239, "idx": 74},
                        {"id": 8582, "idx": 75},
                        {"id": 237, "idx": 76},
                        {"id": 123, "idx": 77},
                        {"id": 447, "idx": 78},
                        {"id": 235, "idx": 79},
                        {"id": 8582, "idx": 80},
                        {"id": 236, "idx": 81},
                        {"id": 241, "idx": 82},
                        {"id": 37929, "idx": 83},
                    ],
                },
                {
                    "text": "🧑🏿‍🏭️",
                    "tokens": [
                        {"id": 8582, "idx": 84},
                        {"id": 100, "idx": 85},
                        {"id": 239, "idx": 86},
                        {"id": 8582, "idx": 87},
                        {"id": 237, "idx": 88},
                        {"id": 123, "idx": 89},
                        {"id": 447, "idx": 90},
                        {"id": 235, "idx": 91},
                        {"id": 8582, "idx": 92},
                        {"id": 237, "idx": 93},
                        {"id": 255, "idx": 94},
                        {"id": 37929, "idx": 95},
                    ],
                },
                {
                    "text": "🧑🏿‍💻️",
                    "tokens": [
                        {"id": 8582, "idx": 96},
                        {"id": 100, "idx": 97},
                        {"id": 239, "idx": 98},
                        {"id": 8582, "idx": 99},
                        {"id": 237, "idx": 100},
                        {"id": 123, "idx": 101},
                        {"id": 447, "idx": 102},
                        {"id": 235, "idx": 103},
                        {"id": 8582, "idx": 104},
                        {"id": 240, "idx": 105},
                        {"id": 119, "idx": 106},
                        {"id": 37929, "idx": 107},
                    ],
                },
            ],
        ),
        (
            "是美國一個人工智能研究實驗室 由非營利組織OpenAI Inc",
            "openai-community/gpt2",
            [
                {"text": "是", "tokens": [{"id": 42468, "idx": 0}]},
                {"text": "美", "tokens": [{"id": 163, "idx": 1}, {"id": 122, "idx": 2}, {"id": 236, "idx": 3}]},
                {"text": "國", "tokens": [{"id": 28839, "idx": 4}, {"id": 233, "idx": 5}]},
                {"text": "一", "tokens": [{"id": 31660, "idx": 6}]},
                {"text": "個", "tokens": [{"id": 161, "idx": 7}, {"id": 222, "idx": 8}, {"id": 233, "idx": 9}]},
                {"text": "人", "tokens": [{"id": 21689, "idx": 10}]},
                {"text": "工", "tokens": [{"id": 32432, "idx": 11}, {"id": 98, "idx": 12}]},
                {"text": "智", "tokens": [{"id": 162, "idx": 13}, {"id": 247, "idx": 14}, {"id": 118, "idx": 15}]},
                {"text": "能", "tokens": [{"id": 47797, "idx": 16}, {"id": 121, "idx": 17}]},
                {"text": "研", "tokens": [{"id": 163, "idx": 18}, {"id": 254, "idx": 19}, {"id": 242, "idx": 20}]},
                {"text": "究", "tokens": [{"id": 163, "idx": 21}, {"id": 102, "idx": 22}, {"id": 114, "idx": 23}]},
                {"text": "實", "tokens": [{"id": 43380, "idx": 24}, {"id": 99, "idx": 25}]},
                {"text": "驗", "tokens": [{"id": 165, "idx": 26}, {"id": 102, "idx": 27}, {"id": 245, "idx": 28}]},
                {"text": "室", "tokens": [{"id": 22522, "idx": 29}, {"id": 97, "idx": 30}]},
                {"text": " 由", "tokens": [{"id": 13328, "idx": 31}, {"id": 242, "idx": 32}, {"id": 109, "idx": 33}]},
                {"text": "非", "tokens": [{"id": 165, "idx": 34}, {"id": 251, "idx": 35}, {"id": 252, "idx": 36}]},
                {"text": "營", "tokens": [{"id": 163, "idx": 37}, {"id": 229, "idx": 38}, {"id": 253, "idx": 39}]},
                {"text": "利", "tokens": [{"id": 26344, "idx": 40}, {"id": 102, "idx": 41}]},
                {"text": "組", "tokens": [{"id": 163, "idx": 42}, {"id": 113, "idx": 43}, {"id": 226, "idx": 44}]},
                {"text": "織", "tokens": [{"id": 163, "idx": 45}, {"id": 117, "idx": 46}, {"id": 242, "idx": 47}]},
                {"text": "Open", "tokens": [{"id": 11505, "idx": 48}]},
                {"text": "AI", "tokens": [{"id": 20185, "idx": 49}]},
                {"text": " Inc", "tokens": [{"id": 3457, "idx": 50}]},
            ],
        ),
        (
            "<|im_start|>test<|im_end|>",
            "openai-community/gpt2",
            [
                {"text": "<", "tokens": [{"id": 27, "idx": 0}]},
                {"text": "|", "tokens": [{"id": 91, "idx": 1}]},
                {"text": "im", "tokens": [{"id": 320, "idx": 2}]},
                {"text": "_", "tokens": [{"id": 62, "idx": 3}]},
                {"text": "start", "tokens": [{"id": 9688, "idx": 4}]},
                {"text": "|", "tokens": [{"id": 91, "idx": 5}]},
                {"text": ">", "tokens": [{"id": 29, "idx": 6}]},
                {"text": "test", "tokens": [{"id": 9288, "idx": 7}]},
                {"text": "<", "tokens": [{"id": 27, "idx": 8}]},
                {"text": "|", "tokens": [{"id": 91, "idx": 9}]},
                {"text": "im", "tokens": [{"id": 320, "idx": 10}]},
                {"text": "_", "tokens": [{"id": 62, "idx": 11}]},
                {"text": "end", "tokens": [{"id": 437, "idx": 12}]},
                {"text": "|", "tokens": [{"id": 91, "idx": 13}]},
                {"text": ">", "tokens": [{"id": 29, "idx": 14}]},
            ],
        ),
        (
            "<|im_start|>test<|im_end|>",
            "Xenova/gpt-4",
            [
                {"text": "<|im_start|>", "tokens": [{"id": 100264, "idx": 0}]},
                {"text": "test", "tokens": [{"id": 1985, "idx": 1}]},
                {"text": "<|im_end|>", "tokens": [{"id": 100265, "idx": 2}]},
            ],
        ),
    ],
)
def test_get_segments(client, input_text, tokenizer_name, expected_output):
    response = client.post("/tokenize", json={"input_text": input_text, "tokenizer_name": tokenizer_name})

    # Ensure the response data is loaded correctly
    data = response.get_json()

    assert response.status_code == 200
    assert data == expected_output


@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        (
            "由非營利組織",
            ["由", "非", "營", "利", "組", "織"],
        ),
        (
            "👩‍👦‍👦 👩‍👧‍👦 👩‍👧‍👧 👩‍👩‍👦 👩‍👩‍👧 🇨🇿",
            ["👩‍👦‍👦", " 👩‍👧‍👦", " 👩‍👧‍👧", " 👩‍👩‍👦", " 👩‍👩‍👧", " 🇨🇿"],
        ),
    ],
)
def test_get_segments_edge_cases(input_text, expected_output):
    tokenizer = AutoTokenizer.from_pretrained("openai-community/gpt2")

    assert [x["text"] for x in get_segments(tokenizer, input_text)] == expected_output
