# TODO

1. Surast koki normalesni favicon ir idet i `public/favicon.ico`
    - Partially done, bet paieskot kokio artimesnio sielai, gal koki emoji?
1. ~~Pabandyt nucopint tiktokenizer~~
1. ~~Pakeist tiktokenizer API calls i `tokenizers-js`~~ -> nepaejo
1. ~~Panasu, kad python backend veikia, vienintelis, ka reikia padaryt, tai fronte gavus atsakyma is backend pramappint `text -> graphemer.splitGraphemes(text)` (kitaip emoji nesusirenderina)~~ -> Issisprende, kai buvo perrasytas algoritmas
1. Kode pilna `TODO`, reikia pro juos praeit
1. Pridet authentication backende, kad tik mes galetume kreiptis. Jauciu reikia sugeneruot koki unique string ir tada fronte ji issiust is kokio `.env` uzloadinus, o backende tikrint, ar sutampa atsiustas string.
1. Dabar leidziam visus origins (CORS check isjungtas). Reiktu issiaiskint, koks turetu but realybej
1. ~~Padaryt input field tokenizerio pavadinimui (dabar ten yra `TextArea` componentas, turetu but kazkas kaip TextInput, kur ne multiline)~~
1. Issiaiskint, kaip veikia "Show whitespace" mygtukas
1. Nutrynem [useParams](https://github.com/dqbd/tiktokenizer/blob/bd217ec7e019762070d9f388693b946c0f74dc01/src/pages/index.tsx#L69), reikia pasiaiskint ar cia kazkuo svarbu
1. tiktokenizer dabar ant kiekvieno change inpute callina funkcija, musu atveju tikriausiai gana inefficient butu, nes uzspammintume backend, tai galvoju pradziai padaryt, kad pridedam mygtuka ir tik paspaudus mygtuka nuvaziuoja POST request i backenda. Ilgainiui geresnis sprendimas turbut butu pridet kazkoki delay, kad tik baigus rasyt nusiustu uzklausa i backend (pamenu Aleksiunas kazkada moke toki padaryt, galima paklaust gal XDD)
1. ~~Pakeist footer, GitHub links, etc.~~
1. Uztikrint, kad visi tokenizers butu accessible (pvz LLaMA 2 by default neveiks man atrodo, nes reikia but leidima gavus ir hugging face checkina, kad LLaMA 2 tokenizeri galetu parsisiust tik pasivalidave vartotojai). As turiu leidima, tai tik reikia susetupint
    - Lyg LLaMA 2 susetupinau, reikia dar pamastyt, ar kitu tokiu "gated" tokenizeriu yra
    - Pamastyt, ar imanoma butu leist zmonems naudot ju private tokenizers?
1. Paziuret, ar mums svarbu exposint tokius `AutoTokenizer.from_pretrained` parametrus kaip `revision`, `subfolder`, `use_fast`, `trust_remote_code` (galbut yra ir kitu)
    - Itariu, kad truputi pamaste sumastytume kaip per daug nesivarginant sita padaryt, gal pvz padaryt, kad request body gali `kwargs` acceptint
1. Kaip busim done su frontend praeit failus istrint nereikalingus dalykus bei siaip pasiaiskint, kokiu ten libu prirasyta, gal irgi ne visko reikia
    - Turbut neblogas budas tai padaryt butu eit per `package.json`, pagooglint ka kiekvienas library daro ir jei manom, kad nereikia, istrinam (tik ten reikia kazkaip specifiskai trint su npm, man atrodo neuztenka tiesiog istrint is `package.json`, reikia patikrint)
1. ~~Pahostint frontend kazkur~~
    1. ~~Tikriausiai kokiam GitHub pages~~
1. Pahostint backend kazkur
    1. Gal tas pythonanywhere paeitu
1. Tiktokenizer turi [special treatment chat modeliams](https://github.com/dqbd/tiktokenizer/blob/bd217ec7e019762070d9f388693b946c0f74dc01/src/pages/index.tsx#L55), gal reiktu ir mums pamastyt, kaip galetume toki implementint, nes nemazai chat modeliu yra



# Papildomi testai

1. Pratestuot su ivairiais modeliais:
    1. ~~[gpt-2](openai-community/gpt2)~~ -> patestavau
    1. [gpt-3.5-turbo](https://huggingface.co/Xenova/gpt-3.5-turbo)
    1. [gpt-4](https://huggingface.co/Xenova/gpt-4)
        - Truputi testavau
    1. google-bert/bert-base-cased
    1. text-embedding-3-large
    1. T5
    1. (low priority) [text-embedding-ada-002](https://huggingface.co/Xenova/text-embedding-ada-002)
    1. (low priority) [text-davinci-003](https://huggingface.co/Xenova/text-davinci-003)
1. Parasyt papildomu unit tests
