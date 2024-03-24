import {
  type GetServerSideProps,
  type InferGetServerSidePropsType,
  type NextPage,
} from "next";
import Head from "next/head";
import { useMemo, useState } from "react";
import { Github, Twitter } from "lucide-react";

import { TokenViewer } from "~/sections/TokenViewer";
import { TextArea } from "~/components/Input";
import { Button } from "~/components/Button";

// function isChatModel(
//   params: { model: TiktokenModel } | { encoder: TiktokenEncoding }
// ): params is {
//   model: "gpt-3.5-turbo" | "gpt-4" | "gpt-4-32k" | "gpt-4-1106-preview";
// } {
//   return (
//     "model" in params &&
//     (params.model === "gpt-3.5-turbo" ||
//       params.model === "gpt-4" ||
//       params.model === "gpt-4-1106-preview" ||
//       params.model === "gpt-4-32k")
//   );
// }

const Home: NextPage<InferGetServerSidePropsType<typeof getServerSideProps>> = (
  props
) => {
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
      const response = await fetch("http://127.0.0.1:8000/tokenize", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          // Add any other headers your API needs
        },
        body: JSON.stringify({
          tokenizer_name: tokenizerName,
          input_text: inputText,
        }),
      });
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      const result = await response.json();
      console.log(result);
      setData(result);
    } catch (error) {
      setError(error.message);
    } finally {
      setIsFetching(false);
    }
  };

  return (
    <>
      <Head>
        <title>trailtoken</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <main className="mx-auto flex min-h-screen max-w-[1200px] flex-col gap-4 p-8">
        <div className="flex flex-col justify-between gap-2 sm:flex-row sm:items-center">
          <h1 className="text-4xl font-bold">trailtoken</h1>
        </div>

        <div className="grid gap-4 md:grid-cols-2">
          <section className="flex flex-col gap-4">
            <TextArea
              value={tokenizerName}
              onChange={(e) => setTokenizerName(e.target.value)}
              className="min-h-[256px] rounded-md border p-4 font-mono shadow-sm"
            />
            <TextArea
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              className="min-h-[256px] rounded-md border p-4 font-mono shadow-sm"
            />
            <Button onClick={fetchData}>Tokenize</Button>
          </section>

          <section className="flex flex-col gap-4">
            <TokenViewer data={data} isFetching={isFetching} />
            {/* @TODO: Cia ChatGPT response, reiktu gal labiau pacheckint */}
            {error && <p>Error: {error}</p>}
          </section>
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
              href="https://duong.dev" // Pridet Lauryno link
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
              href="https://twitter.com/__dqbd" // @ TODO: pridet Lauryno twitter
            >
              <Twitter />
            </a>
          </div>
        </div>
      </main>
    </>
  );
};

export const getServerSideProps: GetServerSideProps = async (context) => {
  return { props: { query: context.query } };
};

export default Home;
