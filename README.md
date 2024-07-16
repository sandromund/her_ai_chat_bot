# HER

This AI runs locally and can be spoken to directly via microphone.

This runs on my toaster (Windows 10, 16GB RAM, AMD Ryzen 5, NVIDA GeForce RTX 2070 Super).

## Run

1. Install [llama2-uncensored](https://ollama.com/library/llama2-uncensored) and run it

```shell
ollama run llama2-uncensored
```

OR use [LM Studio](https://lmstudio.ai/) and run a Local Inference Server

The thinker import in [src/ai.py]() needs to be adapted if u change the LLM.

````python
from src.thinker import ThinkerLMStudio as Thinker
````

Adapt the [config.yaml]() if necessary and run the main.

````shell
python main.py
````

### Alternative generation web UI

If you don`t want to work with Python the [text-generation-webui](https://github.com/oobabooga/text-generation-webui) to
use e.g. [Mistral](https://huggingface.co/TheBloke/CapybaraHermes-2.5-Mistral-7B-AWQ) is also nice.
Follow a [guide](https://www.youtube.com/watch?v=hGHgMUWC3GI) and inspect http://localhost:7860/?__theme=dark .

