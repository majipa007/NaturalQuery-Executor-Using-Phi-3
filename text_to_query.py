from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, BitsAndBytesConfig


class Text_to_query:
    def __init__(self):
        quantization_config = BitsAndBytesConfig(load_in_4bit=True)

        self.model = AutoModelForCausalLM.from_pretrained("Majipa/text-to-SQL",
                                                          device_map="cuda",
                                                          torch_dtype="auto",
                                                          quantization_config=quantization_config)

        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-4k-instruct")
        self.pipe = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
        )
        self.generation_args = {
            "max_new_tokens": 500,
            "temperature": 0.7,
            "return_full_text": False,
        }

    def query(self, inp):
        messages = [
            {"role": "system", "content": "You are a helpful text-to-SQL assistant."},
            {"role": "user",
             "content": f"question:{inp} context:CREATE TABLE contacts (contact_id INTEGER PRIMARY KEY,first_name TEXT "
                        f"NOT NULL,last_name TEXT NOT NULL,email TEXT NOT NULL UNIQUE,phone TEXT NOT NULL UNIQUE)"},
        ]
        output = self.pipe(messages, **self.generation_args)
        return output[0]['generated_text']


x = Text_to_query()
print(x.query("show me the whole data base"))
