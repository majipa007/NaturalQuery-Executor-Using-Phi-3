from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, BitsAndBytesConfig

quantization_config = BitsAndBytesConfig(load_in_4bit=True)

model = AutoModelForCausalLM.from_pretrained("Majipa/text-to-SQL",
                                             device_map="cuda",
                                             torch_dtype="auto",
                                             quantization_config=quantization_config)

tokenizer = AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-4k-instruct")

pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
)

generation_args = {
    "max_new_tokens": 500,
    "temperature": 0.7,
    "return_full_text": False,
}


def query(inp):
    messages = [
        {"role": "system", "content": "You are a helpful text-to-SQL assistant."},
        {"role": "user",
         "content": f"{inp}"},
    ]
    output = pipe(messages, **generation_args)
    print(output[0]['generated_text'])


text = None
while text != 'bye':
    text = input("Enter your command!")
    query(text)