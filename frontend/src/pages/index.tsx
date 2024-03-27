import { type NextPage } from "next";
import Head from "next/head";
import { useMemo, useState } from "react";
import { Github, Twitter } from "lucide-react";

import { TokenViewer } from "~/sections/TokenViewer";
import { TextArea, TokenizerInput } from "~/components/Input";
import { Button } from "~/components/Button";

const Home: NextPage = () => {
  // @TODO: this should probably be a more sensible default or empty?
  const [tokenizerName, setTokenizerName] = useState<string>(
    "openai-community/gpt2"
  );

  // @TODO: this text is here for quick testing, it should be more sensible or empty
  const [inputText, setInputText] = useState<string>(
    "This is my favourite emoji 😁👩‍👦‍👦 👩‍👧‍👦 👩‍👧‍👧 👩‍👩‍👦 👩‍👩‍👧 🇨🇿由非營利組織<|endoftext|>"
  );

  // @TODO: pridet error handling, ChatGPT siule toki:

  const [data, setData] = useState([]);
  const [isFetching, setIsFetching] = useState(false);
  const [error, setError] = useState(null);

  const fetchData = async () => {
    setIsFetching(true);
    try {
      // @TODO: add a check if env is development and then make the request to localhost
      const response = await fetch(
        // "https://augustasm.pythonanywhere.com/tokenize",
        "http://127.0.0.1:5000/tokenize",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            // Add any other headers your API needs
          },
          body: JSON.stringify({
            tokenizer_name: tokenizerName,
            input_text: inputText,
          }),
        }
      );
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      const result = await response.json();
      setData(result);
    } catch (error: any) {
      // TODO: set up proper error handling
      setError(error.message);
    } finally {
      setIsFetching(false);
    }
  };

  return (
    <>
      <main className="mx-auto flex min-h-screen max-w-[1200px] flex-col gap-4 p-8">
        <Head>
          <title>trailtoken</title>
          <link
            rel="icon"
            href="/trailtoken/icons8-artificial-intelligence-96.png"
          />
        </Head>
        <div className="flex flex-col justify-between gap-2 sm:flex-row sm:items-center">
          <h1 className="text-4xl font-bold">trailtoken</h1>
        </div>

        {/* Line 2: Tokenizer Input across the grid */}
        <div className="grid gap-4 md:grid-cols-1">
          <TextArea
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            className="min-h-[256px] rounded-md border p-4 font-mono shadow-sm"
          />
        </div>

        {/* Line 1: TokenizerInput and Tokenize Button with space between */}
        <div className="flex items-center justify-between gap-4">
          <TokenizerInput
            value={tokenizerName}
            onChange={(e) => setTokenizerName(e.target.value)}
            className="mr-2 flex-grow rounded-md border p-4 font-mono shadow-sm" // Added margin-right to TokenizerInput
          />
          <Button onClick={fetchData} className="ml-2">
            Tokenize
          </Button>
        </div>

        {/* Line 3: TokenViewer */}
        <div className="grid gap-4 md:grid-cols-1">
          <TokenViewer data={data} isFetching={isFetching} />
          {/* @TODO: handle errors better */}
          {error && <p>Error: {error}</p>}
        </div>

        <style jsx>
          {`
            .diagram-link:hover > span {
              margin-left: 0;
            }

            .diagram-link > svg {
              opacity: 0;
              transform: scale(0.8);
            }
            .diagram-link:hover > svg {
              opacity: 1;
              transform: scale(1);
            }
          `}
        </style>
        <div className="flex justify-between text-center md:mt-6">
          <p className=" text-sm text-slate-400">
            Built by{" "}
            <a
              target="_blank"
              rel="noreferrer"
              className="text-slate-800"
              href="https://augustasmacijauskas.github.io/personal-website/"
            >
              Augustas Macijauskas
            </a>{" "}
            and{" "}
            <a
              target="_blank"
              rel="noreferrer"
              className="text-slate-800"
              href="https://www.linkedin.com/in/laurynas-lopata-46a23480/"
            >
              Laurynas Lopata
            </a>
          </p>

          <div className="flex items-center gap-4">
            <a
              target="_blank"
              rel="noreferrer"
              className="text-slate-800"
              href="https://github.com/AugustasMacijauskas/trailtoken"
            >
              <Github />
            </a>
            <a
              target="_blank"
              rel="noreferrer"
              className="text-slate-800"
              href="https://twitter.com/augustasmac"
            >
              <Twitter />
            </a>
            <a
              target="_blank"
              rel="noreferrer"
              className="text-slate-800"
              href="https://twitter.com/CS_Laurynas"
            >
              <Twitter />
            </a>
          </div>
        </div>
      </main>
    </>
  );
};

export default Home;
