from transformers import AutoTokenizer

from main import get_segments


# @TODO: the random emoji test does not work:
# "👩‍👦‍👦 👩‍👧‍👦 👩‍👧‍👧 👩‍👩‍👦 👩‍👩‍👧 🇨🇿" -> ["👩‍👦‍👦", " 👩‍👧‍👦", " 👩‍👧‍👧", " 👩‍👩‍👦", " 👩‍👩‍👧", " 🇨🇿"]
def test_filter_step_data():
    tokenizer = AutoTokenizer.from_pretrained("openai-community/gpt2")

    assert [x.text for x in get_segments(tokenizer, "由非營利組織")] == ["由", "非", "營", "利", "組", "織"]
