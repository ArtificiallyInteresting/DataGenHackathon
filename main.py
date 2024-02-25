from dotenv import load_dotenv
import llm
import data

load_dotenv()

def main():
    header, rows = data.input()
    datagen = llm.llm()
    new_data = datagen.generate_data(header, rows)
    print(new_data)
    data.write(header, new_data.content)

if __name__ == "__main__":
    main()