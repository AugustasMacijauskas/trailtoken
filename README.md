# trailtoken

An application that visualises open source LLM tokenizers.


# Usage

To launch the frontend locally, run the following commands:
```bash
cd frontend/
npm install
npm run dev
```

and you should be able to access the website at [http://localhost:3000/trailtoken](http://localhost:3000/trailtoken)

To run the backend locally, execute:
```bash
cd backend/
pip install -r requirements. txt
python src/main.py
```

and you should be able to make requests to `http://127.0.0.1:5000/`. In particular, a request to tokenizer text can be made to `http://127.0.0.1:5000/tokenize`. The body of the request has the following structure:
```json
{
  "tokenizer_name": string,
  "input_text": string
}
```

Other useful frontend commands are
```bash
npm run lint  # for linting
npm run build # build the site
npm run start # run the built site
```

# Tests

Check backend test coverage with
```bash
pytest --cov-report=term-missing:skip-covered --cov=src/
```

# Acknowledgements

Inspired by Andrej Karpathy's [video](https://www.youtube.com/watch?v=zduSFxRajkE) on tokenization and a [similar tool](https://tiktokenizer.vercel.app/) for visualising OpenAI tokenizers.

# Cite

You can cite this work by using the following
```bibtex
@misc{trailtoken2024,
  author = {Lopata, Laurynas and Macijauskas, Augustas},
  title = {trailtoken: {O}pen {S}ource {LLM} {V}isualiser},
  year = {2024},
  howpublished = {\url{https://augustasmacijauskas.github.io/trailtoken/}},
  note = {Accessed: 2024-04-02}
}
```
