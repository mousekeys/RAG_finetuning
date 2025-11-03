# RAG_finetuning

## To dos:
  * Performed RAG and LLM finetuning, for data analysis.
  * This could be made more context rich and better by using SLM instead of json.
  * Creating a simple automation approach that automates finding the records could improve user expereince.
  * QwenVL-8b didn't perform well on images and took a large amount of time as well. So,I had to resort to OCR.
  * Deppseek-r1:8b works great and fast as well, with chromaDB for RAG which has 1024 size embeddings. The texts are small so, using a smaller embedding model would make it more space effecient.
  * Creating a easier way to finetune LLM, such as a script that would take the data and streamline the entire finetuning process, would allow things to be more personalized for now.
  * Currently, the code is hardcoded for images of bank statement from mobile banking. Finetuning qwenVL for OCR and data extarction would make it more versatile.

### Note to self: There's copilot AI generated base code in the pull request section, the code generated isn't used here. Its available in the pull for better structuring the code look at it for better structuing the current code.
