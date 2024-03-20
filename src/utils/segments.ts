import { type Tiktoken } from "tiktoken";
import { AutoTokenizer } from "@xenova/transformers";
import Graphemer from "graphemer";

const textDecoder = new TextDecoder();
const graphemer = new Graphemer();

type Token = {
  id: number;
  idx: number;
};
export type Segment = {
  text: string;
  tokens: Token[];
};

export async function getSegments(encoder: Tiktoken, inputText: string) {
  const tokenizer = await AutoTokenizer.from_pretrained(
    "codellama/CodeLlama-7b-Instruct-hf"
  );
  const { input_ids } = await tokenizer(inputText);
  const encoding = Array.from(input_ids.data).map((item: any) => Number(item)); // this should be typed better
  // Toliau ziuret nuo cia

  // const encoding = encoder.encode(inputText, "all");
  console.log(tokenizer.model.vocab);
  console.log(tokenizer.decoder);
  console.log(encoding);
  const segments: Segment[] = [];

  // let byteAcc: number[] = [];
  let tokenAcc: { id: number; idx: number }[] = [];
  let inputGraphemes = graphemer.splitGraphemes(inputText);
  console.log(inputGraphemes);

  console.log("--------------");
  for (let idx = 0; idx < encoding.length; idx++) {
    const token = encoding[idx]!;

    // console.log(token, ...encoder.decode_single_token_bytes(token));
    // byteAcc.push(...encoder.decode_single_token_bytes(token));
    tokenAcc.push({ id: token, idx });

    // const segmentText = textDecoder.decode(new Uint8Array(byteAcc));
    const segmentTextRaw = tokenizer.model.convert_ids_to_tokens([token]);
    if (tokenizer.special_tokens.includes(segmentTextRaw[0])) {
      continue;
    }
    // console.log(segmentTextRaw, segmentTextRaw[0]![0] === "▁");
    let segmentText = tokenizer.decoder(segmentTextRaw);
    if (
      segmentTextRaw[0]![0] === "▁" &&
      segmentTextRaw[0]!.length > 1 &&
      idx > 1
    ) {
      segmentText = " " + segmentText;
    }
    const graphemes = graphemer.splitGraphemes(segmentText);

    console.log(
      graphemes,
      segmentText,
      // inputGraphemes.slice(0, graphemes.length - 1)
      inputGraphemes
    );
    if (graphemes.every((item, idx) => inputGraphemes[idx] === item)) {
      console.log(`"${segmentText}"`, graphemes);
      segments.push({ text: segmentText, tokens: tokenAcc });

      // byteAcc = [];
      tokenAcc = [];
      inputGraphemes = inputGraphemes.slice(graphemes.length);
    }
    console.log("--------------");
  }

  console.log(segments);

  return segments;
}
