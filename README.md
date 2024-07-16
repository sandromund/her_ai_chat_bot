# HER

This AI runs locally and can be spoken to directly via microphone.

This runs on my toaster (Windows 10, 16GB RAM, AMD Ryzen 5, NVIDA GeForce RTX 2070 Super).

## Run

(OPTIONAL) Install [llama2-uncensored](https://ollama.com/library/llama2-uncensored) and run it

```shell
ollama run llama2-uncensored
```

(RECOMMENDED) Use [LM Studio](https://lmstudio.ai/) and run a Local Inference Server

The thinker import in src/ai.py needs to be adapted if u change the LLM.

````python
from src.thinker import ThinkerLMStudio as Thinker
````

Adapt the config.yaml if necessary and run the main.

````shell
python main.py
````

### Alternative generation web UI

If you don`t want to work with Python the [text-generation-webui](https://github.com/oobabooga/text-generation-webui) to
use e.g. [Mistral](https://huggingface.co/TheBloke/CapybaraHermes-2.5-Mistral-7B-AWQ) is also nice.
Follow a [guide](https://www.youtube.com/watch?v=hGHgMUWC3GI) and inspect http://localhost:7860/?__theme=dark .

## Next
- Add a knowledge base / RAG
- Improve Speach Recognition
  - https://github.com/oliverguhr/wav2vec2-live
  - https://www.youtube.com/watch?v=k6nIxWGdrS4
  - https://www.youtube.com/watch?v=2kSPbH4jWME
- German Support / Change to German


``````
git submodule add https://github.com/oliverguhr/wav2vec2-live.git libs/wav2vec2-live

``````